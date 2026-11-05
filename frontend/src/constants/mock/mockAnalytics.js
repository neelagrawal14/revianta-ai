/**
 * Chart-ready mock series for /analytics. Kept as plain arrays of
 * {label, value} (or similar) so any chart wrapper can consume them
 * without reshaping.
 */
export const HEALTH_OVER_TIME = {
  labels: ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
  values: [49, 52, 55, 58, 56, 58],
};

export const RISK_DISTRIBUTION = {
  labels: ['Low', 'Medium', 'High'],
  values: [1, 2, 1],
};

export const RESEARCH_ACTIVITY = {
  labels: ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
  values: [24, 31, 28, 40, 37, 53],
};

export const PAPER_GROWTH = {
  labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
  values: [1200, 1850, 2600, 3400, 4100, 4800],
};

export const TECHNOLOGY_GROWTH = {
  labels: ['Computer Vision', 'Reinforcement Learning', 'NLP', 'GNN', 'TinyML'],
  values: [38, 22, 27, 14, 9],
};

export const SIMILARITY_DISTRIBUTION = {
  labels: ['0\u201320%', '20\u201340%', '40\u201360%', '60\u201380%', '80\u2013100%'],
  values: [4, 9, 18, 26, 11],
};

export const DATASET_AVAILABILITY = {
  labels: ['Available', 'Restricted', 'Gated', 'Must Build', 'Unknown'],
  values: [14, 9, 5, 6, 3],
};

export const PROJECT_COMPLEXITY = {
  labels: ['Low', 'Medium', 'High'],
  values: [1, 2, 1],
};

export const RESEARCH_TRENDS = {
  labels: ['Foundation Models', 'Edge AI', 'Multi-Agent Systems', 'Graph Learning', 'Synthetic Data'],
  values: [72, 58, 41, 33, 47],
};
