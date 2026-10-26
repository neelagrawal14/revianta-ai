import { useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { BookMarked, ExternalLink, FileText } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import SearchBar from '../../components/common/SearchBar';
import SelectField from '../../components/common/SelectField';
import GlassCard from '../../components/common/GlassCard';
import Badge from '../../components/common/Badge';
import EmptyState from '../../components/common/EmptyState';
import { getPapersForProject } from '../../constants/mock';

const SORTS = [
  { value: 'similarity', label: 'Sort: Similarity' },
  { value: 'year', label: 'Sort: Newest' },
  { value: 'citations', label: 'Sort: Most cited' },
];

function PaperCard({ paper }) {
  const [saved, setSaved] = useState(false);
  return (
    <GlassCard className="p-5">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h3 className="font-display text-base text-text">{paper.title}</h3>
          <p className="mt-1 text-sm text-text-dim">
            {paper.authors.join(', ')} · {paper.year} · {paper.source}
          </p>
        </div>
        <div className="flex shrink-0 flex-col items-end gap-1">
          <span className="font-mono text-sm text-cyan">{paper.similarity}%</span>
          <span className="text-[11px] text-text-faint">similarity</span>
        </div>
      </div>

      <p className="mt-3 text-sm leading-relaxed text-text-dim">{paper.abstract}</p>

      <div className="mt-4 flex flex-wrap gap-1.5">
        {paper.technologies.map((t) => (
          <Badge key={t}>{t}</Badge>
        ))}
      </div>

      <div className="mt-4 flex items-center justify-between border-t border-line pt-4">
        <span className="text-xs text-text-faint">{paper.citationCount} citations</span>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSaved((v) => !v)}
            className={`flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs transition-colors ${
              saved ? 'border-indigo/35 bg-indigo/10 text-indigo-soft' : 'border-line text-text-dim hover:text-text'
            }`}
          >
            <BookMarked size={13} />
            {saved ? 'Saved' : 'Save'}
          </button>
          <button className="flex items-center gap-1.5 rounded-full border border-line px-3 py-1.5 text-xs text-text-dim hover:text-text">
            Open <ExternalLink size={12} />
          </button>
        </div>
      </div>
    </GlassCard>
  );
}

export default function ProjectPapersPage() {
  const { projectId } = useParams();
  const papers = useMemo(() => getPapersForProject(projectId), [projectId]);
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState('similarity');

  const filtered = useMemo(() => {
    let list = papers.filter((p) => p.title.toLowerCase().includes(query.toLowerCase()));
    if (sort === 'similarity') list = [...list].sort((a, b) => b.similarity - a.similarity);
    if (sort === 'year') list = [...list].sort((a, b) => b.year - a.year);
    if (sort === 'citations') list = [...list].sort((a, b) => b.citationCount - a.citationCount);
    return list;
  }, [papers, query, sort]);

  return (
    <PageContainer>
      <SectionHeader
        title="Papers"
        description="Research papers Revianta found most similar to this project — mock results shown until the research API is connected."
      />

      <div className="mt-6 flex flex-wrap items-center gap-3">
        <SearchBar
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search papers…"
          hint={null}
          className="h-11 w-full max-w-sm"
        />
        <SelectField value={sort} onChange={(e) => setSort(e.target.value)} options={SORTS} />
      </div>

      {filtered.length > 0 ? (
        <div className="mt-6 grid gap-4 lg:grid-cols-2">
          {filtered.map((paper) => (
            <PaperCard key={paper.id} paper={paper} />
          ))}
        </div>
      ) : (
        <EmptyState
          className="mt-8"
          icon={FileText}
          title="No papers match your search"
          description="Try a different search term, or clear the search to see all results."
        />
      )}
    </PageContainer>
  );
}
