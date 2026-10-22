# CyberShield-Auto

### Autonomous Cyber Threat Detection and Response System

CyberShield-Auto is a Python-based cybersecurity project focused on detecting suspicious activity, investigating security events, assessing risk, and supporting controlled defensive responses on a Windows endpoint.

The project aims to bring these activities into one modular application. Its design separates threat detection from response authorization so that identifying a potential threat does not automatically grant permission to modify the system.

**Project status:** Early development — requirements, architecture, security specifications, and development workflows are being established. Core detection and response capabilities remain under development.

---

## Table of Contents

* [Overview](#overview)
* [Problem Statement](#problem-statement)
* [Project Objectives](#project-objectives)
* [Planned Features](#planned-features)
* [System Architecture](#system-architecture)
* [Technology Stack](#technology-stack)
* [Dataset](#dataset)
* [Security Principles](#security-principles)
* [Project Structure](#project-structure)
* [Getting Started](#getting-started)
* [Development Workflow](#development-workflow)
* [Documentation](#documentation)
* [Current Status and Limitations](#current-status-and-limitations)
* [Future Development](#future-development)
* [Contributing](#contributing)
* [License](#license)

---

## Overview

Security monitoring tools can generate alerts without providing enough context to determine what happened, how serious an event is, or what action should follow.

CyberShield-Auto is being designed to address this problem through a structured workflow that validates security events, identifies suspicious activity, collects supporting evidence, assesses risk, and evaluates possible defensive responses against explicit policies.

The initial target is a single Windows computer. The application is being developed in Python with a modular architecture so that collection, detection, investigation, policy evaluation, and response verification can be developed and tested independently.

The long-term goal is to build an explainable and testable defensive security prototype rather than an unrestricted automation tool.

## Problem Statement

Effective incident handling requires more than identifying an unusual event.

A security system must also consider false positives, gather relevant evidence, distinguish severity from confidence, and avoid taking disruptive actions without sufficient authorization.

CyberShield-Auto addresses these concerns through a design that separates the major stages of security analysis and response.

The project also distinguishes endpoint monitoring from network intrusion detection. Network-flow datasets can support experiments with network traffic, but they do not replace the Windows telemetry required to investigate process, file, or authentication activity on an endpoint.

## Project Objectives

The primary objectives are to:

1. Establish a modular Python foundation for defensive monitoring on Windows.
2. Define common schemas for validating and normalizing supported security events.
3. Develop explainable, rule-based threat detection.
4. Investigate suspicious events using supporting evidence and event correlation.
5. Assess risk while keeping severity and confidence distinct.
6. Evaluate proposed response actions through an independent policy engine.
7. Support controlled response execution and post-action verification.
8. Maintain structured incident records and audit logs.
9. Provide an API and, later, a dashboard for monitoring and investigation.
10. Evaluate detection behavior using appropriate datasets, synthetic events, and security-focused tests.

These objectives describe the intended system. Each capability must be implemented and verified before it can be considered complete.

## Planned Features

The following capabilities define the intended direction of development.

| Component                 | Purpose                                                                                 |
| ------------------------- | --------------------------------------------------------------------------------------- |
| Event collection          | Gather supported Windows endpoint security events.                                      |
| Event validation          | Validate incoming records and normalize their structure.                                |
| Threat detection          | Identify suspicious activity using explainable detection rules.                         |
| Investigation             | Connect findings with relevant evidence and related events.                             |
| Risk assessment           | Record severity, confidence, and investigation context.                                 |
| Response policy engine    | Determine whether a proposed action satisfies the configured security policy.           |
| Response executor         | Perform only explicitly permitted defensive actions.                                    |
| Response verification     | Check and record whether an authorized action achieved its intended result.             |
| Storage and audit         | Maintain incident history and records of important decisions and actions.               |
| API                       | Expose selected functionality through a structured application interface.               |
| Alerting and dashboard    | Present findings and investigation information to the user.                             |
| AI-assisted investigation | Help summarize evidence and explain findings without independently authorizing actions. |

These features are planned capabilities, not a claim that every component is currently implemented.

## System Architecture

The intended processing flow is:

```text
Windows Endpoint Events
          |
          v
Event Validation and Normalization
          |
          v
Threat Detection
          |
          v
Investigation and Evidence Correlation
          |
          v
Risk Assessment
          |
          v
Independent Response Policy Engine
          |
          v
Restricted Response Executor
          |
          v
Outcome Verification
          |
          v
Incident Records, Audit Logs and Alerts
          |
          v
API and Dashboard
```

The diagram describes the planned architecture. The complete end-to-end pipeline has not yet been implemented.

Each component should have a clearly defined responsibility. In particular, the detection engine must not independently authorize disruptive actions, and AI-generated recommendations must remain subject to the same policy controls as other proposed actions.

## Technology Stack

The project is being developed around the following technologies:

| Technology     | Intended role                                    |
| -------------- | ------------------------------------------------ |
| Python         | Primary programming language                     |
| FastAPI        | Backend API                                      |
| Pydantic       | Data validation and structured schemas           |
| Uvicorn        | Local ASGI server                                |
| pandas         | Dataset inspection and processing                |
| NumPy          | Numerical operations                             |
| scikit-learn   | Machine-learning experiments and evaluation      |
| CICIDS2017     | Network intrusion-detection evaluation dataset   |
| pytest         | Planned automated testing                        |
| SQLite         | Planned local data storage                       |
| Streamlit      | Planned dashboard                                |
| Git and GitHub | Version control and source-code hosting          |
| Antigravity    | Development environment and AI-assisted workflow |

The final dependency versions and installation commands must be confirmed against the repository's configuration before deployment.

## Dataset

### CICIDS2017

CICIDS2017 is the selected dataset for network intrusion-detection experiments.

It provides network traffic and flow information that can be used to investigate traffic classification, preprocessing, feature selection, and detection evaluation.

Dataset experiments should examine:

* Feature types and data quality.
* Missing values and duplicate records.
* Class distribution and imbalance.
* Preprocessing consistency.
* Data leakage and evaluation methodology.
* Suitable metrics, including precision, recall, and false-positive rates.

**Important distinction:** CICIDS2017 is a network-flow dataset. It does not provide genuine Windows process, file, or authentication telemetry for endpoint monitoring. Endpoint-specific functionality requires suitable Windows event sources or clearly identified synthetic test events.

No detection-accuracy or production-effectiveness claim is made here because such results must be established through completed experiments.

## Security Principles

CyberShield-Auto is intended for defensive use. Security controls are part of its architecture, not optional additions.

### Detection and response are separate

A detection indicates that activity may be suspicious. It does not, by itself, authorize a response.

### Safe defaults

Development should use detection-only or simulation mode by default. Real response actions must require explicit authorization through the configured policy.

### Restricted actions

The response system should use an allowlist of permitted actions, validate targets, apply least privilege, and reject unknown or unauthorized operations.

### Verification and auditing

Important decisions and response attempts should be recorded. When a response is implemented, the system should verify its outcome rather than assume success.

### AI remains advisory

AI components may summarize evidence, explain findings, and recommend next steps. They must not independently authorize or execute response actions.

### Fail safely

If validation, policy evaluation, or a required safety check fails, the system should avoid executing the affected response.

## Project Structure

The repository contains project documentation and an early application foundation.

The following is a conceptual overview of the main areas; it is not a complete inventory of every file.

```text
Cyber-Shield-Auto/
|
|-- README.md
|-- .gitignore
|-- .agent/
|   `-- workflows/
|       `-- cybershield-development.md
|
|-- src/
|   `-- api/
|       |-- main.py
|       `-- schemas.py
|
|-- docs/
|   |-- PROJECT_OVERVIEW.md
|   |-- PROJECT_REQUIREMENTS.md
|   |-- SYSTEM_ARCHITECTURE.MD
|   |-- DEVELOPMENT_ROADMAP.md
|   |-- DEVELOPMENT_GUIDE.md
|   |-- DEVELOPMENT_PROGRESS_REPORT.md
|   |-- THREAT_MODEL.md
|   |-- THREAT_DETECTION_ENGINE.md
|   |-- SECURITY_REQUIREMENTS.md
|   |-- AUTOMATED_RESPONSE_POLICY.md
|   |-- TESTING_STRATEGY.md
|   `-- ...
|
|-- data/
|   `-- README.md
|
`-- models/
    `-- README.md
```

This overview should be reconciled with the actual repository if files or directories change.

## Getting Started

### Prerequisites

The planned development environment uses:

* Windows 10 or Windows 11.
* Python.
* Git.
* Antigravity or another compatible code editor.
* The dependencies specified by the project's configuration.

Dataset experiments may require additional storage and memory.

### Clone the repository

```powershell
git clone https://github.com/aditya00801/Cyber-Shield-Auto.git
cd Cyber-Shield-Auto
```

### Inspect the project

Before running the application, review the project requirements, architecture, and development guide.

```powershell
Get-Content .\docs\PROJECT_OVERVIEW.md
Get-Content .\docs\DEVELOPMENT_GUIDE.md
```

The application setup instructions are still being finalized. Check the repository's dependency configuration and the current API implementation before installing dependencies or launching the server.

Do not assume that the planned detection and response pipeline is available in the current prototype.

## Development Workflow

Development follows a small-change, test-and-review process.

1. Inspect the repository and current Git status.
2. Identify the current development phase.
3. Select one logical change.
4. Implement the change without disturbing unrelated work.
5. Add or update relevant tests.
6. Run appropriate validation.
7. Review the diff for accidental changes and security issues.
8. Create a meaningful Git commit for the completed logical change.
9. Verify the commit and remaining working-tree state.

The Antigravity development workflow is documented in:

`.agent/workflows/cybershield-development.md`

The workflow is intended to support automatic local commits after completed and validated changes. Pushing to GitHub remains a separate operation unless automatic pushing is explicitly enabled.

Never commit secrets, credentials, or unrelated changes.

## Documentation

The `docs/` directory contains the project's specifications, architecture decisions, security requirements, and development plans.

| Document                         | Purpose                                       |
| -------------------------------- | --------------------------------------------- |
| `PROJECT_OVERVIEW.md`            | Project purpose, scope, and objectives        |
| `PROJECT_REQUIREMENTS.md`        | Functional and non-functional requirements    |
| `SYSTEM_ARCHITECTURE.MD`         | System components and their relationships     |
| `DEVELOPMENT_ROADMAP.md`         | Development phases and milestones             |
| `DEVELOPMENT_GUIDE.md`           | Development practices and repository workflow |
| `DEVELOPMENT_PROGRESS_REPORT.md` | Recorded project status and outstanding work  |
| `THREAT_MODEL.md`                | Threat analysis and security risks            |
| `THREAT_DETECTION_ENGINE.md`     | Detection-engine design                       |
| `SECURITY_REQUIREMENTS.md`       | Security controls and requirements            |
| `AUTOMATED_RESPONSE_POLICY.md`   | Policy-controlled response design             |
| `TESTING_STRATEGY.md`            | Planned testing and validation approach       |
| `DATA_STORAGE_AND_PRIVACY.md`    | Data-handling and privacy requirements        |
| `API_SPECIFICATION.md`           | API design and expected behavior              |
| `ALERTING_AND_MONITORING.md`     | Alerting and monitoring design                |
| `DATASET.md`                     | Dataset selection and handling                |
| `ARCHITECTURAL_DECISION_LOG.md`  | Recorded architectural decisions              |

Consult the relevant documents before changing a component.

## Current Status and Limitations

The repository has established a substantial documentation and planning foundation. Development is transitioning from repository and specification work toward the application foundation.

The current progress report identifies the following limitations:

* The API is still a basic prototype.
* The full Windows endpoint event-collection pipeline remains to be implemented.
* The rule-based detection engine and complete investigation workflow remain development tasks.
* Policy-controlled response execution and outcome verification remain planned capabilities.
* A complete automated test suite has not yet been established.
* The full end-to-end application has not yet been verified.

These statements should be updated as implementation and testing progress.

CyberShield-Auto is not yet presented as a production-ready security product. It should not be relied upon as the sole protection for a real system.

## Future Development

Development will proceed in stages:

1. Complete the repository and application foundation.
2. Establish event schemas and validation.
3. Implement and test supported event collection.
4. Develop explainable rule-based detection.
5. Add network-dataset preprocessing and evaluation.
6. Build investigation, evidence correlation, and risk assessment.
7. Implement an independent response policy engine.
8. Add restricted response execution and outcome verification.
9. Integrate storage, audit logging, and alerting.
10. Expand the API and build the dashboard.
11. Integrate advisory AI assistance where appropriate.
12. Perform integration, regression, and security testing.
13. Document limitations and evaluate the completed prototype.

The development roadmap is the authoritative reference for phase ordering and acceptance criteria.

## Contributing

This is an evolving academic and development project.

Contributions should follow the documented architecture, preserve security controls, and include appropriate tests for changed behavior.

Before submitting a change:

* Review existing requirements and implementation.
* Keep changes focused.
* Validate inputs.
* Avoid hardcoded secrets.
* Test both permitted and denied behavior for security-sensitive features.
* Update relevant documentation.
* Review the final diff.
* Use a descriptive commit message.

Do not introduce unrestricted system access or bypass the response policy.

## License

A license has not yet been specified in this README. The repository owner should select and add an appropriate license before the project is distributed for reuse.

---

**CyberShield-Auto — building a more explainable, controlled, and testable defensive security workflow.**
