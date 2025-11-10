import Link from "next/link";
import { Button } from "@/components/ui/button";
import HealthCheck from "@/components/health-check";
import AuthLayout from "@/components/auth/auth-layout";
import ProjectsList from "@/components/projects/projects-list";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto flex max-w-6xl flex-col gap-12 px-6 py-12">
        <section className="space-y-6 rounded-3xl border border-white/10 bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 p-10 shadow-2xl">
          <div className="space-y-4">
            <p className="text-xs uppercase tracking-[0.4em] text-slate-300">
              ZapPro Workspace
            </p>
            <h1 className="text-4xl font-semibold leading-tight sm:text-5xl lg:text-6xl">
              Coordinate projects, teams, and materials without losing sight.
            </h1>
            <p className="text-base text-slate-200">
              ZapPro unifies FastAPI routes with a Next.js 15 experience so you can
              plan, execute, and automate every delivery from a single board.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href="/health">Frontend health</Link>
            </Button>
            <Button variant="outline" asChild size="lg">
              <Link href="http://localhost:8000/health">API health</Link>
            </Button>
          </div>
          <div className="grid gap-6 rounded-2xl border border-white/20 bg-white/5 p-6 text-slate-100 md:grid-cols-2">
            <HealthCheck />
            <AuthLayout />
          </div>
        </section>

        <section
          aria-label="Projects"
          data-testid="projects-list"
          className="space-y-6 rounded-3xl bg-white p-8 shadow-xl text-slate-900"
        >
          <div className="flex flex-col gap-2">
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">
              Live board
            </p>
            <h1
              data-testid="projects-heading"
              className="text-3xl font-bold"
            >
              Projects
            </h1>
            <p className="text-base text-slate-600">
              Track open efforts, launch plan stages, and keep your delivery
              pipeline synchronized with the FastAPI backend.
            </p>
          </div>
          <ProjectsList />
        </section>
      </div>
    </main>
  );
}
