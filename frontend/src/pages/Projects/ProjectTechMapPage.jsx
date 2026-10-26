import { useMemo } from 'react';
import { useParams } from 'react-router-dom';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import ForceGraph from '../../components/graph/ForceGraph';
import { getTechMapForProject } from '../../constants/mock';

export default function ProjectTechMapPage() {
  const { projectId } = useParams();
  const { nodes, links } = useMemo(() => getTechMapForProject(projectId), [projectId]);

  return (
    <PageContainer>
      <SectionHeader
        title="Technology Map"
        description="How the technologies, models, and tools around this project connect — drag to pan, scroll to zoom, click a node for details."
      />
      <div className="mt-6">
        <ForceGraph
          nodes={nodes}
          links={links}
          emptyLabel="technologies"
          legend="Domains, models, and tools this project's approach draws on, sized and grouped by role."
        />
      </div>
    </PageContainer>
  );
}
