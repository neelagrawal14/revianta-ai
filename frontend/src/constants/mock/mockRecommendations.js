import { MOCK_PROJECTS } from '../mockData';

/**
 * Cross-project recommendation feed for /recommendations. Each entry is
 * derived (in this mock) from a project's risk profile — in production
 * this comes from `recommendationApi.list()`.
 */
export const MOCK_RECOMMENDATIONS = [
  {
    id: 'rec-1',
    projectId: 'smart-traffic-system',
    riskFlag: 'HIGH IMPLEMENTATION RISK',
    severity: 'high',
    why: 'Edge deployment plus multi-agent coordination adds substantial engineering surface area before you can validate the core idea.',
    recommendation: 'Reduce the technology stack: ship a single-intersection agent first, defer multi-agent coordination to a v2.',
    expectedImpact: 'Cuts implementation risk from High to Medium; shortens time-to-first-validation by an estimated 6\u20138 weeks.',
  },
  {
    id: 'rec-2',
    projectId: 'crop-disease-detection',
    riskFlag: 'HIGH DATASET RISK',
    severity: 'medium',
    why: 'Available leaf-disease datasets are inconsistently labeled across regions and crop types.',
    recommendation: 'Use an available pre-annotated dataset (e.g. PlantVillage-style corpus) for initial training before collecting field data.',
    expectedImpact: 'Removes several weeks of manual labeling from the critical path.',
  },
  {
    id: 'rec-3',
    projectId: 'resume-screening-ai',
    riskFlag: 'HIGH NOVELTY RISK',
    severity: 'high',
    why: 'Resume ranking approaches in the research corpus closely resemble the current project design, with little differentiation.',
    recommendation: 'Add a differentiating methodology, such as fairness-aware ranking constraints or explainability scoring, to stand apart from prior work.',
    expectedImpact: 'Improves defensibility and reduces the chance of duplicating unpublished internal efforts elsewhere.',
  },
  {
    id: 'rec-4',
    projectId: 'resume-screening-ai',
    riskFlag: 'HIGH BUSINESS RISK',
    severity: 'high',
    why: 'Automated candidate ranking carries regulatory and reputational exposure if not carefully audited.',
    recommendation: 'Introduce a bias-audit checkpoint before any production ranking decision reaches a hiring manager.',
    expectedImpact: 'Reduces downstream legal/compliance risk; slows initial rollout by roughly 2\u20133 weeks.',
  },
  {
    id: 'rec-5',
    projectId: 'materials-discovery-net',
    riskFlag: 'MODERATE RESEARCH RISK',
    severity: 'medium',
    why: 'Simulated property data may not transfer cleanly to physical electrolyte synthesis.',
    recommendation: 'Validate the top 5 GNN-recommended candidates experimentally before scaling simulation-only search.',
    expectedImpact: 'Surfaces sim-to-real gaps early, before further compute is spent on simulation-only refinement.',
  },
];

export function getRecommendationsForProject(projectId) {
  return MOCK_RECOMMENDATIONS.filter((r) => r.projectId === projectId);
}

export function getProjectName(projectId) {
  return MOCK_PROJECTS.find((p) => p.id === projectId)?.name || 'Unknown project';
}
