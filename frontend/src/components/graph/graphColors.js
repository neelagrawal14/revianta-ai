/**
 * Shared node-group color palette for ForceGraph, used by both the
 * Technology Map/Galaxy and the Knowledge Graph so the same node type
 * always reads as the same color across the app.
 */
export const GRAPH_GROUP_COLORS = {
  project: '#5b5ff0',
  paper: '#35e0d0',
  technology: '#9153ea',
  domain: '#7c80f5',
  model: '#f2b25c',
  tool: '#35e0d0',
  concept: '#ef6a7c',
};

export function colorForGroup(group) {
  return GRAPH_GROUP_COLORS[group] || '#8990d6';
}
