# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

py-ABAC is an Attribute-Based Access Control (ABAC) library for Python. Its design stems from the XACML standard and the Vakt ABAC SDK. Policies are authored as JSON, parsed into `Policy` objects, stored in a pluggable backend, and evaluated by a `PDP` (Policy Decision Point) against an `AccessRequest` to return an allow/deny decision.

## Development commands

Install dependencies (editable install with all dev extras):
```bash
pip install -e .[dev]
```

Run the default (non-integration) test suite:
```bash
pytest -m "not integration"
# or
make test
```

Run a single test file / test:
```bash
pytest tests/test_policy/test_policy.py
pytest tests/test_policy/test_policy.py::TestPolicy::test_some_case -v
```

Run tests with coverage (writes `htmlcov/`):
```bash
make coverage MARK='"not integration"'
```

Lint and security scan:
```bash
pylint py_abac        # or: make lint
bandit -r py_abac      # or: make security
```

Build docs (Sphinx, from `docs/`):
```bash
cd docs && make html
```

### Integration tests (storage backends)

Backend-specific tests are marked with pytest markers (`mongo`, `sql`, `redis`, `file`, `integration`) declared in [pytest.ini](pytest.ini). They require live backends, spun up via Docker:
```bash
cd tests && docker-compose up -d && cd ..
```
Then run per-backend, using the same env vars CI uses (see [.travis.yml](.travis.yml)):
```bash
MONGODB_HOST="mongodb://mongo:password@localhost:27017" pytest -m mongo
SQL_HOST="mysql+pymysql://mysql:password@localhost/py_abac" pytest -m sql
SQL_HOST="postgresql+psycopg2cffi://postgres:password@localhost/py_abac" pytest -m sql
REDIS_HOST="localhost" REDIS_PORT="6379" pytest -m redis
pytest -m file
```
SQL tests default to an in-memory SQLite engine (`DEFAULT_SQL_HOST` in `tests/test_storage/test_sql/__init__.py`) when `SQL_HOST` is unset, so `pytest -m sql` works without Docker for SQLite-compatible cases. Mongo/Redis tests need the corresponding service reachable at their `DEFAULT_*_HOST` unless overridden.

## Architecture

### Evaluation flow

1. `AccessRequest` (`py_abac/request.py`) wraps subject/resource/action (each an id + attribute dict) and context attributes, parsed from JSON via `AccessRequest.from_json`.
2. `PDP.is_allowed(request)` (`py_abac/pdp.py`) builds an `EvaluationContext`, fetches candidate `Policy` objects from `storage.get_for_target(...)` (a cheap pre-filter by subject/resource/action id), then further filters with `policy.fits(ctx)` (full rule + target evaluation), then combines results with the configured `EvaluationAlgorithm`.
3. Three evaluation algorithms live as static/instance methods on `PDP`: `ALLOW_OVERRIDES`, `DENY_OVERRIDES` (default), `HIGHEST_PRIORITY` (deny-overrides among the highest-priority policy group).

### Policy structure (`py_abac/policy/`)

A `Policy` (`policy.py`) has `targets` (`targets.py`) and `rules` (`rules.py`):
- **Targets** are a cheap match on subject/resource/action id using Unix-style `fnmatch` globbing (e.g. `"*"`). This is the pre-filter storage backends use to narrow candidates.
- **Rules** hold, per access-control-element (`subject`/`resource`/`action`/`context`), either a dict (implicit AND of conditions) or a list of dicts (implicit OR of AND-groups). Each condition maps an attribute path (ObjectPath notation, e.g. `"$.name"`) to a condition object.

### Conditions (`py_abac/policy/conditions/`)

Conditions are organized by category: `numeric`, `string`, `collection`, `attribute` (compares two attribute paths against each other rather than a literal), `logic` (`AllOf`/`AnyOf`/`Not`, composing other conditions), `object`, `others` (`CIDR`, `Exists`, `NotExists`, `Any`). All implement `ConditionBase.is_satisfied(ctx)`.

Every condition class is paired with a marshmallow schema class. New condition types must be registered in the `type_schemas` map in `conditions/schema.py` (a `marshmallow_oneofschema.OneOfSchema`), keyed by class name — this is what lets policy JSON's `"condition": "Equals"` field resolve to the right class on load.

### Attribute resolution (`py_abac/context.py`, `py_abac/provider/`)

`EvaluationContext.get_attribute_value(ace, attribute_path)` first checks the request's own attributes (`RequestAttributeProvider`), then falls through to any custom `AttributeProvider` instances passed into `PDP(...)`, in order, stopping at the first non-None result. A call stack guards against infinite recursion if a custom provider itself triggers attribute lookups. Implement `AttributeProvider.get_attribute_value(ace, attribute_path, ctx)` to source attributes dynamically (e.g. from an external user/resource service) instead of requiring callers to pass everything in the request.

### Storage backends (`py_abac/storage/`)

All backends implement the abstract `Storage` interface (`storage/base.py`): `add`, `get`, `get_all`, `get_for_target`, `update`, `delete`. `get_for_target` is the target-based pre-filter query, implemented differently per backend (e.g. Mongo/SQL query on indexed target fields; in-memory/file scan and match with `fnmatch`).

Backends: `memory` (in-process dict, no persistence), `file` (JSON file, uses `dotty-dict`/`flatten-dict`), `mongo`, `sql` (SQLAlchemy, MySQL/Postgres/SQLite), `redis`. Mongo and SQL backends additionally implement schema/index migrations via the `Migration`/`MigrationSet`/`Migrator` classes in `storage/migration.py` (see `storage/mongo/migrations.py`, `storage/sql/migrations.py`) — each backend's `MigrationSet` tracks the last-applied migration number and runs pending migrations up in order.

Each optional backend's dependency (`pymongo`, `SQLAlchemy`, `redis`, `dotty-dict`/`flatten-dict`) is an extras_require group in `setup.py` (`mongo`, `sql`, `file`) — only installed when that backend is used.

### Adding a new condition type

1. Create the condition class (extends the relevant category base, implements `is_satisfied`) and its schema class in the appropriate `conditions/<category>/` subpackage.
2. Register both in `conditions/schema.py`'s `type_schemas` dict.
3. Add tests under `tests/test_policy/test_conditions/`.

### Adding a new storage backend

Implement `Storage` (`storage/base.py`) in a new `storage/<backend>/` package, add its dependency as a new `extras_require` group in `setup.py`, and add tests under `tests/test_storage/test_<backend>/` (plus PDP integration tests under `tests/test_pdp/`) marked with a corresponding pytest marker registered in `pytest.ini`.

## Release process

- Day-to-day PRs (bug fixes, docs, small features) target `master` directly.
- A larger body of work destined for the next version accumulates on a staging branch named `rc-vX.Y.Z` (e.g. `rc-v0.5.0`). While one is active, PRs for changes intended for that release target the `rc-vX.Y.Z` branch instead of `master`.
- When the release is ready, the `rc-vX.Y.Z` branch is merged into `master` via a single PR (see e.g. PR #13 "Rc v0.4.0", PR #10 "Rc0.2.1"), `py_abac/version.py`'s `__version__` is bumped, a new section is added to `CHANGELOG.md`, and a `vX.Y.Z` tag is cut from `master`.
- If no `rc-vX.Y.Z` branch is currently active (or the existing one is stale — check `git log origin/master..origin/rc-vX.Y.Z` for commits unique to it), treat `master` as the target instead of creating/using a stale rc branch.
