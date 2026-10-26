import { useMemo } from 'react';
import { useParams } from 'react-router-dom';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import ForceGraph from '../../components/graph/ForceGraph';
import { getKnowledgeGraphForProject } from '../../constants/mock';

/**
 * The project's knowledge graph — signature visual #4 (in its
 * project-scoped form): this project, its most similar papers, and the
 * technologies connecting them, as one immersive graph.
 */
export default function ProjectGraphPage() {
  const { projectId } = useParams();
  const { nodes, links } = useMemo(() => getKnowledgeGraphForProject(projectId), [projectId]);

  return (
    <PageContainer>
      <SectionHeader
        title="Knowledge Graph"
        description="This project, the papers most similar to it, and the technologies tying them together."
      />
      <div className="mt-6">
        <ForceGraph
          nodes={nodes}
          links={links}
          emptyLabel="connections"
          legend="Line weight reflects relationship strength — similarity to papers, technology usage, and related concepts."
        />
      </div>
    </PageContainer>
  );
}
