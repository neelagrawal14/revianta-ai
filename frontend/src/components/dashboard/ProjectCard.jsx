import { Link } from 'react-router-dom';
import { ArrowUpRight, Clock3 } from 'lucide-react';
import GlassCard from '../common/GlassCard';
import Badge, { riskTone } from '../common/Badge';
import { cn } from '../../utils/cn';

function healthColor(score) {
  if (score == null) return 'rgba(148,163,214,0.35)';
  if (score >= 65) return 'var(--color-cyan)';
  if (score >= 40) return 'var(--color-amber)';
  return 'var(--color-rose)';
}

export default function ProjectCard({ project }) {
  const healthScore = Number.isFinite(project.healthScore) ? Math.max(0, Math.min(100, project.healthScore)) : null;
  const progress = Number.isFinite(project.progress) ? Math.max(0, Math.min(100, project.progress)) : null;
  const tags = Array.isArray(project.tags) ? project.tags : [];
  const risk = project.risk || null;
  const color = healthColor(healthScore);

  return (
    <GlassCard interactive className="group flex flex-col gap-4 p-5">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h3 className="truncate font-display text-base text-text">{project.name || project.title || `Project ${project.id}`}</h3>
          <p className="mt-1 line-clamp-2 text-sm text-text-dim">{project.description || 'No project description available.'}</p>
        </div>
        <div className="relative grid h-14 w-14 shrink-0 place-items-center">
          <svg viewBox="0 0 44 44" className="h-14 w-14 -rotate-90">
            <circle cx="22" cy="22" r="18" fill="none" stroke="rgba(148,163,214,0.15)" strokeWidth="4" />
            {healthScore !== null && <circle cx="22" cy="22" r="18" fill="none" stroke={color} strokeWidth="4" strokeLinecap="round" strokeDasharray={`${(healthScore / 100) * 113} 113`} />}
          </svg>
          <span className="absolute font-mono text-xs font-medium text-text">{healthScore === null ? '—' : `${healthScore}%`}</span>
        </div>
      </div>

      {tags.length ? (
        <div className="flex flex-wrap gap-1.5">{tags.map((tag) => <Badge key={String(tag)}>{String(tag)}</Badge>)}</div>
      ) : <p className="text-xs text-text-faint">No technologies added yet</p>}

      <div>
        <div className="mb-1.5 flex items-center justify-between text-xs text-text-faint">
          <span>Progress</span><span className="font-mono">{progress === null ? '—' : `${progress}%`}</span>
        </div>
        <div className="h-1.5 w-full overflow-hidden rounded-full bg-white/[0.06]">
          <div className="h-full rounded-full bg-gradient-to-r from-indigo to-cyan" style={{ width: `${progress ?? 0}%` }} />
        </div>
      </div>

      <div className="flex items-center justify-between border-t border-line pt-4">
        <div className="flex items-center gap-3 text-xs text-text-faint">
          {risk ? <Badge tone={riskTone(risk)}>{risk} Risk</Badge> : <Badge>Risk not assessed</Badge>}
          <span className="flex items-center gap-1"><Clock3 size={12} />{project.lastAnalyzed || 'Not analyzed'}</span>
        </div>
        <Link to={`/projects/${project.id}`} className={cn('flex items-center gap-1 text-sm font-medium text-indigo-soft transition-colors hover:text-cyan')}>
          Open Project <ArrowUpRight size={14} className="transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
        </Link>
      </div>
    </GlassCard>
  );
}
