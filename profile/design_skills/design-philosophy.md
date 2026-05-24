# Design Philosophy

Every interface should be distinctive, polished, and deliberate. The design worker owns the visual direction.

## Core Principles

- Visual richness is allowed. Decorative, cinematic, technical, system-like, dense, minimal, editorial, playful, glassy, brutalist, dark, light, colorful, or restrained directions are all valid when they serve the brief.
- Do not confuse decoration with text clutter. UI chrome, motifs, panels, rails, badges, diagrams, and future-feature affordances can enrich the screen. Meaningless telemetry, log, or status text walls usually weaken the screen. Use such text only when it provides useful context, supports the concept, or implies a plausible product function.
- Create rhythm through variation in spacing, scale, density, typography, motion, and component shape.
- Decide the mood from the user brief before writing CSS. Do not default to a house style.
- Use animation when it reinforces hierarchy, state, narrative, or perceived product quality.
- Mock controls and future-feature UI can be used when they make the artifact feel like a real product surface.

## Typography

Typography is a major design lever. Select type treatment to match the artifact's mood and audience. System fonts, local CSS stacks, imported fonts, mono accents, expressive display faces, or quiet editorial typography are all valid if allowed by the brief and environment.

## Styling

- Tailwind CSS utilities are available and useful for speed and consistency.
- Custom CSS, CSS variables, SVG, canvas, CSS-only motifs, local component styles, and inline styles are allowed when they improve the result.
- Prefer functional React components and hooks for new React work.

## Responsive Design

- Design the full responsive range, including narrow 390px screens.
- Use comfortable touch targets on mobile.
- Use structural sidebars, bento expansions, dense canvases, or data surfaces on larger screens when they serve the artifact.
- Prefer fluid sizing and container-aware calculations.
