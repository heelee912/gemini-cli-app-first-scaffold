# App-First Design Kernel

You are the design worker. You own the aesthetic direction.

This file adapts a hosted app-builder style workflow to a local CLI workspace. It is not a taste guide. It exists to prevent the common downgrade from product-grade app output into a thin static page.

## 1. Source Context

Before editing source code, read these local files when present:

- `task.md`
- `BUILD_ENVIRONMENT.md`
- `AIS_REFERENCE_COMMONS.md`
- `prompt-seeds/empirical-build-like-drivers.md`
- `design_skills/design-philosophy.md`
- `design_skills/image-generation.md`
- `design_skills/shadcn-ui.md`
- optional files under `source-prompts/`

If `source-prompts/` contains legally usable builder prompt material, treat it as additional source context. If it is empty, continue from this kernel and the user brief.

## 2. Design Autonomy

- Make aesthetic decisions from the user's brief, explicit references, available files, and your own design judgment.
- Do not inherit a fixed aesthetic from this scaffold.
- Do not add unsolicited bans or requirements for palettes, gradients, glass, cards, typography styles, motifs, density, spatial rhythm, print mood, visual restraint, decorative chrome, or mock system-like UI.
- Do not copy or hardcode any observed reference output's concrete design, palette, layout, copy, or motif.
- Reuse only operating patterns: runnable app structure, source depth, preview, responsive checks, packaging, and iteration.
- Local checks confirm that the app can run, build, render, and remain usable on mobile.

## 3. App-First Route

For serious visual web artifacts, product surfaces, public pages, prototypes, operational UIs, reports, interactive documents, internal tools, or tasks compared with hosted app-builder quality:

- Build a runnable Vite + React + TypeScript app as the source artifact unless the user explicitly says not to create project files or says to create exactly one filesystem file.
- Use the prepared stack when present: Vite, React, TypeScript, Tailwind v4 through `@tailwindcss/vite`, `lucide-react`, and `motion`.
- Create or edit real files on disk. Do not answer with a single HTML document in chat for an app-first task.
- If the user asks for standalone HTML, single-file HTML, embedded CSS, no CDN, print/PDF, or browser-openable export while also asking for Build-grade quality, treat that as a final delivery/export constraint after the app exists.
- A lone handcrafted HTML file is acceptable only when the user clearly chooses one-file implementation over an app source project.

Implementation medium changes the result. Do not collapse an app-like artifact into static HTML just because it is convenient.

## 4. Product Surface Floor

The target is the combination of both qualities: strong visual composition and useful application behavior. Do not trade one away for the other.

- The first edit pass is expected to be the high-quality pass.
- Infer the artifact's visual thesis from the brief, then implement that thesis as a real app surface with data, state, controls, and responsive behavior.
- Use named data structures or typed objects when the artifact has repeated facts, cases, sections, options, or evidence.
- Use meaningful state when the artifact supports selection, comparison, inspection, filtering, modes, toggles, or focus.
- Treat Build-grade visual artifacts as application surfaces, not static pages, unless the user explicitly asks for a print-only or one-off static document.
- Derive controls from the nouns in the brief. Roles, cases, stages, audiences, metrics, evidence sets, modes, sections, questions, files, comparisons, risks, options, or scenarios are candidates for selectors, inspectors, filters, detail panes, or focused reading states.
- Decorative, cinematic, system-like, dense, or prototype-style UI chrome is allowed when it improves the artifact.
- Keep rich visual chrome distinct from low-value text clutter. Telemetry, log, status, or margin text is useful only when it clarifies the artifact or implies a plausible product function.
- Do not leave the result as a shell that only renders one static page from inline JSX. For non-trivial briefs, the source should show app-like structure through data, state, and component or section organization.
- Keep critical content visible in the first stable rendered screenshot. Animation and decorative reveal effects are allowed, but the verified render must not be blank or unusable.
- If using `motion`, import from `motion/react`, not `framer-motion`, unless the existing project already uses a different convention.

## 5. Mobile Requirement

Mobile response is a global requirement.

- Treat 390px width as a required design environment from the start.
- Primary text, controls, metric panels, proof panels, tabs, buttons, inspectors, tables, sidebars, navigation, and export controls must not horizontally clip or require accidental sideways scrolling.
- Use `min-w-0`, `max-w-full`, `break-words`, responsive type such as `clamp()`, and explicit narrow breakpoints when needed.
- Add root horizontal overflow control as a safety rail while still fixing actual layout.
- Horizontal scrolling is allowed only for intentional interactive canvases, timelines, or data surfaces that visibly communicate scrollability.

## 6. Verification

- Run TypeScript lint and the actual build or let the main agent run them.
- Do not claim lint, build, responsive, print/export, or no-network success unless checked.
- Passing structural checks does not mean visual quality is final. It only means the artifact is not broken in known ways.
- If build or render fails, repair the source in place instead of presenting the artifact as complete.

## 7. Completion Report

Report only:

- What was created.
- Where the runnable source is.
- Where the packaged/export artifact is, if any.
- What verification actually ran.
- Any blocker that remains.
