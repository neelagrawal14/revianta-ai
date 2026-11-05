import { MOCK_PROJECTS } from '../mockData';
import { seededRandom, round } from './helpers';

export const RISK_DIMENSIONS = [
  { id: 'technical', label: 'Technical Risk' },
  { id: 'dataset', label: 'Dataset Risk' },
  { id: 'implementation', label: 'Implementation Risk' },
  { id: 'novelty', label: 'Novelty Risk' },
  { id: 'research', label: 'Research Risk' },
  { id: 'deployment', label: 'Deployment Risk' },
  { id: 'business', label: 'Business Risk' },
];

function severityFor(score) {
  if (score >= 60) return 'High';
  if (score >= 35) return 'Medium';
  return 'Low';
}

/**
 * Hand-authored NRIE (Revianta Risk Intelligence Engine) result for the
 * flagship demo project — the exact figures used as the worked example
 * throughout the product brief.
 */
const SMART_TRAFFIC_RISK = {
  overallHealth: 68,
  riskLevel: 'Medium',
  modelVersion: null,
  dimensions: [
    {
      id: 'technical',
      label: 'Technical Risk',
      score: 72,
      severity: 'High',
      reason: 'Combines real-time computer vision with reinforcement learning under hard latency constraints.',
      factors: ['Real-time inference budget under 50ms', 'Multi-agent coordination adds system complexity', 'Sensor noise affects state estimation'],
    },
    {
      id: 'dataset',
      label: 'Dataset Risk',
      score: 18,
      severity: 'Low',
      reason: 'A strong public dataset closely matches the target use case.',
      factors: ['Urban Intersection Flow Dataset covers similar geography', 'Simulation data available for pretraining', 'Some sensor variance across cities'],
    },
    {
      id: 'implementation',
      label: 'Implementation Risk',
      score: 65,
      severity: 'High',
      reason: 'Edge deployment and multi-agent training both add non-trivial engineering overhead.',
      factors: ['Cross-intersection communication protocol needed', 'Edge hardware constraints limit model size', 'Sim-to-real transfer historically lossy'],
    },
    {
      id: 'novelty',
      label: 'Novelty Risk',
      score: 60,
      severity: 'Medium',
      reason: 'Core approach closely follows recent published methods rather than introducing a new mechanism.',
      factors: ['High similarity to 2+ recent papers', 'Coordination method already explored in prior work', 'Opportunity to differentiate on deployment, not method'],
    },
    {
      id: 'research',
      label: 'Research Risk',
      score: 22,
      severity: 'Low',
      reason: 'The research direction is well-trodden with a decade of prior work to build on.',
      factors: ['12+ years of adaptive signal control literature', 'Clear evaluation benchmarks exist', 'Active research community'],
    },
    {
      id: 'deployment',
      label: 'Deployment Risk',
      score: 58,
      severity: 'Medium',
      reason: 'Municipal deployment involves procurement, hardware installation, and safety validation.',
      factors: ['Requires physical hardware installation', 'Safety validation for live intersections', 'Procurement cycles outside engineering control'],
    },
    {
      id: 'business',
      label: 'Business Risk',
      score: 30,
      severity: 'Medium',
      reason: 'Clear public-sector demand, but sales cycles to municipalities are long.',
      factors: ['Strong demand from city transportation departments', 'Long municipal procurement cycles', 'Competing vendors in adjacent space'],
    },
  ],
  aiRecommendation:
    'Use a smaller pre-annotated dataset and simplify the initial deployment target to a single intersection to reduce technical and implementation risk before pursuing multi-intersection coordination.',
};

function generateRiskFor(project) {
  const rand = seededRandom(`risk:${project.id}`);
  const dimensions = RISK_DIMENSIONS.map((dim) => {
    const score = round(15 + rand() * 70);
    return {
      ...dim,
      score,
      severity: severityFor(score),
      reason: `Estimated from project scope, technology stack, and similarity to prior ${project.domain.toLowerCase()} work.`,
      factors: [
        `${project.tags[0]} maturity in this domain`,
        `${project.deploymentTarget} deployment considerations`,
        `${project.datasetStatus.toLowerCase()} dataset landscape`,
      ],
    };
  });

  return {
    overallHealth: project.healthScore,
    riskLevel: project.risk,
    modelVersion: null,
    dimensions,
    aiRecommendation: `Prioritize de-risking ${dimensions.sort((a, b) => b.score - a.score)[0].label.toLowerCase()} first — it currently contributes the most to overall project risk.`,
  };
}

const RISK_BY_PROJECT = {
  'smart-traffic-system': SMART_TRAFFIC_RISK,
};

export function getRiskForProject(projectId) {
  if (RISK_BY_PROJECT[projectId]) return RISK_BY_PROJECT[projectId];
  const project = MOCK_PROJECTS.find((p) => p.id === projectId);
  return project ? generateRiskFor(project) : null;
}
