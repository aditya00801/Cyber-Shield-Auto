# CyberShield-Auto Architectural Decision Log

**Project:** CyberShield-Auto
**Document status:** Active Architectural Record
**Last updated:** 2026-10-22

---

## 1. Purpose

This document logs significant architectural decisions for CyberShield-Auto using Architecture Decision Records (ADRs). Each record details the context, considered options, decision taken, consequences, and current status.

---

## 2. Decision Summary

| ADR ID | Decision Title | Status | Date |
| :--- | :--- | :--- | :--- |
| ADR-001 | Decoupled React Frontend and FastAPI Backend Architecture | Accepted | 2026-10-22 |
| ADR-002 | Retirement of Streamlit as Dashboard Technology | Accepted | 2026-10-22 |
| ADR-003 | Backend-Enforced Security, Policy, and Authority Boundaries | Accepted | 2026-10-22 |
| ADR-004 | REST API Communication with Optional Real-Time Push Evaluation | Accepted | 2026-10-22 |
| ADR-005 | Dual-Track Evaluation: Network Benchmark vs. Endpoint Telemetry | Accepted | 2026-10-22 |

---

## 3. Architecture Decision Records

### ADR-001: Decoupled React Frontend and FastAPI Backend Architecture

* **Status:** Accepted
* **Date:** 2026-10-22
* **Context:**
  CyberShield-Auto requires a responsive user interface to monitor security events, visualize correlated incidents, inspect telemetry evidence, review risk scores, and manage response policies. An architectural model was needed to structure the interaction between user interface components and core detection and response services.
* **Options considered:**
  1. Monolithic Python application rendering server-side templates.
  2. Single coupled desktop GUI application.
  3. Decoupled architecture: React and TypeScript web frontend communicating with a Python FastAPI backend via REST APIs.
* **Decision:**
  Adopt a decoupled client-server architecture:
  * Frontend: React, TypeScript, and Tailwind CSS.
  * Backend: Python, FastAPI, and Pydantic.
  * Interface: Documented REST APIs.
* **Consequences:**
  * Positive: Clear separation of concerns between presentation and system security services. Type-safe UI components allow independent development and testing of dashboard views.
  * Negative: Requires managing two distinct runtime environments (Node.js/npm for frontend build tooling, and Python for backend execution).
  * Implementation status: The backend currently contains a basic FastAPI prototype (`src/api/`). The React frontend is a planned component.

---

### ADR-002: Retirement of Streamlit as Dashboard Technology

* **Status:** Accepted
* **Date:** 2026-10-22
* **Context:**
  Early exploratory notes suggested Streamlit as a potential dashboard framework. However, Streamlit couples UI rendering directly to the Python script execution lifecycle, re-running entire scripts on user interaction. Security monitoring requires fine-grained state management, persistent client-side event filtering, distinct incident investigation tabs, and decoupled API communication.
* **Decision:**
  Explicitly reject and retire Streamlit as the planned dashboard technology. The user interface will be developed as a standalone React and TypeScript application. Streamlit must not be recommended or documented as part of the intended architecture.
* **Consequences:**
  * Streamlit is removed from project documentation, architecture diagrams, requirements, and roadmaps.
  * The frontend design uses established web standards (React, TypeScript, Tailwind CSS) that communicate over standard HTTP REST APIs.

---

### ADR-003: Backend-Enforced Security, Policy, and Authority Boundaries

* **Status:** Accepted
* **Date:** 2026-10-22
* **Context:**
  Automated response capabilities (such as process termination, firewall modification, and account isolation) carry significant operational risk. Malformed inputs, false-positive detections, or compromised client interfaces must not be able to execute unauthorized system-altering commands.
* **Decision:**
  1. The frontend client must never receive direct operating-system access, execution privileges, or raw shell access.
  2. All authorization, policy evaluation, target validation, and defensive executions are enforced exclusively by the backend policy engine.
  3. Client-side checks are treated as usability aids, not security boundaries.
  4. The system operates in detection-only or simulation mode by default. Real response execution requires explicit policy configuration and successful verification checks.
  5. AI-assisted investigation components are strictly advisory. AI cannot authorize, modify, or execute defensive responses.
* **Consequences:**
  * High assurance against unauthorized actions and unintended host disruption.
  * Every privileged operation must pass an allowlist check and target validation routine.

---

### ADR-004: REST API Communication with Optional Real-Time Push Evaluation

* **Status:** Accepted
* **Date:** 2026-10-22
* **Context:**
  The frontend needs to retrieve telemetry records, detection findings, incident lists, and system status from the backend. The team considered whether real-time push protocols (WebSocket or Server-Sent Events) should be mandated immediately or evaluated as an optional enhancement.
* **Decision:**
  Standardize on HTTP REST APIs as the baseline communication protocol. Client polling is supported for initial development. Real-time push mechanisms (such as Server-Sent Events for one-way alert streaming or WebSocket for bidirectional feeds) remain optional architectural considerations under review. Neither will be documented as a confirmed design choice until explicitly approved and implemented.
* **Consequences:**
  * Simplifies backend implementation and client testing during early phases.
  * Keeps API contracts predictable and straightforward to document.

---

### ADR-005: Dual-Track Evaluation: Network Benchmark vs. Endpoint Telemetry

* **Status:** Accepted
* **Date:** 2026-10-22
* **Context:**
  Evaluating threat detection requires appropriate datasets. Network intrusion detection and endpoint host monitoring involve fundamentally different telemetry types. Conflating network flow records with host telemetry leads to invalid experimental claims.
* **Decision:**
  Maintain a clear distinction between:
  1. Benchmark network flows: Evaluated using the published CICIDS2017 dataset for classifier experiments.
  2. Windows endpoint telemetry: Collected from authorized host event sources (such as Windows Security Event 4688) for process and system monitoring.
  3. Synthetic test fixtures: Used for isolated unit and integration testing of schemas, detection rules, and policy evaluation.
* **Consequences:**
  * Prevents conflation of network traffic metrics with host monitoring coverage.
  * Synthetic fixtures will never be described or published as real-world operational observations.
