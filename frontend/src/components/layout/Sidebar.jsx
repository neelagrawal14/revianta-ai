import { NavLink, useParams } from 'react-router-dom';
import { ChevronsLeft, ChevronsRight, Clock3 } from 'lucide-react';
import { WORKSPACE_NAV, PROJECT_NAV } from '../../constants/navigation';
import { MOCK_PROJECTS } from '../../constants/mockData';
import { cn } from '../../utils/cn';

/**
 * Sidebar — primary application navigation.
 * Switches between workspace-level nav and project-scoped nav based on
 * the current route (`/projects/:projectId/*`). Collapsible (state owned
 * by AppShell so the main content can react to width), with tooltips on
 * hover when collapsed.
 */
export default function Sidebar({ mobileOpen, onCloseMobile, collapsed, onToggleCollapsed }) {
  const { projectId } = useParams();
  const project = projectId ? MOCK_PROJECTS.find((p) => p.id === projectId) : null;

  const items = project
    ? PROJECT_NAV.map((item) => ({
        label: item.label,
        icon: item.icon,
        soon: item.soon,
        to: `/projects/${projectId}${item.path ? `/${item.path}` : ''}`,
        end: item.path === '',
      }))
    : WORKSPACE_NAV.map((item) => ({ ...item, end: item.to === '/dashboard' }));

  return (
    <>
      {/* mobile scrim */}
      {mobileOpen && (
        <button
          aria-label="Close navigation"
          onClick={onCloseMobile}
          className="fixed inset-0 z-30 bg-black/60 backdrop-blur-sm lg:hidden"
        />
      )}

      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-40 flex flex-col border-r border-line bg-surface/80 backdrop-blur-2xl transition-all duration-300 ease-out',
          collapsed ? 'w-[76px]' : 'w-[264px]',
          'lg:translate-x-0',
          mobileOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {/* brand */}
        <div className={cn('flex h-16 shrink-0 items-center gap-3 border-b border-line px-4', collapsed && 'justify-center px-0')}>
          <svg width="26" height="26" viewBox="0 0 32 32" className="shrink-0">
            <rect width="32" height="32" rx="8" fill="var(--color-surface-2)" />
            <circle cx="16" cy="9" r="2.4" fill="var(--color-cyan)" />
            <circle cx="8" cy="21" r="2.4" fill="var(--color-indigo)" />
            <circle cx="24" cy="21" r="2.4" fill="var(--color-violet)" />
            <path d="M16 9 L8 21 M16 9 L24 21 M8 21 L24 21" stroke="var(--color-indigo)" strokeWidth="1.1" opacity="0.6" />
          </svg>
          {!collapsed && (
            <span className="font-display text-[15px] font-medium tracking-tight text-text">
              Revianta <span className="text-text-dim">AI</span>
            </span>
          )}
        </div>

        {/* project context strip */}
        {project && !collapsed && (
          <div className="border-b border-line px-4 py-3">
            <p className="mono-tag text-text-faint">Project</p>
            <p className="mt-0.5 truncate text-sm font-medium text-text">{project.name}</p>
          </div>
        )}

        {/* nav */}
        <nav className="flex-1 overflow-y-auto px-2.5 py-4">
          <ul className="space-y-1">
            {items.map(({ label, icon: Icon, to, end, soon }) => (
              <li key={label} className="group relative">
                <NavLink
                  to={to}
                  end={end}
                  onClick={onCloseMobile}
                  className={({ isActive }) =>
                    cn(
                      'flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-colors',
                      collapsed && 'justify-center px-0',
                      isActive
                        ? 'bg-indigo/12 text-text border border-indigo/25 shadow-[0_0_0_1px_rgba(91,95,240,0.12)]'
                        : 'text-text-dim border border-transparent hover:bg-white/[0.04] hover:text-text'
                    )
                  }
                >
                  <Icon size={17} className="shrink-0" />
                  {!collapsed && <span className="truncate">{label}</span>}
                  {!collapsed && soon && (
                    <span className="mono-tag ml-auto shrink-0 text-text-faint">soon</span>
                  )}
                </NavLink>

                {/* tooltip when collapsed */}
                {collapsed && (
                  <span
                    role="tooltip"
                    className="pointer-events-none absolute left-full top-1/2 z-50 ml-2 -translate-y-1/2 whitespace-nowrap rounded-lg border border-line bg-surface-2 px-2.5 py-1.5 text-xs text-text opacity-0 shadow-panel transition-opacity duration-150 group-hover:opacity-100"
                  >
                    {label}{soon ? ' · soon' : ''}
                  </span>
                )}
              </li>
            ))}
          </ul>
        </nav>

        {/* footer: collapse toggle */}
        <div className="border-t border-line p-2.5">
          {!collapsed && (
            <div className="mb-2 flex items-center gap-2 rounded-xl bg-white/[0.03] px-3 py-2 text-text-faint">
              <Clock3 size={14} />
              <span className="text-xs">Synced moments ago</span>
            </div>
          )}
          <button
            onClick={onToggleCollapsed}
            aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            className={cn(
              'hidden w-full items-center justify-center gap-2 rounded-xl border border-line py-2 text-xs text-text-dim transition-colors hover:bg-white/[0.05] hover:text-text lg:flex'
            )}
          >
            {collapsed ? <ChevronsRight size={15} /> : <ChevronsLeft size={15} />}
            {!collapsed && 'Collapse'}
          </button>
        </div>
      </aside>
    </>
  );
}
