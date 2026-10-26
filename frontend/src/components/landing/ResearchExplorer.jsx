import { Link } from 'react-router-dom';
import { ArrowRight, FileText, FolderGit2, Database, ScrollText } from 'lucide-react';
import GlassCard from '../common/GlassCard';
import SearchBar from '../common/SearchBar';

const RESULTS = [
  { icon: FileText, tone: 'text-cyan', kind: 'Paper', title: 'Adaptive Signal Control via Deep Q-Networks', meta: '2024 · cited by 38' },
  { icon: FolderGit2, tone: 'text-indigo-soft', kind: 'Repository', title: 'traffic-rl-sim', meta: '1.2k stars 00b7 active' },
  { icon: Database, tone: 'text-violet', kind: 'Dataset', title: 'Urban Intersection Flow Dataset', meta: 'CC-BY-4.0' },
  { icon: ScrollText, tone: 'text-amber', kind: 'Patent', title: 'Method for Predictive Traffic Signal Timing', meta: 'Filed 2023' },
];

export default function ResearchExplorer() {
  return (
    <section className="px-4 py-20 sm:px-6 lg:py-28">
      <div className="mx-auto max-w-6xl">
        <div className="flex flex-wrap items-end justify-between gap-6">
          <div className="max-w-xl">
            <h2 className="font-display text-3xl text-text sm:text-4xl">
              Explore the research landscape directly.
            </h2>
            <p className="mt-4 text-text-dim">
              Search across papers, repositories, datasets, and patents — the same index
              Revianta uses to analyze your projects.
            </p>
          </div>
          <Link to="/dashboard" className="flex items-center gap-1.5 text-sm font-medium text-indigo-soft hover:text-cyan">
            Explore intelligence <ArrowRight size={14} />
          </Link>
        </div>

        <GlassCard tone="strong" className="mt-10 p-5">
          <SearchBar placeholder="Search 'adaptive traffic signal control'…" className="h-12 w-full" />
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {RESULTS.map(({ icon: Icon, tone, kind, title, meta }) => (
              <div key={title} className="flex items-start gap-3 rounded-2xl border border-line bg-white/[0.02] p-4">
                <Icon size={17} className={`mt-0.5 shrink-0 ${tone}`} />
                <div className="min-w-0">
                  <p className="mono-tag text-text-faint">{kind}</p>
                  <p className="mt-0.5 truncate text-sm text-text">{title}</p>
                  <p className="mt-0.5 text-xs text-text-faint">{meta}</p>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </section>
  );
}
