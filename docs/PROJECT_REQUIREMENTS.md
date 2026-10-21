# CyberShield-Auto

## Project requirements specification

| Field             | Value                                                                                                                                                                        |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Document ID       | CSA-PRS-001                                                                                                                                                                  |
| Version           | 1.1                                                                                                                                                                          |
| Status            | Draft, pending review                                                                                                                                                        |
| Project phase     | Phase 0: Documentation and planning                                                                                                                                          |
| Initial platform  | Windows                                                                                                                                                                      |
| Primary language  | Python                                                                                                                                                                       |
| Related documents | `docs/PROJECT_OVERVIEW.md`, `docs/SYSTEM_ARCHITECTURE.MD`, `docs/THREAT_MODEL.md`, `docs/THREAT_DETECTION_ENGINE.md`, `docs/AUTOMATED_RESPONSE_POLICY.md`, `docs/DATASET.md` |

## 1. Purpose

This document defines the functional, security, data, operational, and performance requirements for CyberShield-Auto.

It describes what the application must do, how its components should behave, and how implementation will be evaluated.

Each requirement must be traceable to the relevant design, implementation, and test evidence. A requirement is not complete simply because a corresponding class, module, or file exists.

Requirements use the following priority levels:

* **P0: Required.** Necessary for the initial release.
* **P1: Important.** Needed for a complete implementation but may be introduced in a later development phase.
* **P2: Future.** Outside the initial release unless the scope changes.

The words MUST, SHOULD, and MAY describe mandatory, recommended, and optional behavior respectively.

## 2. Project objectives

CyberShield-Auto aims to:

1. Collect supported security-relevant events.
2. Validate and normalize event data.
3. Detect documented suspicious behavior.
4. Investigate findings using available evidence.
5. Assess threat severity and detection confidence.
6. Evaluate response recommendations against explicit policies.
7. Execute authorized defensive actions.
8. Verify the outcome of each executed action.
9. Maintain incident records and security alerts.
10. Provide a dashboard for monitoring and investigation.
11. Record important security decisions and response outcomes.
12. Support automated testing and future extensions.

The application must not claim that a threat has been removed merely because an action was attempted.

## 3. Scope

### 3.1 Initial release

The initial release targets one Windows computer and uses a modular Python architecture.

The planned capabilities include:

* Event collection from supported sources.
* Event validation and normalization.
* Rule-based threat detection.
* Investigation and evidence collection.
* Incident correlation where supported.
* Severity and confidence assessment.
* Policy-controlled response decisions.
* A limited set of defensive actions.
* Post-response verification.
* Alert and incident management.
* Local storage and audit records.
* A monitoring dashboard.
* Automated tests and documentation.

Development will begin with synthetic events and controlled test scenarios. System-changing actions must be tested in an isolated environment before they are enabled on a real endpoint.

### 3.2 Network intrusion detection

CICIDS2017 is the selected dataset for network intrusion detection experiments.

The dataset contains network traffic records suitable for developing and evaluating network detection methods. It does not provide all the operating-system telemetry required for Windows endpoint monitoring.

The project must distinguish between:

* Network intrusion detection using CICIDS2017.
* Endpoint monitoring using supported Windows event sources.
* Synthetic events used to test components that lack suitable real-world telemetry.

The available dataset files, feature columns, labels, preprocessing requirements, and usage terms must be inspected before model development.

Dataset evaluation results must not be presented as proof that the application detects threats on a live Windows computer.

### 3.3 Exclusions

The initial release does not require:

* Enterprise-scale deployment.
* Centralized management of multiple computers.
* Guaranteed detection of every attack.
* Unrestricted remote access.
* Arbitrary command execution generated by an AI model.
* Automatic deletion of suspicious files based solely on a detection result.
* Unrestricted modification of operating-system security settings.
* An AI model with independent authority over the computer.
* Claims of complete protection against all threats.

Changes to the scope must be documented and reviewed.

## 4. Requirement categories

| Prefix | Category                   |
| ------ | -------------------------- |
| FR     | Functional requirement     |
| NFR    | Non-functional requirement |
| SEC    | Security requirement       |
| DAT    | Data requirement           |
| INT    | Integration requirement    |
| TST    | Testing requirement        |
| OPS    | Operational requirement    |

