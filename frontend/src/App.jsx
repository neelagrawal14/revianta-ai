import { Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/Landing/LandingPage';
import LoginPage from './pages/Auth/LoginPage';
import RegisterPage from './pages/Auth/RegisterPage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import ProjectsPage from './pages/Projects/ProjectsPage';
import NewProjectPage from './pages/Projects/NewProjectPage';
import ProjectDetailPage from './pages/Projects/ProjectDetailPage';
import ProjectPapersPage from './pages/Projects/ProjectPapersPage';
import ProjectGithubPage from './pages/Projects/ProjectGithubPage';
import ProjectDatasetsPage from './pages/Projects/ProjectDatasetsPage';
import ProjectPatentsPage from './pages/Projects/ProjectPatentsPage';
import ProjectTechMapPage from './pages/Projects/ProjectTechMapPage';
import ProjectTimelinePage from './pages/Projects/ProjectTimelinePage';
import ProjectGraphPage from './pages/Projects/ProjectGraphPage';
import ProjectNotesPage from './pages/Projects/ProjectNotesPage';
import ProjectExperimentsPage from './pages/Projects/ProjectExperimentsPage';
import ProjectGapsPage from './pages/Projects/ProjectGapsPage';
import ProjectReferencesPage from './pages/Projects/ProjectReferencesPage';
import ProjectRiskPage from './pages/Projects/ProjectRiskPage';
import ResearchExplorerPage from './pages/ResearchExplorerPage';
import LiveSearchPage from './pages/LiveSearchPage';
import ResearchGapsPage from './pages/ResearchGapsPage';
import RecommendationsPage from './pages/RecommendationsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import ReportsPage from './pages/ReportsPage';
import SettingsPage from './pages/SettingsPage';
import TechnologyGalaxyPage from './pages/TechnologyGalaxyPage';
import GlobalTimelinePage from './pages/GlobalTimelinePage';
import AppShellWithTitle from './routes/AppShellWithTitle';

export default function App() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Authenticated application shell */}
      <Route element={<AppShellWithTitle />}>
        <Route path="/dashboard" element={<DashboardPage />} />

        <Route path="/projects" element={<ProjectsPage />} />
        <Route path="/projects/new" element={<NewProjectPage />} />
        <Route path="/projects/:projectId" element={<ProjectDetailPage />} />
        <Route path="/projects/:projectId/papers" element={<ProjectPapersPage />} />
        <Route path="/projects/:projectId/github" element={<ProjectGithubPage />} />
        <Route path="/projects/:projectId/datasets" element={<ProjectDatasetsPage />} />
        <Route path="/projects/:projectId/patents" element={<ProjectPatentsPage />} />
        <Route path="/projects/:projectId/tech-map" element={<ProjectTechMapPage />} />
        <Route path="/projects/:projectId/timeline" element={<ProjectTimelinePage />} />
        <Route path="/projects/:projectId/graph" element={<ProjectGraphPage />} />
        <Route path="/projects/:projectId/notes" element={<ProjectNotesPage />} />
        <Route path="/projects/:projectId/experiments" element={<ProjectExperimentsPage />} />
        <Route path="/projects/:projectId/gaps" element={<ProjectGapsPage />} />
        <Route path="/projects/:projectId/references" element={<ProjectReferencesPage />} />
        <Route path="/projects/:projectId/risk" element={<ProjectRiskPage />} />

        <Route path="/research" element={<ResearchExplorerPage />} />
        <Route path="/live-search" element={<LiveSearchPage />} />
        <Route path="/research-gaps" element={<ResearchGapsPage />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/tech-graph" element={<TechnologyGalaxyPage />} />
        <Route path="/timeline" element={<GlobalTimelinePage />} />
      </Route>

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
