import { MOCK_PROJECTS } from '../mockData';
import { seededRandom, pickOne, pickN, round } from './helpers';

/**
 * Hand-authored paper set for the flagship demo project. Other projects
 * fall back to `generatePapersFor()` below so every project's Papers page
 * has something real to render — none of this is live search data.
 */
const SMART_TRAFFIC_PAPERS = [
  {
    id: 'p1',
    title: 'Adaptive Traffic Signal Control via Deep Q-Networks',
    authors: ['R. Chen', 'M. Okafor'],
    year: 2024,
    citationCount: 138,
    source: 'arXiv',
    similarity: 94,
    technologies: ['Reinforcement Learning', 'Computer Vision'],
    abstract:
      'Proposes a deep Q-learning agent that adjusts intersection signal timing from live camera feeds, reducing average wait time by 27% in simulation against fixed-cycle baselines.',
  },
  {
    id: 'p2',
    title: 'Multi-Intersection Coordination for Urban Traffic Flow',
    authors: ['S. Patel', 'J. Lindqvist', 'A. Osei'],
    year: 2023,
    citationCount: 96,
    source: 'IEEE Xplore',
    similarity: 88,
    technologies: ['Reinforcement Learning', 'Graph Networks'],
    abstract:
      'Extends single-intersection RL control to a coordinated multi-agent setting, using a graph attention layer to share state between neighboring intersections.',
  },
  {
    id: 'p3',
    title: 'Real-Time Vehicle Detection for Edge Traffic Systems',
    authors: ['T. Kowalski'],
    year: 2023,
    citationCount: 71,
    source: 'CVPR Workshops',
    similarity: 81,
    technologies: ['Computer Vision', 'Edge Compute'],
    abstract:
      'Benchmarks lightweight detector architectures (YOLO-tiny variants) for vehicle counting on Jetson-class hardware under real-world lighting conditions.',
  },
  {
    id: 'p4',
    title: 'Simulation-to-Reality Transfer in Traffic Signal RL',
    authors: ['H. Nakamura', 'L. Fischer'],
    year: 2022,
    citationCount: 54,
    source: 'arXiv',
    similarity: 76,
    technologies: ['Reinforcement Learning', 'Simulation'],
    abstract:
      'Studies the sim-to-real gap for RL traffic controllers trained in SUMO, identifying sensor-noise modeling as the largest contributor to deployment performance loss.',
  },
  {
    id: 'p5',
    title: 'A Survey of Learning-Based Adaptive Traffic Signal Control',
    authors: ['P. Andersson'],
    year: 2021,
    citationCount: 212,
    source: 'Semantic Scholar',
    similarity: 69,
    technologies: ['Reinforcement Learning'],
    abstract:
      'Surveys twelve years of learning-based signal control research, categorizing approaches by state representation, reward design, and coordination strategy.',
  },
  {
    id: 'p6',
    title: 'Edge-Deployed CNNs for Congestion Estimation',
    authors: ['Y. Zhou', 'D. Martins'],
    year: 2022,
    citationCount: 43,
    source: 'IEEE Xplore',
    similarity: 63,
    technologies: ['Computer Vision', 'Edge Compute'],
    abstract:
      'Compares quantized CNN backbones for estimating queue length from fixed roadside cameras, with a focus on inference latency under 50ms.',
  },
];

const PAPER_TEMPLATES = [
  { suffix: 'A Systematic Review', source: 'Semantic Scholar', technologies: 0 },
  { suffix: 'Benchmarking Recent Approaches', source: 'arXiv', technologies: 1 },
  { suffix: 'Toward Practical Deployment', source: 'IEEE Xplore', technologies: 0 },
  { suffix: 'Open Challenges and Opportunities', source: 'ACM Digital Library', technologies: 1 },
  { suffix: 'A Comparative Study', source: 'arXiv', technologies: 0 },
];

const AUTHOR_POOL = ['A. Ibrahim', 'C. Novak', 'E. Larsson', 'F. Tanaka', 'G. Silva', 'K. Meier', 'N. Adeyemi', 'V. Popescu'];

function generatePapersFor(project) {
  const rand = seededRandom(`papers:${project.id}`);
  return PAPER_TEMPLATES.map((tpl, i) => {
    const topic = pickOne(rand, project.tags);
    return {
      id: `${project.id}-paper-${i}`,
      title: `${topic}: ${tpl.suffix} for ${project.domain}`,
      authors: pickN(rand, AUTHOR_POOL, 1 + Math.floor(rand() * 2)),
      year: 2021 + Math.floor(rand() * 4),
      citationCount: Math.floor(rand() * 180),
      source: tpl.source,
      similarity: round(50 + rand() * 45),
      technologies: pickN(rand, project.tags, Math.min(2, project.tags.length)),
      abstract: `A ${tpl.suffix.toLowerCase()} of ${topic.toLowerCase()} techniques as applied to problems resembling ${project.name.toLowerCase()}, evaluated on synthetic and public benchmarks.`,
    };
  });
}

const PAPERS_BY_PROJECT = {
  'smart-traffic-system': SMART_TRAFFIC_PAPERS,
};

export function getPapersForProject(projectId) {
  if (PAPERS_BY_PROJECT[projectId]) return PAPERS_BY_PROJECT[projectId];
  const project = MOCK_PROJECTS.find((p) => p.id === projectId);
  return project ? generatePapersFor(project) : [];
}