Each requirement has a unique identifier. Implementations and tests should use these identifiers where practical to maintain traceability.

## 5. Functional requirements

### 5.1 Event collection

#### FR-001: Continuous monitoring

**Priority:** P0

The system MUST collect supported security events while the relevant monitoring component is running.

Acceptance criteria:

* The monitoring component starts and stops predictably.
* Supported events are collected through documented interfaces.
* Collection failures are recorded.
* Unavailable or disabled sources are reported accurately.
* The application does not claim coverage of an event source that it cannot access.

#### FR-002: Event normalization

**Priority:** P0

The system MUST convert collected events into a common, validated data structure.

Where applicable, an event should contain:

* A unique event identifier.
* A timestamp.
* An event source.
* An event category.
* Relevant process, file, account, or network metadata.
* Attributes required by the applicable detection rules.

Acceptance criteria:

* Valid events pass schema validation.
* Invalid events are rejected or safely handled.
* Missing optional fields do not crash the processing pipeline.
* Timestamps and identifiers follow documented formats.
* Original evidence can be traced to the normalized event.

#### FR-003: Event processing reliability

**Priority:** P0

The system MUST handle malformed events, duplicate events, and temporary collection failures without unnecessarily crashing unrelated components.

Acceptance criteria:

* Invalid events produce controlled errors.
* Duplicate events do not automatically trigger repeated high-impact actions.
* Processing failures are visible in diagnostic logs.
* Recovery behavior is tested.
* Failed processing is not silently reported as successful.

### 5.2 Threat detection

#### FR-004: Rule-based detection

**Priority:** P0

The system MUST support configurable, deterministic detection rules.

Each rule must define:

* A unique rule identifier.
* A threat category.
* Detection conditions.
* Required evidence.
* Severity-assessment inputs or rules.
* A description.
* An investigation or response recommendation, where applicable.

Acceptance criteria:

* Rules produce predictable results for defined inputs.
* Each finding identifies the matching rule.
* Rules can be tested independently.
* Invalid rule configurations are rejected.
* A recommendation does not automatically authorize a response.

#### FR-005: Detection evidence

**Priority:** P0

Every detection MUST include evidence supporting the finding.

Acceptance criteria:

* The finding references its triggering event or events.
* The matching rule is recorded.
* The explanation identifies the observed behavior.
* Observed facts are distinguished from assumptions.
* Missing evidence is represented explicitly.

#### FR-006: Threat categories

**Priority:** P0

The initial detection engine MUST support a documented subset of these categories:

1. Suspicious process behavior.
2. Known malicious file indicators.
3. Repeated authentication failures, when suitable event sources are available.
4. Suspicious network activity.
5. Unexpected changes to selected persistence locations.

Network detection using CICIDS2017 must be evaluated separately from endpoint detection.

Acceptance criteria:

* Every implemented category has documented detection conditions.
* Each rule has positive and negative test cases.
* Required data sources are identified.
* Unsupported categories are marked as unavailable or planned.
* Dataset-based evaluation is not confused with live endpoint validation.

#### FR-007: False-positive handling

**Priority:** P0

The system MUST account for legitimate activity that resembles malicious behavior.

Acceptance criteria:

* A detection alone does not establish that an event is malicious.
* Severity and confidence are stored separately.
* High-impact responses require stronger evidence and authorization.
* False-positive scenarios are included in tests.
* Uncertain findings remain distinguishable from confirmed observations.

### 5.3 Investigation

#### FR-008: Context collection

**Priority:** P0

The investigation component MUST collect additional context when an incident meets the configured investigation criteria.

Possible context includes process metadata, event history, file metadata, and associated network activity.

Acceptance criteria:

* Investigation results reference their supporting evidence.
* Missing context is recorded.
* Permission failures are handled safely.
* Event data cannot cause the investigator to execute arbitrary commands.
* Investigation failures do not bypass response authorization.

#### FR-009: Event correlation

**Priority:** P1

The system SHOULD correlate related events into an incident when documented conditions are satisfied.

Acceptance criteria:

