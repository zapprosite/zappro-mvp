"use client";

import { useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useAuth } from "@/hooks/use-auth";
import { useProjects, ProjectRecord } from "@/hooks/use-projects";

const sampleStatusLabels: Record<ProjectRecord["status"], string> = {
  planning: "Planejamento",
  active: "Ativo",
  completed: "Concluído",
  paused: "Pausado",
};

const sampleProjects: ProjectRecord[] = [
  {
    id: -1,
    name: "ZapPro Demo",
    description: "Board demonstrativo com entregas sincronizadas ao backend.",
    status: "planning",
    owner_id: 0,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: -2,
    name: "Projeto Mostruário",
    description: "Controle fictício de materiais com estados visuais.",
    status: "active",
    owner_id: 0,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

import ProjectCard from "./project-card";
import ProjectForm from "./project-form";
import { KanbanBoard } from "@/components/tasks/kanban-board";

export default function ProjectsList() {
  const { isAuthenticated } = useAuth();
  const { projects, isLoading, error } = useProjects();
  const [showForm, setShowForm] = useState(false);
  const [editingProject, setEditingProject] = useState<ProjectRecord | null>(null);
  const [tasksProject, setTasksProject] = useState<ProjectRecord | null>(null);

  if (!isAuthenticated) {
    return (
      <div className="space-y-6">
        <Card>
          <CardContent className="p-6 text-center">
            <p className="text-muted-foreground">
              Faça login para revisar e gerenciar projetos. Enquanto isso, explore o quadro
              demonstrativo abaixo.
            </p>
          </CardContent>
        </Card>

        <section
          aria-label="Projetos de exemplo"
          className="space-y-4 rounded-2xl border border-white/10 bg-white/5 p-4"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-muted-foreground">
                Amostra viva
              </p>
              <p className="text-sm text-muted-foreground">
                Lista fictícia para validar a interface mesmo sem autenticação.
              </p>
            </div>
          </div>
          <h1
            data-testid="projects-heading"
            className="text-3xl font-bold text-white"
          >
            Projects
          </h1>
          <div className="grid gap-4 sm:grid-cols-2">
            {sampleProjects.map((project) => {
              const updatedAtValue =
                project.updated_at ?? project.created_at ?? new Date().toISOString();
              return (
                <Card
                  key={`sample-project-${project.id}`}
                  className="border-dashed border-white/20 bg-slate-950/60 text-white"
                >
                  <CardHeader className="space-y-2">
                    <div className="flex items-center justify-between gap-2">
                      <CardTitle className="text-lg">{project.name}</CardTitle>
                      <Badge className="text-xs uppercase tracking-[0.2em]">
                        {sampleStatusLabels[project.status]}
                      </Badge>
                    </div>
                    <CardDescription className="text-sm text-slate-200">
                      {project.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-2">
                    <p className="text-xs text-muted-foreground">
                      Atualizado em {new Date(updatedAtValue).toLocaleDateString("pt-BR")}
                    </p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </section>
      </div>
    );
  }

  const handleNewProject = () => {
    setEditingProject(null);
    setShowForm(true);
  };

  const handleEdit = (project: ProjectRecord) => {
    setEditingProject(project);
    setShowForm(true);
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setEditingProject(null);
  };

  const handleViewTasks = (project: ProjectRecord) => {
    setTasksProject(project);
    setShowForm(false);
  };

  const handleBackFromTasks = () => {
    setTasksProject(null);
  };

  if (tasksProject) {
    return (
      <KanbanBoard
        projectId={tasksProject.id}
        projectName={tasksProject.name}
        onBack={handleBackFromTasks}
      />
    );
  }

  if (showForm) {
    return <ProjectForm project={editingProject} onClose={handleCloseForm} />;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-muted-foreground">
            Active portfolio
          </p>
          <p className="text-sm text-muted-foreground">
            Capture new work, update status, and export coverage insights.
          </p>
        </div>
        <Button onClick={handleNewProject}>New project</Button>
      </div>

      {isLoading && <p>Carregando projetos...</p>}
      {error && <p className="text-red-600">Erro: {error}</p>}

      {!isLoading && projects.length === 0 && (
        <Card>
          <CardContent className="p-6 text-center space-y-3">
            <p className="text-muted-foreground">Nenhum projeto encontrado.</p>
            <Button onClick={handleNewProject}>Criar primeiro projeto</Button>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {projects.map((project) => (
          <ProjectCard
            key={project.id}
            project={project}
            onEdit={handleEdit}
            onViewTasks={handleViewTasks}
          />
        ))}
      </div>
    </div>
  );
}
