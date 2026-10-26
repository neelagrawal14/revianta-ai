import { useMemo, useRef, useState } from 'react';
import { ZoomIn, ZoomOut, Maximize2, X } from 'lucide-react';
import useForceLayout from './useForceLayout';
import { colorForGroup } from './graphColors';
import SearchBar from '../common/SearchBar';
import Badge from '../common/Badge';
import GlassCard from '../common/GlassCard';
import { cn } from '../../utils/cn';

const WIDTH = 900;
const HEIGHT = 560;

/**
 * ForceGraph — Revianta's signature graph visualization, shared by the
 * Technology Map/Galaxy pages and the Knowledge Graph page. Renders an
 * SVG force layout with zoom, pan, hover-highlight, click-to-select
 * (with a built-in side detail panel), search, and group filtering.
 */
export default function ForceGraph({ nodes, links, legend, className, emptyLabel = 'technologies' }) {
  const { nodes: laidOutNodes, links: laidOutLinks } = useForceLayout(nodes, links, WIDTH, HEIGHT);

  const [transform, setTransform] = useState({ x: 0, y: 0, k: 1 });
  const [dragging, setDragging] = useState(false);
  const dragStart = useRef({ x: 0, y: 0, tx: 0, ty: 0 });

  const [hoveredId, setHoveredId] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [query, setQuery] = useState('');
  const [hiddenGroups, setHiddenGroups] = useState(() => new Set());

  const groups = useMemo(() => [...new Set(laidOutNodes.map((n) => n.group))], [laidOutNodes]);

  const nodeById = useMemo(() => new Map(laidOutNodes.map((n) => [n.id, n])), [laidOutNodes]);

  const visibleNodeIds = useMemo(() => {
    const set = new Set();
    laidOutNodes.forEach((n) => {
      if (!hiddenGroups.has(n.group)) set.add(n.id);
    });
    return set;
  }, [laidOutNodes, hiddenGroups]);

  const matchIds = useMemo(() => {
    if (!query.trim()) return null;
    const q = query.toLowerCase();
    return new Set(laidOutNodes.filter((n) => n.label.toLowerCase().includes(q)).map((n) => n.id));
  }, [laidOutNodes, query]);

  const activeId = hoveredId || selectedId;
  const neighborIds = useMemo(() => {
    if (!activeId) return null;
    const set = new Set([activeId]);
    laidOutLinks.forEach((l) => {
      const s = l.source.id ?? l.source;
      const t = l.target.id ?? l.target;
      if (s === activeId) set.add(t);
      if (t === activeId) set.add(s);
    });
    return set;
  }, [activeId, laidOutLinks]);

  const selectedNode = selectedId ? nodeById.get(selectedId) : null;
  const selectedConnections = useMemo(() => {
    if (!selectedNode) return [];
    return laidOutLinks
      .filter((l) => (l.source.id ?? l.source) === selectedId || (l.target.id ?? l.target) === selectedId)
      .map((l) => {
        const otherId = (l.source.id ?? l.source) === selectedId ? l.target.id ?? l.target : l.source.id ?? l.source;
        return { node: nodeById.get(otherId), type: l.type };
      })
      .filter((c) => c.node);
  }, [selectedNode, selectedId, laidOutLinks, nodeById]);

  function zoomBy(factor) {
    setTransform((t) => ({ ...t, k: Math.min(2.4, Math.max(0.45, t.k * factor)) }));
  }

  function resetView() {
    setTransform({ x: 0, y: 0, k: 1 });
    setSelectedId(null);
  }

  function handlePointerDown(e) {
    if (e.target.closest('[data-graph-node]')) return;
    setDragging(true);
    dragStart.current = { x: e.clientX, y: e.clientY, tx: transform.x, ty: transform.y };
  }

  function handlePointerMove(e) {
    if (!dragging) return;
    const dx = e.clientX - dragStart.current.x;
    const dy = e.clientY - dragStart.current.y;
    setTransform((t) => ({ ...t, x: dragStart.current.tx + dx, y: dragStart.current.ty + dy }));
  }

  function handlePointerUp() {
    setDragging(false);
  }

  function handleWheel(e) {
    e.preventDefault();
    zoomBy(e.deltaY < 0 ? 1.1 : 0.9);
  }

  function toggleGroup(group) {
    setHiddenGroups((prev) => {
      const next = new Set(prev);
      if (next.has(group)) next.delete(group);
      else next.add(group);
      return next;
    });
  }

  if (!nodes?.length) {
    return (
      <GlassCard className="flex flex-col items-center justify-center gap-2 py-20 text-center text-text-dim">
        <p className="font-display text-lg text-text">No {emptyLabel} mapped yet</p>
        <p className="text-sm">Run research intelligence on this project to build its graph.</p>
      </GlassCard>
    );
  }

  return (
    <div className={cn('relative', className)}>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <SearchBar
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search nodes…"
          hint={null}
          className="h-10 w-full max-w-xs"
        />
        <div className="flex flex-wrap items-center gap-1.5">
          {groups.map((g) => (
            <button
              key={g}
              onClick={() => toggleGroup(g)}
              className={cn(
                'flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs transition-colors',
                hiddenGroups.has(g)
                  ? 'border-line text-text-faint opacity-50'
                  : 'border-line-strong text-text-dim hover:text-text'
              )}
            >
              <span className="h-1.5 w-1.5 rounded-full" style={{ background: colorForGroup(g) }} />
              {g}
            </button>
          ))}
        </div>
      </div>

      <GlassCard className="relative overflow-hidden p-0">
        <div className="absolute right-3 top-3 z-10 flex gap-1.5">
          <button onClick={() => zoomBy(1.2)} aria-label="Zoom in" className="rounded-lg border border-line bg-surface/80 p-1.5 text-text-dim hover:text-text">
            <ZoomIn size={15} />
          </button>
          <button onClick={() => zoomBy(0.83)} aria-label="Zoom out" className="rounded-lg border border-line bg-surface/80 p-1.5 text-text-dim hover:text-text">
            <ZoomOut size={15} />
          </button>
          <button onClick={resetView} aria-label="Reset view" className="rounded-lg border border-line bg-surface/80 p-1.5 text-text-dim hover:text-text">
            <Maximize2 size={15} />
          </button>
        </div>

        <svg
          viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
          className={cn('h-[420px] w-full select-none sm:h-[520px]', dragging ? 'cursor-grabbing' : 'cursor-grab')}
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
          onPointerLeave={handlePointerUp}
          onWheel={handleWheel}
        >
          <g transform={`translate(${transform.x} ${transform.y}) scale(${transform.k})`}>
            {laidOutLinks.map((l, i) => {
              const s = l.source;
              const t = l.target;
              if (!visibleNodeIds.has(s.id) || !visibleNodeIds.has(t.id)) return null;
              const dimmed = activeId && !(neighborIds?.has(s.id) && neighborIds?.has(t.id));
              return (
                <line
                  key={i}
                  x1={s.x} y1={s.y} x2={t.x} y2={t.y}
                  stroke="rgba(148,163,214,0.35)"
                  strokeWidth={1}
                  opacity={dimmed ? 0.12 : 0.5}
                />
              );
            })}

            {laidOutNodes.map((n) => {
              if (!visibleNodeIds.has(n.id)) return null;
              const isMatch = !matchIds || matchIds.has(n.id);
              const isNeighbor = !activeId || neighborIds?.has(n.id);
              const dimmed = !isMatch || !isNeighbor;
              const radius = 8 + (n.value || 1) * 7;
              const color = colorForGroup(n.group);
              const isSelected = n.id === selectedId;

              return (
                <g
                  key={n.id}
                  data-graph-node
                  transform={`translate(${n.x} ${n.y})`}
                  opacity={dimmed ? 0.25 : 1}
                  className="cursor-pointer transition-opacity duration-200"
                  onMouseEnter={() => setHoveredId(n.id)}
                  onMouseLeave={() => setHoveredId(null)}
                  onClick={() => setSelectedId(n.id === selectedId ? null : n.id)}
                >
                  {isSelected && <circle r={radius + 6} fill="none" stroke={color} strokeWidth={1.5} opacity={0.6} />}
                  <circle r={radius} fill={color} opacity={0.18} />
                  <circle r={radius * 0.55} fill={color} />
                  <text
                    y={radius + 14}
                    textAnchor="middle"
                    fill="#c7cbe8"
                    fontSize={11}
                    fontFamily="Manrope, sans-serif"
                    className="pointer-events-none"
                  >
                    {n.label.length > 22 ? `${n.label.slice(0, 20)}…` : n.label}
                  </text>
                </g>
              );
            })}
          </g>
        </svg>
      </GlassCard>

      {legend && <p className="mt-3 text-xs text-text-faint">{legend}</p>}

      {selectedNode && (
        <GlassCard tone="strong" className="mt-4 p-5">
          <div className="flex items-start justify-between gap-4">
            <div>
              <Badge>{selectedNode.group}</Badge>
              <h3 className="mt-2 font-display text-lg text-text">{selectedNode.label}</h3>
            </div>
            <button
              onClick={() => setSelectedId(null)}
              aria-label="Close details"
              className="rounded-lg p-1.5 text-text-faint hover:bg-white/[0.05] hover:text-text"
            >
              <X size={16} />
            </button>
          </div>

          {selectedConnections.length > 0 && (
            <div className="mt-4 border-t border-line pt-4">
              <p className="mb-2 text-xs text-text-faint">Connected to</p>
              <div className="flex flex-wrap gap-1.5">
                {selectedConnections.map(({ node, type }) => (
                  <span
                    key={node.id}
                    className="mono-tag rounded-full border border-line bg-white/[0.03] px-2.5 py-1 text-text-dim"
                  >
                    {node.label} <span className="text-text-faint">· {type}</span>
                  </span>
                ))}
              </div>
            </div>
          )}
        </GlassCard>
      )}
    </div>
  );
}
