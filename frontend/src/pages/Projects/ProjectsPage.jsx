import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, FolderKanban, RefreshCw } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
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
  const score = project.healthScore ?? project.health_score;
  return {
    ...project,
    id: String(project.id),
    title: project.title || project.name || `Project ${project.id}`,
    name: project.name || project.title || `Project ${project.id}`,
    description: project.description || 'No project description available.',
    tags: Array.isArray(project.tags) ? project.tags : technologies,
    healthScore: score != null && Number.isFinite(Number(score)) ? Number(score) : null,
    progress: project.progress != null && Number.isFinite(Number(project.progress)) ? Number(project.progress) : null,
    risk: project.risk || project.risk_level || null,
    lastAnalyzed: project.lastAnalyzed || project.last_analyzed || null,
  };
}

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadProjects() {
    setLoading(true);
    setError('');
    try {
      const response = await projectApi.list();
      setProjects(getProjectItems(response).map(normalizeProject));
    } catch (err) {
      setError(err?.message || 'Unable to load projects. Check that the backend and database are running.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadProjects(); }, []);

  const filteredProjects = useMemo(() => {
    const query = search.trim().toLowerCase();
    if (!query) return projects;
    return projects.filter((project) => [
      project.title, project.name, project.description,
      ...(Array.isArray(project.technologies) ? project.technologies : []),
      ...(Array.isArray(project.tags) ? project.tags : []),
    ].filter(Boolean).join(' ').toLowerCase().includes(query));
  }, [projects, search]);

  return (
    <PageContainer>
      <SectionHeader title="Projects" description="Your research projects and their current status."
        action={<GlowButton as={Link} to="/projects/new" size="sm"><Plus size={16} />New project</GlowButton>} />
      <div className="mt-6 flex flex-wrap items-center gap-3">
        <input type="search" value={search} onChange={(event) => setSearch(event.target.value)}
          placeholder="Search your projects..." aria-label="Search projects"
          className="h-11 w-full max-w-sm rounded-full border border-white/10 bg-white/5 px-5 text-sm text-white outline-none transition focus:border-indigo-400" />
        <button type="button" onClick={loadProjects} disabled={loading}
          className="inline-flex h-10 items-center gap-2 rounded-full border border-white/10 px-4 text-sm text-slate-300 transition hover:bg-white/5 disabled:opacity-50">
          <RefreshCw size={15} className={loading ? 'animate-spin' : ''} />Refresh
        </button>
      </div>
      {loading ? (
        <div className="mt-8 text-sm text-slate-400">Loading projects from Revianta AI...</div>
      ) : error ? (
        <div className="mt-8 rounded-xl border border-rose-500/30 bg-rose-500/5 p-5">
          <p className="text-sm text-rose-300">{error}</p>
          <button type="button" onClick={loadProjects} className="mt-3 text-sm text-indigo-300 hover:text-indigo-200">Try again</button>
        </div>
      ) : filteredProjects.length ? (
        <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {filteredProjects.map((project) => <ProjectCard key={project.id} project={project} />)}
        </div>
      ) : (
        <EmptyState className="mt-8" icon={FolderKanban}
          title={search ? 'No matching projects' : 'No projects yet'}
          description={search ? 'Try another search term.' : 'Create a project to begin exploring it with Revianta AI.'}
          actionLabel={search ? undefined : 'New project'} />
      )}
    </PageContainer>
  );
}
