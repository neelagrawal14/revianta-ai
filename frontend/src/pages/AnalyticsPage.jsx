import PageContainer from '../components/layout/PageContainer';
import GlassCard from '../components/common/GlassCard';
import { AnalyticsLineChart, AnalyticsBarChart } from '../components/analytics/AnalyticsCharts';
import {
  HEALTH_OVER_TIME,
  RESEARCH_ACTIVITY,
  PAPER_GROWTH,
  TECHNOLOGY_GROWTH,
  SIMILARITY_DISTRIBUTION,
  DATASET_AVAILABILITY,
  PROJECT_COMPLEXITY,
  RESEARCH_TRENDS,
  RISK_DISTRIBUTION,
} from '../constants/mock/mockAnalytics';

const CHARTS = [
  { title: 'Project health over time', ...HEALTH_OVER_TIME, kind: 'line', color: '#35e0d0', fill: 'rgba(53,224,208,0.12)' },
  { title: 'Risk distribution', ...RISK_DISTRIBUTION, kind: 'bar', color: '#ef6a7c' },
  { title: 'Research activity', ...RESEARCH_ACTIVITY, kind: 'line', color: '#5b5ff0', fill: 'rgba(91,95,240,0.12)' },
  { title: 'Paper growth (field-wide)', ...PAPER_GROWTH, kind: 'line', color: '#9153ea', fill: 'rgba(145,83,234,0.12)' },
  { title: 'Technology growth', ...TECHNOLOGY_GROWTH, kind: 'bar', color: '#f2b25c' },
  { title: 'Similarity distribution', ...SIMILARITY_DISTRIBUTION, kind: 'bar', color: '#35e0d0' },
  { title: 'Dataset availability', ...DATASET_AVAILABILITY, kind: 'bar', color: '#7c80f5' },
  { title: 'Project complexity', ...PROJECT_COMPLEXITY, kind: 'bar', color: '#9153ea' },
  { title: 'Research trends', ...RESEARCH_TRENDS, kind: 'bar', color: '#5b5ff0' },
];

export default function AnalyticsPage() {
  return (
    <PageContainer>
      <p className="mono-tag text-indigo-soft">Workspace analytics</p>
      <h1 className="mt-2 font-display text-3xl text-text sm:text-4xl">Research Analytics</h1>
      <p className="mt-2 max-w-lg text-text-dim">
        Aggregate view across every project's health, risk, and research activity — mock data
        shown until connected to the live analysis pipeline.
      </p>

      <div className="mt-8 grid gap-4 lg:grid-cols-2">
        {CHARTS.map((chart) => (
          <GlassCard key={chart.title} className="p-5">
            <p className="mb-3 text-sm text-text-dim">{chart.title}</p>
            {chart.kind === 'line' ? (
              <AnalyticsLineChart labels={chart.labels} values={chart.values} color={chart.color} fillColor={chart.fill} />
            ) : (
              <AnalyticsBarChart labels={chart.labels} values={chart.values} color={chart.color} />
            )}
          </GlassCard>
        ))}
      </div>
    </PageContainer>
  );
}