* Correlation rules define the fields and time windows they use.
* Unrelated events are not combined without justification.
* Original event identifiers are preserved.
* Duplicate observations are handled predictably.
* Tests cover unrelated events and boundary conditions.

#### FR-010: Investigation results

**Priority:** P0

The investigation component MUST produce a structured result containing:

* An incident identifier.
* Collected evidence.
* Relevant event references.
* Findings.
* Missing information.
* Investigation status.
* A recommended next step, where appropriate.

AI may assist with investigation summaries when that integration is implemented.

AI-generated conclusions MUST remain distinguishable from verified evidence. They must not independently authorize actions.

### 5.4 Risk assessment

#### FR-011: Severity classification

**Priority:** P0

Each actionable incident MUST receive a severity classification.

Initial levels:

* Informational.
* Low.
* Medium.
* High.
* Critical.

Acceptance criteria:

* Classification follows documented rules.
* Severity is stored with the incident.
* The decision can be traced to its inputs.
* Boundary conditions are tested.
* Missing evidence does not silently become evidence of low risk.

#### FR-012: Confidence assessment

**Priority:** P0

The system MUST distinguish classification confidence from potential threat severity.

Acceptance criteria:

* Confidence and severity are separate fields.
* Missing evidence is represented explicitly.
* Uncertain classifications do not automatically authorize destructive actions.
* Uncalibrated scores are not presented as verified probabilities.
* The basis for confidence is documented.

#### FR-013: Response recommendation

**Priority:** P0

The risk assessment component MUST produce a structured recommendation when a response is appropriate.

The recommendation must identify:

* The incident.
* Assessed severity.
* Supporting evidence.
* Proposed action category.
* Justification.
* Confidence and uncertainty.
* Additional authorization conditions.

A recommendation is not authorization to execute the action.

### 5.5 Policy-controlled response

#### FR-014: Explicit authorization

**Priority:** P0

Every automated action MUST pass through an explicit response policy before execution.

Acceptance criteria:

* Permitted actions are defined in an allowlist.
* Unsupported actions are rejected.
* The policy engine operates independently of AI recommendations.
* Every authorization decision is recorded.
* Policy errors fail closed.
* An unavailable policy engine cannot grant permission.

#### FR-015: Automated defensive actions

**Priority:** P0

The system MUST support a limited set of controlled defensive actions selected during architecture design.

Candidate actions include:

* Recording an incident.
* Collecting additional evidence.
* Terminating a confirmed malicious test process.
* Quarantining a validated malicious test file.

The initial implementation must define the exact supported actions. Listing a candidate action in this document does not mean that the action is implemented.

Acceptance criteria:

* Each action has explicit preconditions.
* Each action is restricted to an authorized target.
* Unauthorized targets are rejected.
* Results and errors are recorded.
* Each action can be tested safely in an isolated environment.
* Potentially disruptive actions require appropriate authorization.

#### FR-016: Reversible responses

**Priority:** P0

The system MUST prefer reversible, low-impact responses when they provide suitable protection.

Acceptance criteria:

* Each action declares whether it is reversible.
* Recovery procedures are documented where applicable.
* Disruptive actions have stricter authorization conditions.
* The system does not describe an action as reversible without a defined recovery mechanism.

#### FR-017: Automatic operation

**Priority:** P0

The system MUST support automatic execution of configured defensive actions when the applicable policy permits them.

This requirement does not authorize unrestricted autonomous behavior.

Acceptance criteria:

* Permitted routine actions can execute without individual approval when the configured policy allows it.
* Actions outside the policy are rejected or escalated.
* AI recommendations cannot bypass authorization.
* The reason for allowing or denying an action is recorded.
* Detection-only mode prevents system-changing responses.
* Simulation mode does not perform real system-changing operations.

#### FR-018: Response failure handling

**Priority:** P0

If an action fails, times out, or produces an uncertain result, the system MUST record the outcome and follow its configured failure policy.

Acceptance criteria:

* Failures are distinguishable from successes.
* Unverified outcomes are not reported as successful remediation.
* Retries are bounded and documented.
* Failed responses update the incident or generate an alert as required.
* A failure does not trigger an unrestricted alternative action.

