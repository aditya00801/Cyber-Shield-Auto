# CyberShield-Auto

## Autonomous cyber threat detection, investigation, response, and verification

| Field                     | Description                                                                 |
| ------------------------- | --------------------------------------------------------------------------- |
| Project name              | CyberShield-Auto                                                            |
| Category                  | Cybersecurity, threat detection, AI agents, and automated incident response |
| Initial platform          | Windows                                                                     |
| Primary language          | Python                                                                      |
| Development approach      | Documentation-first, modular architecture, test-driven development          |
| Project phase             | Planning and documentation                                                  |
| Network detection dataset | CICIDS2017                                                                  |
| Initial operating model   | Local endpoint with controlled response policies                            |

## 1. Project overview

CyberShield-Auto is a planned defensive cybersecurity application that will detect suspicious activity, investigate potential threats, assess risk, and support authorized responses.

The project aims to connect event monitoring, threat detection, incident investigation, response authorization, verification, and alerting in one application.

The first version will focus on a single Windows computer. Development will begin with controlled test data and deterministic detection rules. Additional capabilities will be introduced as the core workflow is implemented and tested.

The project will use CICIDS2017 to develop and evaluate network intrusion detection. Additional synthetic events or suitable Windows telemetry will be needed to test endpoint-specific capabilities such as process monitoring, file activity, and authentication events.

AI-assisted investigation may be added to explain findings and summarize evidence. The AI component will not have independent authority to execute system commands or approve its own recommendations.

The central workflow is:

1. Collect security-relevant events.
2. Validate and normalize the event data.
3. Detect suspicious patterns.
4. Gather and correlate supporting evidence.
5. Assess severity and confidence.
6. Evaluate proposed responses against explicit security policies.
7. Execute permitted actions when the required conditions are met.
8. Verify the outcome.
9. Notify the user and update the incident record.

The system must distinguish a detected threat from a successful response and a verified resolution.

## 2. Problem statement

Security monitoring can produce large amounts of information without giving users a clear understanding of which events matter or what to do next.

CyberShield-Auto addresses several related problems.

### 2.1 Delayed detection

Suspicious activity can go unnoticed when relevant events are not collected or analyzed promptly.

The application should process supported events efficiently and identify documented threat patterns.

### 2.2 Limited investigation

An individual alert may not provide enough context to explain what happened or how serious the incident is.

CyberShield-Auto should associate findings with available evidence and related events.

### 2.3 Manual response

Investigating and responding to an incident can require several manual steps.

The application aims to automate selected defensive actions when its policies, evidence requirements, and authorization checks permit them.

### 2.4 Inconsistent risk assessment

Different events carry different levels of risk. An unusual process does not necessarily indicate malware, and a high-impact event may still have uncertain classification.

The application should evaluate severity and confidence separately and consider uncertainty before recommending a response.

### 2.5 Unverified remediation

Executing an action does not prove that the threat has been removed.

CyberShield-Auto should check the relevant system state and report whether the action succeeded, failed, or could not be verified.

### 2.6 Risks from automation

Incorrect automated actions can interrupt legitimate processes, damage data, or disrupt network access.

The response system must therefore use explicit authorization rules, restricted operations, audit records, and an emergency stop.

## 3. Vision and objectives

The project aims to build a modular defensive security application that helps users understand suspicious activity and respond to threats within clearly defined limits.

### 3.1 Primary objectives

CyberShield-Auto is intended to:

* Collect selected security-relevant events.
* Validate and normalize incoming data.
* Detect documented suspicious patterns.
* Evaluate network traffic using the selected detection approach.
* Investigate findings using available evidence.
* Correlate related observations into incidents.
* Assign severity and confidence.
* Evaluate proposed actions through a policy engine.
* Execute permitted defensive actions.
* Verify response outcomes.
* Display alerts and incident history.
* Maintain audit records.
* Provide a dashboard for monitoring and investigation.
* Support automated testing throughout development.

