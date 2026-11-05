import { MOCK_PROJECTS } from '../mockData';
import { seededRandom, pickOne, pickN, round } from './helpers';

const SMART_TRAFFIC_REPOS = [
  {
    id: 'r1',
    name: 'traffic-rl-sim',
    owner: 'urbanml',
    description: 'Reinforcement-learning traffic signal simulator built on SUMO with a Gym-compatible API.',
    stars: 1240,
    language: 'Python',
    topics: ['reinforcement-learning', 'traffic', 'simulation'],
    similarity: 91,
    activity: 'Active',
    lastUpdated: '3 days ago',
  },
  {
    id: 'r2',
    name: 'edge-vehicle-detect',
    owner: 'jetson-vision',
    description: 'Quantized YOLO variants tuned for Jetson Nano/Orin vehicle detection at the edge.',
    stars: 812,
    language: 'Python',
    topics: ['computer-vision', 'edge-ai', 'yolo'],
    similarity: 84,
    activity: 'Active',
    lastUpdated: '1 week ago',
  },
  {
    id: 'r3',
    name: 'multi-agent-signal-control',
    owner: 'graph-rl-lab',
    description: 'Graph attention multi-agent RL for coordinated intersection control across a city grid.',
    stars: 356,
    language: 'Python',
    topics: ['multi-agent', 'graph-neural-networks', 'traffic'],
    similarity: 78,
    activity: 'Moderate',
    lastUpdated: '3 weeks ago',
  },
  {
    id: 'r4',
    name: 'sumo-scenarios',
    owner: 'opentraffic',
    description: 'A collection of realistic SUMO city scenarios for benchmarking adaptive signal controllers.',
    stars: 204,
    language: 'XML / Python',
    topics: ['simulation', 'benchmark', 'sumo'],
    similarity: 66,
    activity: 'Archived',
    lastUpdated: '8 months ago',
  },
];

const REPO_TEMPLATES = [
  { name: 'baseline-toolkit', activity: 'Active' },
  { name: 'reference-implementation', activity: 'Moderate' },
  { name: 'benchmark-suite', activity: 'Active' },
  { name: 'community-models', activity: 'Archived' },
];

const OWNER_POOL = ['open-research', 'lab-collective', 'ml-community', 'field-notes-ai'];

function generateReposFor(project) {
  const rand = seededRandom(`repos:${project.id}`);
  return REPO_TEMPLATES.map((tpl, i) => {
    const topic = pickOne(rand, project.tags);
    return {
      id: `${project.id}-repo-${i}`,
      name: `${topic.toLowerCase().replace(/\s+/g, '-')}-${tpl.name}`,
      owner: pickOne(rand, OWNER_POOL),
      description: `${tpl.name.replace(/-/g, ' ')} for ${topic.toLowerCase()} work related to ${project.domain.toLowerCase()}.`,
      stars: Math.floor(rand() * 900),
      language: pickOne(rand, ['Python', 'TypeScript', 'C++']),
      topics: pickN(rand, project.tags, Math.min(2, project.tags.length)).map((t) => t.toLowerCase().replace(/\s+/g, '-')),
      similarity: round(45 + rand() * 45),
      activity: tpl.activity,
      lastUpdated: `${1 + Math.floor(rand() * 8)} weeks ago`,
    };
  });
}

const REPOS_BY_PROJECT = {
  'smart-traffic-system': SMART_TRAFFIC_REPOS,
};

export function getRepositoriesForProject(projectId) {
  if (REPOS_BY_PROJECT[projectId]) return REPOS_BY_PROJECT[projectId];
  const project = MOCK_PROJECTS.find((p) => p.id === projectId);
  return project ? generateReposFor(project) : [];
}
