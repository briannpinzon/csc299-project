<!--
Sync Impact Report

- Version change: 1.0.0 → 1.1.0
- Defined principles (placeholders → concrete):
	- [PRINCIPLE_1_NAME] → I. Code Clarity & Simplicity
	- [PRINCIPLE_2_NAME] → II. Code Quality & Maintainability
	- [PRINCIPLE_3_NAME] → III. Testing Standards (Test-First where practical)
	- [PRINCIPLE_4_NAME] → IV. User Experience Consistency
	- [PRINCIPLE_5_NAME] → V. Observability & Release Discipline
- Added/Modified sections:
	- Development Workflow & Quality Gates: added mandatory documentation
		requirement for merges to `master`.
	- Operational Constraints (no change)
- Removed sections: none (placeholders filled)
- Templates updated:
	- `.specify/templates/plan-template.md` ✅ updated
	- `.specify/templates/tasks-template.md` ✅ updated
	- `.specify/templates/spec-template.md` ⚠ pending (review suggested)
	- `.specify/templates/commands/` ⚠ pending (directory not found)
- Follow-up TODOs:
	- TODO(RATIFICATION_DATE): Provide original ratification date for the project.
	- Manual review: `.specify/templates/spec-template.md` to confirm language aligns with local project needs.
-->

# Names2 Constitution

## Core Principles

### I. Code Clarity & Simplicity
All code MUST be written for readability first. Functions and modules MUST be small,
single-purpose, and have names that express intent. Comments are only used to
explain "why" — NOT "what". Developers MUST prefer explicit, obvious
implementations over clever or terse ones. Premature optimization is
disallowed unless justified and documented in the PR. Rationale: Clear code
reduces review time, lowers onboarding friction, and reduces long-term
maintenance cost.

### II. Code Quality & Maintainability
All changes MUST pass static analysis and linters configured for the project.
Every non-trivial change MUST include a peer review by a code owner or an
assigned reviewer. Dependencies MUST be evaluated for security, license, and
maintenance risk before acceptance. Architecture decisions MUST favor
composition and encapsulation to reduce coupling. Rationale: High-quality code
and reviews prevent regressions and make future changes safer.

### III. Testing Standards (Test-First where practical)
Tests are mandatory for all new features and bug fixes. Developers SHOULD write
tests before implementation when feasible (Test-First / TDD). Required test
levels:
- Unit tests for logic and edge cases.
- Integration tests for interactions between modules or services.
- Contract or API tests for public interfaces.
All CI pipelines MUST run the full test suite and MUST block merges on failing
tests. Rationale: Automated tests provide fast feedback and protect against
regressions.

### IV. User Experience Consistency
User-facing behavior (APIs, CLIs, GUIs, error messages) MUST follow documented
patterns for naming, error handling, and user feedback. Error messages MUST be
actionable and localized where applicable. Accessibility and keyboard
navigation considerations MUST be included for UI work. Acceptance criteria in
specs MUST include explicit user scenarios and success criteria. Rationale:
Consistent UX reduces user confusion and support overhead.

### V. Observability & Release Discipline
Systems MUST emit structured logs and key metrics for important flows. Errors
and unexpected states MUST be recorded with sufficient context to debug in
production. Releases MUST follow semantic versioning for public interfaces
(MAJOR.MINOR.PATCH) and include changelogs and migration notes for breaking
changes. Rationale: Observability and disciplined releases make incidents
resolvable and upgrades predictable.

### VI. Use Emojis in Output 
Add emojis in program output when possible. Be happy!
## Operational Constraints

The project has no enforced runtime platform locked in this constitution. Any
technology choices MUST be documented in the implementation plan and justified
against the principles above. Security, data retention, and performance
constraints SHOULD be declared per-spec: if none are declared, the plan MUST
include a short justification. Rationale: Constraints must be explicit to guide
design trade-offs.

## Development Workflow & Quality Gates

- All work MUST be tracked in a feature-specific `specs/[feature]/` folder with
	an implementation plan and tasks.
- Every PR MUST reference its spec/plan and list affected acceptance scenarios.
- CI checks required before merge: linters, unit tests, integration smoke tests,
- CI checks required before merge: linters, unit tests, integration smoke tests,
  and any project-specific contract tests.
- Complexity exceptions (architectural deviations) MUST be documented in the
	plan and approved by at least two senior reviewers.

- Documentation: User-facing documentation (README, quickstart, API docs,
  and any migration notes) MUST be created or updated in the same PR that is
  merged into the `master` branch. If immediate docs updates are impossible,
  the PR MUST include an explicit documented follow-up task with an owner and
  a deadline; the follow-up must be merged within a reasonable timeframe and
  be tracked in the corresponding spec. Exceptions require explicit approval
  in the PR and a documented plan. Rationale: Ensures users and integrators
  always have accurate guidance when code reaches `master`.

## Governance

Amendments:
- Proposals to amend the constitution MUST be documented as a spec with
	rationale and migration plan.
- Amendments require approval by a quorum of project maintainers (defined in
	repository CODEOWNERS or an agreed list) and must pass an implementation
	review where applicable.

Versioning Policy:
- Use semantic versioning for the constitution itself. Bump rules:
	- MAJOR: Backward-incompatible governance or principle removals/redefinitions.
	- MINOR: Addition of new principle(s) or material expansion of guidance.
	- PATCH: Clarifications, wording, typo fixes, non-semantic refinements.

Compliance & Review Expectations:
- The `Constitution Check` section in implementation plans MUST list which
	principles apply and how the plan meets them.
- PR reviewers MUST verify relevant principle alignment and mark any
	deviations as review comments.
- Annual reviews: The constitution SHOULD be reviewed yearly for relevance.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date
| **Last Amended**: 2025-11-21
