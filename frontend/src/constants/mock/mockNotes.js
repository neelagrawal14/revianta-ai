export const MOCK_NOTES_BY_PROJECT = {
  'smart-traffic-system': [
    {
      id: 'n1',
      title: 'Latency budget for edge inference',
      body: 'Need sub-50ms inference per frame on Jetson Orin to keep the control loop responsive. Quantized YOLO-tiny hits ~38ms in early tests.',
      tags: ['edge', 'performance'],
      pinned: true,
      updatedAt: '2 days ago',
    },
    {
      id: 'n2',
      title: 'Reward shaping ideas',
      body: 'Consider penalizing queue-length variance across approaches, not just total wait time, to avoid starving one direction.',
      tags: ['reinforcement-learning'],
      pinned: false,
      updatedAt: '4 days ago',
    },
    {
      id: 'n3',
      title: 'Dataset licensing question',
      body: 'Check whether the Urban Intersection Flow Dataset license permits commercial redistribution of derived models.',
      tags: ['dataset', 'legal'],
      pinned: false,
      updatedAt: '1 week ago',
    },
  ],
};

export function getNotesForProject(projectId) {
  return MOCK_NOTES_BY_PROJECT[projectId] || [];
}
