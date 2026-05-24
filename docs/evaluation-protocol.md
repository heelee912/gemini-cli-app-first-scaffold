# Evaluation Protocol

This workflow does not assign automatic design scores.

## What The Agent Verifies

- The project has app-like structure.
- Dependencies install.
- TypeScript lint passes.
- The app builds.
- Standalone packaging preserves the built app.
- Chrome can capture desktop and 390px mobile full-page screenshots.
- Key interaction states are reachable when the brief needs them.

## What The Human Judges

- Visual quality.
- Taste.
- Whether the artifact feels like a product surface rather than a page.
- Whether the result is close enough to the target benchmark.
- Whether a revision loop should continue.

## Common Failure Modes

- The worker returns one handcrafted HTML file when an app source project was needed.
- The app renders a generic static page with no useful state.
- The app has many controls that do not help the audience inspect, compare, export, navigate, or decide.
- The first screenshot is blank because critical content was hidden behind reveal animation.
- The direct `dist/index.html` shell is mistaken for a direct-open final artifact. Use `standalone.html` packaging instead.
- The Chrome command-line screenshot path produces a false blank image. Prefer CDP full-page capture.

## Repair Policy

Repair build, render, packaging, mobile clipping, and concrete interaction defects. Do not flatten a promising visual direction to satisfy arbitrary counts or metric gates.
