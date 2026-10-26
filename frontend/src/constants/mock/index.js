/**
 * Barrel export for all Part 2 mock data. Import from here (rather than
 * individual files) in pages, e.g.:
 *   import { getPapersForProject, getRiskForProject } from '../../constants/mock';
 */
export { getPapersForProject } from './mockPapers';
export { getRepositoriesForProject } from './mockRepositories';
export { getDatasetsForProject, DATASET_STATUSES } from './mockDatasets';
export { getPatentsForProject } from './mockPatents';
export { getTechMapForProject, getGlobalTechnologyGalaxy } from './mockTechnologies';
export { getKnowledgeGraphForProject } from './mockGraph';
export { getTimelineForProject, GLOBAL_TIMELINE } from './mockTimeline';
export { getRiskForProject, RISK_DIMENSIONS } from './mockRiskData';
export { MOCK_RECOMMENDATIONS, getRecommendationsForProject, getProjectName } from './mockRecommendations';
export { MOCK_RESEARCH_GAPS, getGapsForDomain } from './mockGaps';
export { getNotesForProject } from './mockNotes';
export { getExperimentsForProject, EXPERIMENT_STATUSES } from './mockExperiments';
export * as analytics from './mockAnalytics';
export { MOCK_REPORTS } from './mockReports';
