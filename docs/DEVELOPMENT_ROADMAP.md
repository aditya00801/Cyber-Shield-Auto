# CyberShield-Auto Development Roadmap

## 1. Document information

| Field                   | Details                                 |
| ----------------------- | --------------------------------------- |
| Project                 | CyberShield-Auto                        |
| Document                | Development roadmap                     |
| Version                 | 1.0                                     |
| Status                  | Draft, pending review                   |
| Initial platform        | Windows                                 |
| Primary language        | Python                                  |
| Architecture            | Modular application                     |
| Initial deployment      | Single authorized Windows computer      |
| Development environment | Antigravity IDE and integrated terminal |

## 2. Purpose

This roadmap defines the planned development sequence for CyberShield-Auto, from repository preparation through implementation, testing, security validation, and release.

Each phase identifies its objective, prerequisites, tasks, expected deliverables, tests, acceptance criteria, and completion conditions.

The roadmap is intended to guide implementation one phase at a time. Work should not advance simply because the source files exist. Each phase must meet its acceptance criteria before dependent work begins.

## 3. Project goals

CyberShield-Auto aims to build a defensive security application that can:

* Collect supported security events.
* Validate and normalize event data.
* Detect suspicious activity using documented rules.
* Evaluate network intrusion detection methods using CICIDS2017.
* Investigate incidents and correlate related evidence.
* Assess threat severity and confidence.
* Evaluate proposed actions through an independent policy engine.
* Execute a limited set of authorized defensive actions.
* Verify response outcomes.
* Maintain incident history and audit records.
* Provide alerts and a monitoring dashboard.
* Use AI to assist with evidence-based investigation when configured.

These are planned capabilities. Their implementation status must be established through code inspection and testing.

## 4. Development principles

### 4.1 Documentation before implementation

Review the requirements and design documents before implementing a new component.

Update documentation when a technical decision changes the intended behavior.

### 4.2 One phase at a time

Complete the current phase's tasks and tests before starting dependent work.

If a phase exposes a design problem, resolve it before building additional components on top of it.

### 4.3 Security before autonomy

Begin with detection-only operation and simulated responses.

Do not enable real system-changing actions until the policy engine, target validation, permissions, failure handling, audit logging, and verification procedures have passed their tests.

### 4.4 AI remains advisory

AI may summarize evidence or explain a finding. It must not execute arbitrary commands, authorize its own recommendations, or bypass response policies.

### 4.5 Test continuously

Every meaningful change should have corresponding tests. Run relevant regression tests after changes to shared models, interfaces, or security-sensitive components.

### 4.6 Track verified progress

Update a phase's status only after checking the implementation and required tests.

A successful build, a generated file, or a passing isolated test does not prove that the complete feature works.

### 4.7 Use milestone-based Git commits

Commit coherent, tested changes at meaningful milestones.

Before committing, review the changed files, inspect the diff, and run the appropriate tests. Never commit secrets, local credentials, virtual environments, or unintended dataset files.

## 5. Phase summary

| Phase | Name                                          | Main deliverable                                         | Dependency                  |
| ----- | --------------------------------------------- | -------------------------------------------------------- | --------------------------- |
| 0     | Repository and documentation foundation       | Reviewed project documentation and development standards | Existing repository         |
| 1     | Python environment and application foundation | Reproducible environment and application configuration   | Phase 0                     |
| 2     | Event schemas and validation                  | Validated event models                                   | Phase 1                     |
| 3     | Event collection                              | Supported event-source adapters                          | Phase 2                     |
| 4     | Rule-based threat detection                   | Tested detection engine                                  | Phase 2                     |
| 5     | Network intrusion detection                   | Reproducible CICIDS2017 evaluation                       | Phase 1                     |
| 6     | Investigation and correlation                 | Evidence-based investigation results                     | Phases 3 and 4              |
| 7     | Risk assessment                               | Structured severity and confidence decisions             | Phase 6                     |
| 8     | Response policy engine                        | Tested authorization decisions                           | Phases 1, 2, and 7          |
| 9     | Controlled response executor                  | Restricted, testable response actions                    | Phase 8                     |
| 10    | Response verification                         | Verified action outcomes                                 | Phase 9                     |
| 11    | Incident storage and audit                    | Persistent incident and audit records                    | Phases 2, 6, 7, and 8       |
| 12    | FastAPI backend                               | Validated API for supported operations                   | Relevant service interfaces |
| 13    | Dashboard and alerting                        | Incident monitoring interface                            | Phases 11 and 12            |
| 14    | AI-assisted investigation                     | Optional evidence-grounded explanations                  | Phase 6                     |
| 15    | End-to-end integration                        | Integrated application workflow                          | Required core phases        |
| 16    | Security and reliability hardening            | Verified security controls and failure behavior          | Phases 8 to 15              |
| 17    | Packaging and deployment                      | Reproducible installation and operating instructions     | Phase 16                    |
| 18    | Release validation                            | Acceptance evidence and release decision                 | Phase 17                    |

