---
applyTo: "**/*.py"
---
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
