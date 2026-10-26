import {
  LayoutGrid,
  FolderKanban,
  Compass,
  Network,
  GitBranch,
  ShieldAlert,
  Sparkles,
  BarChart3,
  FileBarChart,
  FileText,
  FolderGit2,
  Database,
  ScrollText,
  Map,
  Waypoints,
  NotebookText,
  FlaskConical,
  BookMarked,
  TriangleAlert,
  Zap,
} from 'lucide-react';

/**
 * Primary, workspace-level navigation (rendered when no project is active).
 * Every route here now has a real page (Part 2) — none render
 * ComingSoonPage any more.
 */
export const WORKSPACE_NAV = [
  { label: 'Overview', to: '/dashboard', icon: LayoutGrid },
  { label: 'Projects', to: '/projects', icon: FolderKanban },
  { label: 'Research Explorer', to: '/research', icon: Compass },
  { label: 'Live Search', to: '/live-search', icon: Zap },
  { label: 'Technology Graph', to: '/tech-graph', icon: Network },
  { label: 'Research Timeline', to: '/timeline', icon: GitBranch },
  { label: 'Research Gaps', to: '/research-gaps', icon: ShieldAlert },
  { label: 'Recommendations', to: '/recommendations', icon: Sparkles },
  { label: 'Analytics', to: '/analytics', icon: BarChart3 },
  { label: 'Reports', to: '/reports', icon: FileBarChart },
];

/**
 * Project-scoped navigation, shown once a project is opened.
 * `path` is relative to `/projects/:projectId`. All routes now render
 * real Part 2 pages.
 */
export const PROJECT_NAV = [
  { label: 'Overview', path: '', icon: LayoutGrid },
  { label: 'Papers', path: 'papers', icon: FileText },
  { label: 'GitHub', path: 'github', icon: FolderGit2 },
  { label: 'Datasets', path: 'datasets', icon: Database },
  { label: 'Patents', path: 'patents', icon: ScrollText },
  { label: 'Tech Map', path: 'tech-map', icon: Map },
  { label: 'Timeline', path: 'timeline', icon: Waypoints },
  { label: 'Graph', path: 'graph', icon: Network },
  { label: 'Notes', path: 'notes', icon: NotebookText },
  { label: 'Experiments', path: 'experiments', icon: FlaskConical },
  { label: 'Research Gaps', path: 'gaps', icon: ShieldAlert },
  { label: 'References', path: 'references', icon: BookMarked },
  { label: 'Risk', path: 'risk', icon: TriangleAlert },
];
