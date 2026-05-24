# Image Guidance

Use images only when they reinforce the artifact's purpose and visual identity.

- Prefer no external network calls when the deliverable must be offline or standalone.
- Use local assets when provided by the user.
- Use generated or placeholder imagery only when it improves the artifact.
- Every image must have useful `alt` text.
- If using external image URLs, include `referrerPolicy="no-referrer"` on `<img>` tags to reduce host referrer issues.

Common aspect ratios:

| Use Case | Aspect Ratio |
| --- | --- |
| Hero or banner | 16:9 |
| Avatar or profile | 1:1 |
| Card thumbnail | 4:3 |
| Mobile full-screen | 9:16 |
| Portrait | 3:4 |
