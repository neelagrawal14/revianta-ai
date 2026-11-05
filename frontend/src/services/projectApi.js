import { http } from './api';

/**
 * projectApi — CRUD + lifecycle calls for research projects.
 * Expected FastAPI routes (adjust to match the real backend contract):
 *   GET    /projects
 *   GET    /projects/:id
 *   POST   /projects
 *   PATCH  /projects/:id
 *   DELETE /projects/:id
 */
export const projectApi = {
  list: (params) => http.get('/projects', params),
  get: (projectId) => http.get(`/projects/${projectId}`),
  create: (payload) => http.post('/projects', payload),
  update: (projectId, payload) => http.patch(`/projects/${projectId}`, payload),
  remove: (projectId) => http.delete(`/projects/${projectId}`),
};
