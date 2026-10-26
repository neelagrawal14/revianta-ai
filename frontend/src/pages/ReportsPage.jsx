import { Link } from 'react-router-dom';
import { Eye, Download, FileBarChart } from 'lucide-react';
import PageContainer from '../components/layout/PageContainer';
import GlassCard from '../components/common/GlassCard';
import Badge, { riskTone } from '../components/common/Badge';
import EmptyState from '../components/common/EmptyState';
import { MOCK_REPORTS } from '../constants/mock/mockReports';

const STATUS_TONE = { Ready: 'cyan', 'Needs Review': 'amber', Incomplete: 'rose' };

export default function ReportsPage() {
  return (
    <PageContainer>
      <p className="mono-tag text-indigo-soft">One report per project</p>
      <h1 className="mt-2 font-display text-3xl text-text sm:text-4xl">Reports</h1>
      <p className="mt-2 max-w-lg text-text-dim">
        A snapshot of each project's health and risk. PDF export isn't wired up yet, so
        Export/Download appear as placeholders rather than faking a download.
      </p>

      {MOCK_REPORTS.length > 0 ? (
        <div className="mt-8 space-y-3">
          {MOCK_REPORTS.map((report) => (
            <GlassCard key={report.id} className="flex flex-wrap items-center justify-between gap-4 p-5">
              <div className="min-w-0">
                <Link to={`/projects/${report.projectId}`} className="font-display text-base text-text hover:text-indigo-soft">
                  {report.projectName}
                </Link>
                <p className="mt-1 text-xs text-text-faint">Last analysis {report.lastAnalysis}</p>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <div className="text-right">
                  <p className="font-mono text-sm text-text">{report.healthScore}%</p>
                  <p className="text-[11px] text-text-faint">health</p>
                </div>
                <Badge tone={riskTone(report.riskLevel)}>{report.riskLevel} Risk</Badge>
                <Badge tone={STATUS_TONE[report.reportStatus]}>{report.reportStatus}</Badge>

                <div className="flex gap-1.5">
                  <Link
                    to={`/projects/${report.projectId}/risk`}
                    className="flex items-center gap-1.5 rounded-full border border-line px-3 py-1.5 text-xs text-text-dim hover:text-text"
                  >
                    <Eye size={13} /> View
                  </Link>
                  <button
                    disabled={!report.exportReady}
                    title="PDF export isn't available yet"
                    className="flex items-center gap-1.5 rounded-full border border-line px-3 py-1.5 text-xs text-text-faint opacity-50"
                  >
                    <Download size={13} /> Export
                  </button>
                </div>
              </div>
            </GlassCard>
          ))}
        </div>
      ) : (
        <EmptyState className="mt-8" icon={FileBarChart} title="No reports yet" description="Reports appear once a project has been analyzed." />
      )}
    </PageContainer>
  );
}
