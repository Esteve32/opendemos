# GitHub Copilot: Repository Custom Instructions (Colibri Style)

Project scope
- Repository: Esteve32/opendemos
- Purpose: Various project demos in browsers (HTML, etc.)
- Primary languages: HTML, Python, Shell

Colibri style principles
- Clarity first: write simple, explicit code and prose; avoid cleverness that reduces readability.
- Minimal dependencies: prefer standard platform features; only use dependencies already present or clearly justified.
- Reproducible demos: make each example runnable with minimal setup (open in browser or run a single command).
- Accessible and semantic: for UI, use semantic HTML and accessible patterns (labels, ARIA where appropriate).
- Consistent formatting: respect existing configurations (.editorconfig, Prettier, ESLint, Black, isort, flake8, shfmt) if present.
- Security and privacy: never include secrets; use environment variables and placeholders.
- Documentation-first: briefly document purpose and how to run/try changes.

Authoring guidance for Copilot
- Scope changes narrowly and keep examples self-contained.
- If suggesting new examples, include a short "How to run" note in comments or README.
- Prefer clear names and small functions; avoid over-engineering.

Language-specific guidance
- HTML/CSS/JS: prefer vanilla approaches; no new frameworks unless the repo already uses them. Use semantic HTML, small modular CSS, and unobtrusive JS. Avoid network calls unless required by the demo.
- Python: prefer the standard library; if a dependency is essential, choose well-established packages. Provide a usage example or docstring. Add a --dry-run option for scripts that change files or state.
- Shell: write POSIX-compatible scripts when possible; include set -eu (and set -o pipefail for bash). Avoid destructive commands by default; offer confirmation flags.

Pull requests and code review
- Keep PRs small and focused with imperative commit messages (e.g., "Add demo for X").
- If behavior or usage changes, update README or example index accordingly.

Non-goals / guardrails
- Do not introduce heavy build systems, analytics, or external services unless already part of the repo.
- Do not break existing demos without providing a migration note.