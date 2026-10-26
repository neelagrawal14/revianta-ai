import { useLocation } from 'react-router-dom';
import { Sparkles } from 'lucide-react';
import PageContainer from '../components/layout/PageContainer';
import GlassCard from '../components/common/GlassCard';

/**
 * ComingSoonPage — placeholder for routes reserved for Part 2
 * (Research Explorer, Technology Graph, Papers, GitHub, Datasets,
 * Patents, Tech Map, Timeline, Graph, Notes, Experiments, Research
 * Gaps, References, Risk, Recommendations, Analytics, Reports).
 *
 * Renders so the sidebar's "soon" links don't 404 during Part 1.
 */
export default function ComingSoonPage({ label }) {
  const location = useLocation();
  const derivedLabel =
    label ||
    location.pathname
      .split('/')
      .filter(Boolean)
      .pop()
      ?.replace(/-/g, ' ')
      ?.replace(/\b\w/g, (c) => c.toUpperCase()) ||
    'This section';

  return (
    <PageContainer>
      <GlassCard className="flex flex-col items-center gap-4 py-20 text-center">
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-indigo/10 text-indigo-soft">
          <Sparkles size={20} />
        </div>
        <div>
          <h1 className="font-display text-xl text-text">{derivedLabel} is coming in Part 2</h1>
          <p className="mx-auto mt-2 max-w-sm text-sm text-text-dim">
            This section of Revianta is reserved for the next phase of the build, once the
            research engine is wired up.
          </p>
        </div>
      </GlassCard>
    </PageContainer>
  );
}