#### FR-019: Emergency stop

**Priority:** P0

The system MUST provide a mechanism to disable automated response execution without necessarily disabling event collection and alerting.

Acceptance criteria:

* The emergency stop blocks new automated actions.
* Its current state is visible.
* Requests to execute actions while it is active are rejected.
* The mechanism is tested.
* The application records attempts that were blocked where logging remains available.

### 5.6 Response verification

#### FR-020: Action verification

**Priority:** P0

Every automated defensive action MUST have a defined verification procedure.

Acceptance criteria:

* Verification checks the intended post-action state.
* Verification results are recorded.
* Success, failure, and inconclusive outcomes are distinguishable.
* Verification failure does not trigger an unrestricted alternative action.
* An action result is not treated as proof that the entire incident is resolved.

#### FR-021: Continued threat monitoring

**Priority:** P1

The system SHOULD monitor for evidence that suspicious behavior continues or returns after a response.

Acceptance criteria:

* Relevant follow-up events can be associated with the incident.
* Persistent or recurring behavior updates incident status.
* An incident is not closed merely because an action command returned successfully.
* Missing follow-up telemetry is not represented as proof that the threat is gone.

### 5.7 Alerting and dashboard

#### FR-022: Incident alerts

**Priority:** P0

The system MUST notify the dashboard when an actionable incident is created or an important incident status changes.

Acceptance criteria:

* Alerts include an incident identifier, severity, detection time, and summary.
* Response status is updated as the workflow progresses.
* Alert-delivery failures are handled and logged.
* Alert latency is measured against an agreed performance target.

#### FR-023: Incident details

**Priority:** P0

The dashboard MUST display relevant incident evidence, severity, investigation findings, and response status.

Acceptance criteria:

* Users can distinguish detected, investigating, responding, and verified incidents.
* Unverified incidents are not labelled resolved.
* Errors and uncertainty are visible.
* Recommendations are distinguishable from actions that were actually executed.

#### FR-024: Incident history

**Priority:** P0

The system MUST store and display a searchable incident history.

Acceptance criteria:

* Incident records can be retrieved by identifier.
* Records include relevant response history.
* Timestamps follow a documented convention.
* Access follows the security and privacy requirements.
* Storage failures are reported.

### 5.8 Auditability

#### FR-025: Decision audit

**Priority:** P0

The system MUST record important security decisions and response actions.

Where applicable, audit records must include:

* Event and incident references.
* Detection rule.
* Investigation findings.
* Risk assessment.
* Policy decision.
* Requested action and target.
* Execution result.
* Verification result.
* Timestamps and relevant errors.

Audit records must not expose credentials, API keys, or unnecessary sensitive information.

## 6. Non-functional requirements

### NFR-001: Detection latency

**Priority:** P0

The provisional target is to evaluate supported events within five seconds at the 95th percentile under a documented test workload.

Collection latency and detection latency must be measured separately. The target must be validated against the actual event sources and test environment.

### NFR-002: Alert latency

**Priority:** P0

The provisional target is to display an actionable incident within five seconds of incident creation at the 95th percentile under the documented test workload.

### NFR-003: Resource consumption

**Priority:** P1

Monitoring should avoid excessive CPU, memory, disk, and network consumption.

Resource targets will be established after a representative workload has been defined and measured.

### NFR-004: Processing capacity

**Priority:** P1

The event-processing pipeline SHOULD handle the expected test workload without uncontrolled queue growth or silent event loss.

The expected event rate and overload behavior must be documented.

### NFR-005: Fault isolation

A failure in one component SHOULD NOT unnecessarily crash unrelated components.

### NFR-006: Recoverability

The system MUST recover predictably from temporary failures when recovery is supported.

### NFR-007: Data integrity

Incident and audit records MUST preserve consistent identifiers, timestamps, and status transitions.

### NFR-008: Idempotency

Repeated processing of the same event or action request MUST NOT cause uncontrolled duplicate side effects.

### NFR-009: Modular architecture

Monitoring, detection, investigation, risk assessment, policy evaluation, response, verification, and alerting MUST have distinct responsibilities.

### NFR-010: Documentation