The sequence may be adjusted when repository inspection identifies existing, tested components. Existing work should be reused when it meets the documented requirements.

Phases 4 and 5 can progress independently after the application foundation is ready. Their results should remain separate because network dataset evaluation and live Windows endpoint monitoring test different capabilities.

## 6. Phase 0: Repository and documentation foundation

**Status:** In progress until the existing documents have been reviewed and the phase acceptance criteria are met.

### Objective

Establish a consistent source of truth for project scope, requirements, architecture, security controls, and development procedures.

### Prerequisites

* The CyberShield-Auto repository exists.
* The current documentation files are available for review.

### Tasks

1. Inspect the repository structure and current Git branch.
2. Review `README.md`.
3. Review `docs/PROJECT_OVERVIEW.md`.
4. Review `docs/PROJECT_REQUIREMENTS.md`.
5. Review `docs/SYSTEM_ARCHITECTURE.MD`.
6. Review `docs/THREAT_MODEL.md`.
7. Review `docs/THREAT_DETECTION_ENGINE.md`.
8. Review `docs/AUTOMATED_RESPONSE_POLICY.md`.
9. Review `docs/AI_AGENT_DESIGN.md`.
10. Review `docs/ALERTING_AND_MONITORING.md`.
11. Review `docs/DATA_STORAGE_AND_PRIVACY.md`.
12. Review `docs/API_SPECIFICATION.md`.
13. Review `docs/TESTING_STRATEGY.md`.
14. Review `docs/DATASET.md`.
15. Review `docs/ARCHITECTURAL_DECISION_LOG.md`.
16. Review `docs/DEPLOYMENT_GUIDE.md`.
17. Review the existing development roadmap.
18. Resolve conflicting file references and inconsistent terminology.
19. Identify requirements that lack measurable acceptance criteria.
20. Record important unresolved decisions.

### Expected deliverables

* Consistent project documentation.
* A reviewed requirements specification.
* A reviewed system architecture.
* A threat model and response-policy design.
* A detailed development roadmap.
* A list of unresolved decisions.

### Validation

* Confirm all referenced files exist.
* Check Markdown formatting.
* Check for duplicate or contradictory requirements.
* Confirm the distinction between planned, implemented, and tested features.
* Confirm CICIDS2017 is described as a network intrusion detection dataset.
* Confirm the documented response safeguards agree across relevant documents.

### Acceptance criteria

Phase 0 is complete when the required documents have been reviewed, critical contradictions have been resolved or explicitly recorded, and the implementation sequence is agreed upon.

### Git milestone

Create a documentation milestone commit after reviewing the staged diff and confirming that no unrelated changes or secrets are included.

## 7. Phase 1: Python environment and application foundation

### Objective

Create a reproducible development environment and a minimal application foundation.

### Prerequisites

Phase 0 must be complete.

### Tasks

1. Inspect the existing Python project structure.
2. Confirm the supported Python version.
3. Review `pyproject.toml` and dependency management.
4. Configure a project virtual environment.
5. Confirm that dependencies install reproducibly.
6. Establish the application package structure.
7. Add validated configuration loading.
8. Add structured application logging.
9. Define a consistent exception-handling approach.
10. Add basic application startup and shutdown behavior.
11. Configure automated test discovery.
12. Confirm `.gitignore` excludes local environments, secrets, caches, and generated artifacts.
13. Add or review `.env.example` if environment-based configuration is required.
14. Document installation and test commands.

### Expected deliverables

* Reproducible Python environment.
* Application package foundation.
* Validated configuration.
* Logging and error-handling conventions.
* Working automated test setup.

### Tests

* Application imports successfully.
* Invalid configuration produces a clear error.
* Missing optional configuration is handled as documented.
* Secrets are not printed in logs.
* Tests run from the documented commands.
* Installation does not depend on undeclared local packages.

### Acceptance criteria

A clean environment can install the declared dependencies, import the application, validate its configuration, and run the initial tests.

### Git milestone

Commit the verified environment and application foundation.

## 8. Phase 2: Event schemas and validation

### Objective

Define the common data structures used throughout the application.

### Prerequisites

Phase 1 must be complete.

### Tasks

