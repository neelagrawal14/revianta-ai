import { http } from './api';

/**
 * recommendationApi — technology / methodology / scope recommendations
 * derived from a project's risk + similarity analysis.
 * Expected FastAPI routes:
 *   GET /recommendations                  -> cross-project feed
 *   GET /projects/:id/recommendations      -> project-scoped
 */
export const recommendationApi = {
  list: (params) => http.get('/recommendations', params),
  forProject: (projectId) => http.get(`/projects/${projectId}/recommendations`),
};