Public interfaces, configuration variables, detection rules, response policies, and important architectural decisions MUST be documented.

### NFR-011: Testability

Components MUST support deterministic tests without requiring real attacks or unrestricted administrative privileges.

### NFR-012: Understandable alerts

Alerts MUST explain the observed behavior and any action taken in language appropriate for the intended user.

### NFR-013: Clear status

The interface MUST distinguish recommendations, authorization decisions, attempted actions, successful operations, and verified outcomes.

### NFR-014: Platform boundaries

The initial release MUST identify Windows-specific integrations.

Core event models, detection logic, and policy interfaces SHOULD minimize unnecessary dependence on platform-specific implementation details.

## 7. Security requirements

### SEC-001: Least privilege

Each component MUST operate with the minimum privileges necessary.

### SEC-002: Restricted action execution

The response subsystem MUST accept only explicitly supported and authorized action types.

### SEC-003: Input validation

Events, configuration values, policy definitions, and action requests MUST be validated.

### SEC-004: Credential protection

Credentials and API keys MUST NOT be hardcoded or committed to version control.

### SEC-005: AI isolation

AI-generated text MUST NOT be interpreted directly as an executable command.

AI-assisted recommendations must pass through structured validation and policy authorization.

### SEC-006: Safe defaults

The initial configuration MUST use detection-only mode. Simulation mode must also be available for testing response decisions without performing real system changes.

### SEC-007: Audit protection

Unauthorized modification or deletion of audit records MUST be prevented to the extent supported by the deployment environment.

### SEC-008: Failure safety

Unexpected policy-engine errors MUST NOT grant permission to execute an action.

### SEC-009: Access control

Administrative functionality and sensitive incident data MUST be protected against unauthorized access.

### SEC-010: Response scope

Every response operation MUST be limited to the authorized resource and intended action.

### SEC-011: Emergency stop

The emergency-stop mechanism MUST prevent automated response execution while preserving incident logging where possible.

### SEC-012: Monitoring integrity

The system SHOULD detect and report failures of its own monitoring components when those failures are observable.

## 8. Data requirements

### DAT-001: Event schema

Events MUST follow a documented schema with validated field types.

### DAT-002: Incident schema

Incidents MUST have stable identifiers and explicit lifecycle states.

Proposed states include:

* Detected.
* Investigating.
* Assessed.
* Response authorized.
* Responding.
* Verification pending.
* Resolved.
* Unresolved.
* Escalated.

The architecture must define valid transitions and prevent inconsistent state changes.

### DAT-003: Action records

Every action record MUST identify the requested operation, target, authorization decision, execution result, and verification status.

### DAT-004: Timestamps

Events and incident records MUST use consistent timestamp conventions.

### DAT-005: Retention

The system MUST define retention and deletion policies for event records, incidents, and diagnostic logs.

### DAT-006: Data minimization

The system MUST avoid collecting unrelated personal information.

### DAT-007: Sensitive information

Secrets, credentials, and unnecessary sensitive content MUST NOT appear in ordinary diagnostic or alert messages.

## 9. Integration requirements

### INT-001: Operating-system integration

The monitoring component MUST use documented interfaces appropriate to the supported Windows environment.

### INT-002: Dashboard integration

The dashboard MUST receive incident updates through a documented interface.

### INT-003: Storage integration

Incident creation and updates MUST use a defined persistence interface.

### INT-004: Optional AI integration

AI-assisted investigation MAY be introduced as an optional component.

Core deterministic detection and policy checks MUST continue to behave predictably when the AI service is unavailable.

### INT-005: Configuration

Environment-specific settings MUST be configurable without modifying application source code.

Configuration must be validated at startup, and secrets must be kept out of source control.

### INT-006: Dataset processing

**Priority:** P0 for the network detection evaluation work.

The project MUST document how CICIDS2017 data is loaded, validated, preprocessed, and evaluated.

Acceptance criteria:

* The actual dataset files and fields are inspected.
* Target labels are documented.
* Invalid or missing values are handled consistently.
* Training and evaluation data are separated appropriately when machine learning is used.
* Data leakage is considered and tested for.
* Evaluation metrics and limitations are recorded.
* Dataset-based results are reported separately from live endpoint detection results.