1. Define a normalized security-event model.
2. Define event identifiers and timestamp conventions.
3. Define supported event-source and event-category fields.
4. Define models for process, file, authentication, and network metadata where required.
5. Define a structured detection-finding model.
6. Define incident and evidence-reference models.
7. Define severity and confidence representations.
8. Define action-request and action-result models.
9. Define response-verification results.
10. Add schema validation and field constraints.
11. Define handling for unknown or missing optional fields.
12. Document schema versioning.

### Expected deliverables

* Event models.
* Finding and incident models.
* Action and verification models.
* Validation tests.
* Schema documentation.

### Tests

* Valid input is accepted.
* Invalid field types are rejected or handled according to the schema.
* Missing required fields produce controlled validation errors.
* Optional fields behave consistently.
* Identifiers and timestamps follow the documented format.
* Invalid action requests cannot pass validation unnoticed.

### Acceptance criteria

Every core model has documented fields and automated tests covering valid, invalid, and boundary inputs.

### Git milestone

Commit the validated data models.

## 9. Phase 3: Windows event collection

### Objective

Collect supported endpoint events through documented Windows interfaces.

### Prerequisites

Phases 1 and 2 must be complete.

### Tasks

1. Confirm which Windows event sources are available in the development environment.
2. Select the first event source based on permissions, reliability, and testing needs.
3. Define a collector interface.
4. Implement the first collector.
5. Normalize collected records into the event schema.
6. Record source availability and collection errors.
7. Handle missing permissions.
8. Define polling or subscription behavior as appropriate.
9. Prevent uncontrolled duplicate processing.
10. Add a way to run tests without access to live event sources.
11. Document monitoring limitations.

### Expected deliverables

* Collector interface.
* At least one tested event-source adapter.
* Normalized event output.
* Collection health reporting.
* Synthetic event fixtures.

### Tests

* Valid events are normalized.
* Malformed records are handled safely.
* Permission failures are reported.
* Source unavailability is visible.
* Repeated records are handled predictably.
* Collection can stop without leaving uncontrolled background work.

### Acceptance criteria

The collector produces validated events from its documented source and reports failures without claiming unsupported monitoring coverage.

### Git milestone

Commit the first verified event collector.

## 10. Phase 4: Rule-based threat detection

### Objective

Build a deterministic detection engine that evaluates normalized events against documented rules.

### Prerequisites

Phase 2 must be complete. Phase 3 may supply real events, but the detection engine should also work with synthetic inputs.

### Tasks

1. Define the rule interface.
2. Define rule identifiers, descriptions, conditions, and evidence requirements.
3. Define severity-assessment inputs.
4. Implement the rule evaluation pipeline.
5. Implement the first small set of detection rules.
6. Record the matching rule and supporting evidence.
7. Distinguish a finding from a confirmed malicious event.
8. Add duplicate-finding handling.
9. Define how rules are enabled, disabled, and configured.
10. Document unsupported detection categories.
11. Add representative benign scenarios.
12. Add false-positive tests.

### Expected deliverables

* Rule interface.
* Detection engine.
* Initial documented rules.
* Structured findings.
* Detection test suite.

### Tests

* Positive cases trigger the expected rule.
* Negative cases do not trigger unsupported findings.
* Boundary conditions behave predictably.
* Invalid rule configuration is rejected.
* Evidence references are preserved.
* Reprocessing an event does not create uncontrolled duplicate actions.

### Acceptance criteria

Every implemented rule has a description, test cases, evidence requirements, and documented limitations.

### Git milestone

Commit the initial tested detection engine.

## 11. Phase 5: Network intrusion detection using CICIDS2017

### Objective

Establish a reproducible evaluation pipeline for network intrusion detection.

### Prerequisites

Phase 1 must be complete. The dataset files and applicable usage terms must be available for inspection.

### Tasks

1. Inspect the actual dataset files.
2. Record the filenames, formats, and available labels.
3. Identify feature columns and the target label.
4. Check data types, missing values, duplicates, and invalid records.
5. Inspect class distribution.
6. Document preprocessing decisions.
7. Separate features from target labels.
8. Define an appropriate train, validation, and test strategy if machine learning is used.
9. Check for data leakage, including duplicate or closely related records crossing splits.
10. Establish a simple baseline before introducing more complex models.
11. Select evaluation metrics appropriate to class imbalance and operational risk.
12. Record false positives and false negatives.
13. Save experiment configuration and results.
14. Document model limitations and reproducibility steps.
15. Define how, if at all, network detection results will integrate with the application.

### Expected deliverables

* Dataset inventory.
* Reproducible preprocessing pipeline.
* Baseline evaluation.
* Documented metrics.
* Experiment results.
* Dataset limitations.

