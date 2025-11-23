```markdown
# Feature Specification: Personal PKMS + Task Manager + AI Agents

**Feature Branch**: `001-pkms-task-agent`  
**Created**: 2025-11-23  
**Status**: Draft  
**Input**: User description: "Develop a software that includes a personal knowledge management system (PKMS), personal task management system, and includes the use of AI agents to possibly summarize or do something else with the input given from the user. Must be written in Python and run on Windows, macOS, and Linux. Should also use JSON files to save tasks and notes."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Capture & Retrieve Notes (Priority: P1)

As a knowledge worker, I want to create, tag, and search notes so I can capture and later retrieve information quickly.

**Why this priority**: Core PKMS capability — captures the primary user value (store and retrieve knowledge).

**Independent Test**: Create a note with title/body/tags; search by keyword and tag; verify the expected note is returned.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** the user creates a note with title "Meeting" and body "Agenda: X" and tag "work", **Then** the note is persisted to JSON and retrievable by search for "Meeting", "Agenda", or tag "work".
2. **Given** multiple notes exist, **When** the user searches with a tag filter and keyword, **Then** only matching notes are returned sorted by relevance or newest.

---

### User Story 2 - Task Management & Reminders (Priority: P1)

As a user managing personal tasks, I want to create tasks, mark them complete, set optional due dates, and list tasks by status so I can organize work.

**Why this priority**: Task management is another core product pillar; must be independently testable.

**Independent Test**: Create tasks, set due date, toggle complete flag, and query active/overdue tasks.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** the user creates a task "Finish report" with due date tomorrow, **Then** task is saved to JSON and appears in the "Active" list and in "Due Soon" when appropriate.
2. **Given** a task is marked complete, **When** the user lists active tasks, **Then** completed task is excluded unless the user requests completed tasks.

---

### User Story 3 - AI Summarization & Assistants (Priority: P2)

As a user with long notes or meeting transcripts, I want an AI agent to summarize content and suggest task candidates so I can act quickly on captured information.

**Why this priority**: Adds significant productivity value while being safely decoupled from core PKMS and task store.

**Independent Test**: Provide a sample long note, request "Summarize"; verify generated summary is stored as a note draft and suggested tasks are produced.

**Acceptance Scenarios**:

1. **Given** a note with >500 words, **When** the user requests "Summarize", **Then** the agent produces a concise summary (1–3 sentences) saved as a new note and suggests 0..N task candidates.
2. **Given** the user accepts a suggested task, **When** they confirm, **Then** the task is created in the task store and persisted to JSON.

---

### Edge Cases

- What happens when JSON storage is corrupted? App MUST surface a clear recovery flow (restore from backup or manual fix).  
- How does the system behave offline? Core create/read operations MUST work offline using local JSON files; AI features may show offline notice and queue requests.  
- Very large notes (>5MB): The system SHOULD chunk or reject with guidance; AI summarization may require truncation with an explicit warning.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The application MUST allow creating, reading, updating, and deleting Notes with fields: id, title, body, tags, created_at, updated_at.
- **FR-002**: The application MUST allow creating, reading, updating, and deleting Tasks with fields: id, title, description, due_date (optional), status (todo/in-progress/done), created_at, updated_at.
- **FR-003**: The application MUST persist Notes and Tasks to local JSON files (`notes.json`, `tasks.json`) in a configurable user data directory.
- **FR-004**: The application MUST provide search across notes by keyword, title, and tags and support basic filters (date range, tag, notebook).
- **FR-005**: The application MUST expose an action to run an AI agent on a selected note that returns a summary and optional task suggestions.
- **FR-006**: The system MUST provide a simple CLI and/or minimal GUI entrypoint to create and list notes/tasks (the initial MVP MAY be CLI-first but must not prevent future GUI additions).
- **FR-007**: The application MUST run on Windows, macOS, and Linux using Python 3.10+ (packaging instructions and OS-specific paths documented in `plan.md`).
- **FR-008**: The application MUST provide export/import for JSON backups and a mechanism to recover from malformed JSON (backup restore or manual repair steps).
- **FR-009**: Tasks created from agent suggestions MUST be editable and attributable (source: agent suggestion metadata).
- **FR-010**: The application MUST include a configurable data retention option and document the default retention (assumption: indefinite unless user purges).
- **FR-011**: The application MUST run core operations (create/read/list) locally without network connectivity; AI features should degrade gracefully.
- **FR-012**: The application MUST include automated tests covering unit, integration, and acceptance flows as defined by each user story.

### Key Entities

- **Note**: id (string/uuid), title (string), body (string), tags (list[string]), created_at (ISO8601), updated_at (ISO8601), source (manual|agent).
- **Task**: id (string/uuid), title (string), description (string), due_date (ISO8601|null), status (enum), created_at (ISO8601), updated_at (ISO8601), source (manual|agent).
- **AgentResult**: id, note_id (optional), summary (string), suggestions (list of candidate tasks), confidence (optional float), created_at.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create, persist, and retrieve a new Note or Task within 5 seconds on a typical desktop machine.
- **SC-002**: Search returns relevant results for keyword queries with an accuracy (manual spot-check) that meets expectations for relevance in 90% of tested cases for a sample dataset of 100 notes.
- **SC-003**: AI-assisted summarization produces concise summaries that human evaluators rate as "useful" or better in at least 70% of trials on a 20-sample set (evaluation process to be defined in plan).
- **SC-004**: Offline core operations (create/read/list) succeed on Windows/macOS/Linux without network connectivity; AI actions produce a clear offline message instead of failing silently.
- **SC-005**: Automated tests for P1 flows pass in CI on pushes and PRs (unit + integration smoke tests).

## Assumptions

- The application will target Python 3.10+ and use cross-platform libraries only (no platform-locked dependencies).  
- AI capabilities may use external services or local models depending on user configuration — the spec focuses on behavior, not implementation details.  
- JSON files are the canonical local storage format; if a user configures an external store later, migration tooling will be provided.

## Non-Goals (Out of scope for initial MVP)

- Multi-user sync or real-time collaborative editing.  
- Full GUI experience (desktop GUI is optional for MVP; CLI-first is acceptable).  
- Advanced AI pipelines or fine-tuning; the MVP uses a summarization/assistant interface only.

## Next Steps

1. Create `plan.md` that defines packaging, test matrix (OSes + Python versions), and CI configuration.  
2. Define minimal CLI commands and file-layout in `plan.md` and implement foundational tasks: project layout, JSON storage module, test harness.  
3. Write tests for P1 flows and verify failure-to-pass cycle (test-first).

---

*Spec ready for planning.*

``` 