## 10. Testing requirements

### TST-001: Unit tests

Every critical module MUST have unit tests covering normal, boundary, and failure cases.

### TST-002: Detection tests

Every implemented detection rule MUST have positive and negative test cases.

### TST-003: Policy tests

The response policy MUST be tested against permitted and prohibited actions.

### TST-004: Response tests

Defensive actions MUST be tested in a controlled environment before being enabled on a real computer.

### TST-005: Verification tests

Tests MUST cover successful actions, failed actions, incomplete verification, and continued suspicious behavior.

### TST-006: Integration tests

The detection-to-response workflow MUST be tested with controlled event scenarios.

### TST-007: Regression tests

Previously validated behavior MUST remain functional after changes.

### TST-008: Failure injection

Tests MUST include missing permissions, unavailable services, malformed events, timeouts, and storage failures.

### TST-009: False-positive evaluation

Detection rules MUST be evaluated against representative benign events.

### TST-010: Reproducibility

Tests MUST be reproducible using documented commands and test data.

### TST-011: Dataset evaluation

Network detection experiments MUST document preprocessing, data splitting, metrics, and limitations.

### TST-012: Security boundary tests

Tests MUST verify that untrusted event content, AI output, and unauthorized requests cannot bypass response policy or execute arbitrary commands.

## 11. Operational requirements

### OPS-001: Configuration

The application MUST validate configuration at startup and report invalid settings clearly.

### OPS-002: Startup behavior

The service MUST report whether required monitoring sources and components initialized successfully.

### OPS-003: Shutdown behavior

The service MUST shut down predictably and avoid leaving incomplete state transitions where possible.

### OPS-004: Health status

The application SHOULD expose a health status that distinguishes overall availability from the availability of individual components.

### OPS-005: Diagnostics

Operational errors MUST be recorded without exposing secrets.

### OPS-006: Response mode

The application MUST expose its current operating mode, including whether automated responses are enabled.

### OPS-007: Safe recovery

After restarting, the application MUST recover stored incidents without falsely claiming that unfinished actions were completed.

### OPS-008: Emergency recovery

The operator MUST have a documented way to disable automated response execution when an unsafe condition is detected.

## 12. Initial acceptance criteria

The following scenarios define minimum end-to-end behavior for the initial release.

### Scenario A: Benign event

**Given:** A normal event is collected.

**When:** The event is evaluated.

**Then:**

* The event is processed successfully.
* The system does not invent an unsupported threat.
* No defensive action occurs without authorization.

### Scenario B: Recognized suspicious event

**Given:** A controlled event matches a documented detection rule.

**When:** The event is evaluated.

**Then:**

* A finding is generated.
* The matching rule and evidence are recorded.
* The incident receives an appropriate status.

### Scenario C: Additional investigation

**Given:** An incident requires more evidence.

**When:** The investigation component runs.

**Then:**

* Available context is collected.
* Missing information is recorded.
* The result references its supporting evidence.

### Scenario D: Authorized automated action

**Given:** A controlled test incident satisfies an automated response policy.

**When:** The response engine evaluates the incident.

**Then:**

* The policy permits the action.
* The action operates only on the intended test resource.
* The result is recorded.
* Verification is performed.

### Scenario E: Prohibited action

**Given:** A proposed action falls outside the configured policy.

**When:** The response engine evaluates the request.

**Then:**

* The action is rejected.
* No prohibited side effect occurs.
* The decision is recorded.
* An alert is generated when required by policy.

### Scenario F: Failed response

**Given:** An authorized test action fails.

**When:** The response engine receives the failure.

**Then:**

* The action is not reported as successful.
* The failure is recorded.
* The incident remains unresolved or is escalated as appropriate.
* The configured failure policy is followed.

### Scenario G: Continuing threat

**Given:** Suspicious behavior continues after an attempted response.

**When:** Follow-up monitoring detects the behavior.

**Then:**

* The new event is associated with the incident where appropriate.
* The incident is updated.
* The system does not falsely declare the threat eliminated.

### Scenario H: Emergency stop

**Given:** Automated response is disabled.