These are project objectives. Each capability must be implemented and tested before it can be considered complete.

### 3.2 Future objectives

Potential future improvements include:

* Machine-learning-based anomaly detection.
* AI-assisted incident summaries.
* Threat intelligence enrichment.
* Advanced event correlation.
* Additional Windows event sources.
* Centralized monitoring of multiple authorized computers.
* Historical incident analytics.
* Automated security reports.
* Support for additional operating systems.

These capabilities are subject to implementation priorities and further design review.

## 4. Target users

The initial project is intended for:

### Individual computer users

Users who want greater visibility into suspicious activity on their own computers.

### Students and cybersecurity researchers

Users who want to study threat detection, network traffic analysis, incident investigation, and defensive automation in a controlled environment.

### Developers and security engineers

Users who want to extend detection rules, test security policies, and evaluate response reliability.

### Small organizations

Organizations may be considered in a future version that supports centralized management of authorized endpoints.

Enterprise-scale management is outside the initial scope.

## 5. Project scope

### 5.1 Initial scope

The initial release will focus on one Windows computer and a modular Python application.

The planned capabilities include:

* Event validation and normalization.
* Rule-based threat detection.
* Network intrusion detection experiments using CICIDS2017.
* Investigation and event correlation.
* Risk assessment.
* Response policy evaluation.
* Selected defensive actions.
* Post-response verification.
* Alert and incident management.
* Local data storage.
* A monitoring dashboard.
* Automated tests.

Development will begin with synthetic events and controlled test cases. Real operating-system integrations and system-changing actions will be introduced incrementally.

### 5.2 CICIDS2017 scope

CICIDS2017 is the dataset selected for network intrusion detection work.

It can support experiments involving labeled network traffic and evaluation of detection models. Its use does not, by itself, provide all the information required for endpoint monitoring.

The project must separately define and test the event sources needed for capabilities such as:

* Process creation and termination.
* File creation and modification.
* Authentication activity.
* Selected startup or persistence changes.
* Windows security events.

The available dataset files, feature columns, label values, and preprocessing requirements must be inspected and documented before model development.

### 5.3 Out of scope for the initial release

The initial version will not promise:

* Detection of every possible cyberattack.
* Unrestricted remote access to computers.
* Arbitrary command execution generated by an AI model.
* Automatic deletion of files based solely on suspicion.
* Unrestricted modification of operating-system security settings.
* Unauthorized monitoring of third-party computers.
* Offensive exploitation capabilities.
* Guaranteed threat removal without supporting evidence.

The application is intended for defensive use on systems and resources the operator is authorized to manage.

## 6. Core capabilities

### 6.1 Event collection

The monitoring component will collect events from supported sources while the service is running.

Potential sources include Windows security logs, process metadata, file activity, and network connection information.

The final list will depend on available interfaces, permissions, and implementation requirements.

The collector should report failures and gaps in monitoring coverage.

### 6.2 Event validation and normalization

Incoming data must be validated before it reaches the detection engine.

The processing layer will standardize fields such as timestamps, event types, source identifiers, and event-specific attributes.

Malformed events should be rejected or handled according to documented rules without crashing unrelated processing tasks.

### 6.3 Threat detection

The first detection implementation will prioritize deterministic rules because their behavior is easier to test and explain.

Possible detection categories include:

* Suspicious process activity.
* Known malicious file indicators.
* Repeated authentication failures.
* Suspicious network connections.
* Unexpected changes to selected persistence locations.
* Repeated related events that warrant investigation.

Detection quality will depend on the available event data and the coverage of the implemented rules.

### 6.4 Network intrusion detection

CICIDS2017 will be used to develop and evaluate network traffic classification.

The workflow may include:

1. Inspecting the available dataset files.
2. Identifying the feature columns and target labels.
3. Cleaning and validating the records.
4. Preparing the features.
5. Separating training, validation, and test data if machine learning is used.
6. Evaluating predictions with suitable metrics.
7. Recording limitations and reproducible results.

