import { Link, useParams } from 'react-router-dom';
import { Menu, Bell, ChevronRight } from 'lucide-react';
import SearchBar from '../common/SearchBar';
import { MOCK_PROJECTS } from '../../constants/mockData';

/**
 * TopBar — premium header inside the application shell.
 * Shows the current page title, project context (breadcrumb) when
 * inside a project, global search, notifications, and profile.
 */
export default function TopBar({ title, onOpenMobileNav }) {
  const { projectId } = useParams();
  const project = projectId ? MOCK_PROJECTS.find((p) => p.id === projectId) : null;

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center gap-3 border-b border-line bg-base/70 px-4 backdrop-blur-xl sm:px-6">
      <button
        onClick={onOpenMobileNav}
        aria-label="Open navigation"
        className="rounded-lg p-2 text-text-dim hover:bg-white/[0.05] hover:text-text lg:hidden"
      >
        <Menu size={19} />
      </button>

      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-1.5 text-sm">
          {project && (
            <>
              <span className="truncate text-text-dim">{project.name}</span>
              <ChevronRight size={14} className="shrink-0 text-text-faint" />
            </>
          )}
          <h1 className="truncate font-display text-[15px] font-medium text-text">{title}</h1>
        </div>
      </div>

      <SearchBar className="hidden w-full max-w-xs md:flex" />

      <button
        aria-label="Notifications"
        className="relative rounded-lg p-2 text-text-dim hover:bg-white/[0.05] hover:text-text"
      >
        <Bell size={18} />
        <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-cyan" />
      </button>

      <Link
        to="/settings"
        aria-label="Settings"
        className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-indigo-soft to-violet text-xs font-semibold text-white"
      >
        RA
      </Link>
    </header>
  );
}