**When:** A new incident would normally trigger an automated action.

**Then:**

* No automated response is executed.
* Detection and logging continue where available.
* The operating mode remains visible.

### Scenario I: Component failure

**Given:** A required component becomes unavailable.

**When:** The system attempts to process an event or response.

**Then:**

* The failure is recorded.
* Authorization controls are not bypassed.
* The affected capability is reported as unavailable.
* Recovery follows the documented policy.

### Scenario J: CICIDS2017 evaluation

**Given:** The documented dataset and evaluation configuration are available.

**When:** The network detection evaluation runs.

**Then:**

* Input data is validated.
* Preprocessing follows the documented procedure.
* Evaluation uses the defined data split.
* Results include the selected metrics.
* Limitations are recorded.
* The results are not presented as proof of live endpoint detection.

## 13. Requirement traceability

Every implemented requirement must be traceable through this chain:

**Requirement → Design component → Implementation → Test case → Verification result**

Examples:

| Requirement | Design component        | Example verification                             |
| ----------- | ----------------------- | ------------------------------------------------ |
| FR-002      | Event processing        | Schema-validation tests                          |
| FR-004      | Detection engine        | Rule-matching tests                              |
| FR-011      | Risk assessment         | Severity boundary tests                          |
| FR-014      | Policy engine           | Authorization tests                              |
| FR-020      | Verification component  | Post-action verification tests                   |
| FR-022      | Alerting                | Alert-delivery tests                             |
| SEC-005     | AI integration boundary | AI-output validation and command-injection tests |
| INT-006     | Dataset processing      | Reproducible dataset evaluation                  |
| TST-012     | Security testing        | Attempts to bypass policy restrictions           |

The traceability record must be updated as implementation progresses.

A requirement must not be marked complete merely because a corresponding file or class exists.

## 14. Assumptions and constraints

The initial design assumes that:

1. Windows is the initial target platform.
2. Python is the primary implementation language.
3. The first deployment targets one computer.
4. Monitoring capabilities depend on available operating-system interfaces and permissions.
5. The initial detection engine uses deterministic rules.
6. AI integration is optional for the core workflow.
7. Automated responses are restricted by explicit policy.
8. Dangerous response scenarios are initially simulated in controlled tests.
9. Administrative privileges are not always available.
10. Performance targets will be validated through measurement.
11. CICIDS2017 supports network detection evaluation but does not replace endpoint telemetry.
12. Proposed technology choices remain subject to architecture review.

Changes to these assumptions must be reflected in the relevant project documents.

## 15. Requirement change management

Requirements may change when implementation reveals technical constraints or testing identifies weaknesses.

Each change MUST:

1. Identify the affected requirement.
2. Explain the reason for the change.
3. Identify security and compatibility implications.
4. Update the relevant documentation.
5. Update acceptance criteria and tests where necessary.
6. Record significant architectural decisions in `docs/ARCHITECTURAL_DECISION_LOG.md`.

Security controls must not be weakened simply to make a test pass.

## 16. Definition of done

A requirement is complete only when:

* Its implementation exists.
* Its behavior matches the documented requirement.
* Relevant automated tests pass.
* Failure behavior has been evaluated.
* Security implications have been considered.
* Documentation has been updated.
* The result has been verified.

A successful build or the presence of a source file does not establish completion.

## 17. Current status and next steps

**Document status:** Draft, pending review.

**Project phase:** Planning and documentation.

**Implementation status:** This specification does not establish which application components have been implemented or tested.

Before implementation begins, the project should:

1. Review this specification against `docs/PROJECT_OVERVIEW.md`.
2. Resolve conflicts between the requirements and existing design documents.
3. Confirm the initial Windows monitoring scope.
4. Inspect the available CICIDS2017 files and confirm the evaluation plan.
5. Review `docs/SYSTEM_ARCHITECTURE.MD` and `docs/THREAT_MODEL.md`.
6. Confirm response boundaries and failure behavior.
7. Define measurable performance targets using the intended test environment.
8. Maintain traceability between requirements, implementation, and tests.

The system architecture should explain how these requirements map to components and how data moves through the detection, investigation, authorization, response, and verification workflow.
