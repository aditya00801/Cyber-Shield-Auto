# Threat Detection Engine Specification

**Project:** CyberShield-Auto
**Document status:** Draft
**Target platform:** Windows
**Implementation language:** Python

## 1. Purpose

The Threat Detection Engine monitors security events, identifies suspicious activity, and produces structured findings for further investigation.

It is the first security analysis component in CyberShield-Auto. It receives events from approved monitoring sources, validates their data, evaluates detection rules, and records evidence when an event matches a known suspicious pattern.

The engine must explain why it flagged an event. Each finding should contain the relevant evidence, detection rule, severity, confidence, and recommended next steps when sufficient information is available.

The engine does not execute defensive actions. It passes its findings to the investigation and policy components, which determine what should happen next.

## 2. Scope

The initial version will use rule-based detection. This approach is easier to test, explain, and debug while the project establishes its event-processing and investigation workflows.

### 2.1 Included in the initial scope

* Validate and normalize incoming security events.
* Detect suspicious behavior using configurable rules.
* Identify known suspicious file indicators.
* Detect unusual process activity when the required telemetry is available.
* Identify repeated authentication failures when suitable Windows event data is available.
* Evaluate suspicious network activity using available connection metadata.
* Detect unexpected changes to selected persistence locations.
* Correlate related events when they share relevant identifiers or occur within a defined time window.
* Assign severity and confidence scores separately.
* Record evidence and explain why a rule matched.
* Deduplicate repeated findings.
* Send detection results to the investigation and alerting components.
* Maintain an auditable record of detection decisions.

### 2.2 Excluded from the initial scope

The initial engine will not:

* Execute commands on the operating system.
* Terminate processes or quarantine files.
* Modify Windows security settings.
* Disable accounts or change permissions.
* Treat an AI-generated explanation as proof of malicious activity.
* Claim that an event is malicious when the available evidence only establishes that it is unusual.

Defensive actions belong to the separate response-policy and execution components.

## 3. Design principles

The engine must follow these principles throughout implementation.

**Evidence-based detection:** Every finding must identify the event data or rule conditions that triggered it.

**Explainable decisions:** A developer or analyst must be able to understand why the engine generated a finding.

**Separation of responsibilities:** Detection identifies suspicious activity. Investigation adds context. The policy engine authorizes any proposed response.

**Configurable rules:** Detection thresholds and rule settings should be adjustable without rewriting the entire engine.

**Failure visibility:** Invalid events, unavailable data sources, and processing errors must be recorded. A processing failure must never be reported as a clean security result.

**Controlled automation:** The engine must not have unrestricted permission to change the system.

**Testability:** Each rule should be testable with known matching and non-matching events.

## 4. High-level processing flow

The detection pipeline follows this sequence:

1. Receive an event from an approved source.
2. Validate the event structure and required fields.
3. Normalize timestamps, event types, and relevant identifiers.
4. Reject malformed events or route them to an error record.
5. Select detection rules applicable to the event.
6. Evaluate the rules against the event and available context.
7. Create findings for matching rules.
8. Calculate severity and confidence independently.
9. Correlate related findings when the required evidence is available.
10. Deduplicate repeated findings.
11. Store the findings and their supporting evidence.
12. Publish the results to the investigation and alerting components.

The pipeline should preserve the original event or an appropriate evidence reference so that investigators can trace a finding back to its source.

## 5. Event data model

All supported monitoring sources should produce events in a common format before the engine evaluates them.

A proposed event schema is shown below. The final Pydantic model should enforce the required fields and their validation rules.

```python
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SecurityEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime
    source: str

    host_id: str
    severity_hint: str | None = None

    process_id: int | None = None
    process_name: str | None = None
    file_path: str | None = None
    file_hash: str | None = None

    source_ip: str | None = None
    destination_ip: str | None = None
    destination_port: int | None = Field(
        default=None,
        ge=1,
        le=65535,
    )

    username: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)
```

This is a proposed schema, not an implemented feature.

The schema should be refined as the supported Windows event sources are selected. For example, authentication events, process events, and network events will not necessarily populate the same fields.

### 5.1 Field requirements

