"use client";
import { useAuthStore } from "@/stores/auth-store";
import { useProjectsStore } from "@/stores/projects-store";
import { useTasksStore } from "@/stores/tasks-store";
import { useMemo, useState } from "react";

export default function StoresExample() {
  const { user, isAuthenticated, login, logout } = useAuthStore();
  const { projects, selectedProjectId, addProject, selectProject, removeProject } =
    useProjectsStore();
  const { addTask, removeTask, getTasksByProject } = useTasksStore();

  const [projectName, setProjectName] = useState("");
  const [taskTitle, setTaskTitle] = useState("");

  const tasks = useMemo(
    () => (selectedProjectId ? getTasksByProject(selectedProjectId) : []),
    [getTasksByProject, selectedProjectId]
  );

  return (
    <div className="mt-8 grid gap-6 rounded border p-4">
      <h3 className="text-lg font-medium">Zustand Stores Demo</h3>

      <section className="grid gap-2">
        <h4 className="font-semibold">Auth</h4>
        {isAuthenticated ? (
          <div className="flex items-center gap-3">
            <span className="text-sm">Logged in as {user?.email}</span>
            <button className="rounded bg-gray-200 px-3 py-1" onClick={() => logout()}>
              Logout
            </button>
          </div>
        ) : (
          <button
            className="w-fit rounded bg-gray-200 px-3 py-1"
            onClick={() => login({ id: 1, email: "demo@zap.pro" }, "demo-token")}
          >
            Mock Login
          </button>
        )}
      </section>

      <section className="grid gap-3">
        <h4 className="font-semibold">Projects</h4>
        <div className="flex gap-2">
          <input
            className="rounded border px-2 py-1"
            placeholder="New project name"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
          />
          <button
            className="rounded bg-gray-200 px-3 py-1"
            onClick={() => {
              if (!projectName.trim()) return;
              addProject(projectName.trim());
              setProjectName("");
            }}
          >
            Add Project
          </button>
        </div>
        <ul className="grid gap-1">
          {projects.map((p) => (
            <li key={p.id} className="flex items-center gap-2">
              <button
                className={`rounded px-2 py-1 ${
                  selectedProjectId === p.id ? "bg-gray-300" : "bg-gray-100"
                }`}
                onClick={() => selectProject(p.id)}
              >
                {p.name}
              </button>
              <button
                className="rounded bg-red-200 px-2 py-1"
                onClick={() => removeProject(p.id)}
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      </section>

      <section className="grid gap-3">
        <h4 className="font-semibold">Tasks (selected project)</h4>
        <div className="flex gap-2">
          <input
            className="rounded border px-2 py-1"
            placeholder="New task title"
            value={taskTitle}
            onChange={(e) => setTaskTitle(e.target.value)}
            disabled={!selectedProjectId}
          />
          <button
            className="rounded bg-gray-200 px-3 py-1 disabled:opacity-50"
            disabled={!selectedProjectId || !taskTitle.trim()}
            onClick={() => {
              if (!selectedProjectId) return;
              addTask(selectedProjectId, taskTitle.trim());
              setTaskTitle("");
            }}
          >
            Add Task
          </button>
        </div>
        {selectedProjectId ? (
          <ul className="grid gap-1">
            {tasks.map((t) => (
              <li key={t.id} className="flex items-center gap-2">
                <span className="text-sm">{t.title}</span>
                <button
                  className="rounded bg-red-200 px-2 py-1"
                  onClick={() => removeTask(t.id)}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-muted-foreground">Select a project to manage tasks.</p>
        )}
      </section>
    </div>
  );
}
