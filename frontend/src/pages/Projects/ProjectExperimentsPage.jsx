import { useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { FlaskConical } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import SelectField from '../../components/common/SelectField';
import GlassCard from '../../components/common/GlassCard';
import Badge from '../../components/common/Badge';
import EmptyState from '../../components/common/EmptyState';
import { getExperimentsForProject, EXPERIMENT_STATUSES } from '../../constants/mock';

const STATUS_TONE = { PLANNED: 'neutral', RUNNING: 'indigo', COMPLETED: 'cyan', FAILED: 'rose' };
const FILTERS = [{ value: 'all', label: 'All statuses' }, ...EXPERIMENT_STATUSES.map((s) => ({ value: s, label: s }))];

export default function ProjectExperimentsPage() {
  const { projectId } = useParams();
  const experiments = useMemo(() => getExperimentsForProject(projectId), [projectId]);
  const [status, setStatus] = useState('all');

  const filtered = status === 'all' ? experiments : experiments.filter((e) => e.status === status);

  if (experiments.length === 0) {
    return (
      <PageContainer>
        <EmptyState icon={FlaskConical} title="No experiments logged" description="Track experiments here as you test approaches for this project." />
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <SectionHeader title="Experiments" description="What's been tried on this project, and what came of it." />

      <SelectField value={status} onChange={(e) => setStatus(e.target.value)} options={FILTERS} className="mt-6" />

      <div className="mt-6 space-y-3">
        {filtered.map((exp) => (
          <GlassCard key={exp.id} className="p-5">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h3 className="font-display text-base text-text">{exp.experiment}</h3>
                <p className="mt-1 text-sm text-text-dim">{exp.objective}</p>
              </div>
              <Badge tone={STATUS_TONE[exp.status]}>{exp.status}</Badge>
            </div>

            <div className="mt-3 flex flex-wrap gap-1.5">
              {exp.technologies.map((t) => (
                <Badge key={t}>{t}</Badge>
              ))}
            </div>

            {(exp.result || exp.notes) && (
              <div className="mt-4 space-y-2 border-t border-line pt-4 text-sm">
                {exp.result && <p className="text-text-dim"><span className="text-text-faint">Result — </span>{exp.result}</p>}
                {exp.notes && <p className="text-text-faint">{exp.notes}</p>}
              </div>
            )}

            <p className="mt-3 text-xs text-text-faint">{exp.date}</p>
          </GlassCard>
        ))}
      </div>
    </PageContainer>
  );
}
