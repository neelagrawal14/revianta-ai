import GlassCard from '../common/GlassCard';
import Badge from '../common/Badge';

const SIGNALS = [
  { label: 'Semantic similarity', value: 94, note: 'vs. 3 related papers' },
  { label: 'Technology overlap', value: 71, note: 'vs. 2 active repositories' },
  { label: 'Patent proximity', value: 38, note: 'vs. 1 filed patent' },
];

export default function IntelligenceEngine() {
  return (
    <section id="intelligence-engine" className="px-4 py-20 sm:px-6 lg:py-28">
      <div className="mx-auto grid max-w-6xl items-center gap-12 lg:grid-cols-2 lg:gap-16">
        <div>
          <h2 className="font-display text-3xl text-text sm:text-4xl">
            The Intelligence Engine reads what you'd spend weeks finding.
          </h2>
          <p className="mt-4 max-w-md text-text-dim">
            Every idea is embedded and compared against a live index of research papers,
            open-source repositories, datasets, and patent filings — surfacing what's
            already been tried, and what hasn't.
          </p>

          <ul className="mt-8 space-y-3 text-sm text-text-dim">
            <li className="flex gap-2.5"><span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-cyan" /> Vector search across millions of research artifacts</li>
            <li className="flex gap-2.5"><span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-cyan" /> Technology-stack extraction from real repositories</li>
            <li className="flex gap-2.5"><span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-cyan" /> Continuous re-scoring as new work is published</li>
          </ul>
        </div>

        <GlassCard tone="strong" className="p-6">
          <div className="flex items-center justify-between">
            <p className="mono-tag text-text-faint">similarity_analysis.run</p>
            <Badge tone="cyan">Live</Badge>
          </div>

          <div className="mt-6 space-y-5">
            {SIGNALS.map((s) => (
              <div key={s.label}>
                <div className="flex items-baseline justify-between text-sm">
                  <span className="text-text">{s.label}</span>
                  <span className="font-mono text-text-dim">{s.value}%</span>
                </div>
                <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-white/[0.06]">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-indigo to-cyan"
                    style={{ width: `${s.value}%` }}
                  />
                </div>
                <p className="mt-1.5 text-xs text-text-faint">{s.note}</p>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </section>
  );
}
