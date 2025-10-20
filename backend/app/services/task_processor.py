"""Background task processor for async agent operations.

This service provides background processing for agent tasks using threading.
For production, consider using Celery with Redis.
"""

import asyncio
import threading
from typing import Any, Callable, Dict, Optional
from queue import Queue
import time


class TaskProcessor:
    """Background task processor using threading."""

    def __init__(self):
        """Initialize the task processor."""
        self.task_queue: Queue = Queue()
        self.worker_thread: Optional[threading.Thread] = None
        self.running = False
        self.results: Dict[str, Any] = {}

    def start(self) -> None:
        """Start the background worker thread."""
        if self.running:
            return

        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        print("Task processor started")

    def stop(self) -> None:
        """Stop the background worker thread."""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        print("Task processor stopped")

    def _worker(self) -> None:
        """Worker thread that processes tasks from the queue."""
        while self.running:
            try:
                # Get task from queue (with timeout)
                if not self.task_queue.empty():
                    task = self.task_queue.get(timeout=1)

                    if task:
                        task_id = task.get("id")
                        func = task.get("func")
                        args = task.get("args", ())
                        kwargs = task.get("kwargs", {})
                        callback = task.get("callback")

                        print(f"Processing task {task_id}")

                        try:
                            # Check if function is async
                            if asyncio.iscoroutinefunction(func):
                                # Run async function
                                loop = asyncio.new_event_loop()
                                asyncio.set_event_loop(loop)
                                result = loop.run_until_complete(func(*args, **kwargs))
                                loop.close()
                            else:
                                # Run sync function
                                result = func(*args, **kwargs)

                            # Store result
                            self.results[task_id] = {
                                "status": "completed",
                                "result": result,
                            }

                            # Call callback if provided
                            if callback:
                                callback(result)

                            print(f"Task {task_id} completed")

                        except Exception as e:
                            print(f"Task {task_id} failed: {str(e)}")
                            self.results[task_id] = {
                                "status": "failed",
                                "error": str(e),
                            }

                        self.task_queue.task_done()
                else:
                    # Sleep briefly if queue is empty
                    time.sleep(0.1)

            except Exception as e:
                print(f"Worker error: {str(e)}")
                time.sleep(1)

    def submit_task(
        self,
        task_id: str,
        func: Callable,
        args: tuple = (),
        kwargs: Dict = None,
        callback: Optional[Callable] = None,
    ) -> str:
        """Submit a task to the background queue.

        Args:
            task_id: Unique identifier for the task
            func: Function to execute
            args: Positional arguments for the function
            kwargs: Keyword arguments for the function
            callback: Optional callback function to call with result

        Returns:
            Task ID
        """
        if not self.running:
            raise RuntimeError("Task processor not running. Call start() first.")

        task = {
            "id": task_id,
            "func": func,
            "args": args,
            "kwargs": kwargs or {},
            "callback": callback,
        }

        self.task_queue.put(task)
        self.results[task_id] = {"status": "pending"}

        return task_id

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of a task.

        Args:
            task_id: Task identifier

        Returns:
            Task status dictionary
        """
        return self.results.get(
            task_id, {"status": "not_found", "error": "Task not found"}
        )

    def clear_completed(self) -> int:
        """Clear completed tasks from results.

        Returns:
            Number of tasks cleared
        """
        completed = [
            tid
            for tid, result in self.results.items()
            if result.get("status") in ["completed", "failed"]
        ]

        for task_id in completed:
            del self.results[task_id]

        return len(completed)


# Global task processor instance
_task_processor: Optional[TaskProcessor] = None


def get_task_processor() -> TaskProcessor:
    """Get or create the global task processor instance.

    Returns:
        TaskProcessor instance
    """
    global _task_processor

    if _task_processor is None:
        _task_processor = TaskProcessor()

    return _task_processor


