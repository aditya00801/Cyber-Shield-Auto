# CyberShield-Auto

## System Architecture Document

**Project:** CyberShield-Auto
**Document:** System Architecture
**Version:** 1.0
**Status:** Draft — Pending Review
**Architecture Style:** Modular, Layered, Event-Driven
**Initial Platform:** Windows
**Primary Language:** Python
**Deployment Target:** Single computer
**Development Stage:** Documentation and Planning

---

# 1. Purpose

This document defines the proposed technical architecture of CyberShield-Auto.

It identifies the system's major components, their responsibilities, communication interfaces, data flow, security boundaries, failure-handling requirements, and deployment structure.

The architecture translates the project's objectives and requirements into an implementation blueprint.

The primary architectural goal is to create a defensive security system that can:

1. Monitor security-relevant system events.
2. Detect suspicious behavior.
3. Investigate potential threats.
4. Assess threat severity and confidence.
5. Select authorized defensive actions.
6. Execute permitted actions automatically.
7. Verify response outcomes.
8. Generate real-time alerts.
9. Maintain an auditable incident history.

The architecture must support these capabilities without granting unrestricted system access to AI components.

# 2. Architectural Principles

The following principles govern the design.

## 2.1 Modularity

Each component must have a clearly defined responsibility.

Monitoring, detection, investigation, risk assessment, response authorization, response execution, verification, and alerting must remain logically separate.

## 2.2 Separation of Detection and Response

Detecting suspicious activity must not automatically authorize a system-changing action.

All automated responses must pass through a dedicated policy enforcement component.

## 2.3 Least Privilege

Components must operate with only the permissions they require.

The event collector should not automatically receive permission to terminate processes or modify files.

Privileged operations should be isolated behind a restricted response interface.

## 2.4 Evidence-Based Decisions

Detection results and response recommendations must reference observable evidence.

An AI-generated explanation is not sufficient evidence by itself.

## 2.5 Controlled Autonomy

The system must support unattended execution of explicitly authorized defensive actions.

It must reject actions outside the configured policy.

## 2.6 Fail-Safe Behavior

Failures must not bypass security controls.

If the policy engine is unavailable, automated response execution must fail closed.

## 2.7 Testability

Every major component must be testable independently.

The architecture must support simulated events, deterministic tests, and isolated response testing.

## 2.8 Platform Isolation

Windows-specific monitoring and response operations must be separated from platform-independent detection and incident-management logic.

This will make future Linux support easier to introduce.

---

# 3. High-Level Architecture

The system is organized into seven logical layers.

```text
+-------------------------------------------------------+
|                   USER INTERFACE                      |
|                                                       |
|              Security Dashboard                       |
|              Real-Time Alerts                          |
|              Incident History                          |
+--------------------------+----------------------------+
                           |
                           v
+-------------------------------------------------------+
|                INCIDENT MANAGEMENT                    |
|                                                       |
|       Incident State Manager | Alert Dispatcher        |
+--------------------------+----------------------------+
                           |
                           v
+-------------------------------------------------------+
|              RESPONSE VERIFICATION                    |
|                                                       |
|         Action Result | Outcome Verification           |
+--------------------------+----------------------------+
                           |
                           v
+-------------------------------------------------------+
|              RESPONSE EXECUTION                       |
|                                                       |
|       Policy Enforcement | Action Dispatcher           |
|       Restricted Response Adapters                     |
+--------------------------+----------------------------+
                           ^
                           |
+-------------------------------------------------------+
|              RISK AND INVESTIGATION                   |
|                                                       |
|       Investigation Engine | Risk Assessment           |
|       Evidence Correlation | Response Recommendation   |
+--------------------------+----------------------------+
                           ^
                           |
+-------------------------------------------------------+
|              THREAT DETECTION                          |
|                                                       |
|       Rule Engine | Detection Scoring                  |
|       Detection Evidence | Incident Candidates         |
+--------------------------+----------------------------+
                           ^
                           |
+-------------------------------------------------------+
|              EVENT PROCESSING                          |
|                                                       |
|       Event Validation | Normalization                 |
|       Deduplication | Filtering                        |
+--------------------------+----------------------------+
                           ^
                           |
+-------------------------------------------------------+
|              OPERATING-SYSTEM MONITORING               |
|                                                       |
|       Windows Event Sources | Process Metadata         |
|       Selected File Events | Network Metadata          |
+-------------------------------------------------------+

          Shared Infrastructure:
          Database | Audit Logging | Configuration
          Health Monitoring | Policy Store
```