The project must guard against data leakage and report performance on the dataset separately from performance on live network traffic.

### 6.5 Investigation and correlation

The investigation component will gather available evidence related to a finding.

Depending on the event sources, this may include process metadata, file information, network connection details, authentication events, or related observations.

The component should identify missing evidence and distinguish observed facts from inferences.

### 6.6 Risk assessment

Risk assessment will consider evidence strength, confidence, potential impact, affected resources, and the consequences of a proposed response.

Severity and confidence must remain separate values.

A detection score alone must not grant permission to perform a high-impact operation.

### 6.7 Automated response

The response system will execute only operations permitted by the response policy.

Potential actions may include collecting additional evidence, terminating a confirmed malicious process, or quarantining a file when the implementation and policy support those operations.

Every action must have defined authorization conditions, target restrictions, failure handling, and verification requirements.

Detection-only mode and simulation mode will support development and testing before real system-changing actions are enabled.

### 6.8 Response verification

The verification component will inspect the relevant state after an action.

It must distinguish among:

* Action succeeded and the intended result was verified.
* Action failed.
* Action was executed, but the outcome remains uncertain.
* The action succeeded, but suspicious activity continues.

A successful command does not prove that the entire incident has been resolved.

### 6.9 Alerts and incident history

The application will maintain structured records containing relevant observations, findings, policy decisions, response attempts, and verification results.

Alerts should explain why the event was flagged and show the current incident and response status.

The dashboard should distinguish detections from actions that have actually been executed and verified.

## 7. Proposed system architecture

CyberShield-Auto uses a decoupled architecture separating the user interface from backend application services.

The main components are:

| Component                 | Responsibility                                              |
| ------------------------- | ----------------------------------------------------------- |
| Monitoring                | Collects events from supported sources                      |
| Event processing          | Validates and normalizes data                               |
| Detection engine          | Evaluates rules and produces findings                       |
| Investigation             | Gathers evidence and correlates events                      |
| Risk assessment           | Evaluates severity, confidence, and impact                  |
| Policy engine             | Determines which actions are permitted                      |
| Response executor         | Performs approved operations                                |
| Verification              | Checks action outcomes                                      |
| Incident management       | Maintains incident state and history                        |
| Alerting                  | Communicates detections and response outcomes               |
| Storage                   | Persists incidents, findings, and audit records             |
| Backend REST API (FastAPI)| Exposes structured endpoints and enforces security policies |
| Frontend Dashboard (React)| Displays alerts, investigations, findings, and status       |
| AI integration            | Provides optional investigation summaries                   |

The expected processing flow is:

**Monitoring → Event processing → Detection → Investigation → Risk assessment → Policy evaluation → Response → Verification → Storage and alerts → Backend REST API → Frontend Dashboard**

Not every event will require every stage. The implementation may close low-risk events without further investigation when the configured rules support that decision.

### Frontend and Backend Separation

The system divides responsibilities between two distinct tiers:

1. **Frontend tier (React, TypeScript, Tailwind CSS):** Renders the security dashboard, incident investigation views, alerts list, risk indicators, response status, audit trails, and system settings. The frontend communicates with the backend exclusively via documented REST APIs. Real-time alert streaming options (such as Server-Sent Events or WebSocket) remain under evaluation and are not confirmed design decisions. The frontend client does not receive direct operating-system access.
2. **Backend tier (Python, FastAPI, Pydantic):** Executes all security event intake, request validation, rule evaluation, forensic analysis, policy enforcement, restricted response execution, verification checks, and persistent storage. All access controls and security constraints are enforced on the backend.

## 8. AI integration

AI may assist with explaining findings, summarizing evidence, and preparing investigation notes.

The AI component will receive only the data needed for the requested task, subject to the project's privacy requirements.

Its outputs must be validated and checked against the evidence supplied to it.

The AI component must not:

* Execute arbitrary system commands.
* Modify response policies.
* Grant itself permissions.
* Approve its own recommendations.
* Bypass the policy engine.
* Present unsupported conclusions as confirmed facts.

