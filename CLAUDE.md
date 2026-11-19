# Python Base - Template Project

Starter Python project pre-configured with uv, ruff, ty, and pre-commit.

## Quick Reference

```bash
make install        # Create venv + install deps (including dev)
make test           # Run pytest
make lint           # Format + lint + type-check (ruff, shfmt, toml-sort, ty)
make type-check     # ty check only
make pre-commit-run # Run all pre-commit hooks
make clean          # Remove .venv and caches
make rename NEW=x   # Rename package from python_base to x
```

## Project Layout

- `src/python_base/` — Main package (use `make rename` to change)
- `tests/` — Pytest test files
- `scripts/` — Standalone scripts

## Tooling

- **Package manager**: uv (not pip/poetry)
- **Linter/formatter**: ruff (line-length 120, target py310)
- **Type checker**: ty
- **Tests**: pytest (testpaths=tests, pythonpath=src)
- **Pre-commit**: ruff-format, ruff lint, shfmt, toml-sort

## Agent Team

Agent definitions live in `.claude/agents/` (orchestrator, implementer, reviewer). When asked to "pick up issue(s)" or "start polling for issues", follow the orchestrator workflow directly in the main conversation — do not spawn it as a sub-agent.

## Conventions

- Run `make lint` before committing — pre-commit hooks enforce this
- All source goes under `src/python_base/`; tests mirror the source structure in `tests/`
- Python >=3.10 required
- Keep this file updated as the project evolves — new deps, conventions, or structural changes should be reflected here

## Coding Standards

- Functional core, imperative shell — FP patterns internally, straightforward public APIs
- Code duplication is often better than the wrong abstraction
- Errors-as-types / errors-as-return-values over try-except; nested try-except is prohibited
- Composition over inheritance
- Early returns and sensible defaults over if-else
- Prefer match-case over if-elif-else
- Liberal use of asserts to affirm expected state
- Global import statements only
- Modern Python 3.10+ type annotations (`list[int]` not `List[int]`)
- Prefer Literals over string enumerations
- Products are `@dataclass` (preferably frozen), sums are `|`, eliminate with `match`
- Protocols and ABCs for decoupling and type lambdas
- Docstrings with argument types, return types, and exceptions; include tensor shapes if applicable
- Liberal logging for observability; never use f-strings in log calls — use structured logging or logger formatting
- Be judicious with comments — skip the obvious, preserve the complex
