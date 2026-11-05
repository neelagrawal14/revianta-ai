import { http } from './api';

/**
 * researchApi — the research corpus: papers, repositories, datasets,
 * patents, and the unified cross-source search behind /research.
 * Expected FastAPI routes:
 *   GET /research/search?q=&sources=papers,github,datasets,patents
 *   GET /projects/:id/papers
 *   GET /projects/:id/github
 *   GET /projects/:id/datasets
 *   GET /projects/:id/patents
 *   GET /research-gaps
 */
export const researchApi = {
  search: (query, params) => http.get('/research/search', { q: query, ...params }),
  papers: (projectId, params) => http.get(`/projects/${projectId}/papers`, params),
  repositories: (projectId, params) => http.get(`/projects/${projectId}/github`, params),
  datasets: (projectId, params) => http.get(`/projects/${projectId}/datasets`, params),
  patents: (projectId, params) => http.get(`/projects/${projectId}/patents`, params),
  gaps: (params) => http.get('/research-gaps', params),
};