This diagram represents logical relationships, not necessarily separate operating-system processes.

The initial implementation should use a modular Python application wherever possible. Separate services should be introduced only when they provide a clear operational or security benefit.

# 4. Major System Components

## 4.1 Windows Monitoring Adapter

**Responsibility:** Collect security-relevant events from supported Windows interfaces.

Potential event sources include:

* Windows security event logs.
* Process creation events.
* Selected file-system events.
* Network connection metadata.
* Relevant operating-system configuration changes.

The specific sources must be confirmed during implementation planning.

### Responsibilities

1. Initialize configured event sources.
2. Collect available events.
3. Convert source-specific data into internal event objects.
4. Report collection failures.
5. Track event timestamps and source identifiers.
6. Avoid collecting unnecessary personal information.

### Restrictions

The monitoring adapter must not execute defensive actions.

It must not assume that administrative permissions are available.

If an event source is unavailable, the system must report the resulting monitoring limitation.

## 4.2 Event Processing Engine

**Responsibility:** Convert collected observations into validated, normalized events.

### Responsibilities

* Validate event schemas.
* Normalize timestamps and field names.
* Assign internal event identifiers.
* Handle malformed input.
* Deduplicate events where appropriate.
* Filter irrelevant events according to configuration.
* Forward valid events to the detection engine.

### Output

A normalized event object containing the fields needed for subsequent analysis.

The original source event should remain available when it is necessary for investigation, subject to the data-retention policy.

## 4.3 Threat Detection Engine

**Responsibility:** Identify suspicious activity using documented detection rules.

The first version will prioritize deterministic rules.

### Responsibilities

* Evaluate incoming events.
* Match event patterns against configured rules.
* Identify the rule responsible for a detection.
* Record supporting evidence.
* Assign a detection score where appropriate.
* Produce a structured detection result.

### Output

A detection result containing:

* Detection identifier.
* Related event identifiers.
* Detection rule identifier.
* Threat category.
* Evidence.
* Initial severity assessment.
* Confidence information.
* Recommended investigation level.

The detection engine must not execute system-changing actions.

## 4.4 Investigation Engine

**Responsibility:** Gather additional context about suspicious activity.

### Responsibilities

* Retrieve relevant event history.
* Examine available process metadata.
* Correlate related events.
* Collect associated file or network metadata.
* Identify missing information.
* Construct an evidence record.
* Produce a structured investigation result.

### Investigation Result

The result must distinguish:

* Observed facts.
* Rule-derived conclusions.
* Inferences.
* Missing evidence.
* Investigation errors.

AI assistance may be added to summarize evidence, but AI output must remain separate from the underlying evidence record.

## 4.5 Risk Assessment Engine

**Responsibility:** Determine the incident's potential severity and the confidence of the available evidence.

The engine should evaluate:

* Evidence strength.
* Threat severity.
* Potential impact.
* Scope of affected resources.
* Whether suspicious behavior is continuing.
* Possible false positives.
* Potential consequences of a response.

### Output

A structured risk assessment containing:

* Incident identifier.
* Severity.
* Confidence.
* Supporting evidence.
* Uncertainties.
* Recommended response category.
* Required authorization conditions.

Severity and confidence must be separate fields.

A severe potential impact combined with uncertain evidence should trigger further investigation or a carefully selected containment policy rather than automatically authorize destructive action.

## 4.6 Response Policy Engine

**Responsibility:** Decide whether a proposed defensive action is permitted.

This component is a critical security boundary.

### Responsibilities

