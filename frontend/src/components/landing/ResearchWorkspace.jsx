import GlassCard from '../common/GlassCard';
import Badge from '../common/Badge';
import { FileText, FolderGit2, Database, ScrollText } from 'lucide-react';

const TILES = [
  { icon: FileText, label: 'Papers', count: 24 },
  { icon: FolderGit2, label: 'Repositories', count: 9 },
  { icon: Database, label: 'Datasets', count: 5 },
  { icon: ScrollText, label: 'Patents', count: 3 },
];

export default function ResearchWorkspace() {
  return (
    <section id="workspace" className="px-4 py-20 sm:px-6 lg:py-28">
      <div className="mx-auto grid max-w-6xl items-center gap-12 lg:grid-cols-2 lg:gap-16">
        <GlassCard tone="strong" className="order-2 p-6 lg:order-1">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-display text-[15px] text-text">Smart Traffic System</p>
              <p className="mono-tag mt-0.5 text-text-faint">workspace / overview</p>
            </div>
            <Badge tone="amber">Medium Risk</Badge>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3">
            {TILES.map(({ icon: Icon, label, count }) => (
              <div key={label} className="rounded-2xl border border-line bg-white/[0.02] p-4">
                <Icon size={16} className="text-indigo-soft" />
                <p className="mt-3 font-display text-xl text-text">{count}</p>
                <p className="text-xs text-text-faint">{label}</p>
              </div>
            ))}
          </div>
        </GlassCard>

        <div className="order-1 lg:order-2">
          <h2 className="font-display text-3xl text-text sm:text-4xl">
            One workspace, every source in context.
          </h2>
          <p className="mt-4 max-w-md text-text-dim">
            Papers, repositories, datasets, and patents live next to your notes and
            experiments — not in separate tabs you'll forget to revisit.
          </p>
          <ul className="mt-8 space-y-3 text-sm text-text-dim">
            <li className="flex gap-2.5"><span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-indigo-soft" /> Auto-organized by relevance to your project</li>
            <li className="flex gap-2.5"><span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-indigo-soft" /> Notes and experiments stay linked to their source</li>
            <li className="flex gap-2.5"><span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-indigo-soft" /> Health score updates as your research evolves</li>
          </ul>
        </div>
      </div>
    </section>
  );
}