If the AI provider is unavailable or returns invalid output, the core detection and policy components should continue to behave predictably.

## 9. Security and safety requirements

CyberShield-Auto is itself a security-sensitive application. Its own design must reduce the risk of unauthorized access and unsafe actions.

The following requirements will guide implementation:

1. Apply least privilege.
2. Validate incoming event data and response requests.
3. Separate detection from response authorization.
4. Restrict the executor to an explicit action allowlist.
5. Validate targets before executing an action.
6. Deny actions when authorization cannot be established.
7. Protect configuration files and credentials.
8. Record security-relevant decisions and outcomes.
9. Provide an emergency stop for automated responses.
10. Support detection-only and simulation modes.
11. Handle failures without silently reporting success.
12. Minimize unnecessary collection of sensitive information.
13. Test response behavior in isolation before enabling it on a real endpoint.

These requirements will be developed further in the dedicated security and response-policy documents.

## 10. Proposed technology stack

The initial technology choices reflect the intended architecture:

| Technology               | Layer / Component     | Intended use                                        |
| ------------------------ | --------------------- | --------------------------------------------------- |
| React                    | Frontend              | Security dashboard and client interface             |
| TypeScript               | Frontend              | Type-safe frontend client logic                     |
| Tailwind CSS             | Frontend styling      | Dashboard layout and interface styling              |
| Python                   | Backend               | Core application logic and detection services       |
| FastAPI                  | Backend API           | REST API endpoints and request routing              |
| Pydantic                 | Validation            | Validation of events, findings, and action requests |
| REST APIs                | Communication         | Frontend and backend communication interface        |
| pandas                   | Data processing       | Tabular data inspection and dataset handling        |
| NumPy                    | Numerical computation | Array and numerical operations                      |
| scikit-learn             | Machine learning      | Planned detection experiments and model evaluation  |
| CICIDS2017               | Benchmark dataset     | Network intrusion detection evaluation data         |
| SQLite                   | Data storage          | Initial local database                              |
| pytest                   | Testing               | Automated unit, integration, and security tests     |
| Git                      | Version control       | Source-code version control                         |
| Windows event interfaces | Telemetry             | Collection of supported endpoint events             |

The repository currently contains a basic FastAPI prototype in `src/api/`. The React frontend is a planned component. Final dependencies and operating-system interfaces will be confirmed as implementation proceeds.

## 11. Data management and privacy

Security events may contain account identifiers, process details, file paths, timestamps, and network metadata.

The application should collect only the information needed for its documented functions.

The data design must define:

* Which event sources are collected.
* Which fields are retained.
* Where records are stored.
* Who can access incident information.
* How long records are retained.
* How records are deleted.
* How credentials and other secrets are protected.
* How diagnostic logs avoid unnecessary sensitive information.

CICIDS2017 must be handled according to its applicable usage and licensing terms. Dataset transformations should be documented so experiments can be reproduced.

Centralized collection or transmission of endpoint events will require additional authentication, access control, encryption, and privacy safeguards.

## 12. Testing and evaluation

Testing will begin with synthetic events and isolated components.

The test strategy will cover:

### Unit tests

Validate event models, detection rules, risk calculations, policy decisions, and incident state transitions.

### Integration tests

Check the flow of data through detection, investigation, response authorization, storage, and verification.

### Dataset evaluation

Evaluate network detection using CICIDS2017. Report the data split, class distribution, preprocessing, and metrics used.

### Response tests

Confirm that permitted actions are accepted and prohibited actions are rejected.

### Failure tests

Simulate invalid events, missing permissions, unavailable services, timeouts, failed actions, and inconclusive verification.

### Security tests

Test access controls, policy enforcement, secret handling, audit records, and attempts to bypass response restrictions.

The application must not be described as fully tested solely because its unit tests pass.

## 13. Performance and reliability

Performance targets will be defined after the initial implementation and test environment are established.