1. Receive a structured action proposal.
2. Validate the proposed action.
3. Verify that the action type is supported.
4. Check the applicable policy.
5. Evaluate evidence and authorization conditions.
6. Check the current operating mode.
7. Check whether the emergency stop is active.
8. Reject unauthorized actions.
9. Record the authorization decision.

### Example

A detection engine identifies a suspicious process.

The risk assessment engine recommends terminating it.

The policy engine checks:

* Is process termination an enabled action?
* Does the incident satisfy the required evidence threshold?
* Is the process an eligible target?
* Is the action permitted in the current operating mode?
* Does the action comply with restrictions on critical processes?
* Is the required authorization available?

Only after these checks may the response executor receive the approved action.

The policy engine must not rely solely on an AI-generated recommendation.

## 4.7 Response Execution Engine

**Responsibility:** Perform authorized defensive operations.

The executor will use restricted response adapters.

Possible initial adapters include:

* Process termination for eligible targets.
* File quarantine in a controlled location.
* Recording an incident without changing system state.

Additional adapters may be implemented after their security and recovery requirements have been documented.

### Responsibilities

* Validate the approved action request.
* Verify the target identity.
* Confirm the authorization decision.
* Execute the permitted operation.
* Apply timeouts where appropriate.
* Record execution results.
* Report failures.

### Restrictions

The executor must not accept arbitrary shell commands generated by an AI model.

It must not silently expand the scope of an authorized action.

It must not treat a failed authorization check as permission to proceed.

## 4.8 Verification Engine

**Responsibility:** Verify whether an executed action achieved its intended outcome.

### Responsibilities

* Retrieve the action's verification procedure.
* Inspect the relevant system state.
* Compare the observed state with the expected result.
* Record verification evidence.
* Identify incomplete or failed outcomes.
* Update the incident lifecycle.

### Example

After terminating an eligible process, the verification engine checks whether the process is no longer running.

If the process has stopped, the engine records that specific outcome.

It must not conclude that the entire threat has been eliminated unless the available evidence supports that broader conclusion.

## 4.9 Incident Management Engine

**Responsibility:** Maintain the lifecycle of security incidents.

Suggested incident states include:

* Detected.
* Investigating.
* Assessed.
* Response Authorized.
* Responding.
* Verification Pending.
* Resolved.
* Unresolved.
* Escalated.

### Responsibilities

* Create incident records.
* Associate related detections.
* Track investigation progress.
* Record policy decisions.
* Track response actions.
* Record verification results.
* Maintain consistent state transitions.
* Prevent unsupported transitions.

Incident status changes must be recorded in the audit history.

## 4.10 Alert Dispatcher

**Responsibility:** Deliver security notifications.

### Responsibilities

* Generate structured alerts.
* Notify the dashboard about new incidents.
* Update alert status as the incident progresses.
* Include relevant evidence summaries.
* Report notification failures.
* Avoid exposing credentials or unnecessary sensitive information.

The initial version will prioritize local dashboard notifications.

External notifications can be considered later.

## 4.11 Database Layer

**Responsibility:** Persist events, incidents, action records, and audit information.

SQLite is proposed for the initial local implementation.

The database layer should expose application-level interfaces so that the storage technology can be replaced later without rewriting the detection and response engines.

## 4.12 Dashboard

**Responsibility:** Present the system's security state to the user.

The dashboard should display:

* Current monitoring status.
* Recent detections.
* Incident severity.
* Investigation findings.
* Response decisions.
* Action execution status.
* Verification results.
* Incident history.
* Component health.
* Current automated-response mode.

The interface must clearly distinguish detected threats from verified remediation outcomes.

---

# 5. End-to-End Data Flow

The normal processing sequence is as follows.

## Step 1: Event Collection

A Windows monitoring adapter observes a supported security event.

## Step 2: Event Validation

The event processing engine validates the event and converts it into the internal schema.

Invalid events are handled according to the error policy.

## Step 3: Detection

The detection engine evaluates the normalized event against configured rules.

If no rule matches, the event may be retained according to the data policy without creating an incident.

## Step 4: Investigation

