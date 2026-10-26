import { useLocation, useParams } from 'react-router-dom';
import AppShell from '../components/layout/AppShell';
import { APP_ROUTE_TITLES } from './routeTitles';
import { PROJECT_NAV } from '../constants/navigation';
import { MOCK_PROJECTS } from '../constants/mockData';

function titleCase(slug) {
  return slug.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function AppShellWithTitle() {
  const location = useLocation();
  const { projectId } = useParams();

  let title = APP_ROUTE_TITLES[location.pathname];

  if (!title && projectId) {
    const project = MOCK_PROJECTS.find((p) => p.id === projectId);
    const sub = location.pathname.split(`/projects/${projectId}/`)[1];
    const navItem = sub ? PROJECT_NAV.find((n) => n.path === sub) : PROJECT_NAV[0];
    title = navItem ? navItem.label : project?.name || 'Project';
  }

  if (!title) {
    const last = location.pathname.split('/').filter(Boolean).pop();
    title = last ? titleCase(last) : 'Revianta AI';
  }

  return <AppShell title={title} />;
}
