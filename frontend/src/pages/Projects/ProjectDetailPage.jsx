import { useMemo } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowUpRight, Clock3, Network, TriangleAlert, FolderX } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import GlassCard from '../../components/common/GlassCard';
import Badge, { riskTone } from '../../components/common/Badge';
import HealthOrb from '../../components/common/HealthOrb';
import GapCard from '../../components/research/GapCard';
import ForceGraph from '../../components/graph/ForceGraph';
import EmptyState from '../../components/common/EmptyState';
import {
  getPapersForProject,
  getRiskForProject,
  getKnowledgeGraphForProject,
  getRecommendationsForProject,
  getGapsForDomain,
} from '../../constants/mock';
import { MOCK_PROJECTS } from '../../constants/mockData';

export default function ProjectDetailPage() {
  const { projectId } = useParams();
  const project = MOCK_PROJECTS.find((p) => p.id === projectId);

  const papers = useMemo(() => (project ? getPapersForProject(projectId).slice(0, 3) : []), [project, projectId]);
  const risk = useMemo(() => (project ? getRiskForProject(projectId) : null), [project, projectId]);
  const graph = useMemo(() => (project ? getKnowledgeGraphForProject(projectId) : null), [project, projectId]);
  const recommendations = useMemo(() => (project ? getRecommendationsForProject(projectId).slice(0, 2) : []), [project, projectId]);
  const gaps = useMemo(() => (project ? getGapsForDomain(project.domain).slice(0, 1) : []), [project]);

  if (!project) {
    return (
      <PageContainer>
        <EmptyState
          icon={FolderX}
          title="Project not found"
          description="This project doesn't exist in the current workspace, or mock data was reset."
          actionLabel="Back to projects"
          onAction={() => (window.location.href = '/projects')}
        />
      </PageContainer>
    );
  }

  const topRiskDimension = risk ? [...risk.dimensions].sort((a, b) => b.score - a.score)[0] : null;

  return (
    <PageContainer>
      {/* Workspace header */}
      <div className="flex flex-wrap items-start justify-between gap-6">
        <div>
          <p className="mono-tag text-indigo-soft">{project.domain}</p>
          <h1 className="mt-2 font-display text-3xl text-text">{project.name}</h1>
          <p className="mt-2 max-w-xl text-text-dim">{project.description}</p>
          <div className="mt-4 flex flex-wrap items-center gap-3 text-sm text-text-faint">
            <Badge tone={riskTone(project.risk)}>{project.status}</Badge>
            <span className="flex items-center gap-1.5"><Clock3 size={13} /> Last analysis {project.lastAnalyzed}</span>
          </div>
        </div>
        <HealthOrb score={project.healthScore} size={120} />
      </div>

      {/* Technologies */}
      <section className="mt-10">
        <h2 className="font-display text-lg text-text">Technologies</h2>
        <div className="mt-3 flex flex-wrap gap-1.5">
          {project.tags.map((tag) => (
            <Badge key={tag}>{tag}</Badge>
          ))}
        </div>
      </section>

      {/* Similar work + risk snapshot */}
      <div className="mt-10 grid gap-6 lg:grid-cols-[1.3fr_1fr]">
        <section>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-display text-lg text-text">Similar work</h2>
            <Link to={`/projects/${projectId}/papers`} className="flex items-center gap-1 text-sm text-indigo-soft hover:text-cyan">
              View all papers <ArrowUpRight size={13} />
            </Link>
          </div>
          <div className="space-y-3">
            {papers.map((paper) => (
              <GlassCard key={paper.id} className="flex items-start justify-between gap-4 p-4">
                <div className="min-w-0">
                  <p className="truncate text-sm text-text">{paper.title}</p>
                  <p className="mt-1 text-xs text-text-faint">{paper.authors.join(', ')} · {paper.year}</p>
                </div>
                <span className="shrink-0 font-mono text-sm text-cyan">{paper.similarity}%</span>
              </GlassCard>
            ))}
          </div>
        </section>

        <section>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-display text-lg text-text">Risk snapshot</h2>
            <Link to={`/projects/${projectId}/risk`} className="flex items-center gap-1 text-sm text-indigo-soft hover:text-cyan">
              Full report <ArrowUpRight size={13} />
            </Link>
          </div>
          <GlassCard className="p-5">
            <div className="flex items-center gap-4">
              <HealthOrb score={project.healthScore} size={84} label="Health" />
              <div>
                <Badge tone={riskTone(project.risk)}>{project.risk} Risk</Badge>
                {topRiskDimension && (
                  <p className="mt-2 flex items-center gap-1.5 text-xs text-text-dim">
                    <TriangleAlert size={12} className="text-amber" />
                    Highest: {topRiskDimension.label} ({topRiskDimension.score}%)
                  </p>
                )}
              </div>
            </div>
          </GlassCard>
        </section>
      </div>

      {/* Knowledge graph preview */}
      <section className="mt-10">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="flex items-center gap-2 font-display text-lg text-text">
            <Network size={17} className="text-indigo-soft" /> Knowledge graph preview
          </h2>
          <Link to={`/projects/${projectId}/graph`} className="flex items-center gap-1 text-sm text-indigo-soft hover:text-cyan">
            Open full graph <ArrowUpRight size={13} />
          </Link>
        </div>
        {graph && <ForceGraph nodes={graph.nodes} links={graph.links} />}
      </section>

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <section className="mt-10">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-display text-lg text-text">Recommendations</h2>
            <Link to="/recommendations" className="flex items-center gap-1 text-sm text-indigo-soft hover:text-cyan">
              All recommendations <ArrowUpRight size={13} />
            </Link>
          </div>
          <div className="grid gap-4 lg:grid-cols-2">
            {recommendations.map((rec) => (
              <GlassCard key={rec.id} className="p-5">
                <Badge tone={rec.severity === 'high' ? 'rose' : 'amber'}>{rec.riskFlag}</Badge>
                <p className="mt-3 text-sm text-text">{rec.recommendation}</p>
                <p className="mt-2 text-xs text-text-faint">{rec.why}</p>
              </GlassCard>
            ))}
          </div>
        </section>
      )}

      {/* Research gaps for this project's domain */}
      {gaps.length > 0 && (
        <section className="mt-10 mb-4">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-display text-lg text-text">Research gaps</h2>
            <Link to={`/projects/${projectId}/gaps`} className="flex items-center gap-1 text-sm text-indigo-soft hover:text-cyan">
              View all <ArrowUpRight size={13} />
            </Link>
          </div>
          {gaps.map((gap) => (
            <GapCard key={gap.id} gap={gap} />
          ))}
        </section>
      )}
    </PageContainer>
  );
}
