---
applyTo: "**/*.tsx"
---
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
