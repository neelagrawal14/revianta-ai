import { useMemo } from 'react';
import { forceSimulation, forceManyBody, forceLink, forceCenter, forceCollide } from 'd3-force';

/**
 * useForceLayout — runs a d3-force simulation synchronously (a fixed
 * number of ticks, not a live animation loop) to produce a stable node
 * layout for <ForceGraph/>. Static layout keeps this cheap and
 * deterministic instead of re-simulating on every frame.
 */
export default function useForceLayout(nodes, links, width, height) {
  return useMemo(() => {
    if (!nodes?.length) return { nodes: [], links: [] };

    const nodeIds = new Set(nodes.map((n) => n.id));
    const simNodes = nodes.map((n) => ({ ...n }));
    const simLinks = links
      .filter((l) => nodeIds.has(l.source) && nodeIds.has(l.target))
      .map((l) => ({ ...l }));

    const simulation = forceSimulation(simNodes)
      .force('charge', forceManyBody().strength(-160))
      .force(
        'link',
        forceLink(simLinks)
          .id((d) => d.id)
          .distance(78)
          .strength(0.55)
      )
      .force('center', forceCenter(width / 2, height / 2))
      .force(
        'collide',
        forceCollide().radius((d) => 16 + (d.value || 1) * 8)
      )
      .stop();

    for (let i = 0; i < 320; i++) simulation.tick();

    return { nodes: simNodes, links: simLinks };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [nodes, links, width, height]);
}
