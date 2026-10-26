import { Link } from 'react-router-dom';
import FuturisticBackground from '../../components/common/FuturisticBackground';
import NodeGraph from '../../components/common/NodeGraph';

/**
 * AuthLayout — full-screen dark environment + futuristic visual +
 * glass panel, shared by /login and /register.
 */
export default function AuthLayout({ eyebrow, title, subtitle, children }) {
  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-4 py-10">
      <FuturisticBackground variant="cinematic" />

      <div className="grid w-full max-w-5xl items-center gap-10 lg:grid-cols-[1fr_1.1fr] lg:gap-16">
        {/* visual side */}
        <div className="hidden lg:block">
          <Link to="/" className="mb-8 flex items-center gap-2.5">
            <svg width="26" height="26" viewBox="0 0 32 32">
              <rect width="32" height="32" rx="8" fill="var(--color-surface-2)" />
              <circle cx="16" cy="9" r="2.4" fill="var(--color-cyan)" />
              <circle cx="8" cy="21" r="2.4" fill="var(--color-indigo)" />
              <circle cx="24" cy="21" r="2.4" fill="var(--color-violet)" />
              <path d="M16 9 L8 21 M16 9 L24 21 M8 21 L24 21" stroke="var(--color-indigo)" strokeWidth="1.1" opacity="0.6" />
            </svg>
            <span className="font-display text-[15px] font-medium text-text">Revianta AI</span>
          </Link>
          <h2 className="max-w-sm font-display text-3xl leading-tight text-text">
            Research intelligence, before you build.
          </h2>
          <div className="glass mt-8 rounded-[24px] p-5">
            <NodeGraph className="h-auto w-full opacity-90" />
          </div>
        </div>

        {/* form side */}
        <div className="glass-strong mx-auto w-full max-w-md rounded-[24px] p-8 shadow-panel sm:p-10">
          <Link to="/" className="mb-8 flex items-center gap-2.5 lg:hidden">
            <svg width="24" height="24" viewBox="0 0 32 32">
              <rect width="32" height="32" rx="8" fill="var(--color-surface-2)" />
              <circle cx="16" cy="9" r="2.4" fill="var(--color-cyan)" />
              <circle cx="8" cy="21" r="2.4" fill="var(--color-indigo)" />
              <circle cx="24" cy="21" r="2.4" fill="var(--color-violet)" />
              <path d="M16 9 L8 21 M16 9 L24 21 M8 21 L24 21" stroke="var(--color-indigo)" strokeWidth="1.1" opacity="0.6" />
            </svg>
            <span className="font-display text-[15px] font-medium text-text">Revianta AI</span>
          </Link>

          {eyebrow && <p className="mono-tag text-indigo-soft">{eyebrow}</p>}
          <h1 className="mt-2 font-display text-2xl text-text">{title}</h1>
          {subtitle && <p className="mt-2 text-sm text-text-dim">{subtitle}</p>}

          <div className="mt-8">{children}</div>
        </div>
      </div>
    </div>
  );
}
