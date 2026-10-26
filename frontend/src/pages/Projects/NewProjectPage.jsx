
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Sparkles,
  ArrowRight,
  ArrowLeft,
  Check,
  AlertCircle,
  LoaderCircle,
} from 'lucide-react';

import PageContainer from '../../components/layout/PageContainer';
import GlassCard from '../../components/common/GlassCard';
import GlowButton from '../../components/common/GlowButton';

import { projectApi } from '../../services/projectApi';
import { riskApi } from '../../services/riskApi';

const STEPS = [
  'Project Identity',
  'Project Description',
  'Project Context',
  'Run Intelligence',
];

const DOMAINS = [
  'Computer Vision',
  'NLP',
  'Robotics',
  'Healthcare AI',
  'Climate & Sustainability',
  'Fintech',
  'Other',
];

const TIMELINES = [
  '< 1 month',
  '1–3 months',
  '3–6 months',
  '6+ months',
];

const DEPLOYMENT_TARGETS = [
  'Cloud API',
  'Mobile',
  'Edge / Embedded',
  'Desktop',
  'Research pipeline (offline)',
];

const DATASET_STATUSES = [
  'Available',
  'Partially available',
  'Must build',
  'Unknown',
];

const TIMELINE_MONTHS = {
  '< 1 month': 1,
  '1–3 months': 2,
  '3–6 months': 5,
  '6+ months': 6,
};

function StepDots({ active }) {
  return (
    <div className="flex items-center gap-2">
      {STEPS.map((label, index) => (
        <div key={label} className="flex items-center gap-2">
          <div
            title={label}
            className={`flex h-7 w-7 items-center justify-center rounded-full border font-mono text-xs ${
              index < active
                ? 'border-cyan/40 bg-cyan/10 text-cyan'
                : index === active
                  ? 'border-indigo/40 bg-indigo/10 text-indigo-soft'
                  : 'border-line text-text-faint'
            }`}
          >
            {index < active ? (
              <Check size={13} />
            ) : (
              String(index + 1).padStart(2, '0')
            )}
          </div>

          {index < STEPS.length - 1 && (
            <div
              className={`h-px w-6 sm:w-10 ${
                index < active ? 'bg-cyan/40' : 'bg-line'
              }`}
            />
          )}
        </div>
      ))}
    </div>
  );
}

function Field({ label, hint, children }) {
  return (
    <div>
      <label className="mb-1.5 block text-sm text-text-dim">
        {label}
      </label>
      {children}
      {hint && (
        <p className="mt-1.5 text-xs text-text-faint">{hint}</p>
      )}
    </div>
  );
}

const inputCls =
  'h-11 w-full rounded-xl border border-line bg-white/[0.03] px-3.5 text-sm text-text placeholder:text-text-faint focus:border-indigo/50 focus:outline-none';

function getResponsePayload(response) {
  return response?.project ?? response?.data ?? response;
}

function parseTeamSize(value) {
  const match = String(value).match(/\d+/);
  return match ? Number(match[0]) : null;
}

function parseTechnologies(value) {
  return value
    .split(',')
    .map((technology) => technology.trim())
    .filter(Boolean);
}

