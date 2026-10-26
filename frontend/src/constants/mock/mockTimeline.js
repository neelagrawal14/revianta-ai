/**
 * Global research timeline — a general computer-vision/AI evolution
 * timeline shown at the workspace-level /timeline page. Project-scoped
 * timelines (getTimelineForProject) are narrower, project-specific cuts.
 */
export const GLOBAL_TIMELINE = [
  {
    year: 2019,
    technology: 'Convolutional Neural Networks (CNN) maturity',
    papers: ['EfficientNet-precursor scaling studies'],
    shift: 'Foundational',
    description:
      'CNNs become the default backbone for vision tasks, with growing focus on efficiency-accuracy trade-offs.',
  },
  {
    year: 2020,
    technology: 'EfficientNet',
    papers: ['EfficientNet: Rethinking Model Scaling for CNNs'],
    shift: 'Efficiency-focused scaling',
    description:
      'Compound scaling of depth/width/resolution sets a new standard for accuracy-per-FLOP across vision benchmarks.',
  },
  {
    year: 2021,
    technology: 'Vision Transformer (ViT)',
    papers: ['An Image is Worth 16x16 Words'],
    shift: 'Architecture shift',
    description:
      'Transformers move from NLP into vision, challenging CNNs as the default architecture for large-scale image tasks.',
  },
  {
    year: 2022,
    technology: 'Segment Anything (SAM)',
    papers: ['Segment Anything'],
    shift: 'Foundation models for vision',
    description:
      'Promptable, zero-shot segmentation shows foundation-model behavior transferring from language into pixel-level vision tasks.',
  },
  {
    year: 2023,
    technology: 'Grounding DINO',
    papers: ['Grounding DINO: Open-Set Object Detection'],
    shift: 'Open-vocabulary detection',
    description:
      'Combines language grounding with detection, enabling open-set recognition without retraining on fixed label sets.',
  },
];

const SMART_TRAFFIC_TIMELINE = [
  {
    year: 2019,
    technology: 'Fixed-cycle + rule-based control',
    papers: ['A Survey of Learning-Based Adaptive Traffic Signal Control (context)'],
    shift: 'Baseline era',
    description: 'Most deployed systems still rely on fixed or simple rule-based signal timing.',
  },
  {
    year: 2021,
    technology: 'Single-agent RL control',
    papers: ['A Survey of Learning-Based Adaptive Traffic Signal Control'],
    shift: 'Learning-based control emerges',
    description: 'Deep RL agents begin outperforming rule-based baselines in simulation for single intersections.',
  },
  {
    year: 2023,
    technology: 'Multi-agent coordination',
    papers: ['Multi-Intersection Coordination for Urban Traffic Flow'],
    shift: 'Coordination across intersections',
    description: 'Graph-based multi-agent methods start coordinating signal timing across intersection networks.',
  },
  {
    year: 2024,
    technology: 'Edge-deployed adaptive control',
    papers: ['Adaptive Traffic Signal Control via Deep Q-Networks'],
    shift: 'Real-world deployment focus',
    description: 'Research shifts toward sim-to-real transfer and on-device inference for practical deployment.',
  },
];

const TIMELINE_BY_PROJECT = {
  'smart-traffic-system': SMART_TRAFFIC_TIMELINE,
};

export function getTimelineForProject(projectId) {
  return TIMELINE_BY_PROJECT[projectId] || GLOBAL_TIMELINE;
}