| Field              | Requirement | Purpose                                          |
| ------------------ | ----------- | ------------------------------------------------ |
| `event_id`         | Required    | Identifies the event within the ingestion system |
| `event_type`       | Required    | Describes the event category                     |
| `timestamp`        | Required    | Establishes when the event occurred              |
| `source`           | Required    | Identifies the event's origin                    |
| `host_id`          | Required    | Identifies the monitored endpoint                |
| `process_id`       | Optional    | Associates activity with a process               |
| `process_name`     | Optional    | Provides process context                         |
| `file_path`        | Optional    | Identifies a file involved in the event          |
| `file_hash`        | Optional    | Supports file-indicator matching                 |
| `source_ip`        | Optional    | Identifies a network source                      |
| `destination_ip`   | Optional    | Identifies a network destination                 |
| `destination_port` | Optional    | Identifies the destination service port          |
| `username`         | Optional    | Associates activity with an account              |
| `details`          | Optional    | Stores additional source-specific evidence       |

Optional fields must remain optional because different event sources provide different information.

The engine must not invent missing values or treat an absent field as evidence of suspicious activity.

## 6. Detection rule system

Detection rules define the conditions under which an event should generate a finding.

Each rule should have a stable identifier, a description, a category, a severity, an enabled state, and a testable matching function.

A conceptual rule definition could look like this:

```python
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class DetectionRule:
    rule_id: str
    name: str
    description: str
    category: str
    severity: str
    enabled: bool
    match: Callable[[dict[str, Any]], bool]
```

This example illustrates the intended structure. The final implementation should use the project's validated event and rule models rather than relying on unvalidated dictionaries throughout the pipeline.

### 6.1 Rule requirements

Every production detection rule must:

* Have a unique and stable identifier.
* State what behavior it detects.
* Define the event types it supports.
* Specify the evidence required for a match.
* Handle missing or malformed data safely.
* Produce a reproducible result for the same input and rule configuration.
* Include tests for matching, non-matching, and incomplete events.
* Document known false-positive conditions.
* Have a defined severity and confidence policy.
* Be possible to enable or disable through approved configuration.

A rule should not match simply because a field contains an unusual value. Its conditions must have a documented security rationale.

## 7. Initial detection categories

The following categories are proposed for the first implementation. Their availability depends on the monitoring sources and telemetry that the project successfully integrates.

### 7.1 Suspicious process activity

The engine evaluates process events for known or clearly defined suspicious patterns.

Potential indicators include:

* A process matching a documented suspicious execution pattern.
* Unexpected relationships between a parent process and its child process.
* Execution associated with a known malicious indicator.
* Multiple related process events that satisfy a defined detection rule.

A process name alone is generally insufficient to establish malicious activity. The engine should consider other available evidence, such as the executable path, process relationships, file reputation, and relevant event context.

### 7.2 Known malicious file indicators

The engine checks available file metadata against configured indicators.

Possible evidence includes:

* A file hash matching a trusted, documented malicious indicator.
* A file associated with a previously confirmed incident.
* File activity matching a specific, documented suspicious pattern.

Hash matching depends on the quality and freshness of the indicator source. A matching hash should include the source and context of the indicator whenever that information is available.

A filename or directory path alone should not be treated as definitive proof of malware.

### 7.3 Repeated authentication failures

The engine evaluates authentication events to identify repeated failures that may indicate password guessing or another account-access threat.

A rule may consider:

* The number of failed attempts.
* The observation window.
* The account involved.
* The source address, when available.
* Whether a successful authentication followed the failures.

Thresholds should be configurable. For example, a rule might detect several failures against the same account within a defined time window. The initial threshold must be validated against realistic test data before being treated as a reliable detection setting.

### 7.4 Suspicious network activity

The engine evaluates available connection metadata against defined indicators and behavioral rules.

Potential indicators include:

* Connections to known malicious destinations.
* Repeated connection attempts matching a documented suspicious pattern.
* Unexpected network activity associated with a process that already has other suspicious indicators.

A destination's unfamiliarity alone does not establish that a connection is malicious. Detection rules should use relevant context and record the evidence supporting each match.

### 7.5 Unexpected persistence changes

The engine monitors selected Windows persistence locations when an approved event source provides the necessary telemetry.

Possible sources include changes to configured startup locations or selected registry keys.

The initial implementation should monitor a deliberately limited set of locations. It should record the changed object, the available initiating-process information, and the time of the change.

An unexpected change should trigger investigation according to the rule's evidence and severity. The engine should not automatically delete entries or modify registry settings.

