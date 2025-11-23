# CSC299 Final Project Constitution
<!--
Sync Impact Report

- Version change: unspecified -> 1.0.0
- Modified principles:
	- [PRINCIPLE_1_NAME] -> I. Code Quality
	- [PRINCIPLE_2_NAME] -> II. Test-First Development
	- [PRINCIPLE_3_NAME] -> III. Comprehensive Testing & Coverage Expectations
	- [PRINCIPLE_4_NAME] -> IV. User Experience Consistency
	- [PRINCIPLE_5_NAME] -> V. Simplicity & Maintainability
- Added sections:
	- `Additional Constraints` (security, performance, accessibility requirements)
	- `Development Workflow` (branching, CI gates, quality gates, releases)
- Removed sections: none
- Templates requiring updates:
	- `.specify/templates/tasks-template.md`: ✅ updated (made tests mandatory)
	- `.specify/templates/plan-template.md`: ✅ checked — aligned with constitution
	- `.specify/templates/spec-template.md`: ✅ checked — already mandates user scenarios & tests
	- `.specify/templates/agent-file-template.md`: ✅ checked
	- `.specify/templates/checklist-template.md`: ✅ checked
- Commands folder: ⚠ no files found at `.specify/templates/commands/` (none to check)
- Follow-up TODOs:
	- `RATIFICATION_DATE`: TODO(RATIFICATION_DATE) — set when constitution is formally ratified

-->

## Core Principles

### I. Code Quality (NON-NEGOTIABLE)
All code merged to the main development branches MUST be clear, maintainable, and reviewable. Code quality requirements include:
- **MUST** follow agreed style and linting rules enforced by CI before merge.
- **MUST** include concise, focused documentation for public APIs and complex implementation decisions.
- **MUST** avoid premature optimization; prefer clarity and correctness.

Rationale: High code quality reduces long-term maintenance cost and makes peer review effective.

### II. Test-First Development (NON-NEGOTIABLE)
Tests are the primary specification for behavior and MUST be written before implementation. Requirements:
- **MUST** write failing tests (unit/integration/contract as applicable) before feature code.
- **MUST** include acceptance tests for each priority user story in the feature spec.
- **MUST** ensure CI runs and passes the test suite before merging.

Rationale: Test-first practices produce reliable software and prevent regressions.

### III. Comprehensive Testing & Coverage Expectations
Testing must be layered and measurable:
- **Unit tests**: Fast, deterministic, and cover core logic.
- **Integration tests**: Verify interactions between components and external dependencies.
- **Contract/Acceptance tests**: Validate end-to-end user journeys and public contracts.
- **Coverage**: Projects SHOULD aim for a pragmatic coverage target (e.g., 70%+ for business logic), with critical code paths fully covered.

Rationale: Layered tests balance fast feedback and confidence for releases.

### IV. User Experience Consistency
User-facing behavior and interfaces MUST be consistent across the product surface:
- **MUST** follow agreed UI/UX patterns, naming, and error-handling conventions documented in the project style guide.
- **MUST** include user scenarios and acceptance criteria in every spec to validate UX decisions.

Rationale: Consistent UX reduces cognitive load for users and support costs.

### V. Simplicity & Maintainability
Designs and implementations MUST prefer the simplest solution that meets requirements:
- **MUST** justify complexity in PR descriptions if a simpler approach was considered and rejected.
- **SHOULD** decompose large features into independently testable user stories.

Rationale: Simpler systems are easier to test, secure, and evolve.

## Additional Constraints

- **Technology stack**: The project SHOULD document primary languages and runtimes in each `plan.md`. If unspecified, default to the language used in the repository.
- **Security**: Security reviews are REQUIRED for features handling PII or authentication. Secrets MUST never be committed to source control.
- **Performance**: Performance goals MUST be set in `plan.md` when performance is a requirement. Benchmarks and acceptable p95/p99 targets MUST be defined.
- **Accessibility**: User-facing interfaces MUST meet common accessibility guidelines (e.g., keyboard navigation, readable contrast) where applicable.

## Development Workflow

- **Branching**: Use short-lived feature branches named `[ID]-short-description`. Merge via pull requests into `main`/`master` after approvals.
- **Code review**: All PRs **MUST** have at least one approving reviewer (two for high-impact changes). Reviews MUST verify tests, style, and rationale for complexity.
- **CI gates**: PRs **MUST** pass automated linters, unit tests, integration tests (as applicable), and a constitution compliance checklist before merging.
- **Quality gates**: Critical changes (security, data model, public APIs) **MUST** include a migration plan and automated regression tests.
- **Releases & versioning**: Use semantic versioning for public artifacts. Breaking changes **MUST** be communicated and follow the deprecation schedule outlined in `plan.md`.

## Governance

This Constitution is the authoritative set of engineering principles for the repository. Key governance rules:

- **Amendments**: Propose an amendment via a PR that updates this file and includes a migration/impact plan. Amendments **MUST** include a rationale and tests (if they affect CI gates).
- **Approval**: Amendments require approval by at least two maintainers or a majority of designated approvers listed in the project metadata. Significant governance changes (removing or redefining principles) are a MAJOR version bump.
- **Versioning policy**:
	- MAJOR: Backward-incompatible governance or principle removals/rewrites.
	- MINOR: Adding a new principle or materially expanding guidance.
	- PATCH: Clarifications, typos, and non-substantive wording changes.
- **Compliance reviews**: Periodic compliance checks (quarterly or before major releases) SHOULD be run to ensure PRs and plans follow this Constitution.
- **Enforcement**: CI checks and PR templates SHOULD include a constitution checklist that reviewers use to verify compliance.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date unknown | **Last Amended**: 2025-11-23

