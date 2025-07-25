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
- When naming variables or functions, use names that describe the effect. For example, instead of `function handleClaimFreeTicket` (a function which opens a dialog box) use `function openClaimFreeTicketDialog`.

Use line breaks to organize code into logical groups. Instead of:

```python
if not client_secret_id:
    raise HTTPException(status.HTTP_400_BAD_REQUEST)
session_id = client_secret_id.split("_secret")[0]
```

Prefer:

```python
if not client_secret_id:
    raise HTTPException(status.HTTP_400_BAD_REQUEST)

session_id = client_secret_id.split("_secret")[0]
```

**DO NOT FORGET**: keep your responses short, dense, and without fluff. I am a senior, well-educated software engineer, and do not need long explanations.

### Agent instructions

- When running python tests, use an already open terminal and the `pytest` binary.
- If you added models, generate a migration with `just migration {add,delete,update}_model_other_description`

## Fastapi

- When throwing a `HTTPException`, do not add a `detail=` and use a named status code (`status.HTTP_400_BAD_REQUEST`)
- Do not return a `dict`, instead create a `class RouteNameResponse`

## Pytest Integration Tests

- Look to tests/factories.py to generate any required database state
  - Here's an example of how to create + persist a factory `DistributionFactory.build(domain=PYTHON_TEST_SERVER_HOST).save()`
- Add the `server` factory to each test
- Use the `faker` factory to generate emails, etc.
- Don't add obvious `assert` descriptions

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

## Python Route Tests

- Polyfactory is the [factory](tests/factories.py) library in use. `ModelNameFactory.build()` is how you generate factories.
- Use `assert_status(response)` to check the response of a client

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
* Do not fix import ordering or other formatting issues.

### Date & DateTime

* Use the `whenever` library for datetime + time instead of the stdlib date library. `Instant.now().format_common_iso()`

### Database & ORM

When accessing database records:

* SQLModel (wrapping SQLAlchemy) is used
* `Model.one(primary_key)` or `Model.get(primary_key)` should be used to retrieve a single record
* Do not manage database sessions, these are managed by a custom tool
  * Use `TheModel(...).save()` to persist a record
  * Use `TheModel.where(...).order_by(...)` to query records. `.where()` returns a SQLAlchemy select object that you can further customize the query.

When writing database models:

* Don't use `Field(...)` unless required (i.e. when specifying a JSON type for a `dict` or pydantic model using `Field(sa_type=JSONB)`). For instance, use `= None` instead of `= Field(default=None)`.
* Add enum classes close to where they are used, unless they are used across multiple classes (then put them at the top of the file)
* Use `ModelName.foreign_key()` when generating a foreign key field
* Store currency as an integer, e.g. $1 = 100.

Example:

```python
class Distribution(
    BaseModel, TimestampsMixin, SoftDeletionMixin, TypeIDMixin("dst"), table=True
):
    """Triple-quoted strings for multi-line class docstring"""

    date_field_with_comment: datetime | None = None
    "use a string under the field to add a comment about the field"

    # no need to add a comment about an obvious field; no need for line breaks if there are no field-level docstrings
    title: str = Field(unique=True)
    state: str

    optional_field: str | None = None

    # here's how relationships are constructed
    doctor_id: TypeIDType = Doctor.foreign_key()
    doctor: Doctor = Relationship()

    @computed_field
    @property
    def order_count(self) -> int:
        return self.where(Order.distribution_id == self.id).count()
```

## React Router

- You are using the latest version of React Router (v7).
- The primary export in a routes file should specify `loaderData` like `export default function RouteNamePage({ loaderData }: Route.ComponentProps)`. `loaderData` is the return value from `clientLoader`.
- Use `href("/products/:id", { id: "abc123" })` to generate a url path for a route managed by the application.
  - Look at [routes.ts](mdc:web/app/routes.ts) to determine what routes and path parameters exist.
- Use `export async function clientLoader(loaderArgs: Route.ClientLoaderArgs)` to define a `clientLoader` on a route.
- Do not define `Route.*` types, these are autogenerated and can be imported from `import type { Route } from "./+types/routeFileName"`
- If URL parameters or query string values need to be checked before rendering the page, do this in a `clientLoader` and not in a `useEffect`
- Never worry about generating types using `pnpm`
- Use [`<AllMeta />`](web/app/components/shared/AllMeta.tsx) instead of MetaFunction or individual `<meta />` tags
- Use the following pattern to reference query string values (i.e. `?theQueryStringParam=value`)