### 7.6 Correlated suspicious behavior

Some threats become apparent only when several events are considered together.

For example, repeated authentication failures followed by a successful login and suspicious process activity may justify a higher-priority investigation than any individual event would.

Correlation rules should specify:

* Which event types are relevant.
* Which fields connect the events.
* The allowed time window.
* The required event sequence or combination.
* The evidence needed to create a correlated finding.
* How repeated or overlapping matches are handled.

Correlation must not imply causation unless the evidence supports that conclusion.

## 8. Detection findings

When a rule matches, the engine creates a structured finding.

A proposed finding schema is:

```python
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class DetectionFinding(BaseModel):
    finding_id: str
    rule_id: str
    title: str
    description: str

    category: str
    severity: Literal[
        "informational",
        "low",
        "medium",
        "high",
        "critical",
    ]

    confidence: float = Field(ge=0.0, le=1.0)

    event_ids: list[str]
    evidence: list[dict[str, Any]]

    detected_at: datetime
    host_id: str

    status: Literal[
        "new",
        "under_investigation",
        "resolved",
        "false_positive",
    ] = "new"
```

The final schema may require additional fields as the incident-management workflow develops.

### 8.1 Finding requirements

Every finding must:

* Reference the rule that produced it.
* Identify the affected host.
* Reference the source events or preserve equivalent evidence.
* Include a severity classification.
* Include a confidence score.
* Record when the finding was created.
* Support investigation and resolution tracking.
* Preserve the distinction between a detection result and a confirmed incident.

The engine must not label an event as confirmed malware solely because a rule matched.

## 9. Severity and confidence

Severity and confidence represent different properties and must be calculated separately.

**Severity** describes the potential impact or urgency associated with the detected behavior.

**Confidence** describes how strongly the available evidence supports the detection rule's conclusion.

A high-severity finding can have low confidence when the possible impact is serious but the evidence is incomplete. Such a finding may need urgent investigation without justifying an automatic system-changing action.

### 9.1 Proposed severity levels

| Level         | Meaning                                                                         | Example                                                          |
| ------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Informational | Activity is worth recording but does not currently indicate a meaningful threat | A routine event relevant to security auditing                    |
| Low           | Limited suspicious evidence with low apparent impact                            | An isolated event matching a weak indicator                      |
| Medium        | Suspicious behavior warrants investigation                                      | Repeated failures that exceed a configured threshold             |
| High          | Strong evidence of potentially serious malicious activity                       | Multiple related indicators associated with a suspicious process |
| Critical      | Evidence indicates a potentially severe or active security incident             | A confirmed high-impact threat with strong supporting evidence   |

These examples are provisional. Actual severity assignments must be tied to documented rules and tested conditions.

### 9.2 Confidence scoring

Confidence must follow a documented rule-specific policy. It should not be generated arbitrarily.

The initial implementation may use fixed confidence values or clearly defined scoring logic for individual rules. More advanced scoring can be introduced after the team has sufficient test data.

The engine must not claim that a score such as `0.95` represents a 95% probability of compromise unless the scoring method has been calibrated and validated for that interpretation.

## 10. Event correlation and deduplication

Repeated events can produce many findings about the same underlying activity. The engine should group related evidence where doing so improves investigation.

### 10.1 Correlation

Correlation may use:

* Host identity.
* Process identifiers and process relationships.
* Account identifiers.
* File hashes.
* Network indicators.
* Event timestamps.
* Incident or investigation identifiers.

The engine must account for time-window boundaries and missing identifiers. It should not combine unrelated events merely because they occurred close together.

### 10.2 Deduplication

Deduplication should prevent identical repeated events from creating unnecessary findings.

A deduplication key may include the rule identifier, host, relevant indicator, and time window. The precise key will depend on the rule category.

When a new event matches an existing finding, the system should update the evidence or occurrence count where appropriate instead of silently discarding the event.

The original events must remain traceable.

## 11. Rule configuration and lifecycle

Rules should be managed through validated configuration.

The configuration must define:

* Rule identifier and version.
* Enabled or disabled state.
* Supported event types.
* Thresholds and time windows, where applicable.
* Severity policy.
* Required evidence.
* Rule-specific settings.
* Any supported suppression or exception conditions.

Configuration changes should be validated before the engine uses them.

