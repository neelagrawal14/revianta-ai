import { MOCK_PROJECTS } from '../mockData';

/**
 * Technology map data: a small directed graph of domains → models/tools →
 * supporting concepts, consumed by <ForceGraph /> on the project-level
 * Technology Map page and the workspace-level Technology Galaxy page.
 */
const SMART_TRAFFIC_TECH_MAP = {
  nodes: [
    { id: 'cv', label: 'Computer Vision', type: 'domain', group: 'domain' },
    { id: 'rl', label: 'Reinforcement Learning', type: 'domain', group: 'domain' },
    { id: 'edge', label: 'Edge Compute', type: 'domain', group: 'domain' },
    { id: 'yolo', label: 'YOLO', type: 'model', group: 'model' },
    { id: 'cnn', label: 'CNN', type: 'model', group: 'model' },
    { id: 'dqn', label: 'Deep Q-Network', type: 'model', group: 'model' },
    { id: 'opencv', label: 'OpenCV', type: 'tool', group: 'tool' },
    { id: 'sumo', label: 'SUMO', type: 'tool', group: 'tool' },
    { id: 'jetson', label: 'Jetson', type: 'tool', group: 'tool' },
    { id: 'edge-ai', label: 'Edge AI', type: 'concept', group: 'concept' },
    { id: 'multi-agent', label: 'Multi-Agent Coordination', type: 'concept', group: 'concept' },
  ],
  links: [
    { source: 'cv', target: 'yolo', type: 'uses' },
    { source: 'cv', target: 'cnn', type: 'uses' },
    { source: 'yolo', target: 'opencv', type: 'related-to' },
    { source: 'cnn', target: 'opencv', type: 'related-to' },
    { source: 'yolo', target: 'edge-ai', type: 'derived-from' },
    { source: 'cnn', target: 'edge-ai', type: 'derived-from' },
    { source: 'rl', target: 'dqn', type: 'uses' },
    { source: 'dqn', target: 'sumo', type: 'related-to' },
    { source: 'dqn', target: 'multi-agent', type: 'derived-from' },
    { source: 'edge', target: 'jetson', type: 'uses' },
    { source: 'edge', target: 'edge-ai', type: 'related-to' },
    { source: 'jetson', target: 'yolo', type: 'related-to' },
  ],
};

function generateTechMapFor(project) {
  const domainNodes = project.tags.map((tag, i) => ({
    id: `domain-${i}`,
    label: tag,
    type: 'domain',
    group: 'domain',
  }));

  const conceptNodes = [
    { id: 'concept-core', label: `${project.domain} Core`, type: 'concept', group: 'concept' },
  ];

  const links = domainNodes.map((n) => ({ source: n.id, target: 'concept-core', type: 'related-to' }));
  for (let i = 0; i < domainNodes.length - 1; i++) {
    links.push({ source: domainNodes[i].id, target: domainNodes[i + 1].id, type: 'related-to' });
  }

  return { nodes: [...domainNodes, ...conceptNodes], links };
}

const TECH_MAP_BY_PROJECT = {
  'smart-traffic-system': SMART_TRAFFIC_TECH_MAP,
};

export function getTechMapForProject(projectId) {
  if (TECH_MAP_BY_PROJECT[projectId]) return TECH_MAP_BY_PROJECT[projectId];
  const project = MOCK_PROJECTS.find((p) => p.id === projectId);
  return project ? generateTechMapFor(project) : { nodes: [], links: [] };
}

/**
 * Global "Technology Galaxy" — an aggregate view across every project's
 * technology tags, for the workspace-level /tech-graph page.
 */
export function getGlobalTechnologyGalaxy() {
  const nodes = [];
  const links = [];
  const seen = new Map();

  MOCK_PROJECTS.forEach((project) => {
    const projectNodeId = `project-${project.id}`;
    nodes.push({ id: projectNodeId, label: project.name, type: 'project', group: 'project', value: 1.4 });

    project.tags.forEach((tag) => {
      const tagId = `tag-${tag.toLowerCase().replace(/\s+/g, '-')}`;
      if (!seen.has(tagId)) {
        seen.set(tagId, true);
        nodes.push({ id: tagId, label: tag, type: 'domain', group: 'domain' });
      }
      links.push({ source: projectNodeId, target: tagId, type: 'uses' });
    });
  });

  return { nodes, links };
}
