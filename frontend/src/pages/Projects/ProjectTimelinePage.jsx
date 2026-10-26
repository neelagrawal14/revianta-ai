import { useMemo } from 'react';
import { useParams } from 'react-router-dom';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import ResearchTimeline from '../../components/timeline/ResearchTimeline';
import { getTimelineForProject } from '../../constants/mock';

export default function ProjectTimelinePage() {
  const { projectId } = useParams();
  const entries = useMemo(() => getTimelineForProject(projectId), [projectId]);

  return (
    <PageContainer className="max-w-3xl">
      <SectionHeader
        title="Research Timeline"
        description="How the approach behind this project has evolved over time."
      />
      <div className="mt-8">
        <ResearchTimeline entries={entries} />
      </div>
    </PageContainer>
  );
}
