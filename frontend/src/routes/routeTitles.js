/**
 * Route metadata used to derive the TopBar title for each authenticated
 * route. Keeping this separate from the JSX route tree (src/App.jsx)
 * makes it easy to extend without touching the router itself.
 */
export const APP_ROUTE_TITLES = {
  '/dashboard': 'Overview',
  '/projects': 'Projects',
  '/projects/new': 'New Project',
  '/research': 'Research Explorer',
  '/live-search': 'Live Search',
  '/research-gaps': 'Research Gaps',
  '/tech-graph': 'Technology Graph',
  '/timeline': 'Research Timeline',
  '/recommendations': 'Recommendations',
  '/analytics': 'Analytics',
  '/reports': 'Reports',
  '/settings': 'Settings',
};
