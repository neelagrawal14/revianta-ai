import { Link } from 'react-router-dom';

const COLUMNS = [
  {
    heading: 'Product',
    links: [
      { label: 'How it works', href: '#how-it-works' },
      { label: 'Intelligence Engine', href: '#intelligence-engine' },
      { label: 'Workspace', href: '#workspace' },
      { label: 'Knowledge Graph', href: '#knowledge-graph' },
    ],
  },
  {
    heading: 'Account',
    links: [
      { label: 'Log in', to: '/login' },
      { label: 'Create account', to: '/register' },
      { label: 'Dashboard', to: '/dashboard' },
    ],
  },
];

export default function Footer() {
  return (
    <footer className="border-t border-line px-4 py-14 sm:px-6">
      <div className="mx-auto flex max-w-6xl flex-col gap-10 lg:flex-row lg:justify-between">
        <div className="max-w-xs">
          <div className="flex items-center gap-2.5">
            <svg width="22" height="22" viewBox="0 0 32 32">
              <rect width="32" height="32" rx="8" fill="var(--color-surface-2)" />
              <circle cx="16" cy="9" r="2.4" fill="var(--color-cyan)" />
              <circle cx="8" cy="21" r="2.4" fill="var(--color-indigo)" />
              <circle cx="24" cy="21" r="2.4" fill="var(--color-violet)" />
              <path d="M16 9 L8 21 M16 9 L24 21 M8 21 L24 21" stroke="var(--color-indigo)" strokeWidth="1.1" opacity="0.6" />
            </svg>
            <span className="font-display text-[15px] text-text">Revianta AI</span>
          </div>
          <p className="mt-3 text-sm text-text-faint">
            Research intelligence, before you build. Formerly known as NOVA.
          </p>
        </div>

        <div className="flex gap-16">
          {COLUMNS.map((col) => (
            <div key={col.heading}>
              <p className="text-sm font-medium text-text">{col.heading}</p>
              <ul className="mt-3 space-y-2.5">
                {col.links.map((l) => (
                  <li key={l.label}>
                    {l.to ? (
                      <Link to={l.to} className="text-sm text-text-faint hover:text-text-dim">
                        {l.label}
                      </Link>
                    ) : (
                      <a href={l.href} className="text-sm text-text-faint hover:text-text-dim">
                        {l.label}
                      </a>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      <div className="mx-auto mt-12 max-w-6xl border-t border-line pt-6 text-xs text-text-faint">
        © {new Date().getFullYear()} Revianta AI. All rights reserved.
      </div>
    </footer>
  );
}
