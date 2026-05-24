# shadcn/ui Guidance

Use shadcn/ui only when it helps the artifact. Do not use it as a default house style.

If initializing shadcn, use non-interactive flags:

```bash
npx shadcn@latest init --defaults
```

Add only the components that the artifact needs:

```bash
npx shadcn add button card dialog sheet
```

Community registries can be useful for richer interaction, but they are optional and should not replace brief-specific design judgment.
