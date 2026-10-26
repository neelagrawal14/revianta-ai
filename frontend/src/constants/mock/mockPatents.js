import { MOCK_PROJECTS } from '../mockData';
import { seededRandom, pickOne, round } from './helpers';

const SMART_TRAFFIC_PATENTS = [
  {
    id: 'pt1',
    title: 'Method for Predictive Traffic Signal Timing',
    year: 2023,
    classification: 'G08G 1/07',
    similarity: 74,
    inventor: 'D. Whitfield et al.',
    relevance: 'High',
  },
  {
    id: 'pt2',
    title: 'Adaptive Intersection Control Using Sensor Fusion',
    year: 2021,
    classification: 'G08G 1/095',
    similarity: 61,
    inventor: 'M. Alvarez',
    relevance: 'Medium',
  },
  {
    id: 'pt3',
    title: 'System for Real-Time Vehicle Queue Estimation',
    year: 2020,
    classification: 'G06V 20/54',
    similarity: 48,
    inventor: 'S. Ridley, J. Kwan',
    relevance: 'Medium',
  },
  {
    id: 'pt4',
    title: 'Distributed Traffic Signal Coordination Protocol',
    year: 2019,
    classification: 'G08G 1/08',
    similarity: 35,
    inventor: 'T. Brandt',
    relevance: 'Low',
  },
];

function generatePatentsFor(project) {
  const rand = seededRandom(`patents:${project.id}`);
  const inventorPool = ['R. Osei', 'L. Bianchi', 'C. Dubois', 'H. Yamada', 'P. Novak'];
  return Array.from({ length: 3 }).map((_, i) => {
    const sim = round(30 + rand() * 55);
    return {
      id: `${project.id}-patent-${i}`,
      title: `${pickOne(rand, project.tags)}-Based Method for ${project.domain}`,
      year: 2019 + Math.floor(rand() * 6),
      classification: `G0${6 + Math.floor(rand() * 3)}${pickOne(rand, ['V', 'G', 'F'])} ${Math.floor(rand() * 30)}/${Math.floor(rand() * 90)}`,
      similarity: sim,
      inventor: pickOne(rand, inventorPool),
      relevance: sim > 60 ? 'High' : sim > 40 ? 'Medium' : 'Low',
    };
  });
}

const PATENTS_BY_PROJECT = {
  'smart-traffic-system': SMART_TRAFFIC_PATENTS,
};

export function getPatentsForProject(projectId) {
  if (PATENTS_BY_PROJECT[projectId]) return PATENTS_BY_PROJECT[projectId];
  const project = MOCK_PROJECTS.find((p) => p.id === projectId);
  return project ? generatePatentsFor(project) : [];
}
