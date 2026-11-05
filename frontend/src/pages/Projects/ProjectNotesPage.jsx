import { useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Pin, Plus, Search, Trash2, NotebookText } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import GlassCard from '../../components/common/GlassCard';
import GlowButton from '../../components/common/GlowButton';
import Badge from '../../components/common/Badge';
import EmptyState from '../../components/common/EmptyState';
import { getNotesForProject } from '../../constants/mock';
import { cn } from '../../utils/cn';

/**
 * ProjectNotesPage — notes live in local component state, seeded from
 * mock data. There's no persistence yet (no backend), so refreshing the
 * page resets anything you add here — that's expected for Part 2.
 */
export default function ProjectNotesPage() {
  const { projectId } = useParams();
  const seedNotes = useMemo(() => getNotesForProject(projectId), [projectId]);
  const [notes, setNotes] = useState(seedNotes);
  const [query, setQuery] = useState('');
  const [draft, setDraft] = useState('');

  const filtered = notes
    .filter((n) => n.title.toLowerCase().includes(query.toLowerCase()) || n.tags.some((t) => t.includes(query.toLowerCase())))
    .sort((a, b) => Number(b.pinned) - Number(a.pinned));

  function addNote() {
    if (!draft.trim()) return;
    setNotes((prev) => [
      { id: `local-${Date.now()}`, title: draft.trim(), body: '', tags: [], pinned: false, updatedAt: 'just now' },
      ...prev,
    ]);
    setDraft('');
  }

  function togglePin(id) {
    setNotes((prev) => prev.map((n) => (n.id === id ? { ...n, pinned: !n.pinned } : n)));
  }

  function removeNote(id) {
    setNotes((prev) => prev.filter((n) => n.id !== id));
  }

  return (
    <PageContainer>
      <SectionHeader title="Notes" description="Research notes for this project — organize, pin, and tag as you go." />

      <GlassCard tone="strong" className="mt-6 flex flex-col gap-3 p-4 sm:flex-row sm:items-center">
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && addNote()}
          placeholder="Quick note title…"
          className="h-10 flex-1 rounded-xl border border-line bg-white/[0.03] px-3.5 text-sm text-text placeholder:text-text-faint focus:border-indigo/40 focus:outline-none"
        />
        <GlowButton size="sm" onClick={addNote}>
          <Plus size={15} /> Add note
        </GlowButton>
      </GlassCard>

      <label className="mt-4 flex h-10 max-w-xs items-center gap-2.5 rounded-full border border-line bg-white/[0.03] px-4">
        <Search size={15} className="text-text-faint" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search notes or tags…"
          className="w-full bg-transparent text-sm text-text placeholder:text-text-faint focus:outline-none"
        />
      </label>

      {filtered.length > 0 ? (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {filtered.map((note) => (
            <GlassCard key={note.id} className={cn('p-5', note.pinned && 'border-indigo/30')}>
              <div className="flex items-start justify-between gap-3">
                <h3 className="font-display text-[15px] text-text">{note.title}</h3>
                <div className="flex shrink-0 gap-1">
                  <button
                    onClick={() => togglePin(note.id)}
                    aria-label={note.pinned ? 'Unpin note' : 'Pin note'}
                    className={cn('rounded-lg p-1.5', note.pinned ? 'text-indigo-soft' : 'text-text-faint hover:text-text-dim')}
                  >
                    <Pin size={14} fill={note.pinned ? 'currentColor' : 'none'} />
                  </button>
                  <button onClick={() => removeNote(note.id)} aria-label="Delete note" className="rounded-lg p-1.5 text-text-faint hover:text-rose">
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
              {note.body && <p className="mt-2 text-sm text-text-dim">{note.body}</p>}
              <div className="mt-3 flex flex-wrap items-center justify-between gap-2">
                <div className="flex flex-wrap gap-1.5">
                  {note.tags.map((t) => (
                    <Badge key={t}>{t}</Badge>
                  ))}
                </div>
                <span className="text-xs text-text-faint">{note.updatedAt}</span>
              </div>
            </GlassCard>
          ))}
        </div>
      ) : (
        <EmptyState className="mt-8" icon={NotebookText} title="No notes yet" description="Add your first note above to start capturing research thoughts." />
      )}
    </PageContainer>
  );
}
