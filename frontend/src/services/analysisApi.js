import { http } from './api';

/**
 * analysisApi — runs and reads results from Revianta's core pipeline
 * (NLP understanding → embeddings → similarity → technology analysis →
 * risk intelligence → recommendations). This is what the "Run Research
 * Intelligence" step in /projects/new will call once the backend exists.
 * Expected FastAPI routes:
 *   POST /projects/:id/analyze          -> kicks off the pipeline
 *   GET  /projects/:id/analysis/status  -> polling target for progress
 *   GET  /projects/:id/technology-map
 *   GET  /projects/:id/knowledge-graph
 *   GET  /projects/:id/timeline
 *   GET  /projects/:id/complexity
 */
export const analysisApi = {
  run: (projectId, payload) => http.post(`/projects/${projectId}/analyze`, payload),
  status: (projectId) => http.get(`/projects/${projectId}/analysis/status`),
  technologyMap: (projectId) => http.get(`/projects/${projectId}/technology-map`),
  knowledgeGraph: (projectId) => http.get(`/projects/${projectId}/knowledge-graph`),
  timeline: (projectId) => http.get(`/projects/${projectId}/timeline`),
  complexity: (projectId) => http.get(`/projects/${projectId}/complexity`),
};
