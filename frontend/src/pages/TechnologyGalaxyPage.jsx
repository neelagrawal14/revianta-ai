import { useMemo } from 'react';
import PageContainer from '../components/layout/PageContainer';
import ForceGraph from '../components/graph/ForceGraph';
import { getGlobalTechnologyGalaxy } from '../constants/mock/mockTechnologies';

export default function TechnologyGalaxyPage() {
  const { nodes, links } = useMemo(() => getGlobalTechnologyGalaxy(), []);

  return (
    <PageContainer>
      <p className="mono-tag text-indigo-soft">Across your workspace</p>
      <h1 className="mt-2 font-display text-3xl text-text sm:text-4xl">Technology Graph</h1>
      <p className="mt-2 max-w-lg text-text-dim">
        Every project in this workspace and the technologies it draws on, as one connected galaxy.
      </p>
      <div className="mt-8">
        <ForceGraph
          nodes={nodes}
          links={links}
          emptyLabel="technologies"
          legend="Each project node connects to the technology domains it uses — shared technologies pull related projects closer together."
        />
      </div>
    </PageContainer>
  );
}
