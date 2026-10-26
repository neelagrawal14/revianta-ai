/**
 * Research-gap suggestions for /research-gaps and the project-scoped
 * gaps tab. These are illustrative UI content only — Revianta does not
 * claim these gaps are scientifically validated findings.
 */
export const MOCK_RESEARCH_GAPS = [
  {
    id: 'gap-1',
    title: 'Underexplored combination: multi-agent RL + edge deployment',
    evidence: 'Most multi-agent traffic-control papers assume cloud-scale compute; very few report edge-hardware benchmarks.',
    relatedPapers: ['Multi-Intersection Coordination for Urban Traffic Flow', 'Real-Time Vehicle Detection for Edge Traffic Systems'],
    confidence: 'Medium',
    opportunity: 'A paper or system demonstrating multi-agent coordination running entirely on edge hardware would fill a clear gap.',
    domain: 'Intelligent Transportation Systems',
  },
  {
    id: 'gap-2',
    title: 'Low dataset coverage for smallholder-farm imagery conditions',
    evidence: 'Public crop-disease datasets are dominated by controlled, well-lit lab photography rather than field conditions.',
    relatedPapers: ['Crop Disease Detection literature (general)'],
    confidence: 'High',
    opportunity: 'A dataset captured under realistic field lighting/occlusion could meaningfully improve model transfer.',
    domain: 'Agricultural Technology',
  },
  {
    id: 'gap-3',
    title: 'Limited deployment research for on-device NLP ranking',
    evidence: 'Most resume-ranking research targets cloud APIs; on-device or privacy-preserving variants are rarely studied.',
    relatedPapers: [],
    confidence: 'Low',
    opportunity: 'Privacy-preserving, on-device candidate ranking is a plausible but currently under-studied direction.',
    domain: 'HR Technology',
  },
  {
    id: 'gap-4',
    title: 'Contradictory findings on GNN transferability for electrolyte discovery',
    evidence: 'Two recent studies report conflicting results on how well GNN property predictions transfer across electrolyte families.',
    relatedPapers: ['Materials Discovery Net literature (general)'],
    confidence: 'Medium',
    opportunity: 'A reconciling study across a shared benchmark set would clarify which factors drive the discrepancy.',
    domain: 'Materials Science',
  },
  {
    id: 'gap-5',
    title: 'Unexplored domain: adaptive signal control for mixed autonomous/human traffic',
    evidence: 'Nearly all reviewed papers assume fully human-driven traffic; autonomous-vehicle mix ratios are rarely modeled.',
    relatedPapers: ['A Survey of Learning-Based Adaptive Traffic Signal Control'],
    confidence: 'Medium',
    opportunity: 'Modeling partial AV adoption could meaningfully change optimal signal-timing strategy.',
    domain: 'Intelligent Transportation Systems',
  },
];

export function getGapsForDomain(domain) {
  return MOCK_RESEARCH_GAPS.filter((g) => g.domain === domain);
}
