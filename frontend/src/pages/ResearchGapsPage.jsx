import { useMemo, useState } from 'react';
import PageContainer from '../components/layout/PageContainer';
import SelectField from '../components/common/SelectField';
import GapCard from '../components/research/GapCard';
import EmptyState from '../components/common/EmptyState';
import { ShieldAlert } from 'lucide-react';
import { MOCK_RESEARCH_GAPS } from '../constants/mock/mockGaps';

const DOMAINS = [...new Set(MOCK_RESEARCH_GAPS.map((g) => g.domain))];
const FILTERS = [{ value: 'all', label: 'All domains' }, ...DOMAINS.map((d) => ({ value: d, label: d }))];

export default function ResearchGapsPage() {
  const [domain, setDomain] = useState('all');
  const gaps = useMemo(
    () => (domain === 'all' ? MOCK_RESEARCH_GAPS : MOCK_RESEARCH_GAPS.filter((g) => g.domain === domain)),
    [domain]
  );

  return (
    <PageContainer>
      <p className="mono-tag text-indigo-soft">Across your research workspace</p>
      <h1 className="mt-2 font-display text-3xl text-text sm:text-4xl">Research Gaps</h1>
      <p className="mt-2 max-w-lg text-text-dim">
        Underexplored technology combinations, coverage gaps, and contradictory findings Revianta has
        flagged. These are illustrative UI suggestions, not scientifically validated conclusions.
      </p>

      <SelectField value={domain} onChange={(e) => setDomain(e.target.value)} options={FILTERS} className="mt-6" />

      {gaps.length > 0 ? (
        <div className="mt-6 grid gap-4 lg:grid-cols-2">
          {gaps.map((gap) => (
            <GapCard key={gap.id} gap={gap} />
          ))}
        </div>
      ) : (
        <EmptyState className="mt-8" icon={ShieldAlert} title="No gaps for this domain" description="Try a different domain filter." />
      )}
    </PageContainer>
  );
}
