import { useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Database, Download, Award } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import SearchBar from '../../components/common/SearchBar';
import GlassCard from '../../components/common/GlassCard';
import Badge from '../../components/common/Badge';
import EmptyState from '../../components/common/EmptyState';
import { getDatasetsForProject } from '../../constants/mock';

const STATUS_TONE = {
  AVAILABLE: 'cyan',
  RESTRICTED: 'amber',
  GATED: 'rose',
  'MUST BUILD': 'rose',
  UNKNOWN: 'neutral',
};

function DatasetCard({ dataset }) {
  return (
    <GlassCard interactive glow={dataset.bestMatch ? 'cyan' : undefined} className="p-5">
      {dataset.bestMatch && (
        <div className="mb-3 flex items-center gap-1.5 text-xs font-medium text-cyan">
          <Award size={13} /> BEST DATASET MATCH
        </div>
      )}
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h3 className="font-display text-base text-text">{dataset.name}</h3>
          <p className="mt-1 text-sm text-text-dim">{dataset.source}</p>
        </div>
        <span className="shrink-0 font-mono text-sm text-cyan">{dataset.relevance}%</span>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-3 border-t border-line pt-4 text-xs text-text-faint">
        <div>
          <p className="flex items-center gap-1"><Download size={11} /> Downloads</p>
          <p className="mt-1 font-mono text-text-dim">{dataset.downloads.toLocaleString()}</p>
        </div>
        <div>
          <p>Size</p>
          <p className="mt-1 font-mono text-text-dim">{dataset.size}</p>
        </div>
        <div>
          <p>Category</p>
          <p className="mt-1 text-text-dim">{dataset.category}</p>
        </div>
      </div>

      <div className="mt-4 flex items-center justify-between border-t border-line pt-4">
        <Badge tone={STATUS_TONE[dataset.accessStatus] || 'neutral'}>{dataset.accessStatus}</Badge>
        <button className="text-sm font-medium text-indigo-soft hover:text-cyan">View source</button>
      </div>
    </GlassCard>
  );
}

export default function ProjectDatasetsPage() {
  const { projectId } = useParams();
  const datasets = useMemo(() => getDatasetsForProject(projectId), [projectId]);
  const [query, setQuery] = useState('');

  const filtered = datasets.filter((d) => d.name.toLowerCase().includes(query.toLowerCase()));

  return (
    <PageContainer>
      <SectionHeader
        title="Datasets"
        description="Datasets Revianta identified as relevant to this project, with access status and relevance scoring."
      />

      <SearchBar value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search datasets…" hint={null} className="mt-6 h-11 w-full max-w-sm" />

      {filtered.length > 0 ? (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {filtered.map((dataset) => (
            <DatasetCard key={dataset.id} dataset={dataset} />
          ))}
        </div>
      ) : (
        <EmptyState className="mt-8" icon={Database} title="No datasets match" description="Try a different search term." />
      )}
    </PageContainer>
  );
}
