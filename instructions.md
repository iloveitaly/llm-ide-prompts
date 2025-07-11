Coding instructions for all programming languages:

- If no language is specified, assume the latest version of python.
- If tokens or other secrets are needed, pull them from an environment variable
- Prefer early returns over nested if statements.
- Prefer `continue` within a loop vs nested if statements.
- Prefer smaller functions over larger functions. Break up logic into smaller chunks with well-named functions.
- Only add comments if the code is not self-explanatory. Do not add obvious code comments.
- Do not remove existing comments.
- When I ask you to write code, prioritize simplicity and legibility over covering all edge cases, handling all errors, etc.
- When a particular need can be met with a mature, reasonably adopted and maintained package, I would prefer to use that package rather than engineering my own solution.
- Never add error handling to recover gracefully from an error without being asked to do so. Fail hard and early with assertions and allowing exceptions to propagate whenever possible

**DO NOT FORGET**: keep your responses short, dense, and without fluff. I am a senior, well-educated software engineer, and do not need long explanations.

### Agent instructions

- When running python tests, use an already open terminal and the `pytest` binary.
- If you added models, generate a migration with `just migration {add,delete,update}_model_other_description`

## Python

When writing Python:

* Assume the latest python, version 3.13.
* Prefer Pathlib methods (including read and write methods, like `read_text`) over `os.path`, `open`, `write`, etc.
* Prefer modern typing: `list[str]` over `List[str]`, `dict[str, int]` over `Dict[str, int]`, etc.
* Use Pydantic models over dataclass or a typed dict.
* Use SQLAlchemy for generating any SQL queries.
* Use `click` for command line argument parsing.
* Use `log.info("the message", the_variable=the_variable)` instead of `log.info("The message: %s", the_variable)` or `print` for logging. This object can be found at `from app import log`.
  * Log messages should be lowercase with no leading or trailing whitespace.
  * No variable interpolation in log messages.
  * Do not coerce database IDs or dates to strings
* Do not worry about import ordering or other formatting issues.

### Date & DateTime

* Use the `whenever` library for datetime + time instead of the stdlib date library. `Instant.now().format_common_iso()`

### Database & ORM

When accessing database records:

* SQLModel (wrapping SQLAlchemy) is used
* Do not manage database sessions, these are managed by a custom tool
  * Use `TheModel(...).save()` to persist a record
  * Use `TheModel.where(...).order_by(...)` to query records. `.where()` returns a SQLAlchemy select object that you can further customize the query.

When writing database models:

* Don't use `Field(...)` unless required (i.e. when specifying a JSON type for a `dict` or pydantic model using `Field(sa_type=JSONB)`). For instance, use `= None` instead of `= Field(default=None)`.
* Add enum classes close to where they are used, unless they are used across multiple classes (then put them at the top of the file)
* Use single double-quote docstrings (a string below the field definition) instead of comments to describe a field's purpose.
* Use `ModelName.foreign_key()` when generating a foreign key field

## Python App

* Files within `app/commands/` should have:
  * Are not designed for CLI execution, but instead are interactor-style internal commands.
  * Should not be used on the queuing system
  * A `perform` function that is the main entry point for the command.
  * Look at existing commands for examples of how to structure the command.
  * Use `TypeIDType` for any parameters that are IDs of models.
* Files within `app/jobs/` should have:
  * Are designed for use on the queuing system.
  * A `perform` function that is the main entry point for the job.
  * Look at existing jobs for examples of how to structure the job.
  * Use `TypeIDType | str` for any parameters that are IDs of models.
* When referencing a command, use the full-qualified name, e.g. `app.commands.transcript_deletion.perform`.
* When queuing a job or `perform`ing it in a test, use the full-qualified name, e.g. `app.jobs.transcript_deletion.perform`.

## Pytest Integration Tests

- Look to tests/factories.py to generate any required database state
  - Here's an example of how to create + persist a factory `DistributionFactory.build(domain=PYTHON_TEST_SERVER_HOST).save()`
- Add the `server` factory to each test
- Use the `faker` factory to generate emails, etc.

## Fastapi

- When generating a HTTPException, do not add a `detail=` and use a named status code (`status.HTTP_400_BAD_REQUEST`)

## React

- Do not write any backend code. Just frontend logic.
- For any backend requirements, create mock responses. Use a function to return mock data so I can easily swap it out later.
- When creating mock data, always specify it in a dedicated `mock.ts` file
- Load mock data using a react router `clientLoader`. Use the Skeleton component to present a loading state.
- If a complex skeleton is needed, create a component function `LoadingSkeleton` in the same file.
- Store components for each major page or workflow in `src/components/$WORKFLOW_OR_PAGE_NAME`.
- Use lowercase dash separated words for file names.
- Use React 19, TypeScript, Tailwind CSS, and ShadCN components.
- Prefer function components, hooks over classes.
- Break up large components into smaller components, but keep them in the same file unless they can be generalized.
- Put any "magic" strings like API keys, hosts, etc into a "constants.ts" file.
- Only use a separate interface for component props if there are more than 4 props.
  - Put the interface definition right above the related function
