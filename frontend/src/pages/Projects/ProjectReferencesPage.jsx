import { useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { FileText, FolderGit2, Database, ScrollText, BookMarked } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import SearchBar from '../../components/common/SearchBar';
import GlassCard from '../../components/common/GlassCard';
import Badge from '../../components/common/Badge';
import EmptyState from '../../components/common/EmptyState';
import { getPapersForProject, getRepositoriesForProject, getDatasetsForProject, getPatentsForProject } from '../../constants/mock';
import { cn } from '../../utils/cn';

const TYPES = [
  { id: 'all', label: 'All', icon: BookMarked },
  { id: 'paper', label: 'Papers', icon: FileText },
  { id: 'repo', label: 'GitHub', icon: FolderGit2 },
  { id: 'dataset', label: 'Datasets', icon: Database },
  { id: 'patent', label: 'Patents', icon: ScrollText },
];

/**
 * References — a saved-items shelf pulling the top result from each
 * research source. There's no cross-page "save" persistence yet (each
 * list page's Save button is local UI state), so this shows Revianta's
 * top pick per source as a stand-in for "what you've saved".
 */
export default function ProjectReferencesPage() {
  const { projectId } = useParams();
  const [type, setType] = useState('all');
  const [query, setQuery] = useState('');

  const items = useMemo(() => {
    const papers = getPapersForProject(projectId)
      .slice(0, 3)
      .map((p) => ({ id: p.id, type: 'paper', title: p.title, meta: `${p.year} · ${p.source}`, score: p.similarity }));
    const repos = getRepositoriesForProject(projectId)
      .slice(0, 2)
      .map((r) => ({ id: r.id, type: 'repo', title: r.name, meta: `${r.owner} · ${r.language}`, score: r.similarity }));
    const datasets = getDatasetsForProject(projectId)
      .slice(0, 2)
      .map((d) => ({ id: d.id, type: 'dataset', title: d.name, meta: d.source, score: d.relevance }));
    const patents = getPatentsForProject(projectId)
      .slice(0, 2)
      .map((p) => ({ id: p.id, type: 'patent', title: p.title, meta: `${p.inventor} · ${p.year}`, score: p.similarity }));
    return [...papers, ...repos, ...datasets, ...patents];
  }, [projectId]);

  const filtered = items.filter(
    (i) => (type === 'all' || i.type === type) && i.title.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <PageContainer>
      <SectionHeader title="References" description="Saved papers, repositories, datasets, and patents for this project, in one shelf." />

      <div className="mt-6 flex flex-wrap items-center gap-3">
        <SearchBar value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search references…" hint={null} className="h-11 w-full max-w-sm" />
        <div className="flex flex-wrap gap-1.5">
          {TYPES.map((t) => (
            <button
              key={t.id}
              onClick={() => setType(t.id)}
              className={cn(
                'flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs transition-colors',
                type === t.id ? 'border-indigo/35 bg-indigo/10 text-indigo-soft' : 'border-line text-text-dim hover:text-text'
              )}
            >
              <t.icon size={13} /> {t.label}
            </button>
          ))}
        </div>
      </div>

      {filtered.length > 0 ? (
        <div className="mt-6 grid gap-3 sm:grid-cols-2">
          {filtered.map((item) => {
            const Icon = TYPES.find((t) => t.id === item.type)?.icon || BookMarked;
            return (
              <GlassCard key={`${item.type}-${item.id}`} className="flex items-start gap-3 p-4">
                <Icon size={16} className="mt-0.5 shrink-0 text-indigo-soft" />
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm text-text">{item.title}</p>
                  <p className="mt-0.5 text-xs text-text-faint">{item.meta}</p>
                </div>
                <Badge tone="cyan" className="shrink-0">{item.score}%</Badge>
              </GlassCard>
            );
          })}
        </div>
      ) : (
        <EmptyState className="mt-8" icon={BookMarked} title="No references match" description="Try a different search term or type filter." />
      )}
    </PageContainer>
  );
}
