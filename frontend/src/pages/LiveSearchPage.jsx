
import { useState } from 'react';
import { Search, ExternalLink, Star, Database, FileText, Code2, Lightbulb } from 'lucide-react';
import PageContainer from '../components/layout/PageContainer';
import GlassCard from '../components/common/GlassCard';
import Badge from '../components/common/Badge';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import { cn } from '../utils/cn';
import {
  searchPapersLive,
  searchGithubLive,
  searchDatasetsLive,
  searchPatentsLive,
  LiveSearchError,
} from '../services/liveSearchApi';

const TABS = [
  { id: 'papers', label: 'Papers', icon: FileText },
  { id: 'github', label: 'GitHub', icon: Code2 },
  { id: 'datasets', label: 'Datasets', icon: Database },
  { id: 'patents', label: 'Patents', icon: Lightbulb },
];

const SEARCHERS = {
  papers: searchPapersLive,
  github: searchGithubLive,
  datasets: searchDatasetsLive,
  patents: searchPatentsLive,
};

const PLACEHOLDERS = {
  papers: 'Search papers, e.g. computer vision',
  github: 'Search repositories, e.g. traffic prediction',
  datasets: 'Search datasets, e.g. satellite imagery',
  patents: 'Search patents, e.g. object detection',
};

export default function LiveSearchPage() {
  const [tab, setTab] = useState('papers');
  const [query, setQuery] = useState('');
  const [status, setStatus] = useState('idle');
  const [error, setError] = useState(null);
  const [results, setResults] = useState([]);

  const activeTab = TABS.find((item) => item.id === tab);

  async function runSearch(event) {
    event?.preventDefault();

    if (!query.trim()) {
      setError('Enter a search query.');
      setStatus('error');
      return;
    }

    setStatus('loading');
    setError(null);
    setResults([]);

    try {
      const data = await SEARCHERS[tab](query, { limit: 10 });
      setResults(data);
      setStatus('done');
    } catch (err) {
      setError(
        err instanceof LiveSearchError
          ? err.message
          : 'Unable to reach the research provider. Please try again.',
      );
      setStatus('error');
    }
  }

  function switchTab(id) {
    setTab(id);
    setStatus('idle');
    setResults([]);
    setError(null);
  }

  return (
    <PageContainer>
      <p className="mono-tag text-indigo-soft">LIVE RESEARCH INTELLIGENCE</p>

      <h1 className="mt-2 font-display text-3xl text-text sm:text-4xl">
        Live Search
      </h1>

      <p className="mt-2 max-w-2xl text-text-dim">
        Discover research publications, open-source projects, machine-learning
        datasets, and patent-search resources through the Revianta AI backend.
        Results are fetched from external providers.
      </p>

      <div className="mt-6 flex flex-wrap gap-2">
        {TABS.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.id}
              type="button"
              onClick={() => switchTab(item.id)}
              className={cn(
                'flex items-center gap-2 rounded-full border px-4 py-2 text-sm transition-colors',
                tab === item.id
                  ? 'border-indigo/35 bg-indigo/10 text-indigo-soft'
                  : 'border-line text-text-dim hover:text-text',
              )}
            >
              <Icon size={15} />
              {item.label}
            </button>
          );
        })}
      </div>

      <form
        onSubmit={runSearch}
        className="mt-6 flex h-12 w-full max-w-2xl items-center gap-3 rounded-full border border-line bg-white/[0.03] px-5 focus-within:border-indigo/40"
      >
        <Search size={17} className="shrink-0 text-text-faint" />

        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={PLACEHOLDERS[tab]}
          aria-label={`Search ${activeTab.label}`}
          className="w-full bg-transparent text-sm text-text placeholder:text-text-faint focus:outline-none"
        />

        <button
          type="submit"
          disabled={status === 'loading'}
          className="rounded-full bg-indigo/20 px-4 py-1.5 text-sm text-indigo-soft transition hover:bg-indigo/30 disabled:opacity-50"
        >
          Search
        </button>
      </form>

      <p className="mt-2 text-xs text-text-faint">
        {activeTab.label} Â· External provider results Â· Maximum 10 per search
      </p>

      <div className="mt-8">
        {status === 'loading' && (
          <LoadingState label={`Searching ${activeTab.label.toLowerCase()}...`} />
        )}

        {status === 'error' && (
          <ErrorState
            title="Live search failed"
            description={error}
            actionLabel="Retry"
            onAction={runSearch}
          />
        )}

        {status === 'done' && results.length === 0 && (
          <EmptyState
            icon={Search}
            title="No results found"
            description="Try a different keyword or a broader search."
          />
        )}

        {status === 'done' && results.length > 0 && (
          <>
            <div className="mb-4 flex items-center justify-between">
              <h2 className="font-display text-lg text-text">
                Search results
              </h2>
              <span className="mono-tag text-text-faint">
                {results.length} results
              </span>
            </div>

            <div className="grid gap-4 lg:grid-cols-2">
              {results.map((item, index) => {
                const key = item.id ?? item.url ?? `${tab}-${index}`;

                if (tab === 'papers') {
                  return (
                    <GlassCard key={key} className="p-5">
                      <h3 className="font-display text-base text-text">
                        {item.title || 'Untitled paper'}
                      </h3>

                      <p className="mt-2 text-sm text-text-dim">
                        {(item.authors || []).slice(0, 4).join(', ') ||
                          'Authors unavailable'}
                        {item.year ? ` Â· ${item.year}` : ''}
                        {item.source ? ` Â· ${item.source}` : ''}
                      </p>

                      <p className="mt-3 line-clamp-4 text-sm text-text-dim">
                        {item.abstract || 'No abstract available.'}
                      </p>

                      <div className="mt-4 flex items-center justify-between border-t border-line pt-4 text-xs text-text-faint">
                        <span>{item.citationCount ?? 0} citations</span>
                        {item.url && (
                          <a
                            href={item.url}
                            target="_blank"
                            rel="noreferrer"
                            className="flex items-center gap-1 text-indigo-soft hover:text-cyan"
                          >
                            Open paper <ExternalLink size={12} />
                          </a>
                        )}
                      </div>
                    </GlassCard>
                  );
                }

                if (tab === 'github') {
                  return (
                    <GlassCard key={key} className="p-5">
                      <h3 className="break-words font-display text-base text-text">
                        {item.name || 'Unnamed repository'}
                      </h3>

                      <p className="mt-2 text-sm text-text-dim">
                        {item.description || 'No description provided.'}
                      </p>

                      <div className="mt-3 flex flex-wrap gap-1.5">
                        {(item.topics || []).slice(0, 5).map((topic) => (
                          <Badge key={topic}>{topic}</Badge>
                        ))}
                      </div>

                      <div className="mt-4 flex items-center justify-between border-t border-line pt-4 text-xs text-text-faint">
                        <span className="flex items-center gap-1">
                          <Star size={12} />
                          {(item.stars ?? 0).toLocaleString()} stars
                          {' Â· '}
                          {item.language || 'Unknown language'}
                        </span>

                        {item.url && (
                          <a
                            href={item.url}
                            target="_blank"
                            rel="noreferrer"
                            className="flex items-center gap-1 text-indigo-soft hover:text-cyan"
                          >
                            Open repo <ExternalLink size={12} />
                          </a>
                        )}
                      </div>
                    </GlassCard>
                  );
                }

                if (tab === 'datasets') {
                  return (
                    <GlassCard key={key} className="p-5">
                      <div className="flex items-start gap-3">
                        <Database size={19} className="mt-1 shrink-0 text-indigo-soft" />
                        <div className="min-w-0">
                          <h3 className="break-words font-display text-base text-text">
                            {item.name || item.id || 'Unnamed dataset'}
                          </h3>
                          <p className="mt-2 text-sm text-text-dim">
                            {item.description || 'Dataset hosted by an external provider.'}
                          </p>
                        </div>
                      </div>

                      <div className="mt-4 flex flex-wrap gap-3 text-xs text-text-faint">
                        <span>
                          Downloads: {(item.downloads ?? 0).toLocaleString()}
                        </span>
                        <span>Likes: {(item.likes ?? 0).toLocaleString()}</span>
                        {item.source && <span>{item.source}</span>}
                      </div>

                      <div className="mt-4 border-t border-line pt-4 text-right">
                        {item.url && (
                          <a
                            href={item.url}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1 text-xs text-indigo-soft hover:text-cyan"
                          >
                            Open dataset <ExternalLink size={12} />
                          </a>
                        )}
                      </div>
                    </GlassCard>
                  );
                }

                return (
                  <GlassCard key={key} className="p-5">
                    <div className="flex items-start gap-3">
                      <Lightbulb size={19} className="mt-1 shrink-0 text-indigo-soft" />
                      <div className="min-w-0">
                        <h3 className="font-display text-base text-text">
                          {item.title || 'Patent search'}
                        </h3>
                        <p className="mt-2 text-sm text-text-dim">
                          {item.abstract || 'Search external patent records for this topic.'}
                        </p>
                        {item.source && (
                          <p className="mt-3 text-xs text-text-faint">
                            Provider: {item.source}
                          </p>
                        )}
                      </div>
                    </div>

                    <div className="mt-4 border-t border-line pt-4">
                      <a
                        href={item.searchUrl || item.url}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 text-sm text-indigo-soft hover:text-cyan"
                      >
                        Search patent records <ExternalLink size={13} />
                      </a>
                    </div>
                  </GlassCard>
                );
              })}
            </div>
          </>
        )}
      </div>
    </PageContainer>
  );
}

