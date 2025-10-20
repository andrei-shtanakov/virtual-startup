"""Helpers for running async callables from synchronous code."""

from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, TypeVar

T = TypeVar("T")


def run_async(func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
    """Run an async function from synchronous code.

    This helper prefers ``asyncio.run`` but gracefully falls back to creating
    a dedicated event loop when called from within an active loop (for example,
    during tests that patch asyncio behaviour).
    """
    try:
        return asyncio.run(func(*args, **kwargs))
    except RuntimeError as exc:
        if "asyncio.run()" not in str(exc):
            raise

        loop = asyncio.new_event_loop()
        try:
            previous_loop: asyncio.AbstractEventLoop | None = None
            try:
                previous_loop = asyncio.get_event_loop()
            except RuntimeError:
                previous_loop = None

            asyncio.set_event_loop(loop)
            return loop.run_until_complete(func(*args, **kwargs))
        finally:
            loop.close()
            try:
                asyncio.set_event_loop(previous_loop)
            except Exception:
                pass
