---
applyTo: "**/*.ts,**/*.tsx"
---
## TypeScript

- Use `pnpm`, not `npm`
- Node libraries are not available
- Use `lib/` for generic code, `utils/` for project utilities, `hooks/` for React hooks, and `helpers/` for page-specific helpers.
- Prefer `function theName() {` over `const theName = () =>`
- Use `import { invariant } from @epic-web/invariant` instead of another invariant library
