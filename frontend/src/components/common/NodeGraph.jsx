/**
 * NodeGraph — Revianta's signature visual motif: papers, technologies,
 * datasets, and patents rendered as a connected knowledge graph.
 * Used on the landing hero and echoed (smaller, quieter) elsewhere.
 * Pure SVG, no external images — matches the "abstract, not stock
 * imagery" instruction.
 */
export default function NodeGraph({ className }) {
  const nodes = [
    { id: 'core', x: 300, y: 210, r: 15, color: 'var(--color-indigo)', label: 'Your Idea' },
    { id: 'p1', x: 130, y: 110, r: 8, color: 'var(--color-cyan)', label: 'Paper' },
    { id: 'p2', x: 90, y: 240, r: 7, color: 'var(--color-cyan)', label: 'Paper' },
    { id: 'p3', x: 175, y: 330, r: 6, color: 'var(--color-cyan)', label: 'Paper' },
    { id: 't1', x: 440, y: 90, r: 9, color: 'var(--color-violet)', label: 'Technology' },
    { id: 't2', x: 490, y: 220, r: 7, color: 'var(--color-violet)', label: 'Technology' },
    { id: 't3', x: 430, y: 330, r: 6, color: 'var(--color-violet)', label: 'Technology' },
    { id: 'd1', x: 300, y: 60, r: 6, color: 'var(--color-indigo-soft)', label: 'Dataset' },
    { id: 'r1', x: 300, y: 370, r: 6, color: 'var(--color-amber)', label: 'Patent' },
  ];

  const links = [
    ['core', 'p1'], ['core', 'p2'], ['core', 'p3'],
    ['core', 't1'], ['core', 't2'], ['core', 't3'],
    ['core', 'd1'], ['core', 'r1'],
    ['t1', 'd1'], ['p1', 'd1'], ['t2', 'r1'], ['p3', 'r1'],
  ];

  const find = (id) => nodes.find((n) => n.id === id);

  return (
    <svg viewBox="0 0 600 420" className={className} role="img" aria-label="Knowledge graph connecting research papers, technologies, datasets, and patents around a project idea">
      <defs>
        <radialGradient id="ng-core-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="var(--color-indigo)" stopOpacity="0.55" />
          <stop offset="100%" stopColor="var(--color-indigo)" stopOpacity="0" />
        </radialGradient>
      </defs>

      <circle cx="300" cy="210" r="90" fill="url(#ng-core-glow)" />

      {links.map(([a, b], i) => {
        const from = find(a);
        const to = find(b);
        return (
          <line
            key={i}
            x1={from.x} y1={from.y} x2={to.x} y2={to.y}
            stroke="rgba(148,163,214,0.35)"
            strokeWidth="1"
          />
        );
      })}

      {nodes.map((n) => (
        <g key={n.id}>
          <circle
            cx={n.x} cy={n.y} r={n.r + 6}
            fill={n.color}
            opacity="0.12"
          />
          <circle
            cx={n.x} cy={n.y} r={n.r}
            fill={n.color}
            style={{ animation: 'pulse-node 3.2s ease-in-out infinite', animationDelay: `${(n.x % 5) * 0.15}s` }}
          />
        </g>
      ))}
    </svg>
  );
}
