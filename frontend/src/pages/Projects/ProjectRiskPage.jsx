
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { riskApi } from '../../services/riskApi';
import { projectApi } from '../../services/projectApi';

const getPayload = (response) =>
  response?.data ?? response?.project ?? response;

const formatScore = (value) => {
  const score = Number(value);
  return Number.isFinite(score) ? score.toFixed(1) : '—';
};

const getRiskColor = (score) => {
  if (score >= 65) return '#ef4444';
  if (score >= 35) return '#f59e0b';
  return '#22c55e';
};

function ScoreCard({ title, value, suffix = '/100', color }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
      <p className="text-sm text-gray-400">{title}</p>
      <div className="mt-3 flex items-end gap-2">
        <span className="text-3xl font-semibold text-white">
          {formatScore(value)}
        </span>
        <span className="mb-1 text-sm text-gray-500">{suffix}</span>
      </div>
      <div className="mt-4 h-2 overflow-hidden rounded-full bg-white/10">
        <div
          className="h-full rounded-full transition-all"
          style={{
            width: `${Math.min(100, Math.max(0, Number(value) || 0))}%`,
            backgroundColor: color,
          }}
        />
      </div>
    </div>
  );
}

export default function ProjectRiskPage() {
  const { projectId } = useParams();

  const [project, setProject] = useState(null);
  const [risk, setRisk] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;

    async function loadReport() {
      setLoading(true);
      setError('');

      try {
        const [projectResponse, riskResponse] = await Promise.all([
          projectApi.get(projectId).catch(() => null),
          riskApi.get(projectId),
        ]);

        if (cancelled) return;

        setProject(
          projectResponse ? getPayload(projectResponse) : null
        );
        setRisk(getPayload(riskResponse));
      } catch (err) {
        if (cancelled) return;

        const message =
          err?.message || 'Unable to load the risk report.';

        setError(
          message.toLowerCase().includes('404') ||
          message.toLowerCase().includes('run analysis first')
            ? 'No risk report exists for this project yet. Run the project analysis first.'
            : message
        );
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    if (projectId) loadReport();

    return () => {
      cancelled = true;
    };
  }, [projectId]);

  if (loading) {
    return (
      <main className="min-h-screen bg-[#090d18] p-8 text-white">
        <p className="animate-pulse text-gray-400">
          Loading Revianta AI risk report...
        </p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-[#090d18] p-8 text-white">
        <Link to="/projects" className="text-sm text-cyan-400">
          ← Back to projects
        </Link>
        <div className="mt-8 max-w-2xl rounded-2xl border border-amber-400/20 bg-amber-400/5 p-6">
          <h1 className="text-xl font-semibold">Risk report unavailable</h1>
          <p className="mt-3 text-gray-300">{error}</p>
          <p className="mt-3 text-sm text-gray-500">
            Check that the project exists, you are signed in, and the
            backend has a saved analysis for this project.
          </p>
        </div>
      </main>
    );
  }

  const overallHealth = Number(risk?.overallHealth ?? 0);
  const overallRisk = Number(risk?.overallRisk ?? 0);
  const dimensions = Array.isArray(risk?.dimensions)
    ? risk.dimensions
    : [];

  const stage2 = risk?.stage2;
  const probabilities =
    stage2?.probabilities ??
    stage2?.class_probabilities ??
    stage2?.classProbabilities ??
    null;

  const prediction =
    stage2?.prediction ??
    stage2?.predicted_outcome ??
    stage2?.predictedOutcome ??
    stage2?.outcome ??
    null;

  const explanation = risk?.aiRecommendation;

  return (
    <main className="min-h-screen bg-[#090d18] px-4 py-8 text-white sm:px-8">
      <div className="mx-auto max-w-7xl">
        <Link
          to="/projects"
          className="text-sm text-cyan-400 transition hover:text-cyan-300"
        >
          ← Back to projects
        </Link>

        <header className="mt-6 flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-cyan-400">
              REVIANTA AI · NRIE
            </p>
            <h1 className="mt-2 text-3xl font-bold tracking-tight sm:text-4xl">
              Risk Intelligence Dashboard
            </h1>
            <p className="mt-2 text-gray-400">
              {project?.title ??
                project?.name ??
                project?.project_title ??
                `Project #${projectId}`}
            </p>
          </div>

          <span className="w-fit rounded-full border border-cyan-400/20 bg-cyan-400/10 px-4 py-2 text-xs text-cyan-300">
            {risk?.modelVersion ?? 'NRIE'} · Live API
          </span>
        </header>

        <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <ScoreCard
            title="Overall Project Health"
            value={overallHealth}
            color="#22c55e"
          />
          <ScoreCard
            title="Overall Risk"
            value={overallRisk}
            color={getRiskColor(overallRisk)}
          />

          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
            <p className="text-sm text-gray-400">Risk Classification</p>
            <p
              className="mt-3 text-2xl font-semibold capitalize"
              style={{ color: getRiskColor(overallRisk) }}
            >
              {risk?.riskLevel ?? 'Not available'}
            </p>
            <p className="mt-3 text-sm text-gray-500">
              Based on the overall NRIE risk score.
            </p>
          </div>
        </section>

        <section className="mt-10">
          <div className="mb-5">
            <h2 className="text-xl font-semibold">Risk Dimensions</h2>
            <p className="mt-1 text-sm text-gray-400">
              Dimension-level scores and explanations returned by NRIE.
            </p>
          </div>

          {dimensions.length === 0 ? (
            <div className="rounded-2xl border border-white/10 p-6 text-gray-400">
              The API returned no risk dimensions for this report.
            </div>
          ) : (
            <div className="grid gap-4 lg:grid-cols-2">
              {dimensions.map((dimension) => (
                <article
                  key={dimension.id ?? dimension.label}
                  className="rounded-2xl border border-white/10 bg-white/[0.04] p-5"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className="font-semibold">
                        {dimension.label ?? dimension.id}
                      </h3>
                      <p className="mt-1 text-sm text-gray-400">
                        {dimension.severity ?? 'Unclassified'} risk
                      </p>
                    </div>
                    <span
                      className="text-2xl font-bold"
                      style={{
                        color: getRiskColor(Number(dimension.score)),
                      }}
                    >
                      {formatScore(dimension.score)}
                    </span>
                  </div>

                  <div className="mt-4 h-2 overflow-hidden rounded-full bg-white/10">
                    <div
                      className="h-full rounded-full"
                      style={{
                        width: `${Math.min(
                          100,
                          Math.max(0, Number(dimension.score) || 0)
                        )}%`,
                        backgroundColor: getRiskColor(
                          Number(dimension.score)
                        ),
                      }}
                    />
                  </div>

                  {dimension.reason && (
                    <p className="mt-4 text-sm leading-6 text-gray-300">
                      {dimension.reason}
                    </p>
                  )}

                  {Array.isArray(dimension.factors) &&
                    dimension.factors.length > 0 && (
                      <div className="mt-4 rounded-xl bg-white/[0.03] p-3">
                        <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">
                          Recommended action
                        </p>
                        <ul className="mt-2 space-y-2 text-sm text-gray-300">
                          {dimension.factors.map((factor, index) => (
                            <li key={index}>• {factor}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                </article>
              ))}
            </div>
          )}
        </section>

        <section className="mt-10 rounded-2xl border border-cyan-400/20 bg-cyan-400/[0.04] p-6">
          <h2 className="text-xl font-semibold">AI Recommendations</h2>
          {explanation ? (
            <p className="mt-3 whitespace-pre-line leading-7 text-gray-300">
              {Array.isArray(explanation)
                ? explanation.join('\n')
                : typeof explanation === 'string'
                  ? explanation
                  : JSON.stringify(explanation, null, 2)}
            </p>
          ) : (
            <p className="mt-3 text-gray-400">
              No general recommendation was returned by the API.
              Review the recommendations under each risk dimension.
            </p>
          )}
        </section>

        <section className="mt-10 rounded-2xl border border-white/10 bg-white/[0.04] p-6">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-purple-300">
              Stage 2 · Trained classifier
            </p>
            <h2 className="mt-2 text-xl font-semibold">
              Project Outcome Prediction
            </h2>
            <p className="mt-2 text-sm leading-6 text-gray-400">
              This prediction is decision support, not a guarantee of the
              project's actual outcome.
            </p>
          </div>

          {!stage2 ? (
            <p className="mt-5 rounded-xl bg-white/[0.03] p-4 text-gray-400">
              Stage 2 results are unavailable. The project may need
              additional inputs or a successful Stage 2 prediction.
            </p>
          ) : (
            <>
              <div className="mt-5 rounded-xl bg-white/[0.03] p-4">
                <p className="text-sm text-gray-400">Predicted outcome</p>
                <p className="mt-2 text-2xl font-semibold text-purple-300">
                  {prediction
                    ? String(prediction)
                    : stage2.status === 'needs_input'
                      ? 'Additional inputs required'
                      : stage2.status ?? 'Prediction available'}
                </p>

                {stage2.message && (
                  <p className="mt-2 text-sm text-gray-300">
                    {stage2.message}
                  </p>
                )}

                {stage2.missing_fields && (
                  <p className="mt-2 text-sm text-amber-300">
                    Missing inputs:{' '}
                    {Array.isArray(stage2.missing_fields)
                      ? stage2.missing_fields.join(', ')
                      : String(stage2.missing_fields)}
                  </p>
                )}
              </div>

              {probabilities &&
                typeof probabilities === 'object' && (
                  <div className="mt-5 space-y-4">
                    <h3 className="font-medium">Outcome probabilities</h3>
                    {Object.entries(probabilities).map(([name, value]) => {
                      const probability = Number(value);
                      const percent =
                        probability <= 1
                          ? probability * 100
                          : probability;

                      return (
                        <div key={name}>
                          <div className="mb-2 flex justify-between gap-4 text-sm">
                            <span className="text-gray-300">{name}</span>
                            <span className="text-gray-400">
                              {formatScore(percent)}%
                            </span>
                          </div>
                          <div className="h-2 overflow-hidden rounded-full bg-white/10">
                            <div
                              className="h-full rounded-full bg-purple-400"
                              style={{
                                width: `${Math.min(
                                  100,
                                  Math.max(0, percent || 0)
                                )}%`,
                              }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}

              {(stage2.shap_explanations || stage2.top_features) && (
                <div className="mt-6">
                  <h3 className="font-medium">Prediction factors</h3>
                  <pre className="mt-3 overflow-x-auto whitespace-pre-wrap rounded-xl bg-black/20 p-4 text-xs leading-6 text-gray-300">
                    {JSON.stringify(
                      stage2.shap_explanations ?? stage2.top_features,
                      null,
                      2
                    )}
                  </pre>
                </div>
              )}
            </>
          )}
        </section>

        {risk?.note && (
          <p className="mt-6 text-xs leading-5 text-gray-500">
            {risk.note}
          </p>
        )}
      </div>
    </main>
  );
}
