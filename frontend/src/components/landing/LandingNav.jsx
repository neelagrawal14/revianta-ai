import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import GlowButton from '../common/GlowButton';

const LINKS = [
  { label: 'How it works', href: '#how-it-works' },
  { label: 'Intelligence Engine', href: '#intelligence-engine' },
  { label: 'Workspace', href: '#workspace' },
  { label: 'Knowledge Graph', href: '#knowledge-graph' },
];

export default function LandingNav() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed inset-x-0 top-0 z-50">
      <div className="mx-auto mt-3 flex max-w-6xl items-center justify-between rounded-full border border-line bg-surface/60 px-4 py-2.5 backdrop-blur-xl sm:px-5">
        <Link to="/" className="flex items-center gap-2.5">
          <svg width="24" height="24" viewBox="0 0 32 32">
            <rect width="32" height="32" rx="8" fill="var(--color-surface-2)" />
            <circle cx="16" cy="9" r="2.4" fill="var(--color-cyan)" />
            <circle cx="8" cy="21" r="2.4" fill="var(--color-indigo)" />
            <circle cx="24" cy="21" r="2.4" fill="var(--color-violet)" />
            <path d="M16 9 L8 21 M16 9 L24 21 M8 21 L24 21" stroke="var(--color-indigo)" strokeWidth="1.1" opacity="0.6" />
          </svg>
          <span className="font-display text-[15px] font-medium tracking-tight text-text">Revianta AI</span>
        </Link>

        <nav className="hidden items-center gap-7 lg:flex">
          {LINKS.map((l) => (
            <a key={l.href} href={l.href} className="text-sm text-text-dim transition-colors hover:text-text">
              {l.label}
            </a>
          ))}
        </nav>

        <div className="hidden items-center gap-3 lg:flex">
          <Link to="/login" className="text-sm text-text-dim transition-colors hover:text-text">
            Log in
          </Link>
          <GlowButton as={Link} to="/register" size="sm">
            Start a project
          </GlowButton>
        </div>

        <button
          className="rounded-lg p-2 text-text lg:hidden"
          onClick={() => setOpen((v) => !v)}
          aria-label={open ? 'Close menu' : 'Open menu'}
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {open && (
        <div className="mx-4 mt-2 flex flex-col gap-1 rounded-2xl border border-line bg-surface/95 p-3 backdrop-blur-xl lg:hidden">
          {LINKS.map((l) => (
            <a
              key={l.href}
              href={l.href}
              onClick={() => setOpen(false)}
              className="rounded-lg px-3 py-2.5 text-sm text-text-dim hover:bg-white/[0.05] hover:text-text"
            >
              {l.label}
            </a>
          ))}
          <div className="mt-1 flex gap-2 border-t border-line pt-3">
            <Link to="/login" className="flex-1 rounded-xl border border-line py-2.5 text-center text-sm text-text-dim">
              Log in
            </Link>
            <Link to="/register" className="flex-1 rounded-xl bg-indigo py-2.5 text-center text-sm text-white">
              Start a project
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