### Tests

* Required dataset files are checked before processing.
* Missing or malformed inputs are handled.
* Target labels are validated.
* Preprocessing produces the documented feature structure.
* Evaluation splits follow the documented strategy.
* Repeated runs with fixed configuration produce reproducible results within the expected limits.

### Acceptance criteria

The project can reproduce a documented network detection experiment and explain its results, limitations, and data-processing decisions.

CICIDS2017 performance must not be reported as proof that Windows process, file, or authentication monitoring works.

### Git milestone

Commit the reproducible dataset-processing pipeline and evaluation documentation. Do not commit large raw datasets unless their inclusion is explicitly justified and permitted.

## 12. Phase 6: Investigation and event correlation

### Objective

Gather supporting evidence for detections and combine related observations into structured incidents.

### Prerequisites

Phases 2 and 4 must be complete.

### Tasks

1. Define the investigation input and output models.
2. Define which findings require additional investigation.
3. Collect available context through approved interfaces.
4. Reference original events in investigation results.
5. Record missing evidence and permission failures.
6. Define correlation keys and time windows.
7. Associate related events with an incident.
8. Preserve original event identifiers.
9. Distinguish direct observations from inferred relationships.
10. Define investigation timeouts and error handling.
11. Prevent event data from becoming executable instructions.
12. Document investigation outcomes.

### Expected deliverables

* Investigation interface.
* Evidence collection routines.
* Incident correlation rules.
* Structured investigation results.

### Tests

* Required context is collected when available.
* Missing context is recorded.
* Unrelated events remain separate.
* Correlated events retain their source identifiers.
* Malformed event content cannot execute commands.
* Investigation failures do not bypass policy controls.

### Acceptance criteria

The investigation component produces traceable evidence and explicit uncertainty without making unsupported claims.

### Git milestone

Commit the tested investigation and correlation components.

## 13. Phase 7: Risk assessment

### Objective

Convert investigation results into consistent risk assessments and structured recommendations.

### Prerequisites

Phase 6 must be complete.

### Tasks

1. Define severity levels.
2. Define the inputs used to assess severity.
3. Define confidence representation.
4. Keep severity and confidence separate.
5. Define how missing evidence affects the assessment.
6. Define recommendation categories.
7. Include justification and supporting evidence.
8. Define additional authorization conditions.
9. Document assessment rules.
10. Add boundary and regression tests.

### Expected deliverables

* Risk-assessment component.
* Documented classification rules.
* Structured response recommendations.
* Test coverage.

### Tests

* Severity follows the documented rules.
* Confidence is represented independently.
* Missing evidence is handled explicitly.
* Unsupported recommendations are rejected.
* Recommendations do not authorize execution.
* Boundary conditions are tested.

### Acceptance criteria

Risk decisions are deterministic where required, explainable, and traceable to their inputs.

### Git milestone

Commit the verified risk-assessment component.

## 14. Phase 8: Response policy engine

### Objective

Implement the security boundary that decides whether a proposed action is permitted.

### Prerequisites

Phases 1, 2, and 7 must be complete.

### Tasks

1. Define the supported action types.
2. Create an explicit action allowlist.
3. Define policy inputs and outputs.
4. Validate the requested action and target.
5. Define authorization requirements for each action.
6. Implement deny-by-default behavior.
7. Add detection-only mode.
8. Add simulation mode.
9. Implement the emergency-stop control.
10. Define handling for missing or contradictory evidence.
11. Define policy-engine failure behavior.
12. Record authorization decisions.
13. Test attempts to bypass policy restrictions.

### Expected deliverables

* Independent policy engine.
* Action allowlist.
* Operating-mode controls.
* Emergency-stop mechanism.
* Authorization audit records.

### Tests

* Permitted actions pass the relevant policy checks.
* Prohibited actions are rejected.
* Invalid targets are rejected.
* Unknown action types are denied.
* Policy-engine errors fail closed.
* Detection-only mode blocks system-changing actions.
* Simulation mode does not perform real system changes.
* Emergency stop blocks new automated actions.
* AI-generated recommendations cannot change authorization decisions.

### Acceptance criteria

No system-changing action can reach the executor without passing the policy engine.

This phase must pass its security tests before work proceeds to real response execution.

### Git milestone

Commit the tested policy engine and authorization controls.

## 15. Phase 9: Controlled response executor

### Objective

Implement a restricted executor for explicitly authorized defensive actions.

### Prerequisites

Phase 8 must be complete.

### Tasks

