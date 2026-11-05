import { MOCK_PROJECTS } from '../mockData';

/**
 * /reports listing. `exportReady` is false everywhere on purpose — no
 * PDF generation exists yet, so the Export/Download actions render as
 * disabled UI placeholders rather than faking a download.
 */
export const MOCK_REPORTS = MOCK_PROJECTS.map((project) => ({
  id: `report-${project.id}`,
  projectId: project.id,
  projectName: project.name,
  healthScore: project.healthScore,
  riskLevel: project.risk,
  lastAnalysis: project.lastAnalyzed,
  reportStatus: project.healthScore > 60 ? 'Ready' : project.healthScore > 35 ? 'Needs Review' : 'Incomplete',
  exportReady: false,
}));
