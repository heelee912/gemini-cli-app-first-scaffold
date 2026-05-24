---
name: build-parity-design-director
description: Use for high-quality visual web apps, product surfaces, interactive artifacts, and app-builder-style frontend work across domains.
---

# Build Parity Design Director

Use this skill when the user asks for premium frontend design, app-builder-style artifacts, audience-facing pages, product surfaces, interactive prototypes, or static exports derived from an app.

Before generating or editing the artifact, read and follow the sibling file:

`GEMINI.md`

## Defaults

- Build project-first with Vite, React, TypeScript, and Tailwind v4.
- Treat static HTML and PDF as packaging or export formats, not the normal implementation medium.
- Preserve the user's task. Do not wrap it in taste-level constraints unless the user supplied those constraints.
- Let the design worker own visual direction.
- Verify through install, lint, build, packaging, and the browser tools available in the host agent environment.

## Scaffold Command

Preferred one-shot command when Gemini CLI is installed:

```bash
python scripts/run_gemini_design_once.py out/my-artifact --name "My Artifact" --brief-file brief.md --force
```

Manual scaffold command:

```bash
python scripts/create_build_like_web_app.py out/my-artifact --name "My Artifact" --brief-file brief.md --force
```

Then run your preferred design worker in the generated artifact folder.

## Packaging Command

```bash
npm run build
python scripts/package_vite_dist_single_html.py out/my-artifact/dist out/my-artifact/standalone.html
```