1. Define the executor interface.
2. Define action-specific preconditions.
3. Validate target identifiers and resource scope.
4. Restrict operations to the allowlist.
5. Implement simulation behavior.
6. Implement the first low-impact response operation.
7. Add bounded execution timeouts.
8. Record execution start, result, and errors.
9. Handle missing permissions.
10. Define cancellation and shutdown behavior.
11. Add isolated test resources.
12. Document the limitations and recovery procedure for each action.

### Expected deliverables

* Restricted response executor.
* Action implementations selected for the initial release.
* Simulation support.
* Execution records.
* Isolated response tests.

### Tests

* Authorized test actions execute against the intended test resources.
* Unauthorized targets are rejected.
* Unknown actions cannot execute.
* Timeouts and permission failures are handled.
* Duplicate requests do not cause uncontrolled side effects.
* The emergency stop blocks new execution.
* Simulation produces no real system-changing side effects.

### Acceptance criteria

Every implemented action has tested preconditions, target restrictions, failure handling, and a documented execution result.

Real system-changing actions remain disabled until the relevant verification and security requirements are satisfied.

### Git milestone

Commit the restricted executor and its isolated tests.

## 16. Phase 10: Response verification

### Objective

Determine whether each response action achieved its intended result.

### Prerequisites

Phase 9 must be complete.

### Tasks

1. Define verification interfaces.
2. Define action-specific postconditions.
3. Implement verification for each supported action.
4. Record verification evidence.
5. Distinguish success, failure, and inconclusive outcomes.
6. Define handling for unavailable verification sources.
7. Check for continuing suspicious behavior where supported.
8. Prevent automatic incident closure based solely on command success.
9. Add recovery and escalation rules.
10. Test verification failure.

### Expected deliverables

* Verification component.
* Action-specific verification procedures.
* Structured verification records.
* Tests for success and failure cases.

### Tests

* Successful actions can be verified.
* Failed actions are reported accurately.
* Inconclusive outcomes remain unresolved.
* Continued suspicious activity updates the incident.
* Missing telemetry is not treated as proof of remediation.

### Acceptance criteria

The system accurately distinguishes successful execution from verified remediation.

### Git milestone

Commit the verified response workflow.

## 17. Phase 11: Incident storage and audit

### Objective

Persist incidents, evidence references, policy decisions, and action history.

### Prerequisites

The core event, investigation, risk, and policy models must be defined.

### Tasks

1. Review the existing storage design.
2. Confirm the initial database choice.
3. Define the incident schema.
4. Define event and evidence-reference relationships.
5. Define action and verification records.
6. Define incident lifecycle transitions.
7. Implement persistence interfaces.
8. Add transaction and error-handling behavior.
9. Define retention and deletion rules.
10. Minimize sensitive data collection.
11. Protect credentials and secrets.
12. Add retrieval and filtering operations.
13. Test restart and recovery behavior.
14. Define backup requirements.

### Expected deliverables

* Persistent incident storage.
* Audit-record storage.
* Data access interfaces.
* Retention rules.
* Database tests.

### Tests

* Records can be created and retrieved.
* Invalid state transitions are rejected.
* Failed writes are reported.
* Relationships remain consistent.
* Restart does not falsely complete unfinished actions.
* Secrets do not appear in stored diagnostics.
* Retention and deletion behavior is tested.

### Acceptance criteria

Incident and audit records remain consistent across supported operations and application restarts.

### Git milestone

Commit the verified persistence and audit components.

## 18. Phase 12: FastAPI backend

### Objective

Expose supported application capabilities through a documented API.

### Prerequisites

The required service interfaces and data models must be available.

### Tasks

1. Review `docs/API_SPECIFICATION.md`.
2. Define the API version and route conventions.
3. Implement health and component-status endpoints.
4. Implement event submission or ingestion endpoints where required.
5. Implement incident retrieval endpoints.
6. Implement finding and alert endpoints.
7. Add request and response validation.
8. Add access control appropriate to the deployment.
9. Restrict request sizes and resource-intensive operations.
10. Handle invalid input and internal errors safely.
11. Add API tests.
12. Document configuration and startup commands.

### Expected deliverables

* FastAPI application.
* Validated request and response models.
* Access-control mechanisms.
* API documentation.
* Endpoint tests.

### Tests

* Valid requests return documented responses.
* Invalid requests are rejected.
* Unauthenticated or unauthorized operations are blocked where applicable.
* Internal errors do not reveal secrets.
* Health checks accurately report component availability.
* API behavior matches the specification.

### Acceptance criteria

The API exposes only documented operations and enforces the required validation and access controls.

### Git milestone

Commit the tested API.

## 19. Phase 13: Frontend dashboard and alerting

