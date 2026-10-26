import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import FuturisticBackground from '../common/FuturisticBackground';
import { cn } from '../../utils/cn';

/**
 * AppShell — the authenticated application frame: Sidebar + TopBar +
 * routed content. Pages render inside via <Outlet/>; pass a page title
 * down through route context (`useOutletContext`) if a page needs to
 * set the TopBar heading dynamically — for now, `title` is passed as
 * a prop wired up per-route in `src/routes`.
 */
export default function AppShell({ title }) {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen">
      <FuturisticBackground />
      <Sidebar
        collapsed={collapsed}
        onToggleCollapsed={() => setCollapsed((v) => !v)}
        mobileOpen={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
      />

      <div className={cn('flex min-h-screen flex-col transition-[margin] duration-300 ease-out', collapsed ? 'lg:ml-[76px]' : 'lg:ml-[264px]')}>
        <TopBar title={title} onOpenMobileNav={() => setMobileOpen(true)} />
        <main className="flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