If a rule matches and investigation is required, the investigation engine gathers relevant context.

## Step 5: Risk Assessment

The risk assessment engine evaluates the available evidence and determines severity, confidence, and potential impact.

## Step 6: Response Recommendation

The risk assessment engine produces a structured recommendation.

A recommendation does not grant permission to execute an action.

## Step 7: Policy Evaluation

The response policy engine evaluates the proposed action against the configured policy and current operating mode.

If the action is prohibited, execution stops and the decision is recorded.

## Step 8: Response Execution

If the action is authorized, the response executor performs the permitted operation.

## Step 9: Verification

The verification engine checks the intended outcome.

## Step 10: Incident Update

The incident manager updates the incident state and stores the response and verification results.

## Step 11: Alert Delivery

The alert dispatcher notifies the dashboard.

## Step 12: Continued Monitoring

The monitoring system continues collecting relevant events.

If suspicious activity returns, the system can update the existing incident or create a related incident according to its correlation rules.

---

# 6. Core Data Contracts

The following structures describe the logical contracts between components.

They are conceptual definitions; their exact Python schemas will be specified during implementation design.

## 6.1 Security Event

```text
SecurityEvent
    event_id
    timestamp
    source
    event_type
    process_metadata
    file_metadata
    account_metadata
    network_metadata
    attributes
```

Optional fields depend on the event category.

Sensitive fields must be minimized according to the privacy policy.

## 6.2 Detection Result

```text
DetectionResult
    detection_id
    event_ids
    rule_id
    threat_category
    evidence
    severity
    confidence
    created_at
```

## 6.3 Investigation Result

```text
InvestigationResult
    investigation_id
    incident_id
    evidence_references
    findings
    missing_information
    investigation_status
    completed_at
```

## 6.4 Risk Assessment

```text
RiskAssessment
    assessment_id
    incident_id
    severity
    confidence
    evidence_references
    uncertainty
    recommended_action
    authorization_requirements
```

## 6.5 Response Request

```text
ResponseRequest
    action_id
    incident_id
    action_type
    target_reference
    justification
    evidence_references
    requested_by
    created_at
```

The request must identify an action type and a structured target. It must not contain an unrestricted command string intended for direct execution.

## 6.6 Authorization Decision

```text
AuthorizationDecision
    decision_id
    action_id
    permitted
    policy_id
    reason
    evaluated_at
```

## 6.7 Response Result

```text
ResponseResult
    action_id
    execution_status
    started_at
    completed_at
    result_summary
    error_code
```

## 6.8 Verification Result

```text
VerificationResult
    verification_id
    action_id
    verification_status
    observed_state
    expected_state
    evidence_references
    verified_at
```

---

# 7. AI Integration Architecture

AI is an optional assistance layer, not the authority responsible for controlling the computer.

The initial implementation should work without an external AI service.

## 7.1 Permitted AI Responsibilities

An AI component may eventually:

* Summarize collected evidence.
* Explain why a detection rule matched.
* Identify potentially relevant relationships between events.
* Suggest additional investigation steps.
* Produce a human-readable incident report.

## 7.2 Restricted AI Responsibilities

The AI component must not independently:

* Execute operating-system commands.
* Bypass response policies.
* Grant itself additional privileges.
* Modify authorization rules.
* Declare an action successful without verification.
* Treat untrusted event data as instructions.

## 7.3 AI Failure Handling

If an AI service is unavailable or produces invalid output:

* Deterministic detection must continue where possible.
* Policy enforcement must remain operational.
* Unauthorized actions must remain prohibited.
* AI-dependent functions must report their degraded status.
* The system must not invent missing evidence.

## 7.4 Recommended Initial Approach

Begin with deterministic rules, structured investigation, and policy-based responses.

Introduce AI only after the core detection-to-response workflow is reliable and measurable.

---

# 8. Security Boundaries

The architecture contains four important trust boundaries.

## Boundary 1: Operating System to Monitoring

Collected events must be treated as untrusted input.

The system must validate event fields and avoid interpreting event content as executable instructions.

## Boundary 2: Detection to Decision

