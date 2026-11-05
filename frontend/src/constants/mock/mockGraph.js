import { MOCK_PROJECTS } from '../mockData';
import { getPapersForProject } from './mockPapers';

/**
 * Knowledge graph data for the project-level /graph page: the project
 * itself, its most similar papers, and the technologies connecting them.
 * Node `group` drives color; `type` drives the icon/legend in the UI.
 */
export function getKnowledgeGraphForProject(projectId) {
  const project = MOCK_PROJECTS.find((p) => p.id === projectId);
  if (!project) return { nodes: [], links: [] };

  const papers = getPapersForProject(projectId).slice(0, 5);
  const projectNodeId = `project-${project.id}`;

  const nodes = [
    { id: projectNodeId, label: project.name, type: 'project', group: 'project', value: 1.6 },
    ...project.tags.map((tag) => ({
      id: `tech-${tag.toLowerCase().replace(/\s+/g, '-')}`,
      label: tag,
      type: 'technology',
      group: 'technology',
    })),
    ...papers.map((p) => ({
      id: `paper-${p.id}`,
      label: p.title,
      type: 'paper',
      group: 'paper',
      value: 0.6 + p.similarity / 150,
    })),
    { id: 'concept-risk', label: 'Deployment Risk', type: 'concept', group: 'concept' },
  ];

  const links = [
    ...project.tags.map((tag) => ({
      source: projectNodeId,
      target: `tech-${tag.toLowerCase().replace(/\s+/g, '-')}`,
      type: 'uses',
    })),
    ...papers.map((p) => ({
      source: projectNodeId,
      target: `paper-${p.id}`,
      type: 'similarity',
      weight: p.similarity,
    })),
    ...papers.slice(0, 2).map((p) => ({
      source: `paper-${p.id}`,
      target: `tech-${(p.technologies[0] || project.tags[0]).toLowerCase().replace(/\s+/g, '-')}`,
      type: 'related-to',
    })),
    { source: projectNodeId, target: 'concept-risk', type: 'related-to' },
  ];

  return { nodes, links };
}
