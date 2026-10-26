import '../../utils/chartSetup';
import { Radar } from 'react-chartjs-2';

/**
 * RiskRadarChart — signature visual #3 (part of the seven-dimensional
 * risk visualization) on the Risk Intelligence page. A dark, restyled
 * Chart.js radar rather than default chart chrome.
 */
export default function RiskRadarChart({ dimensions }) {
  const data = {
    labels: dimensions.map((d) => d.label.replace(' Risk', '')),
    datasets: [
      {
        label: 'Risk score',
        data: dimensions.map((d) => d.score),
        backgroundColor: 'rgba(91, 95, 240, 0.18)',
        borderColor: '#7c80f5',
        borderWidth: 2,
        pointBackgroundColor: '#35e0d0',
        pointBorderColor: '#060811',
        pointBorderWidth: 1.5,
        pointRadius: 4,
        pointHoverRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 700, easing: 'easeOutCubic' },
    scales: {
      r: {
        min: 0,
        max: 100,
        angleLines: { color: 'rgba(148,163,214,0.16)' },
        grid: { color: 'rgba(148,163,214,0.14)' },
        pointLabels: {
          color: '#a9aecb',
          font: { family: 'Manrope', size: 11 },
        },
        ticks: {
          display: true,
          backdropColor: 'transparent',
          color: '#676d90',
          stepSize: 25,
          font: { size: 9 },
        },
      },
    },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#10142a',
        borderColor: 'rgba(148,163,214,0.28)',
        borderWidth: 1,
        titleColor: '#eef0fb',
        bodyColor: '#a9aecb',
        padding: 10,
        callbacks: {
          label: (ctx) => `${ctx.label} risk: ${ctx.raw}%`,
        },
      },
    },
  };

  return (
    <div className="h-72 w-full sm:h-80">
      <Radar data={data} options={options} />
    </div>
  );
}