Detection results must not directly authorize system-changing operations.

The risk assessment and policy components must evaluate the available evidence.

## Boundary 3: Policy to Response Executor

Only validated and authorized action requests may reach the privileged response interface.

The executor must independently validate the request and its target.

## Boundary 4: AI to Core Security Logic

AI-generated text must not be trusted as executable instructions or as proof that a threat exists.

Structured output validation and independent policy enforcement are mandatory.

---

# 9. Failure Handling

The architecture must account for failures in each major component.

| Failure                       | Expected behavior                                                            |
| ----------------------------- | ---------------------------------------------------------------------------- |
| Monitoring source unavailable | Report reduced coverage and continue supported monitoring                    |
| Malformed event               | Reject or isolate the event and record the error                             |
| Detection engine failure      | Record the failure and report degraded detection capability                  |
| Investigation incomplete      | Record missing evidence and avoid unsupported conclusions                    |
| Risk assessment unavailable   | Do not authorize actions requiring that assessment                           |
| Policy engine unavailable     | Reject automated response execution                                          |
| Response execution failure    | Record failure and update the incident                                       |
| Verification inconclusive     | Mark the outcome inconclusive or unresolved                                  |
| Database unavailable          | Apply a documented persistence-failure policy and avoid false success claims |
| Dashboard unavailable         | Continue supported backend processing and record notification failures       |
| AI service unavailable        | Continue deterministic security functions where possible                     |

The system must not silently treat a failed component as if it succeeded.

---

# 10. Concurrency and Event Processing

The initial architecture should minimize concurrency complexity.

A modular Python application can use a controlled event-processing pipeline.

Potential implementation mechanisms include:

* A bounded in-process queue.
* Dedicated workers for event processing.
* Asynchronous I/O where beneficial.
* Separate handling for slower investigation tasks.

The selected design must prevent unbounded memory growth.

High-impact response operations should not be launched concurrently without considering whether they target the same resource or incident.

Duplicate event handling and action idempotency must be designed before enabling automatic responses.

A distributed message broker is not required for the initial single-computer release.

---

# 11. Storage Architecture

The initial database will use SQLite unless implementation constraints justify another choice.

Suggested logical records include:

* Security events.
* Detections.
* Incidents.
* Investigation results.
* Risk assessments.
* Authorization decisions.
* Response actions.
* Verification results.
* Audit records.
* Application health events.

Relationships between records must be traceable through stable identifiers.

The database schema must support incident history and response auditing without storing unnecessary copies of sensitive event content.

Database migrations must be versioned so that future releases can update the schema predictably.

---

# 12. Configuration Architecture

Configuration must be external to application source code.

Configuration categories include:

* Monitoring settings.
* Detection rules.
* Event-retention limits.
* Database location.
* Dashboard settings.
* Logging settings.
* Response policies.
* Automated-response mode.
* Optional AI-service settings.
* Timeouts and processing limits.

Secrets must not be committed to version control.

Invalid configuration must produce a clear startup error.

The development default must not enable high-impact automated actions.

Changes to sensitive response policies must be auditable.

---

# 13. Deployment Architecture

## 13.1 Initial Deployment

The first version will run on one Windows computer.

Its logical components may include:

* A Python monitoring service.
* A local event-processing pipeline.
* A local database.
* A backend API if needed.
* A local dashboard.
* A restricted response interface.

The exact process layout will be finalized during implementation planning.

## 13.2 Future Multi-Computer Deployment

Future versions may introduce:

* A local agent on each authorized computer.
* An authenticated communication channel.
* A central incident-management server.
* A shared database.
* A central dashboard.
* A policy distribution mechanism.

This expansion will require additional threat modeling, mutual authentication where appropriate, transport encryption, authorization controls, and secure update procedures.

It is not part of the initial implementation.

---

# 14. Testing Architecture

Each component must expose interfaces that allow deterministic testing.

## 14.1 Monitoring Tests

Test event parsing, missing sources, permission failures, and event normalization.

## 14.2 Detection Tests

Test rule matches, non-matches, boundary conditions, and false-positive scenarios.

