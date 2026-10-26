
import { http } from './api';

export const riskApi = {
  get: (projectId) => http.get(`/projects/${projectId}/risk`),

  analyze: (projectId, payload) =>
    http.post(`/projects/${projectId}/analyze`, payload),
};
