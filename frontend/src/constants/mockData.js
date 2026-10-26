/**
 * ============================================================
 * MOCK DATA — NOT REAL AI OUTPUT
 * ------------------------------------------------------------
 * Everything in this file (and everything under src/constants/mock/)
 * is placeholder content used to build and preview the Revianta AI
 * interface before the FastAPI backend is connected.
 *
 * None of it comes from a model, a scrape, or a live analysis.
 * When the real API lands, replace these with data fetched via
 * `src/services/*Api.js` — do not read from these files in
 * production code paths.
 * ============================================================
 */

export const MOCK_WORKSPACE_METRICS = [
  { id: 'projects', label: 'Active Projects', value: 6, delta: '+2 this month' },
  { id: 'papers', label: 'Papers Analyzed', value: 428, delta: '+53 this month' },
  { id: 'repos', label: 'Repositories', value: 112, delta: '+9 this month' },
  { id: 'datasets', label: 'Datasets', value: 37, delta: '+4 this month' },
  { id: 'patents', label: 'Patents', value: 61, delta: '+6 this month' },
  { id: 'health', label: 'Avg. Project Health', value: '58%', delta: '-4% this month' },
];

export const MOCK_PROJECTS = [
  {
    id: 'smart-traffic-system',
    name: 'Smart Traffic System',
    description:
      'Adaptive traffic-signal control using real-time computer vision and reinforcement learning.',
    healthScore: 68,
    risk: 'Medium',
    tags: ['Computer Vision', 'Reinforcement Learning', 'Edge Compute'],
    progress: 62,
    lastAnalyzed: '2 days ago',
    domain: 'Intelligent Transportation Systems',
    status: 'In Research',
    teamSize: '2\u20134 people',
    timelineTarget: '4\u20136 months',
    hardware: 'Edge GPU (Jetson-class)',
    deploymentTarget: 'Embedded / Edge',
    datasetStatus: 'Partially available',
    complexity: 'Medium',
    difficultyStars: 3,
    estimatedTime: '4 months',
    skills: ['Python', 'Computer Vision', 'Reinforcement Learning', 'Edge Deployment'],
  },
  {
    id: 'crop-disease-detection',
    name: 'Crop Disease Detection',
    description:
      'On-device classification of leaf imagery to flag early-stage crop disease for smallholder farms.',
    healthScore: 56,
    risk: 'Medium',
    tags: ['Computer Vision', 'TinyML', 'Agritech'],
    progress: 45,
    lastAnalyzed: '5 days ago',
    domain: 'Agricultural Technology',
    status: 'In Research',
    teamSize: '1\u20132 people',
    timelineTarget: '3\u20135 months',
    hardware: 'Mobile / low-power device',
    deploymentTarget: 'Mobile (offline-first)',
    datasetStatus: 'Available, needs cleaning',
    complexity: 'Medium',
    difficultyStars: 3,
    estimatedTime: '3 months',
    skills: ['Python', 'Computer Vision', 'TinyML', 'Mobile Deployment'],
  },
  {
    id: 'resume-screening-ai',
    name: 'Resume Screening AI',
    description:
      'NLP pipeline that ranks candidate resumes against role requirements and prior hiring outcomes.',
    healthScore: 24,
    risk: 'High',
    tags: ['NLP', 'Ranking', 'HR Tech'],
    progress: 21,
    lastAnalyzed: '1 week ago',
    domain: 'HR Technology',
    status: 'At Risk',
    teamSize: '1\u20132 people',
    timelineTarget: '2\u20133 months',
    hardware: 'Standard cloud CPU/GPU',
    deploymentTarget: 'Cloud API',
    datasetStatus: 'Must build / limited access',
    complexity: 'High',
    difficultyStars: 4,
    estimatedTime: '3 months',
    skills: ['Python', 'NLP', 'Fairness & Bias Auditing', 'FastAPI'],
  },
  {
    id: 'materials-discovery-net',
    name: 'Materials Discovery Net',
    description:
      'Graph neural network exploring candidate battery electrolytes from simulated property data.',
    healthScore: 74,
    risk: 'Low',
    tags: ['GNN', 'Simulation', 'Materials Science'],
    progress: 80,
    lastAnalyzed: '1 day ago',
    domain: 'Materials Science',
    status: 'On Track',
    teamSize: '3\u20135 people',
    timelineTarget: '6\u201312 months',
    hardware: 'Multi-GPU cluster',
    deploymentTarget: 'Research pipeline (offline)',
    datasetStatus: 'Available (simulated)',
    complexity: 'High',
    difficultyStars: 4,
    estimatedTime: '8 months',
    skills: ['Python', 'Graph Neural Networks', 'PyTorch', 'Simulation'],
  },
];

export const MOCK_PIPELINE_STAGES = [
  { id: 'idea', label: 'Project Idea', hint: 'You describe what you want to build' },
  { id: 'nlp', label: 'NLP Understanding', hint: 'Parsing intent, scope, and domain' },
  { id: 'embedding', label: 'Embedding', hint: 'Mapping the idea into research space' },
  { id: 'similarity', label: 'Similarity Analysis', hint: 'Surfacing related prior work' },
  { id: 'tech', label: 'Technology Analysis', hint: 'Mapping the technology landscape' },
  { id: 'risk', label: 'Risk Intelligence', hint: 'Flagging feasibility & prior-art risk' },
  { id: 'recs', label: 'Recommendations', hint: 'Suggested directions & citations' },
  { id: 'workspace', label: 'Research Workspace', hint: 'Everything lands in your project' },
];

/**
 * Steps shown by <AnalysisSequence /> while "running" the research
 * pipeline on a new project. Purely a UI sequence — see
 * src/components/common/AnalysisSequence.jsx.
 */
export const MOCK_ANALYSIS_STEPS = [
  'Understanding project',
  'Extracting technologies',
  'Searching research ecosystem',
  'Comparing similarity',
  'Evaluating feasibility',
  'Calculating risk',
  'Generating recommendations',
];
