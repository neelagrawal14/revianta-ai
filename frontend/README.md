# Revianta AI — Frontend

Formerly NOVA. An AI-powered research intelligence platform — not a chatbot, not a
generic dashboard. This is **Part 1**: the visual foundation and application shell.

## Stack

React 19 + Vite + Tailwind CSS v4 (via `@tailwindcss/vite`) + Framer Motion +
lucide-react + Chart.js/react-chartjs-2 + React Router.

## Run it

```bash
npm install
npm run dev      # start dev server
npm run build    # production build (verified working)
npm run preview  # preview the production build
```

## What's implemented (Part 1)

- **Design system** — `src/index.css` defines all color/spacing/radius/glow/type
  tokens via Tailwind v4's `@theme` block. Fonts: Space Grotesk (display), Manrope
  (body), JetBrains Mono (data labels only).
- **FuturisticBackground** (`src/components/common/FuturisticBackground.jsx`) —
  reusable ambient environment (grid + drifting glows + vignette), respects
  `prefers-reduced-motion`.
- **NodeGraph** (`src/components/common/NodeGraph.jsx`) — the signature visual
  motif (papers/tech/datasets/patents as a connected graph), used on the landing
  hero, auth screens, and the Knowledge Graph section.
- **Reusable components** — `GlassCard`, `GlowButton`, `Badge`, `MetricCard`,
  `SectionHeader`, `SearchBar`, `FormField`, `LoadingState`, `EmptyState`,
  `ErrorState` in `src/components/common/`.
- **Layout** — `AppShell`, `Sidebar` (collapsible, tooltips, project-context aware),
  `TopBar`, `PageContainer` in `src/components/layout/`.
- **Landing page** — all 10 sections from the brief, composed in
  `src/pages/Landing/LandingPage.jsx`.
- **Auth** — `/login`, `/register` with a shared glass `AuthLayout`.
- **Dashboard** — `/dashboard`, workspace metrics + project cards, all from
  clearly-labeled mock data (`src/constants/mockData.js`).
- **Projects** — `/projects`, `/projects/new`, `/projects/:projectId` (overview
  only — sub-tabs render placeholders, see below).
- **Routing** — full route tree in `src/App.jsx`. Every sidebar link resolves to
  a real route; anything reserved for Part 2 renders `ComingSoonPage` instead of
  404ing.
- **Responsive** — sidebar collapses to an overlay on mobile, grids stack,
  typography scales down.
- **Accessibility** — semantic headings, visible focus rings (`:focus-visible`),
  `aria-label`s on icon-only buttons, `prefers-reduced-motion` support,
  `role="status"`/`role="alert"` on loading/error states.

## Mock data

Everything under `src/constants/mockData.js` is explicitly placeholder content
for previewing the UI — project health scores, metrics, pipeline stages. It is
never presented as real AI output. When the API lands, replace usages of this
file with real fetches (e.g. via `src/hooks`), not by editing the mock file.

## Reserved for Part 2 (not implemented)

Research Explorer, Technology Graph, Research Timeline, Research Gaps,
Recommendations, Analytics, Reports (workspace-level) — and, inside a project:
Papers, GitHub, Datasets, Patents, Tech Map, Timeline, Graph, Notes, Experiments,
Research Gaps, References, Risk.

All of these already have working sidebar links and routes; they currently
render `src/pages/ComingSoonPage.jsx`. Part 2 replaces that placeholder route
element with the real page per section.

## Live 3D hero (added after Part 1)

`src/components/hero/` holds the interactive 3D research-intelligence
environment behind the landing page hero, built with `three`,
`@react-three/fiber`, and `@react-three/drei`:

- `HeroVisual.jsx` — DOM-level wrapper: tracks pointer/scroll, detects WebGL
  support and `prefers-reduced-motion`, fades the canvas in on mount, and
  falls back to the static `NodeGraph` SVG when WebGL is unavailable.
- `Hero3DScene.jsx` — the `<Canvas>`: lighting rig, camera, and composition.
- `FloatingObjects.jsx` / `FloatingShape.jsx` — the organic set of glass,
  metallic, and matte shapes (spheres, rounded cubes, a low-poly icosahedron,
  rings/torus), each with independent float speed, rotation, and parallax
  depth. Hover adds a small glow + scale bump.
- `ResearchNetwork.jsx` — a small cluster of glowing nodes (project / paper /
  technology / dataset / patent) connected by thin, slowly-pulsing lines —
  the "meaning" layer, kept intentionally text-free.
- `ParticleField.jsx` — one cheap `<points>` draw call for background depth.
- `CameraRig.jsx` — damped camera parallax + a subtle scroll-driven drift.

