export const EXPERIMENT_STATUSES = ['PLANNED', 'RUNNING', 'COMPLETED', 'FAILED'];

export const MOCK_EXPERIMENTS_BY_PROJECT = {
  'smart-traffic-system': [
    {
      id: 'e1',
      experiment: 'Baseline DQN vs fixed-cycle control',
      objective: 'Establish whether a single-intersection DQN agent beats fixed timing on average wait time.',
      status: 'COMPLETED',
      date: '3 weeks ago',
      technologies: ['Reinforcement Learning', 'SUMO'],
      result: 'DQN reduced average wait time by 24% over 500 simulated episodes.',
      notes: 'Reward function still needs tuning for rush-hour scenarios.',
    },
    {
      id: 'e2',
      experiment: 'Quantized YOLO-tiny on Jetson Orin',
      objective: 'Measure real-time inference latency for vehicle detection at the edge.',
      status: 'COMPLETED',
      date: '2 weeks ago',
      technologies: ['Computer Vision', 'Edge Compute'],
      result: 'Achieved 38ms average inference time, within the 50ms budget.',
      notes: 'Accuracy dropped 3% after INT8 quantization — acceptable for this use case.',
    },
    {
      id: 'e3',
      experiment: 'Two-intersection coordination pilot',
      objective: 'Test whether sharing state between two adjacent intersections improves joint throughput.',
      status: 'RUNNING',
      date: 'Started 4 days ago',
      technologies: ['Reinforcement Learning', 'Graph Networks'],
      result: null,
      notes: 'Early runs show promise but training is unstable past 300 episodes.',
    },
    {
      id: 'e4',
      experiment: 'Sim-to-real sensor noise injection',
      objective: 'Evaluate robustness of the trained agent under simulated sensor noise before field deployment.',
      status: 'PLANNED',
      date: 'Not started',
      technologies: ['Reinforcement Learning', 'Simulation'],
      result: null,
      notes: null,
    },
    {
      id: 'e5',
      experiment: 'Full-city multi-agent scale test',
      objective: 'Scale coordination to a 12-intersection simulated grid.',
      status: 'FAILED',
      date: '5 weeks ago',
      technologies: ['Reinforcement Learning', 'Graph Networks'],
      result: 'Training diverged past 8 intersections due to reward sparsity.',
      notes: 'Revisit with hierarchical reward structure before retrying at scale.',
    },
  ],
};

export function getExperimentsForProject(projectId) {
  return MOCK_EXPERIMENTS_BY_PROJECT[projectId] || [];
}
