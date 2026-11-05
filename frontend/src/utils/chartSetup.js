import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  PointElement,
  LineElement,
  BarElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';

/**
 * chartSetup — registers every Chart.js piece used anywhere in the app,
 * once. Import this module (for its side effect) at the top of any file
 * that renders a react-chartjs-2 chart:
 *   import '../../utils/chartSetup';
 */
ChartJS.register(CategoryScale, LinearScale, RadialLinearScale, PointElement, LineElement, BarElement, Filler, Tooltip, Legend);

export default ChartJS;
