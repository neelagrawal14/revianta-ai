import { useMemo } from 'react';
import { useParams } from 'react-router-dom';
import { ScrollText } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import GlassCard from '../../components/common/GlassCard';
import Badge from '../../components/common/Badge';
import EmptyState from '../../components/common/EmptyState';
import { getPatentsForProject } from '../../constants/mock';

const RELEVANCE_TONE = { High: 'rose', Medium: 'amber', Low: 'cyan' };

/** Simple horizontal overlap/novelty bar: higher similarity = more overlap, less novelty. */
function OverlapBar({ similarity }) {
  const novelty = 100 - similarity;
  return (
    <div className="flex h-2 w-full overflow-hidden rounded-full bg-white/[0.06]">
      <div className="h-full bg-gradient-to-r from-rose to-amber" style={{ width: `${similarity}%` }} title={`${similarity}% overlap`} />
      <div className="h-full bg-gradient-to-r from-cyan to-indigo-soft" style={{ width: `${novelty}%` }} title={`${novelty}% novel`} />
    </div>
  );
}

export default function ProjectPatentsPage() {
  const { projectId } = useParams();
  const patents = useMemo(() => getPatentsForProject(projectId), [projectId]);

  if (patents.length === 0) {
    return (
      <PageContainer>
        <EmptyState icon={ScrollText} title="No patents found" description="Revianta hasn't identified related patent filings for this project yet." />
      </PageContainer>
    );
  }

  const avgSimilarity = Math.round(patents.reduce((sum, p) => sum + p.similarity, 0) / patents.length);

  return (
    <PageContainer>
      <SectionHeader
        title="Patents"
        description="Filed patents with claims overlapping this project's approach — useful for spotting prior-art risk early."
      />

      <GlassCard tone="strong" className="mt-6 p-5">
        <div className="flex items-center justify-between text-sm">
          <span className="text-text-dim">Average overlap vs. novelty across {patents.length} patents</span>
          <span className="font-mono text-text">{avgSimilarity}% overlap</span>
        </div>
        <div className="mt-3">
          <OverlapBar similarity={avgSimilarity} />
        </div>
        <div className="mt-2 flex justify-between text-xs text-text-faint">
          <span>Overlaps with prior art</span>
          <span>Novel to this project</span>
        </div>
      </GlassCard>

      <div className="mt-6 space-y-3">
        {patents.map((patent) => (
          <GlassCard key={patent.id} className="p-5">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div className="min-w-0">
                <h3 className="font-display text-base text-text">{patent.title}</h3>
                <p className="mt-1 text-sm text-text-dim">
                  {patent.inventor} · Filed {patent.year} · {patent.classification}
                </p>
              </div>
              <Badge tone={RELEVANCE_TONE[patent.relevance] || 'neutral'}>{patent.relevance} Relevance</Badge>
            </div>
            <div className="mt-4">
              <OverlapBar similarity={patent.similarity} />
              <p className="mt-1.5 text-xs text-text-faint">{patent.similarity}% claim overlap</p>
            </div>
          </GlassCard>
        ))}
      </div>
    </PageContainer>
  );
}
