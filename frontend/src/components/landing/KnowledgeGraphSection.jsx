import NodeGraph from '../common/NodeGraph';

export default function KnowledgeGraphSection() {
  return (
    <section id="knowledge-graph" className="px-4 py-20 sm:px-6 lg:py-28">
      <div className="mx-auto grid max-w-6xl items-center gap-12 lg:grid-cols-2 lg:gap-16">
        <div>
          <h2 className="font-display text-3xl text-text sm:text-4xl">
            See how your idea connects to everything around it.
          </h2>
          <p className="mt-4 max-w-md text-text-dim">
            Every project becomes a live knowledge graph — papers, technologies, datasets,
            and patents plotted by how closely they relate to what you're building.
          </p>
          <ul className="mt-8 space-y-3 text-sm text-text-dim">
            <li className="flex gap-2.5"><span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-violet" /> Zoom from a single citation to the full technology landscape</li>
            <li className="flex gap-2.5"><span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-violet" /> Trace how a technology choice propagates through your risk profile</li>
          </ul>
        </div>

        <div className="glass rounded-[24px] p-5">
          <NodeGraph className="h-auto w-full opacity-90" />
        </div>
      </div>
    </section>
  );
}
