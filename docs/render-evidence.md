# Render Evidence

This document describes how to collect reproducible proof that a generated artifact actually builds, packages, and renders.

## What The Agent Checks

- The project has app-like structure.
- Dependencies install.
- TypeScript lint passes.
- The app builds.
- Standalone packaging preserves the built app.
- Chrome or the user's own browser automation can capture desktop and 390px mobile full-page screenshots.
- Key interaction states are reachable when the brief needs them.

## What The Screenshots Are For

- Show that the artifact is not a blank shell.
- Show the difference between a plain route and the scaffolded route.
- Provide PR and README proof without exposing private local files.
- Help the maintainer decide which screenshots should be published.

## Common Failure Modes

- The worker returns one handcrafted HTML file when an app source project was needed.
- The app renders a generic static page with no useful state.
- The app has many controls that do not help the audience inspect, compare, export, navigate, or decide.
- The first screenshot is blank because critical content was hidden behind reveal animation.
- The direct `dist/index.html` shell is mistaken for a direct-open final artifact. Use `standalone.html` packaging instead.
- The Chrome command-line screenshot path can produce a false blank image. Prefer CDP full-page capture or the user's existing browser automation.

## Repair Policy

Repair build, render, packaging, mobile clipping, and concrete interaction defects. Do not flatten a promising visual direction to satisfy arbitrary counts.