An invalid configuration must generate a visible error. The engine must not silently replace a missing or invalid security threshold with a permissive value.

Rule changes should be recorded so that an investigator can determine which configuration was active when a finding was generated.

## 12. False-positive handling

False positives are expected during the early stages of detection development. The system must make them possible to investigate and correct.

The engine should support:

* Recording a finding as a false positive.
* Preserving the reason for the classification.
* Reviewing the rule and evidence that produced it.
* Adjusting rule thresholds through controlled configuration changes.
* Adding narrow, documented exceptions when justified.
* Testing the revised rule against both matching and non-matching cases.

Suppressions must be limited in scope. Broad exclusions that hide entire event categories or disable useful security checks should require explicit review.

A false-positive classification must not delete the underlying evidence or remove the audit record.

## 13. AI-assisted investigation

AI may help summarize evidence and explain why a finding deserves attention.

It may receive a controlled set of fields, such as:

* The detection rule and its description.
* Relevant event metadata.
* Evidence collected by the engine.
* Severity and confidence.
* Related findings.
* Approved investigation guidance.

The AI component may produce a plain-language summary, list relevant evidence, and suggest investigation steps.

It must not invent evidence, modify the original events, change detection results without an auditable process, or authorize defensive actions. Its output must be distinguishable from verified telemetry and rule-generated findings.

If the AI service is unavailable, the detection engine must continue to operate without it.

## 14. Error handling and resilience

The engine must handle failures without losing visibility into its own operation.

| Condition                     | Expected behavior                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------ |
| Malformed event               | Record the validation failure and prevent the event from entering normal rule evaluation   |
| Missing optional field        | Continue when the selected rule can operate safely without that field                      |
| Missing required evidence     | Do not report a successful match that depends on unavailable evidence                      |
| Invalid rule configuration    | Reject the invalid configuration and report the failure                                    |
| Rule evaluation exception     | Record the error and continue processing independent rules where safe                      |
| Duplicate event               | Avoid creating a duplicate finding while preserving relevant audit information             |
| Storage failure               | Report the failure and avoid claiming that the finding was durably recorded                |
| AI service unavailable        | Continue rule-based detection and use a deterministic explanation where appropriate        |
| Monitoring source unavailable | Mark the source as unavailable or degraded instead of reporting that no threats were found |

The project must define how storage and ingestion failures affect service health and alerting. A system that cannot process events reliably must expose that condition to the operator.

## 15. Performance requirements

The following are proposed initial targets. They must be measured on the actual development system and adjusted using test results.

| Metric                      | Initial target                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------ |
| Event validation            | Complete without unnecessary external service calls                                  |
| Rule evaluation             | Complete within a defined per-event budget                                           |
| Detection and alert latency | Target a 95th-percentile latency of 5 seconds or less under the agreed test workload |
| Rule execution              | Avoid blocking the entire pipeline on a single rule failure                          |
| Memory use                  | Remain within a documented budget for the single-endpoint deployment                 |
| Processing errors           | Record errors with enough context to diagnose the failure                            |

The five-second target applies to detection and alert generation under the agreed test conditions. It does not guarantee that the original Windows event source will deliver every event within that period.

The team must define a representative workload, measure latency, and document the hardware, event volume, and enabled rules used during testing.

## 16. Testing strategy

The detection engine must be tested with synthetic events before it is connected to real defensive actions.

### 16.1 Unit tests

Test individual functions and rules, including:

* Event validation.
* Timestamp normalization.
* Rule matching.
* Threshold evaluation.
* Severity assignment.
* Confidence calculation.
* Correlation.
* Deduplication.
* Configuration validation.
* Error handling.

### 16.2 Positive tests

A positive test supplies evidence that should satisfy a rule.

Examples include:

* A synthetic event containing a configured malicious file hash.
* Authentication failures exceeding a configured threshold.
* A process event matching a documented suspicious pattern.
* A sequence of related events satisfying a correlation rule.

The test must verify the resulting finding, severity, confidence, and supporting evidence.

### 16.3 Negative tests

A negative test verifies that benign or irrelevant events do not trigger the rule.

Examples include:

* Authentication failures below the configured threshold.
* A benign process event without the indicators required by a rule.
* A file with no matching indicator.
* Network activity that does not satisfy the rule's conditions.
* Events that look similar but fall outside a correlation window.