## 14.3 Investigation Tests

Test evidence collection, missing context, and event correlation.

## 14.4 Policy Tests

Test authorized actions, prohibited actions, emergency-stop behavior, and invalid requests.

## 14.5 Response Tests

Use mock executors and isolated test targets to verify action behavior.

## 14.6 Verification Tests

Test successful, failed, incomplete, and inconclusive outcomes.

## 14.7 End-to-End Tests

Feed controlled events into the system and verify the complete detection-to-response workflow.

Tests must verify not only that expected actions occur, but also that prohibited actions do not occur.

---

# 15. Proposed Project Package Structure

The implementation structure will be finalized after the remaining requirements and threat model are reviewed.

The following is a proposed direction, not a list of files that already exist.

```text
CyberShield-Auto/
│
├── README.md
├── AGENTS.md
├── PROJECT_MEMORY.md
├── CHANGELOG.md
├── .env.example
├── pyproject.toml
│
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── PROJECT_REQUIREMENTS.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── THREAT_MODEL.md
│   ├── THREAT_DETECTION_ENGINE.md
│   ├── AI_AGENT_DESIGN.md
│   ├── AUTOMATED_RESPONSE_POLICY.md
│   ├── ALERTING_AND_MONITORING.md
│   ├── DATA_STORAGE_AND_PRIVACY.md
│   ├── API_SPECIFICATION.md
│   ├── SECURITY_REQUIREMENTS.md
│   ├── TESTING_STRATEGY.md
│   ├── DEVELOPMENT_ROADMAP.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── ARCHITECTURAL_DECISION_LOG.md
│
├── src/
│   └── cybershield/
│       ├── monitoring/
│       ├── events/
│       ├── detection/
│       ├── investigation/
│       ├── risk/
│       ├── policies/
│       ├── response/
│       ├── verification/
│       ├── incidents/
│       ├── alerts/
│       ├── storage/
│       ├── api/
│       └── dashboard/
│
└── tests/
    ├── unit/
    ├── integration/
    ├── simulation/
    └── security/
```

Directory names are provisional and will be refined before implementation begins.

# 16. Architectural Decisions Requiring Confirmation

The following decisions remain open.

| Decision               | Initial proposal           | Status                     |
| ---------------------- | -------------------------- | -------------------------- |
| Deployment             | Single Windows computer    | Proposed                   |
| Architecture           | Modular Python application | Proposed                   |
| Detection              | Deterministic rules first  | Proposed                   |
| Storage                | SQLite                     | Proposed                   |
| Dashboard              | Streamlit                  | Proposed                   |
| API                    | FastAPI where required     | Proposed                   |
| AI                     | Optional assistance layer  | Proposed                   |
| Response authorization | Independent policy engine  | Required design constraint |
| Event processing       | Bounded local pipeline     | Proposed                   |
| Multi-computer support | Future extension           | Deferred                   |

These decisions should be recorded in `docs/ARCHITECTURAL_DECISION_LOG.md` when approved.

# 17. Architecture Acceptance Criteria

The architecture will be ready for implementation when:

1. Every major component has a defined responsibility.
2. Component inputs and outputs are documented.
3. The end-to-end event flow is specified.
4. Response authorization is independent of detection and AI recommendations.
5. Privileged operations are isolated behind a restricted interface.
6. Failure behavior is defined for critical components.
7. Event, incident, action, and verification records have stable identifiers.
8. The storage model supports incident traceability.
9. The testing approach covers both allowed and prohibited behavior.
10. The initial deployment model is documented.
11. Open architectural decisions are recorded.
12. The architecture satisfies the approved project requirements.

---

# 18. Current Status

**Document status:** Draft — Pending Review.

**Implementation status:** No implementation is established by this document.

**Next document:** `docs/THREAT_MODEL.md`.

The threat model will identify threats against the monitored computer, threats against CyberShield-Auto itself, abuse of automated response capabilities, and the controls required to reduce those risks.

The architecture must be reviewed against the threat model before high-impact automated response functionality is implemented.
