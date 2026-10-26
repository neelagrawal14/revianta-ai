import PageContainer from '../components/layout/PageContainer';
import ResearchTimeline from '../components/timeline/ResearchTimeline';
import { GLOBAL_TIMELINE } from '../constants/mock/mockTimeline';

export default function GlobalTimelinePage() {
  return (
    <PageContainer className="max-w-3xl">
      <p className="mono-tag text-indigo-soft">Field-wide evolution</p>
      <h1 className="mt-2 font-display text-3xl text-text sm:text-4xl">Research Timeline</h1>
      <p className="mt-2 max-w-lg text-text-dim">
        How the broader technology landscape has shifted year over year, independent of any single project.
      </p>
      <div className="mt-10">
        <ResearchTimeline entries={GLOBAL_TIMELINE} />
      </div>
    </PageContainer>
  );
}
