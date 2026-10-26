import { MOCK_PROJECTS } from '../mockData';
import { seededRandom, pickOne, round } from './helpers';

export const DATASET_STATUSES = ['AVAILABLE', 'RESTRICTED', 'GATED', 'MUST BUILD', 'UNKNOWN'];

const SMART_TRAFFIC_DATASETS = [
  {
    id: 'd1',
    name: 'Urban Intersection Flow Dataset',
    source: 'OpenTraffic Consortium',
    availability: 'AVAILABLE',
    downloads: 18400,
    size: '4.2 GB',
    category: 'Traffic Sensor Data',
    accessStatus: 'AVAILABLE',
    relevance: 96,
    bestMatch: true,
  },
  {
    id: 'd2',
    name: 'CityCam Vehicle Detection Set',
    source: 'CityCam Research Group',
    availability: 'RESTRICTED',
    downloads: 5200,
    size: '11 GB',
    category: 'Annotated Imagery',
    accessStatus: 'RESTRICTED',
    relevance: 84,
    bestMatch: false,
  },
  {
    id: 'd3',
    name: 'Metro Signal Timing Logs',
    source: 'City of Alderbrook Open Data',
    availability: 'AVAILABLE',
    downloads: 2100,
    size: '640 MB',
    category: 'Municipal Records',
    accessStatus: 'AVAILABLE',
    relevance: 71,
    bestMatch: false,
  },
  {
    id: 'd4',
    name: 'Simulated Congestion Scenarios (SUMO)',
    source: 'OpenTraffic Consortium',
    availability: 'AVAILABLE',
    downloads: 9800,
    size: '2.1 GB',
    category: 'Synthetic Simulation',
    accessStatus: 'AVAILABLE',
    relevance: 68,
    bestMatch: false,
  },
  {
    id: 'd5',
    name: 'National Traffic Incident Registry',
    source: 'Federal Transport Authority',
    availability: 'GATED',
    downloads: 640,
    size: '1.8 GB',
    category: 'Incident Records',
    accessStatus: 'GATED',
    relevance: 52,
    bestMatch: false,
  },
];

function generateDatasetsFor(project) {
  const rand = seededRandom(`datasets:${project.id}`);
  const sources = ['Open Research Data Hub', 'Community Data Commons', 'Institutional Archive', 'Public Sector Portal'];
  const categories = ['Sensor Data', 'Annotated Imagery', 'Simulation Output', 'Structured Records'];

  return Array.from({ length: 4 }).map((_, i) => {
    const status = pickOne(rand, DATASET_STATUSES);
    return {
      id: `${project.id}-dataset-${i}`,
      name: `${pickOne(rand, project.tags)} Reference Dataset ${i + 1}`,
      source: pickOne(rand, sources),
      availability: status,
      downloads: Math.floor(rand() * 12000),
      size: `${round(0.3 + rand() * 8, 1)} GB`,
      category: pickOne(rand, categories),
      accessStatus: status,
      relevance: round(40 + rand() * 55),
      bestMatch: i === 0,
    };
  });
}

const DATASETS_BY_PROJECT = {
  'smart-traffic-system': SMART_TRAFFIC_DATASETS,
};

export function getDatasetsForProject(projectId) {
  if (DATASETS_BY_PROJECT[projectId]) return DATASETS_BY_PROJECT[projectId];
  const project = MOCK_PROJECTS.find((p) => p.id === projectId);
  return project ? generateDatasetsFor(project) : [];
}