```typescript
const [searchParams, _setSearchParams] = useSearchParams();
// searchParams contains the value of all query string parameters
const queryStringValue = searchParams.get("theQueryStringParam")
```

### Loading Mock Data

Don't load mock data in the component function with `useEffect`. Instead, load data in a `clientLoader`:

```typescript

// in mock.ts
export async function getServerData(options: any) {
  // ...
}

// in web/app/routes/**/*.ts
export async function clientLoader(loaderArgs: Route.ClientLoaderArgs) {
  // no error reporting is needed, this will be handled by the `getServerData`
  // mock loading functions should return result in a `data` key
  const { data } = await getServerData({ /* ... */ })

  // the return result here is available in `loaderData`
  return data
}
```

### How to use clientLoader

- `export async function clientLoader(loaderArgs: Route.ClientLoaderArgs) {`
- Load any server data required for page load here, not in the component function.
- Use `return redirect(href("/the/url"))` to redirect users
- Use [getQueryParam](web/app/lib/utils.ts) to get query string variables
- `throw new Response` if you need to mimic a 400, 500, etc error
- `loaderArgs` and all sub-objects are all fully typed
- `loaderArgs.params.id` to get URL parameters

### Using API Data

- `~/configuration/client` re-exports all types and functions from `client/*`. Import from `~/configuration/client` instead of anything you find in the `client/` folder/package.
- For each API endpoint, there's a fully typed async function that can be used to call it. Never attempt to call an API endpoint directly.
- When using an import from `~/configuration/client`:
  - use `body:` for request params
  - always `const { data, error } = await theCall()`

## React

- You are using the latest version of React (v19)
- Do not write any backend code. Just frontend logic.
- If a complex skeleton is needed, create a component function `LoadingSkeleton` in the same file.
- Store components for each major page or workflow in `app/components/$WORKFLOW/$COMPONENT.tsx`.
  - If a single page has more than two dedicated components, create a subfolder `app/components/$WORKFLOW/$PAGE/$COMPONENT.tsx`
- Use lowercase dash separated words for file names.
- Use React 19, TypeScript, Tailwind CSS, and ShadCN components.
- Prefer function components, hooks over classes.
- Use ShadCN components in `web/app/components/ui` as your component library. If you need new components, ask for them.
  - Never edit the `web/components/ui/*.tsx` files.
  - You can find a list of components here https://ui.shadcn.com/docs/components
- Break up large components into smaller components, but keep them in the same file unless they can be generalized.
- Put any "magic" strings like API keys, hosts, etc into a "constants.ts" file.
- For React functional components with three or fewer props, always inline the prop types as an object literal directly in the function signature after the destructured parameters (e.g., `function Component({ prop1, prop2 }: { prop1: string; prop2?: number }) { ... })`. Include default values in destructuring and mark optional props with ? in the type object. Do not use separate interfaces or type aliases; keep types inline. For complex types, add inline comments if needed.
- Put the interface definition right above the related function
- Internally, store all currency values as integers and convert them to floats when rendering visually
- When building forms use React Hook Form.
- Include a two line breaks between any `useHook()` calls and any `useState()` definitions for a component.
- When using a function prop inside a `useEffect`, please use a pattern that avoids including the function in the dependency array, like the `useRef` trick.s
- Use the following pattern to reference query string values (i.e. `?theQueryStringParam=value`):

```typescript
const [searchParams, _setSearchParams] = useSearchParams();
// searchParams contains the value of all query string parameters
const queryStringValue = searchParams.get("theQueryStringParam")
```

### Mock Data

- For any backend communication, create mock responses. Use a async function to return mock data that I will swap out later for a async call to an API.
- When creating mock data, always specify it in a dedicated `web/app/mock.ts` file
- Load mock data using a react router `clientLoader`. Use the Skeleton component to present a loading state.

### React Hook Form

Follow this structure when generating a form.

```tsx

// add a mock function simulating server communication
async function descriptiveServerSendFunction(values: any) {
  const mockData = getMockReturnData(/* ... */)
  return new Promise(resolve => setTimeout(() => resolve(mockData), 500));
}

const formSchema = z.object({
  field_name: z.string(),
  // additional schema definition
})

const form = useForm<z.infer<typeof formSchema>>({
  resolver: zodResolver(formSchema),
})

async function onSubmit(values: z.infer<typeof formSchema>) {
  // ...
  await descriptiveSendFunction(values)
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

## Shell

- Assume zsh for any shell scripts. The latest version of modern utilities like ripgrep (rg), fdfind (fd), bat, httpie (http), zq (zed), jq, procs, rsync are installed and you can request I install additional utilities.

## Typescript

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

