
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