### Objective

Build a decoupled web frontend using React, TypeScript, and Tailwind CSS to give users an interactive interface for monitoring incidents, telemetry evidence, system status, and response outcomes over REST APIs.

### Prerequisites

Phase 11 (Storage and audit records) and Phase 12 (FastAPI backend) must be available and verified.

### Tasks

1. Review `docs/PROJECT_REQUIREMENTS.md` (FR-022, FR-023, INT-002) and `docs/API_SPECIFICATION.md`.
2. Initialize the React client application using TypeScript and Tailwind CSS.
3. Implement API client services for backend REST endpoints (`/health`, `/detections`, `/incidents`, `/audit/records`).
4. Build the primary security dashboard overview with status indicators and metric cards.
5. Implement incident list and filtering views with severity and status indicators.
6. Build detailed incident investigation views displaying evidence telemetry and detection context.
7. Implement response status displays and policy decision audits.
8. Add emergency-stop controls and response-mode indicators.
9. Handle API connection errors, timeouts, and validation errors gracefully in the UI.
10. Verify that the frontend contains no direct operating-system execution capabilities.
11. Evaluate optional Server-Sent Events (SSE) or WebSocket integration for live alert streaming.
12. Add client-side unit and component tests.

### Expected deliverables

* Standalone React + TypeScript web frontend application.
* Tailwind CSS styling and responsive dashboard layout.
* Typed REST API client layer.
* Incident investigation and alert views.
* Emergency-stop and response status displays.

### Tests

* Dashboard renders incident lists and health indicators correctly from mock or live API data.
* Status changes (detected, investigating, responding, verified) display accurately.
* Unverified incidents are never marked resolved.
* API disconnections and backend errors are clearly indicated.
* Emergency-stop state is prominent and up to date.
* Client-side tests verify that no OS commands or raw scripts can be issued from the interface.

### Acceptance criteria

Users can inspect detections, review forensic evidence, track response policy decisions, and verify remediation outcomes through a responsive React interface communicating with the backend via REST APIs.

### Git milestone

Commit the tested React frontend dashboard and alerting integration.

## 20. Phase 14: AI-assisted investigation

### Objective

Add optional AI support for evidence summaries and investigation explanations.

### Prerequisites

Phase 6 must be complete. Core deterministic detection and policy enforcement must work without AI.

### Tasks

1. Review `docs/AI_AGENT_DESIGN.md`.
2. Define the provider-independent client interface.
3. Define configuration and timeout behavior.
4. Keep API credentials outside source control.
5. Define the permitted input fields.
6. Prepare prompts using structured evidence.
7. Define a validated response schema.
8. Require the model to distinguish evidence from inference.
9. Handle invalid, incomplete, or unsupported output.
10. Add a deterministic fallback.
11. Protect against prompt injection in event data.
12. Ensure AI output cannot reach the executor as a command.
13. Add tests for provider failures.
14. Record model and configuration details needed for debugging without exposing secrets.

### Expected deliverables

* Optional AI client.
* Structured investigation explanations.
* Configuration support.
* Offline fallback.
* AI-boundary tests.

### Tests

* Valid model responses pass schema validation.
* Invalid responses are rejected or safely handled.
* Provider timeouts are handled.
* Missing credentials do not disable core detection.
* Untrusted event content cannot authorize an action.
* AI recommendations still pass through the policy engine.
* Sensitive data is not sent unnecessarily.

### Acceptance criteria

AI improves explanation quality without becoming a security authority or a dependency for core detection and authorization.

### Git milestone

Commit the tested AI integration and fallback.

## 21. Phase 15: End-to-end integration

### Objective

Verify that the implemented components work together across the complete incident lifecycle.

### Prerequisites

All required core components must be available.

### Tasks

1. Connect event collection to normalization.
2. Connect normalized events to detection.
3. Connect findings to investigation.
4. Connect investigation results to risk assessment.
5. Connect recommendations to the policy engine.
6. Connect authorized requests to the executor.
7. Connect execution results to verification.
8. Persist incident and audit updates.
9. Update alerts and the dashboard.
10. Verify startup, shutdown, and recovery.
11. Test the workflow without AI.
12. Test optional AI integration separately.
13. Record unresolved integration issues.

### Expected deliverables

* Integrated application workflow.
* End-to-end test suite.
* Updated architecture documentation.
* Verified incident lifecycle.

### Tests

At minimum, exercise:

* Benign events.
* Recognized suspicious events.
* Insufficient investigation evidence.
* Authorized simulated actions.
* Prohibited actions.
* Failed response execution.
* Inconclusive verification.
* Emergency-stop activation.
* Storage and API failures.
* AI service unavailability.

