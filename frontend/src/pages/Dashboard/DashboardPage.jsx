import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, FolderKanban, RefreshCw } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import MetricCard from '../../components/common/MetricCard';
import GlowButton from '../../components/common/GlowButton';
import ProjectCard from '../../components/dashboard/ProjectCard';
import EmptyState from '../../components/common/EmptyState';
import { projectApi } from '../../services/projectApi';

function getProjectItems(response) {
  const data = response?.data ?? response;
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.items)) return data.items;
  if (Array.isArray(data?.projects)) return data.projects;
  return [];
}

function normalizeProject(project) {
  const technologies = Array.isArray(project.technologies) ? project.technologies : [];
  return {
    ...project,
    id: String(project.id),
    name: project.name || project.title || `Project ${project.id}`,
    title: project.title || project.name || `Project ${project.id}`,
    description: project.description || 'No project description available.',
    tags: Array.isArray(project.tags) ? project.tags : technologies,
    healthScore: Number.isFinite(Number(project.healthScore ?? project.health_score)) && (project.healthScore ?? project.health_score) != null
      ? Number(project.healthScore ?? project.health_score) : null,
    progress: Number.isFinite(Number(project.progress)) && project.progress != null ? Number(project.progress) : null,
    risk: project.risk || project.risk_level || null,
    lastAnalyzed: project.lastAnalyzed || project.last_analyzed || null,
  };
}

export default function DashboardPage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadProjects() {
    setLoading(true);
    setError('');
    try {
      const response = await projectApi.list();
      setProjects(getProjectItems(response).map(normalizeProject));
    } catch (err) {
      setError(err?.message || 'Unable to load your projects. Check your login and backend connection.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadProjects(); }, []);

  const metrics = [
    { id: 'projects', label: 'Active Projects', value: String(projects.length), delta: 'Your workspace' },
    { id: 'papers', label: 'Papers Analyzed', value: '—', delta: 'Live metric unavailable' },
    { id: 'repos', label: 'Repositories', value: '—', delta: 'Live metric unavailable' },
    { id: 'datasets', label: 'Datasets', value: '—', delta: 'Live metric unavailable' },
    { id: 'patents', label: 'Patents', value: '—', delta: 'Live metric unavailable' },
    { id: 'health', label: 'Avg. Project Health', value: '—', delta: 'Live metric unavailable' },
  ];

  return (
    <PageContainer>
      <div className="mb-10">
        <p className="mono-tag text-indigo-soft">Workspace</p>
        <h1 className="mt-2 font-display text-3xl text-text sm:text-4xl">Your Research Intelligence</h1>
        <p className="mt-2 max-w-lg text-text-dim">A live view of your projects and research workspace.</p>
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        {metrics.map((metric) => <MetricCard key={metric.id} label={metric.label} value={metric.value} delta={metric.delta} />)}
      </div>

      <SectionHeader
        className="mt-14 mb-6"
        title="Active projects"
        description="Projects associated with your signed-in account."
        action={
          <div className="flex items-center gap-2">
            <button type="button" onClick={loadProjects} disabled={loading}
              className="inline-flex h-9 items-center gap-2 rounded-full border border-white/10 px-3 text-sm text-slate-300 transition hover:bg-white/5 disabled:opacity-50">
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} /> Refresh
            </button>
            <GlowButton as={Link} to="/projects/new" size="sm"><Plus size={16} />New project</GlowButton>
          </div>
        }
      />

      {loading ? (
        <p className="mt-8 text-sm text-text-dim">Loading your projects...</p>
      ) : error ? (
        <div className="mt-8 rounded-xl border border-rose-500/30 bg-rose-500/5 p-5">
          <p className="text-sm text-rose-300">{error}</p>
          <button type="button" onClick={loadProjects} className="mt-3 text-sm text-indigo-300 hover:text-indigo-200">Try again</button>
        </div>
      ) : projects.length ? (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {projects.map((project) => <ProjectCard key={project.id} project={project} />)}
        </div>
      ) : (
        <EmptyState className="mt-8" icon={FolderKanban} title="No projects yet"
          description="Your workspace is ready. Create a project to begin exploring it with Revianta AI."
          actionLabel="New project" />
      )}
    </PageContainer>
  );
}