export default function NewProjectPage() {
  const navigate = useNavigate();

  const [step, setStep] = useState(0);
  const [running, setRunning] = useState(false);
  const [analysisError, setAnalysisError] = useState('');
  const [analysisStatus, setAnalysisStatus] = useState('');

  const [form, setForm] = useState({
    name: '',
    domain: DOMAINS[0],
    description: '',
    teamSize: '1–2 people',
    timeline: TIMELINES[1],
    technologies: '',
    hardware: '',
    deploymentTarget: DEPLOYMENT_TARGETS[0],
    datasetStatus: DATASET_STATUSES[0],
    technicalDifficulty: '3',
    similarProjectAwareness: 'unknown',
    researchAvailability: 'unknown',
  });

  function update(field, value) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));

    setAnalysisError('');
  }

  function next() {
    setAnalysisError('');

    if (step === 0 && !form.name.trim()) {
      setAnalysisError('Enter a project name to continue.');
      return;
    }

    if (step === 1 && !form.description.trim()) {
      setAnalysisError('Enter a project description to continue.');
      return;
    }

    setStep((current) => Math.min(current + 1, STEPS.length - 1));
  }

  function back() {
    setAnalysisError('');
    setStep((current) => Math.max(current - 1, 0));
  }

  const canRun =
    form.name.trim().length > 0 &&
    form.description.trim().length > 0 &&
    Number.isFinite(Number(form.technicalDifficulty)) &&
    Number(form.technicalDifficulty) >= 1 &&
    Number(form.technicalDifficulty) <= 5;

  async function runRealAnalysis() {
    if (!canRun || running) return;

    setRunning(true);
    setAnalysisError('');

    let projectId;

    try {
      const technologies = parseTechnologies(form.technologies);

      // 1. Create a project through the existing backend API.
      setAnalysisStatus('Creating your project...');

      const projectResponse = await projectApi.create({
        name: form.name.trim(),
        title: form.name.trim(),
        description: form.description.trim(),
        domain: form.domain,
        technologies,
        hardware: form.hardware.trim(),
        deployment_target: form.deploymentTarget,
        dataset_status: form.datasetStatus,
      });

      const project = getResponsePayload(projectResponse);

      projectId = project?.id ?? project?.project_id;

      if (projectId == null) {
        throw new Error(
          'The project API did not return a project ID.'
        );
      }

      // 2. Run the existing AI analysis pipeline.
      setAnalysisStatus(
        'Running NRIE and Revianta AI analysis...'
      );

      await riskApi.analyze(projectId, {
        project_title: form.name.trim(),
        description: form.description.trim(),
        domain: form.domain,
        technologies_used: technologies,
        dataset_availability: form.datasetStatus,
        hardware_required: form.hardware.trim() || 'unknown',
        deployment_target: form.deploymentTarget,
        team_size: parseTeamSize(form.teamSize),
        planned_timeline_months:
          TIMELINE_MONTHS[form.timeline],
        technical_difficulty: Number(form.technicalDifficulty),
        similar_project_awareness: form.similarProjectAwareness,
        research_availability: form.researchAvailability,
      });

      // 3. Open the newly created project's real risk report.
      setAnalysisStatus('Analysis complete. Opening dashboard...');

      navigate(`/projects/${projectId}/risk`);
    } catch (error) {
      console.error('Revianta project analysis failed:', error);

      const detail =
        error?.message ||
        'An unexpected error occurred during analysis.';

      setAnalysisError(
        projectId != null
          ? `Project #${projectId} was created, but analysis failed: ${detail}`
          : `Could not create the project: ${detail}`
      );
    } finally {
      setRunning(false);
      setAnalysisStatus('');
    }
  }

  return (
    <PageContainer className="max-w-3xl">
      <p className="mono-tag text-indigo-soft">
        AI Research Initialization
      </p>

      <h1 className="mt-2 font-display text-3xl text-text">
        Start a new project
      </h1>

      <p className="mt-2 max-w-lg text-text-dim">
        Describe your research idea and run it through the connected
        Revianta AI intelligence pipeline.
      </p>

      <div className="mt-8 overflow-x-auto pb-1">
        <StepDots active={step} />
      </div>

      <GlassCard tone="strong" className="mt-6 p-6 sm:p-8">
        {running ? (
          <div className="flex flex-col items-center gap-5 py-12 text-center">
            <div className="rounded-2xl border border-cyan/20 bg-cyan/10 p-4">
              <LoaderCircle
                size={34}
                className="animate-spin text-cyan"
              />
            </div>

            <div>
              <h2 className="font-display text-xl text-text">
                Revianta AI is analyzing your project
              </h2>
              <p className="mt-3 text-sm text-text-dim">
                {analysisStatus}
              </p>
            </div>

            <p className="max-w-sm text-xs leading-5 text-text-faint">
              Please keep this page open while the backend processes
              your project.
            </p>
          </div>
        ) : (
          <>
            {step === 0 && (
              <div className="space-y-5">
                <p className="mono-tag text-text-faint">
                  Step 01 — Project Identity
                </p>

                <Field label="Project name">
                  <input
                    value={form.name}
                    onChange={(event) =>
                      update('name', event.target.value)
                    }
                    placeholder="e.g. Smart Traffic System"
                    maxLength={200}
                    className={inputCls}
                  />
                </Field>

                <Field label="Research domain">
                  <select
                    value={form.domain}
                    onChange={(event) =>
                      update('domain', event.target.value)
                    }
                    className={inputCls}
                  >
                    {DOMAINS.map((domain) => (
                      <option
                        key={domain}
                        value={domain}
                        className="bg-surface"
                      >
                        {domain}
                      </option>
                    ))}
                  </select>
                </Field>
              </div>
            )}

            {step === 1 && (
              <div className="space-y-5">
                <p className="mono-tag text-text-faint">
                  Step 02 — Project Description
                </p>

                <Field
                  label="What are you building?"
                  hint="Describe the problem, proposed solution, research objectives, and intended outcome."
                >
                  <textarea
                    rows={7}
                    value={form.description}
                    onChange={(event) =>
                      update('description', event.target.value)
                    }
                    placeholder="Describe your research idea, the problem you want to solve, your proposed approach, and expected results..."
                    maxLength={10000}
                    className="w-full resize-y rounded-xl border border-line bg-white/[0.03] px-3.5 py-3 text-sm text-text placeholder:text-text-faint focus:border-indigo/50 focus:outline-none"
                  />
                </Field>
              </div>
            )}

            {step === 2 && (
              <div className="grid gap-5 sm:grid-cols-2">
                <p className="mono-tag col-span-full text-text-faint">
                  Step 03 — Project Context
                </p>

                <Field label="Team size">
                  <input
                    value={form.teamSize}
                    onChange={(event) =>
                      update('teamSize', event.target.value)
                    }
                    placeholder="e.g. 4 people"
                    className={inputCls}
                  />
                </Field>

                <Field label="Planned timeline">
                  <select
                    value={form.timeline}
                    onChange={(event) =>
                      update('timeline', event.target.value)
                    }
                    className={inputCls}
                  >
                    {TIMELINES.map((timeline) => (
                      <option
                        key={timeline}
                        value={timeline}
                        className="bg-surface"
                      >
                        {timeline}
                      </option>
                    ))}
                  </select>
                </Field>

                <Field
                  label="Technologies"
                  hint="Separate technologies with commas."
                >
                  <input
                    value={form.technologies}
                    onChange={(event) =>
                      update('technologies', event.target.value)
                    }
                    placeholder="Python, PyTorch, OpenCV"
                    className={inputCls}
                  />
                </Field>

                <Field label="Hardware requirements">
                  <input
                    value={form.hardware}
                    onChange={(event) =>
                      update('hardware', event.target.value)
                    }
                    placeholder="e.g. NVIDIA GPU, edge device"
                    className={inputCls}
                  />
                </Field>

                <Field label="Deployment target">
                  <select
                    value={form.deploymentTarget}
                    onChange={(event) =>
                      update('deploymentTarget', event.target.value)
                    }
                    className={inputCls}
                  >
                    {DEPLOYMENT_TARGETS.map((target) => (
                      <option
                        key={target}
                        value={target}
                        className="bg-surface"
                      >
                        {target}
                      </option>
                    ))}
                  </select>
                </Field>

                <Field label="Dataset availability">
                  <select
                    value={form.datasetStatus}
                    onChange={(event) =>
                      update('datasetStatus', event.target.value)
                    }
                    className={inputCls}
                  >
                    {DATASET_STATUSES.map((status) => (
                      <option
                        key={status}
                        value={status}
                        className="bg-surface"
                      >
                        {status}
                      </option>
                    ))}
                  </select>
                </Field>

                <Field
                  label="Technical difficulty (1–5)"
                  hint="1 = straightforward, 5 = highly challenging. Select your honest estimate."
                >
                  <select
                    value={form.technicalDifficulty}
                    onChange={(event) =>
                      update(
                        'technicalDifficulty',
                        event.target.value
                      )
                    }
                    className={inputCls}
                  >
                    <option value="1" className="bg-surface">
                      1 — Very low
                    </option>
                    <option value="2" className="bg-surface">
                      2 — Low
                    </option>
                    <option value="3" className="bg-surface">
                      3 — Moderate
                    </option>
                    <option value="4" className="bg-surface">
                      4 — High
                    </option>
                    <option value="5" className="bg-surface">
                      5 — Very high
                    </option>
                  </select>
                </Field>

                <Field label="Awareness of similar projects">
                  <select
                    value={form.similarProjectAwareness}
                    onChange={(event) =>
                      update(
                        'similarProjectAwareness',
                        event.target.value
                      )
                    }
                    className={inputCls}
                  >
                    <option value="unknown" className="bg-surface">
                      Not sure yet
                    </option>
                    <option value="yes" className="bg-surface">
                      Yes, similar projects exist
                    </option>
                    <option value="no" className="bg-surface">
                      No similar projects known
                    </option>
                  </select>
                </Field>

                <Field label="Research availability">
                  <select
                    value={form.researchAvailability}
                    onChange={(event) =>
                      update(
                        'researchAvailability',
                        event.target.value
                      )
                    }
                    className={inputCls}
                  >
                    <option value="unknown" className="bg-surface">
                      Not sure yet
                    </option>
                    <option value="available" className="bg-surface">
                      Relevant research is available
                    </option>
                    <option value="limited" className="bg-surface">
                      Limited research available
                    </option>
                    <option value="none" className="bg-surface">
                      No relevant research found yet
                    </option>
                  </select>
                </Field>
              </div>
            )}

            {step === 3 && (
              <div className="flex flex-col items-center gap-5 py-6 text-center">
                <div className="rounded-2xl border border-indigo/20 bg-indigo/10 p-4">
                  <Sparkles size={30} className="text-indigo-soft" />
                </div>

                <div>
                  <p className="mono-tag text-text-faint">
                    Step 04 — Run Intelligence
                  </p>

                  <h2 className="mt-3 max-w-md font-display text-xl text-text">
                    Ready to analyze "{form.name || 'your project'}"?
                  </h2>

                  <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-text-dim">
                    Your project will be sent to the existing Revianta AI
                    backend for research intelligence and risk analysis.
                    Stage 2 will use the project inputs provided above.
                  </p>
                </div>

                <div className="w-full max-w-md rounded-xl border border-line bg-white/[0.02] p-4 text-left">
                  <p className="text-xs uppercase tracking-wider text-text-faint">
                    Project summary
                  </p>

                  <div className="mt-3 space-y-2 text-sm">
                    <p className="text-text">
                      <span className="text-text-faint">Domain: </span>
                      {form.domain}
                    </p>

                    <p className="text-text">
                      <span className="text-text-faint">Team: </span>
                      {form.teamSize}
                    </p>

                    <p className="text-text">
                      <span className="text-text-faint">Timeline: </span>
                      {form.timeline}
                    </p>

                    <p className="text-text">
                      <span className="text-text-faint">Technologies: </span>
                      {form.technologies || 'Not specified'}
                    </p>
                  </div>
                </div>

                <GlowButton
                  size="lg"
                  disabled={!canRun}
                  onClick={runRealAnalysis}
                >
                  <Sparkles size={17} />
                  Run Research Intelligence
                </GlowButton>
              </div>
            )}

            {analysisError && (
              <div
                role="alert"
                className="mt-6 flex items-start gap-3 rounded-xl border border-red-400/20 bg-red-400/5 p-4"
              >
                <AlertCircle
                  size={18}
                  className="mt-0.5 shrink-0 text-red-400"
                />
                <div>
                  <p className="text-sm font-medium text-red-300">
                    Integration error
                  </p>
                  <p className="mt-1 break-words text-sm text-text-dim">
                    {analysisError}
                  </p>
                </div>
              </div>
            )}

            {step < 3 && (
              <div className="mt-8 flex items-center justify-between border-t border-line pt-6">
                <GlowButton
                  variant="ghost"
                  size="sm"
                  onClick={back}
                  disabled={step === 0}
                >
                  <ArrowLeft size={15} />
                  Back
                </GlowButton>

                <GlowButton
                  size="sm"
                  onClick={next}
                  disabled={
                    (step === 0 && !form.name.trim()) ||
                    (step === 1 && !form.description.trim())
                  }
                >
                  Next
                  <ArrowRight size={15} />
                </GlowButton>
              </div>
            )}
          </>
        )}
      </GlassCard>
    </PageContainer>
  );
}