### Acceptance criteria

The end-to-end tests demonstrate that data moves through the intended workflow and that failures do not bypass security controls.

### Git milestone

Commit the verified integration workflow.

## 22. Phase 16: Security and reliability hardening

### Objective

Review the application for unsafe behavior, authorization failures, data-handling weaknesses, and reliability problems.

### Prerequisites

The integrated workflow must exist.

### Tasks

1. Review the threat model against the implementation.
2. Review all action execution paths.
3. Test the allowlist and deny-by-default behavior.
4. Test invalid and unauthorized targets.
5. Test emergency-stop behavior.
6. Review access control.
7. Review secret handling.
8. Review sensitive data in logs and database records.
9. Test malformed input.
10. Test timeouts and component failures.
11. Test duplicate event and action processing.
12. Review dependency vulnerabilities.
13. Measure event-processing and alert latency.
14. Measure resource consumption.
15. Evaluate false-positive behavior.
16. Document residual risks.
17. Fix high-priority security defects before enabling real responses.

### Expected deliverables

* Security test results.
* Reliability test results.
* Performance measurements.
* Updated threat model.
* Documented residual risks.

### Acceptance criteria

All required security tests pass, high-priority defects are resolved or explicitly block release, and the remaining limitations are documented.

### Git milestone

Commit security fixes separately from unrelated feature changes.

## 23. Phase 17: Packaging and deployment

### Objective

Make the application installable and usable in a documented environment.

### Prerequisites

The integrated application must pass the required security and reliability checks.

### Tasks

1. Confirm the supported Python version.
2. Verify dependency installation in a clean environment.
3. Document configuration variables.
4. Provide a safe example configuration.
5. Document the startup process.
6. Document the shutdown process.
7. Document required permissions.
8. Explain how to enable and disable response modes.
9. Explain the emergency-stop procedure.
10. Document log and data locations.
11. Document backup and recovery procedures.
12. Verify installation from the written instructions.
13. Document troubleshooting steps.
14. Identify unsupported platforms and configurations.

### Expected deliverables

* Installation instructions.
* Deployment guide.
* Example configuration.
* Troubleshooting documentation.
* Verified startup and shutdown procedures.

### Tests

* Installation succeeds in a clean environment.
* Configuration validation behaves as documented.
* The application starts with safe defaults.
* Required services report their health accurately.
* Recovery procedures work in the supported test environment.

### Acceptance criteria

Another developer can follow the documented process to install, configure, start, test, and stop the application without relying on undocumented local setup.

### Git milestone

Commit verified packaging and deployment documentation.

## 24. Phase 18: Release validation

### Objective

Determine whether the application meets its initial release requirements.

### Prerequisites

Phase 17 must be complete.

### Tasks

1. Run the full automated test suite.
2. Run the required integration tests.
3. Run the security test suite.
4. Verify the acceptance scenarios in `docs/PROJECT_REQUIREMENTS.md`.
5. Confirm the emergency stop works.
6. Confirm the default response mode is safe.
7. Review the documented limitations.
8. Review the dependency list.
9. Verify the installation instructions.
10. Check the Git working tree for unintended changes.
11. Review the release notes.
12. Record the release decision.

### Expected deliverables

* Full test results.
* Acceptance checklist.
* Security review summary.
* Release notes.
* Documented release decision.

### Acceptance criteria

The release is approved only when mandatory requirements have been verified, critical security issues are resolved, and remaining limitations are clearly documented.

A release must be delayed if a critical safety or authorization requirement fails.

### Git milestone

Create a release commit or tag after the final review.

## 25. Cross-phase development workflow

Use the following workflow for each phase.

### Step 1: Inspect

Review the existing implementation, documentation, tests, and Git status before editing.

### Step 2: Plan

Identify the files that need to change and define the expected behavior.

### Step 3: Implement

Make focused changes that fit the current architecture. Avoid unrelated refactoring.

### Step 4: Test

Run the relevant unit tests, integration tests, and security checks.

### Step 5: Review

Inspect the diff for unintended changes, unsafe defaults, secrets, and outdated documentation.

### Step 6: Update documentation

Record changed interfaces, configuration, behavior, and known limitations.

### Step 7: Verify acceptance criteria

Confirm that the phase meets its documented completion conditions.

### Step 8: Commit the milestone

Commit the tested work using a message that describes the change.

### Step 9: Update progress

Update the roadmap only after verifying the phase's completion evidence.

## 26. Git and change-management rules

The project will use milestone-based commits.

Recommended commit prefixes include:

