import { useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Star, GitFork, Clock3, FolderGit2 } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import SearchBar from '../../components/common/SearchBar';
import SelectField from '../../components/common/SelectField';
import GlassCard from '../../components/common/GlassCard';
import Badge from '../../components/common/Badge';
import EmptyState from '../../components/common/EmptyState';
import { getRepositoriesForProject } from '../../constants/mock';

const SORTS = [
  { value: 'similarity', label: 'Sort: Similarity' },
  { value: 'stars', label: 'Sort: Most stars' },
  { value: 'recent', label: 'Sort: Recently updated' },
];

const ACTIVITY_TONE = { Active: 'cyan', Moderate: 'amber', Archived: 'neutral' };

function RepoCard({ repo }) {
  return (
    <GlassCard interactive className="p-5">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <div className="flex items-center gap-1.5 text-sm text-text-faint">
            <FolderGit2 size={14} />
            {repo.owner}
          </div>
          <h3 className="mt-0.5 truncate font-display text-base text-text">{repo.name}</h3>
        </div>
        <span className="shrink-0 font-mono text-sm text-cyan">{repo.similarity}%</span>
      </div>

      <p className="mt-2 text-sm text-text-dim">{repo.description}</p>

      <div className="mt-3 flex flex-wrap gap-1.5">
        {repo.topics.map((t) => (
          <Badge key={t}>{t}</Badge>
        ))}
      </div>

      <div className="mt-4 flex flex-wrap items-center justify-between gap-2 border-t border-line pt-4 text-xs text-text-faint">
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1"><Star size={12} /> {repo.stars.toLocaleString()}</span>
          <span className="flex items-center gap-1"><GitFork size={12} /> {repo.language}</span>
          <span className="flex items-center gap-1"><Clock3 size={12} /> {repo.lastUpdated}</span>
        </div>
        <Badge tone={ACTIVITY_TONE[repo.activity] || 'neutral'}>{repo.activity}</Badge>
      </div>
    </GlassCard>
  );
}

export default function ProjectGithubPage() {
  const { projectId } = useParams();
  const repos = useMemo(() => getRepositoriesForProject(projectId), [projectId]);
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState('similarity');

  const filtered = useMemo(() => {
    let list = repos.filter((r) => r.name.toLowerCase().includes(query.toLowerCase()));
    if (sort === 'similarity') list = [...list].sort((a, b) => b.similarity - a.similarity);
    if (sort === 'stars') list = [...list].sort((a, b) => b.stars - a.stars);
    return list;
  }, [repos, query, sort]);

  return (
    <PageContainer>
      <SectionHeader
        title="GitHub"
        description="Open-source repositories with implementations related to this project."
      />

      <div className="mt-6 flex flex-wrap items-center gap-3">
        <SearchBar value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search repositories…" hint={null} className="h-11 w-full max-w-sm" />
        <SelectField value={sort} onChange={(e) => setSort(e.target.value)} options={SORTS} />
      </div>

      {filtered.length > 0 ? (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {filtered.map((repo) => (
            <RepoCard key={repo.id} repo={repo} />
          ))}
        </div>
      ) : (
        <EmptyState className="mt-8" icon={FolderGit2} title="No repositories match" description="Try a different search term." />
      )}
    </PageContainer>
  );
}