- Internally, store all currency values as integers and convert them to floats when rendering visually
- Never edit (or add) `components/ui/*.tsx` files
- When building forms use React Hook Form.
- Include a two line breaks between any `useHook()` calls and any `useState()` definitions for a component.
- Use `href("/products/:id", { id: "abc123" })` to generate a url path for a route managed by the application.
  - Look at @routes.ts to determine what routes and path parameters exist.

### React Hook Form

Follow this structure when generating a form.

```tsx
const formSchema = z.object({
  field_name: z.string(),
  // additional schema definition
})

const form = useForm<z.infer<typeof formSchema>>({
  resolver: zodResolver(formSchema),
})

async function onSubmit(values: z.infer<typeof formSchema>) {
  // ...
}

return (
  <Form {...form}>
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* form fields */}
    </form>
  </Form>
)
```

## React Router

- The primary export in a routes file should specify `loaderData` like `export default function RouteNamePage({ loaderData }: Route.ComponentProps)`. `loaderData` is the return value from `clientLoader`.
- When using an import from `~/configuration/client` (1) use `body:` for request params and (2) always `const { data, error } = await theCall()` (3) add `invariant(data, "error loading $xyz")`
- Use `export async function clientLoader(loaderArgs: Route.ClientLoaderArgs)` to define a clientLoader on a route.
  - Use `loaderArgs.params.$THE_KEY` to use a query string parameter.
- Do not define `Route.*` types, these are autogenerated and can be imported from `import type { Route } from "./+types/routeFileName"`
- Each non-layout route should define a meta function:

```typescript
export const meta: MetaFunction = () => {
  return [
    { title: "Page Title" },
    {
      name: "description",
      content: "Page Description",
    },
  ]
}
```

### Using API Data

* `~/configuration/client` re-exports all types and functions from `client/*`. Import from `~/configuration/client` instead of anything you find in the `client/` folder/package.
* For each API endpoint, there's a fully typed async function that can be used to call it. Never attempt to call an API endpoint directly.

## React Router Client Loader

Do this in a `clientLoader` and use `loaderData` to render the component. DO NOT create mock data, new interfaces, or mock data loader functions. Instead, assume `loaderData` has all of the data you need to render the component.

## Shell

- Assume zsh for any shell scripts. The latest version of modern utilities like ripgrep (rg), fdfind (fd), bat, httpie (http), zq (zed), jq, procs, rsync are installed and you can request I install additional utilities.

## Typescript

- Use `pnpm`, not `npm`
- Node libraries are not available
- Use `lib/` for generic code, `utils/` for project utilities, `hooks/` for React hooks, and `helpers/` for page-specific helpers.
- Prefer `function theName() {` over `const theName = () =>`
- Use `import { invariant } from @epic-web/invariant` instead of another invariant library

## Typescript Docstring

Add a file-level docstring with a simple description of what this file does.

## Secrets

Here's how environment variables are managed in this application:

- `.envrc` entry point to load the correct env stack. Should not contain secrets and should be simple some shell logic and direnv stdlib calls.
- `.env` common configuration for all systems. No secrets. No dotenv/custom scripts. Just `export`s to modify core configuration settings like `export TZ=UTC`.
- `.env.local` overrides across all environments (dev and test). Useful for things like 1Password service account token and database hosts which mutate the logic followed in `.env.shared`. Not committed to source control.
- `.env.shared` This contains the bulk of your system configuration. Shared across test, CI, dev, etc but not production.
- `.env.shared.local` Override `.env.shared` configuration locally. Not committed to source.
- `.env.dev.local` configuration overrides for non-test environments. `PYTHONBREAKPOINT`, `LOG_LEVEL`, etc. Most of your environment changes end up happening here.
- `.env.test` test-only environment variables (`PYTHON_ENV=test`). This file should generally be short.
- `.env.production.{backend,frontend}` for most medium-sized projects you'll have separate frontend and backend systems (even if your frontend is SPA, which I'm a fan of). These two files enable you to document the variables required to build (in the case of a SPA frontend) or run (in the case of a python backend) your system in production.
- `*.local` files have a `-example` variant which is committed to version control. These document helpful environment variables for local development.
- When writing TypeScript/JavaScript/React, use `requireEnv("THE_ENV_VAR_NAME")` to read an environment variable. `import {requireEnv} from '~/utils/environment'`