| Prefix      | Use                                                      |
| ----------- | -------------------------------------------------------- |
| `docs:`     | Documentation changes                                    |
| `feat:`     | New functionality                                        |
| `fix:`      | Bug fixes                                                |
| `test:`     | Test changes                                             |
| `refactor:` | Internal restructuring without intended behavior changes |
| `security:` | Security-related changes                                 |
| `build:`    | Build and dependency configuration                       |

Examples:

* `docs: complete project requirements`
* `feat: add validated security event models`
* `test: cover response policy boundaries`
* `security: enforce response target validation`

Before committing:

* Check `git status`.
* Inspect `git diff`.
* Run relevant tests.
* Check for secrets and unintended files.
* Confirm the changes belong to the intended milestone.

Do not commit a phase as complete while its mandatory tests are failing.

## 27. Progress tracking

Each phase should have one of these statuses:

| Status      | Meaning                                                |
| ----------- | ------------------------------------------------------ |
| Not started | No implementation work has begun                       |
| In progress | Work is underway                                       |
| Blocked     | A dependency or unresolved issue prevents progress     |
| In review   | Implementation is complete but verification is pending |
| Complete    | Acceptance criteria have been verified                 |

A phase can be marked complete only when its deliverables and required test evidence are available.

The roadmap should record:

* Current phase.
* Completed phases.
* Active tasks.
* Blockers.
* Relevant commits.
* Test results.
* Next action.

Do not mark a phase complete based only on the existence of source files.

## 28. Dependencies and risk management

| Risk                          | Potential impact                          | Planned mitigation                                                      |
| ----------------------------- | ----------------------------------------- | ----------------------------------------------------------------------- |
| Inconsistent documentation    | Conflicting implementation decisions      | Review and reconcile documents before implementation                    |
| Missing Windows permissions   | Incomplete monitoring                     | Report source availability and test permission failures                 |
| False-positive detections     | Unnecessary response actions              | Use evidence requirements, confidence assessment, and benign test cases |
| Unsafe automated actions      | System disruption or data loss            | Use allowlists, target validation, simulation, and the emergency stop   |
| AI output errors              | Incorrect investigation conclusions       | Validate outputs and keep AI advisory                                   |
| Dataset leakage               | Misleading model performance              | Inspect data splits and document preprocessing                          |
| Dataset and endpoint mismatch | Incorrect claims about detection coverage | Evaluate network detection separately from endpoint monitoring          |
| Dependency incompatibility    | Installation or runtime failures          | Pin and test supported dependency versions                              |
| Storage failure               | Lost or inconsistent incident history     | Use defined persistence behavior and recovery tests                     |
| Incomplete verification       | False claims of remediation               | Represent uncertain outcomes explicitly                                 |
| Excessive resource usage      | Degraded computer performance             | Measure resource consumption under representative workloads             |

## 29. Open decisions

The following decisions must be resolved through repository inspection, testing, or documented design review:

1. Which Windows event source will be implemented first?
2. Which endpoint event categories belong in the initial release?
3. Which Python version and dependency set will be supported?
4. Which exact defensive actions will be supported initially?
5. Which actions require explicit human approval?
6. What permissions does each supported action require?
7. Which response actions need rollback support?
8. What are the expected event rate and measurable performance targets?
9. Which CICIDS2017 files and feature set will be used?
10. How will network detection results be represented in incidents?
11. Which database schema and retention defaults will be used?
12. What access control is required for local API and dashboard operations?
13. Which AI provider, if any, will be configured?
14. What constitutes sufficient evidence for each response action?

Record significant architectural choices in `docs/ARCHITECTURAL_DECISION_LOG.md`.

## 30. Definition of done

A development phase is complete when:

* Its required tasks have been completed.
* Its deliverables exist.
* Its acceptance criteria have been checked.
* Required automated tests pass.
* Relevant security checks pass.
* Documentation reflects the actual implementation.
* Known limitations are recorded.
* Changes have been reviewed.
* The milestone has been committed where required.

If a mandatory criterion fails, the phase remains in progress, blocked, or in review.

## 31. Current project status

**Roadmap status:** Draft.

**Current development priority:** Review and align the project documentation before beginning implementation phases.

**Implementation status:** Must be determined from the current repository and verified test results. This roadmap does not assert that any phase is complete.

**Immediate next steps:**

1. Save this roadmap.
2. Review `docs/SYSTEM_ARCHITECTURE.MD`.
3. Resolve architecture decisions that affect the phase sequence.
4. Confirm the supported environment and initial event sources.
5. Begin Phase 1 only after Phase 0 meets its acceptance criteria.
