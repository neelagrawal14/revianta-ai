import '../../utils/chartSetup';
import { Line, Bar } from 'react-chartjs-2';

const GRID = 'rgba(148,163,214,0.1)';
const TICK = '#676d90';
const FONT = { family: 'Manrope', size: 11 };

const baseScales = {
  x: { grid: { color: GRID }, ticks: { color: TICK, font: FONT } },
  y: { grid: { color: GRID }, ticks: { color: TICK, font: FONT }, beginAtZero: true },
};

const baseOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: { duration: 600, easing: 'easeOutCubic' },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#10142a',
      borderColor: 'rgba(148,163,214,0.28)',
      borderWidth: 1,
      titleColor: '#eef0fb',
      bodyColor: '#a9aecb',
      padding: 10,
    },
  },
  scales: baseScales,
};

export function AnalyticsLineChart({ labels, values, color = '#5b5ff0', fillColor = 'rgba(91,95,240,0.12)' }) {
  const data = {
    labels,
    datasets: [
      {
        data: values,
        borderColor: color,
        backgroundColor: fillColor,
        pointBackgroundColor: color,
        pointBorderColor: '#060811',
        pointRadius: 3,
        borderWidth: 2,
        tension: 0.35,
        fill: true,
      },
    ],
  };
  return (
    <div className="h-56">
      <Line data={data} options={baseOptions} />
    </div>
  );
}

export function AnalyticsBarChart({ labels, values, color = '#9153ea' }) {
  const data = {
    labels,
    datasets: [{ data: values, backgroundColor: color, borderRadius: 6, maxBarThickness: 34 }],
  };
  return (
    <div className="h-56">
      <Bar data={data} options={baseOptions} />
    </div>
  );
}
