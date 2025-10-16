import { create } from "zustand";
import { Workflow, Task, WorkflowStatus } from "../types/workflow";

interface WorkflowStore {
  workflows: Workflow[];
  tasks: Task[];
  activeWorkflowId: number | null;
  loading: boolean;
  error: string | null;

  // Actions
  setWorkflows: (workflows: Workflow[]) => void;
  addWorkflow: (workflow: Workflow) => void;
  updateWorkflow: (id: number, updates: Partial<Workflow>) => void;
  updateWorkflowStatus: (id: number, status: WorkflowStatus) => void;
  deleteWorkflow: (id: number) => void;
  setActiveWorkflow: (id: number | null) => void;
  
  setTasks: (tasks: Task[]) => void;
  addTask: (task: Task) => void;
  updateTask: (id: number, updates: Partial<Task>) => void;
  deleteTask: (id: number) => void;
  getTasksByWorkflow: (workflowId: number) => Task[];
  
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  getWorkflowById: (id: number) => Workflow | undefined;
  getActiveWorkflow: () => Workflow | undefined;
  
  // Workflow statistics
  getWorkflowStats: () => {
    total: number;
    active: number;
    completed: number;
    failed: number;
  };
}

/**
 * Workflow Store - Manages workflow and task state across the application
 */
export const useWorkflowStore = create<WorkflowStore>((set, get) => ({
  workflows: [],
  tasks: [],
  activeWorkflowId: null,
  loading: false,
  error: null,

  setWorkflows: (workflows) => set({ workflows, error: null }),

  addWorkflow: (workflow) =>
    set((state) => ({
      workflows: [...state.workflows, workflow],
    })),

  updateWorkflow: (id, updates) =>
    set((state) => ({
      workflows: state.workflows.map((workflow) =>
        workflow.id === id ? { ...workflow, ...updates } : workflow
      ),
    })),

  updateWorkflowStatus: (id, status) =>
    set((state) => ({
      workflows: state.workflows.map((workflow) =>
        workflow.id === id ? { ...workflow, status } : workflow
      ),
    })),

  deleteWorkflow: (id) =>
    set((state) => ({
      workflows: state.workflows.filter((workflow) => workflow.id !== id),
      activeWorkflowId: state.activeWorkflowId === id ? null : state.activeWorkflowId,
    })),

  setActiveWorkflow: (id) => set({ activeWorkflowId: id }),

  setTasks: (tasks) => set({ tasks }),

  addTask: (task) =>
    set((state) => ({
      tasks: [...state.tasks, task],
    })),

  updateTask: (id, updates) =>
    set((state) => ({
      tasks: state.tasks.map((task) => (task.id === id ? { ...task, ...updates } : task)),
    })),

  deleteTask: (id) =>
    set((state) => ({
      tasks: state.tasks.filter((task) => task.id !== id),
    })),

  getTasksByWorkflow: (workflowId) => {
    const state = get();
    return state.tasks.filter((task) => task.workflow_id === workflowId);
  },

  setLoading: (loading) => set({ loading }),

  setError: (error) => set({ error }),

  getWorkflowById: (id) => {
    const state = get();
    return state.workflows.find((workflow) => workflow.id === id);
  },

  getActiveWorkflow: () => {
    const state = get();
    if (!state.activeWorkflowId) return undefined;
    return state.workflows.find((workflow) => workflow.id === state.activeWorkflowId);
  },

  getWorkflowStats: () => {
    const state = get();
    return {
      total: state.workflows.length,
      active: state.workflows.filter((w) => w.status === "in_progress").length,
      completed: state.workflows.filter((w) => w.status === "completed").length,
      failed: state.workflows.filter((w) => w.status === "failed").length,
    };
  },
}));

