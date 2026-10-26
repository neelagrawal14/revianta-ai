import { useMemo } from 'react';
import { useParams } from 'react-router-dom';
import { ShieldAlert } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import EmptyState from '../../components/common/EmptyState';
import GapCard from '../../components/research/GapCard';
import { getGapsForDomain } from '../../constants/mock';
import { MOCK_PROJECTS } from '../../constants/mockData';

export default function ProjectGapsPage() {
  const { projectId } = useParams();
  const project = MOCK_PROJECTS.find((p) => p.id === projectId);
  const gaps = useMemo(() => (project ? getGapsForDomain(project.domain) : []), [project]);

  return (
    <PageContainer>
      <SectionHeader
        title="Research Gaps"
        description="Potential gaps in the research landscape around this project. These are UI suggestions, not validated findings."
      />

      {gaps.length > 0 ? (
        <div className="mt-6 grid gap-4 lg:grid-cols-2">
          {gaps.map((gap) => (
            <GapCard key={gap.id} gap={gap} />
          ))}
        </div>
      ) : (
        <EmptyState
          className="mt-8"
          icon={ShieldAlert}
          title="No gaps surfaced yet"
          description="Revianta hasn't flagged any research gaps specific to this project's domain yet."
        />
      )}
    </PageContainer>
  );
}
