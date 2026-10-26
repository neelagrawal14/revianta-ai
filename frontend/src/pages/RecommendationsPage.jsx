import { Link } from 'react-router-dom';
import { ArrowUpRight, Sparkles } from 'lucide-react';
import PageContainer from '../components/layout/PageContainer';
import GlassCard from '../components/common/GlassCard';
import Badge from '../components/common/Badge';
import EmptyState from '../components/common/EmptyState';
import { MOCK_RECOMMENDATIONS, getProjectName } from '../constants/mock/mockRecommendations';

const SEVERITY_TONE = { high: 'rose', medium: 'amber', low: 'cyan' };

export default function RecommendationsPage() {
  return (
    <PageContainer>
      <p className="mono-tag text-indigo-soft">Derived from project intelligence</p>
      <h1 className="mt-2 font-display text-3xl text-text sm:text-4xl">Recommendations</h1>
      <p className="mt-2 max-w-lg text-text-dim">
        Actionable suggestions based on each project's risk and similarity analysis.
      </p>

      {MOCK_RECOMMENDATIONS.length > 0 ? (
        <div className="mt-8 grid gap-4 lg:grid-cols-2">
          {MOCK_RECOMMENDATIONS.map((rec) => (
            <GlassCard key={rec.id} className="p-5">
              <div className="flex items-start justify-between gap-3">
                <Badge tone={SEVERITY_TONE[rec.severity] || 'amber'}>{rec.riskFlag}</Badge>
                <Link to={`/projects/${rec.projectId}`} className="flex shrink-0 items-center gap-1 text-xs text-text-faint hover:text-text-dim">
                  {getProjectName(rec.projectId)} <ArrowUpRight size={11} />
                </Link>
              </div>

              <div className="mt-4 flex items-start gap-2">
                <Sparkles size={15} className="mt-0.5 shrink-0 text-indigo-soft" />
                <p className="text-[15px] text-text">{rec.recommendation}</p>
              </div>

              <p className="mt-3 text-sm text-text-dim"><span className="text-text-faint">Why it matters — </span>{rec.why}</p>
              <p className="mt-3 border-t border-line pt-3 text-xs text-text-faint">
                <span className="text-text-dim">Expected impact — </span>{rec.expectedImpact}
              </p>
            </GlassCard>
          ))}
        </div>
      ) : (
        <EmptyState className="mt-8" icon={Sparkles} title="No recommendations yet" description="Run research intelligence on a project to generate recommendations." />
      )}
    </PageContainer>
  );
}