**Performance choices:** the whole `@react-three/*` stack is lazy-loaded
(`React.lazy` in `Hero.jsx`) so it ships as its own ~240 KB (gzip) chunk that
loads after the critical text/CTAs paint, not before. Object/particle count
scales down via `useResponsiveTier` (mobile/tablet/desktop), `dpr` is capped
at 1 on mobile, and there's no shadow map — depth reads through material
shading, emissive accents, and layered lighting instead.

**Note:** the installed `three`/`@react-three/fiber` versions require React
19 in the `>=19 <19.3` range as a peer dependency, so `react`/`react-dom` are
pinned to the exact version `19.2.8` in `package.json` (previously a caret
range). If you bump React later, re-check this peer range first.

## Part 2 — Research Intelligence Experience

Adds the actual product on top of the Part 1 shell: every route below is a
real page (no more `ComingSoonPage` placeholders for anything listed here).

**New project-scoped pages** (`/projects/:projectId/...`): Papers, GitHub,
Datasets, Patents, Tech Map, Timeline, Graph, Notes, Experiments, Research
Gaps, References, Risk — plus a fully rebuilt Overview (project workspace
header, technologies, similar work, risk snapshot, knowledge-graph preview,
recommendations, gaps) and a 4-step "AI Research Initialization" wizard at
`/projects/new` with an animated analysis sequence.

**New global pages**: `/research` (unified cross-source search), `/research-gaps`,
`/recommendations`, `/analytics` (9 Chart.js visualizations), `/reports`,
`/settings`, `/tech-graph` (workspace-wide technology galaxy), `/timeline`
(field-wide research evolution).

**Signature visuals**:
- `HealthOrb` (`components/common/`) — animated project-health ring gauge.
- `ForceGraph` (`components/graph/`) — d3-force-powered interactive graph
  with zoom/pan/hover/select/search/filter + a built-in detail panel. Shared
  by Technology Map, the global Technology Galaxy, and the Knowledge Graph.
- `RiskRadarChart` + `RiskDimensionCard` + `RiskHeatmap` (`components/risk/`) —
  the seven-dimension NRIE (Revianta Risk Intelligence Engine) visualization
  on the Risk Intelligence page.
- `ResearchTimeline` (`components/timeline/`) — shared by the global and
  per-project timeline pages.
- `AnalysisSequence` (`components/common/`) — the "Revianta Intelligence
  Engine" step-by-step loading experience used in the New Project wizard.

**API service layer** (`src/services/`): `api.js` (base fetch client, reads
`VITE_API_BASE_URL`), `projectApi.js`, `researchApi.js`, `analysisApi.js`,
`riskApi.js`, `recommendationApi.js` — documented with the FastAPI routes
they expect. Not yet called anywhere; every Part 2 page still renders from
`src/constants/mock/`.

**Mock data** (`src/constants/mock/`): one file per data type
(`mockPapers`, `mockRepositories`, `mockDatasets`, `mockPatents`,
`mockTechnologies`, `mockGraph`, `mockTimeline`, `mockRiskData`,
`mockRecommendations`, `mockGaps`, `mockNotes`, `mockExperiments`,
`mockAnalytics`, `mockReports`), each exporting a `getXForProject(id)`
accessor. The flagship demo project (`smart-traffic-system`) has fully
hand-authored data throughout; the other three projects fall back to a
seeded generator (`mock/helpers.js`) so no page is ever empty. All of it is
explicitly commented as mock, never presented as real analysis output.

**Known simplifications** (documented rather than hidden):
- "Save" on a paper/repo/dataset is local UI state per page — there's no
  shared persistence layer yet, so the References page shows Revianta's
  top pick per source rather than a true cross-page "saved" list.
- Notes are in-memory (React state), seeded from mock data; refreshing
  resets anything you add.
- Report Export/Download buttons are disabled placeholders — no PDF
  generation exists, so nothing is faked.
- `getKnowledgeGraphForProject` can produce a link referencing a
  technology tag that isn't itself a node for some non-flagship projects;
  `ForceGraph`/`useForceLayout` filter these out defensively, so it fails
  safe (fewer links) rather than crashing.

## Notes for Part 2

- `src/context/AuthContext.jsx` is an in-memory placeholder (no real
  session/token handling yet) — login/register just set a mock user and
  redirect to `/dashboard`.
- lucide-react in this project's installed version has dropped brand/logo
  icons (no `Github` export) — repository-related icons use `FolderGit2`
  instead of a GitHub logo.
- Tailwind v4 is configured via the Vite plugin (no `tailwind.config.js`);
  all theme tokens live in `src/index.css`'s `@theme` block.
