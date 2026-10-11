# Writing the README text from the repository

The README is finished text, not a skeleton. Every sentence and every command comes from the repository or from the user. This file says where to look, and what to leave out when there is no evidence.

## Where each fact comes from

| The README says | Read |
|---|---|
| what the project is and for whom | the entry point, the package or manifest description, existing docs, the issue tracker's language; ask the user when these disagree or are silent |
| the problem it solves | existing docs and the code's main flow; ask when it is not written down |
| what it does | the public surface: commands, endpoints, exported functions, UI screens, configuration keys |
| how to install | the manifest and lockfile (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, a Dockerfile, a Helm chart), the release or CI workflow |
| how to use it | the entry point, the scripts or targets (`Makefile`, `package.json` scripts, `justfile`), tests that exercise the main path, examples and fixtures |
| what it needs | the manifest's engine and dependency fields, the CI's matrix, the Dockerfile's base image |
| how it is organized | the folder layout and the module boundaries, read, not guessed |
| how to contribute, license | `CONTRIBUTING.md`, `LICENSE`, the CI; leave the section out when none exists |

## Rules for the text

- Copy a command from where it is defined; never write one from memory. If a command cannot be found, ask. If the defined command cannot work as written (a CI step that uses `npm ci` in a repository with no lockfile), tell the user, use the working equivalent, and record the substitution as an assumption in the questions.
- Take a version, a port, a flag or a path from the file that sets it. A wrong value here is a visitor's first failure. When no file sets it (the address a dev server uses), say what the tool prints instead of stating a value.
- Say what the project does in the words the project uses for itself; do not borrow marketing claims, benchmarks or comparisons the repository cannot back.
- When two sources disagree, name both to the user and ask; do not pick silently. When the project's description promises more than the code does (a stub, a feature with no effect), write what the code does today, state the gap in a status line, and ask the user before promising the rest.
- A manifest that declares a license with no `LICENSE` file is worth a question: say what the manifest declares and flag the missing file.
- Write in the language of the existing docs, or the one the user names.
- Follow the repository's own writing rules (`AGENTS.md`, contributing guide, tests that read the README): counts, dashes and file names may be restricted.

## Sections follow the project, not a template

Choose sections by what a reader of this kind of project needs; leave out the ones with nothing true to say.

- A library or SDK: a minimal working example early, the public surface, supported versions.
- A command-line tool: the command and its output first, the options that matter, install.
- A service or application: what it is for, how to run it locally, configuration, how it is deployed.
- An infrastructure or configuration repository: what it provisions, the environments, how to plan and apply, who owns what.
- A skill or plugin: what it does when asked, how it is installed, what it will not do.

## Do not write without evidence

- Feature lists the code does not implement, roadmap items nobody committed to, "coming soon".
- Badges for services the repository does not use, test or coverage numbers nobody measured.
- Performance, security or scale claims.
- Screenshots or output samples that were not produced by the project.
- Names of people, teams or companies that the repository does not already name.
- Support or contact details that are not in the repository.

Put what is missing on the list of questions for the user instead.

## The fact list

Before writing, make a two-column list: the statement or command, and the file or answer it comes from. Keep it for the verify step; each line of the finished README has a row, and a row with no source is removed or turned into a question.
