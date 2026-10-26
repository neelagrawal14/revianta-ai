import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, FileText, FolderGit2, Database, ScrollText, Compass, Zap } from 'lucide-react';
import PageContainer from '../components/layout/PageContainer';
import GlassCard from '../components/common/GlassCard';
import Badge from '../components/common/Badge';
import EmptyState from '../components/common/EmptyState';
import { getPapersForProject } from '../constants/mock/mockPapers';
import { getRepositoriesForProject } from '../constants/mock/mockRepositories';
import { getDatasetsForProject } from '../constants/mock/mockDatasets';
import { getPatentsForProject } from '../constants/mock/mockPatents';
import { MOCK_PROJECTS } from '../constants/mockData';

// Pool results across every mock project so the unified search has
// something to find regardless of query — this is Revianta's single
// research index in miniature, not four separate search pages.
const ALL_PAPERS = MOCK_PROJECTS.flatMap((p) => getPapersForProject(p.id));
const ALL_REPOS = MOCK_PROJECTS.flatMap((p) => getRepositoriesForProject(p.id));
const ALL_DATASETS = MOCK_PROJECTS.flatMap((p) => getDatasetsForProject(p.id));
const ALL_PATENTS = MOCK_PROJECTS.flatMap((p) => getPatentsForProject(p.id));

const SECTIONS = [
  { id: 'papers', label: 'Papers', icon: FileText, tone: 'text-cyan', data: ALL_PAPERS, getTitle: (i) => i.title, getMeta: (i) => `${i.year} · ${i.source}` },
  { id: 'github', label: 'GitHub', icon: FolderGit2, tone: 'text-indigo-soft', data: ALL_REPOS, getTitle: (i) => i.name, getMeta: (i) => `${i.owner} · ${i.language}` },
  { id: 'datasets', label: 'Datasets', icon: Database, tone: 'text-violet', data: ALL_DATASETS, getTitle: (i) => i.name, getMeta: (i) => i.source },
  { id: 'patents', label: 'Patents', icon: ScrollText, tone: 'text-amber', data: ALL_PATENTS, getTitle: (i) => i.title, getMeta: (i) => `${i.inventor} · ${i.year}` },
];

export default function ResearchExplorerPage() {
  const [query, setQuery] = useState('');

  const results = useMemo(() => {
    if (!query.trim()) return SECTIONS;
    const q = query.toLowerCase();
    return SECTIONS.map((section) => ({
      ...section,
      data: section.data.filter((item) => section.getTitle(item).toLowerCase().includes(q)).slice(0, 6),
    }));
  }, [query]);

  const totalResults = results.reduce((sum, s) => sum + s.data.length, 0);

  return (
    <PageContainer>
      <p className="mono-tag text-indigo-soft">One research intelligence engine</p>
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="mt-2 font-display text-3xl text-text sm:text-4xl">Research Explorer</h1>
          <p className="mt-2 max-w-lg text-text-dim">
            Search papers, GitHub repositories, datasets, and patents in one place — mock results
            drawn from every project in this workspace.
          </p>
        </div>
        <Link
          to="/live-search"
          className="mt-1 flex shrink-0 items-center gap-1.5 rounded-full border border-indigo/30 bg-indigo/10 px-3.5 py-1.5 text-sm text-indigo-soft hover:bg-indigo/15"
        >
          <Zap size={14} /> Try Live Search (real data)
        </Link>
      </div>

      <label className="mt-8 flex h-14 w-full max-w-2xl items-center gap-3 rounded-full border border-line bg-white/[0.03] px-5 focus-within:border-indigo/40">
        <Search size={18} className="text-text-faint" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder='Try "AI Traffic Management"'
          className="w-full bg-transparent text-[15px] text-text placeholder:text-text-faint focus:outline-none"
        />
      </label>

      {totalResults > 0 ? (
        <div className="mt-10 space-y-10">
          {results.filter((s) => s.data.length > 0).map((section) => (
            <section key={section.id}>
              <div className="mb-3 flex items-center gap-2">
                <section.icon size={16} className={section.tone} />
                <h2 className="font-display text-base text-text">{section.label}</h2>
                <span className="text-xs text-text-faint">({section.data.length})</span>
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                {section.data.map((item, i) => (
                  <GlassCard key={i} className="flex items-start justify-between gap-3 p-4">
                    <div className="min-w-0">
                      <p className="truncate text-sm text-text">{section.getTitle(item)}</p>
                      <p className="mt-0.5 text-xs text-text-faint">{section.getMeta(item)}</p>
                    </div>
                    {item.similarity !== undefined && <Badge tone="cyan" className="shrink-0">{item.similarity}%</Badge>}
                    {item.relevance !== undefined && <Badge tone="cyan" className="shrink-0">{item.relevance}%</Badge>}
                  </GlassCard>
                ))}
              </div>
            </section>
          ))}
        </div>
      ) : (
        <EmptyState className="mt-10" icon={Compass} title="No results" description="Try a different search term." />
      )}
    </PageContainer>
  );
}
