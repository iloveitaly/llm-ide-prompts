---
applyTo: "**/*.ts,**/*.tsx"
---
## TypeScript

- Use `pnpm`, not `npm`
- Node libraries are not available
- Use `lib/` for generic code, `utils/` for project utilities, `hooks/` for React hooks, and `helpers/` for page-specific helpers.
- Prefer `function theName() {` over `const theName = () =>`
- Use `import { invariant } from @epic-web/invariant` instead of another invariant library

Here's how frontend code is organized in `web/app/`:

- `lib/` not specific to the project. This code could be a separate package at some point.
- `utils/` project-specific code, but not specific to a particular page.
- `helpers/` page- or section-specific code that is not a component, hook, etc.
- `hooks/` react hooks.
- `configuration/` providers, library configuration, and other setup code.
- `components/` react components.
  - `ui/` reusable ShadCN UI components (buttons, forms, etc.).
  - `shared/` components shared across multiple pages.
  - create additional folders for route- or section-specific components.
