import { Lightbulb } from 'lucide-react';
import GlassCard from '../common/GlassCard';
import Badge from '../common/Badge';

const CONFIDENCE_TONE = { High: 'cyan', Medium: 'amber', Low: 'neutral' };

/**
 * GapCard — one research-gap suggestion. Shared by the global
 * /research-gaps page and each project's Research Gaps tab. Deliberately
 * framed as a UI suggestion, not a validated scientific finding.
 */
export default function GapCard({ gap }) {
  return (
    <GlassCard className="p-5">
      <div className="flex items-start justify-between gap-4">
        <h3 className="font-display text-base text-text">{gap.title}</h3>
        <Badge tone={CONFIDENCE_TONE[gap.confidence] || 'neutral'} className="shrink-0">{gap.confidence} confidence</Badge>
      </div>

      <p className="mt-3 text-sm text-text-dim">
        <span className="text-text-faint">Evidence — </span>{gap.evidence}
      </p>

      {gap.relatedPapers?.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {gap.relatedPapers.map((p) => (
            <span key={p} className="mono-tag rounded-full border border-line bg-white/[0.03] px-2.5 py-1 text-text-faint">
              {p}
            </span>
          ))}
        </div>
      )}

      <div className="mt-4 flex items-start gap-2 rounded-xl border border-indigo/20 bg-indigo/[0.05] p-3 text-sm text-text-dim">
        <Lightbulb size={15} className="mt-0.5 shrink-0 text-indigo-soft" />
        {gap.opportunity}
      </div>
    </GlassCard>
  );
}