Negative tests are essential because a detector that flags too much activity will be difficult to use.

### 16.4 Edge-case tests

The test suite must also cover:

* Missing optional fields.
* Invalid timestamps.
* Duplicate event identifiers.
* Events arriving out of order.
* Empty or oversized evidence fields.
* Unexpected data types.
* Invalid thresholds.
* Overlapping correlation windows.
* Rule exceptions.
* Storage failures.
* Repeated events that cross time-window boundaries.

### 16.5 Integration tests

Integration tests should verify that:

1. An event enters the ingestion pipeline.
2. The engine validates and evaluates it.
3. A matching event produces a finding.
4. The finding is stored with its evidence.
5. Related events are correlated when appropriate.
6. The investigation and alerting components receive the result.
7. Failures remain visible and do not produce misleading success states.

All tests should use controlled fixtures or isolated test environments. Automated response actions should remain disabled while the detection engine is being validated.

## 17. Acceptance criteria

The Threat Detection Engine specification can be considered implemented when the following criteria have been demonstrated through tests.

* [ ] Supported events are validated against the agreed schema.
* [ ] Invalid events are rejected or routed to an error record.
* [ ] Each enabled rule has documented matching conditions.
* [ ] Detection findings identify their triggering rules.
* [ ] Findings preserve references to supporting evidence.
* [ ] Severity and confidence are assigned separately.
* [ ] Correlation rules use documented conditions and time windows.
* [ ] Duplicate findings are handled according to the deduplication policy.
* [ ] False positives can be recorded without deleting evidence.
* [ ] Invalid configuration produces a visible error.
* [ ] A rule failure does not silently appear as a clean result.
* [ ] AI unavailability does not disable rule-based detection.
* [ ] Detection results reach the investigation and alerting components.
* [ ] Unit and integration tests cover positive, negative, and edge cases.
* [ ] Performance has been measured against the agreed workload.
* [ ] No defensive action can be triggered directly by a detection rule.

These criteria describe the expected behavior. They do not indicate that the features have already been implemented.

## 18. Implementation sequence

The work should proceed in the following order.

**Step 1: Define the data models.**
Implement and test the event, rule configuration, and finding models.

**Step 2: Build the rule engine.**
Create a small rule registry and a predictable evaluation interface.

**Step 3: Implement initial rules.**
Start with synthetic file-indicator and authentication-failure events, then add process, network, and persistence rules as their telemetry sources become available.

**Step 4: Add severity and confidence policies.**
Document how each rule assigns these values and test the results.

**Step 5: Add correlation and deduplication.**
Introduce time-window handling and preserve references to all relevant events.

**Step 6: Add persistence and event delivery.**
Store findings and pass them to the investigation and alerting components.

**Step 7: Validate failure behavior.**
Test malformed input, invalid configuration, rule exceptions, and storage failures.

**Step 8: Measure performance.**
Run representative workloads and compare the results with the agreed targets.

**Step 9: Integrate AI-assisted investigation.**
Add optional summaries after the rule-based pipeline is reliable.

**Step 10: Review the security boundary.**
Confirm that detection rules cannot bypass the response-policy engine or directly execute system-changing actions.

## 19. Open design decisions

The following decisions must be resolved during implementation:

* Which Windows event sources will be supported first?
* Will event ingestion initially use Windows Event Log, a controlled simulator, or both?
* Which SQLite tables and indexes will store events, findings, and rule versions?
* What event volume should the first performance test simulate?
* Which indicator sources will be trusted, and how will their freshness be checked?
* How will event timestamps and host identifiers be normalized?
* Which correlation rules will be included in the first release?
* How will rule updates be reviewed and audited?
* What retention period will apply to raw events and investigation evidence?

These decisions should be recorded in `ARCHITECTURAL_DECISION_LOG.md` as the design becomes more concrete.

## 20. Current status

This document defines the intended behavior and implementation requirements for the CyberShield-Auto Threat Detection Engine.

The initial implementation should remain focused on validated event processing, explainable rule-based detection, structured findings, and comprehensive testing. More advanced correlation and AI-assisted investigation can be added after these foundations work reliably.

The engine must always report what it observed, what it concluded, and what evidence supports that conclusion. Any action that changes the monitored system must remain under the control of the separate response-policy and execution components.