Measurements may include:

* Event collection latency.
* Detection latency.
* Alert delivery latency.
* Event-processing throughput.
* CPU and memory consumption.
* Detection precision and recall.
* False-positive rate.
* Response execution success rate.
* Verification success rate.
* Recovery from component failures.

The application should report dropped events, unavailable sources, and inconclusive outcomes rather than presenting incomplete monitoring as normal operation.

## 14. Development roadmap

Development will proceed through the following stages.

| Phase | Focus                                | Completion evidence                                                |
| ----- | ------------------------------------ | ------------------------------------------------------------------ |
| 0     | Project foundation and documentation | Scope, requirements, architecture, and security policies reviewed  |
| 1     | Event models and collection          | Supported events can be validated and processed in tests           |
| 2     | Threat detection                     | Documented test cases produce expected findings                    |
| 3     | Investigation and correlation        | Findings include traceable evidence                                |
| 4     | Risk assessment                      | Risk decisions follow documented rules                             |
| 5     | Response policy                      | Permitted actions are accepted and prohibited actions are rejected |
| 6     | Controlled response                  | Approved actions work in an isolated environment                   |
| 7     | Verification                         | Success, failure, and uncertainty are represented correctly        |
| 8     | Alerting and dashboard               | Incidents and status changes are visible to the user               |
| 9     | Network detection evaluation         | CICIDS2017 experiments produce reproducible results                |
| 10    | Integration and security hardening   | Required integration and security tests pass                       |
| 11    | Packaging and deployment             | Installation and operating instructions are verified               |

The roadmap should be updated using verified implementation and test results.

## 15. Success criteria

The initial release should demonstrate that:

* Supported events can be processed correctly.
* Documented test scenarios produce expected findings.
* Findings include supporting evidence.
* Response policies control all system-changing actions.
* Unauthorized actions are rejected.
* Approved actions can be tested safely.
* Verification accurately reports the result.
* Incident history and audit records are maintained.
* Failures are reported accurately.
* Detection performance can be measured and reproduced.
* The application operates within acceptable resource limits.

Quantitative thresholds will be set when the event sources, hardware constraints, and test environment are known.

## 16. Known limitations

CyberShield-Auto will have limitations that depend on its event sources, permissions, and detection coverage.

Unknown threats may evade detection. Legitimate activity may resemble malicious behavior. A compromised operating system may manipulate local events and records. AI-generated summaries may contain errors, and a defensive action may reduce immediate risk without removing every part of a threat.

The application must communicate these limitations clearly. It must not claim that the computer is completely secure merely because no threats were detected.

## 17. Development principles

The project will follow these principles:

1. Document requirements before implementing the corresponding features.
2. Keep components focused on defined responsibilities.
3. Make requirements testable.
4. Record important architectural decisions.
5. Keep detection separate from response authorization.
6. Use explicit policies for automated actions.
7. Verify response outcomes.
8. Test new behavior and preserve regression tests.
9. Keep AI authority limited to its documented role.
10. Record meaningful development milestones in Git.
11. Update project documentation to match verified progress.
12. Avoid claiming that a feature is complete without evidence.

## 18. Current status

**Project phase:** Planning and documentation.

**Dataset:** CICIDS2017 has been identified for network intrusion detection. The available files and preprocessing requirements must be confirmed.

**Implementation status:** This overview does not establish which application components have been implemented or tested.

**Current priority:** Complete and review the project documentation before proceeding with the planned implementation workflow.

## 19. Summary

CyberShield-Auto aims to connect security event collection, threat detection, investigation, risk assessment, policy-controlled response, verification, and alerting in a modular Python application.

CICIDS2017 will support network intrusion detection experiments. Separate event sources and test data will be needed for Windows endpoint monitoring and other capabilities.

The project will prioritize evidence-based decisions, least privilege, restricted automation, clear audit records, and reproducible testing. New capabilities will be introduced as their requirements, implementation, and security controls are verified.
