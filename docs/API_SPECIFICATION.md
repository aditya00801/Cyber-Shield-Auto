# CyberShield-Auto API Specification

**Project:** CyberShield-Auto
**Document status:** Specification: Active Architecture Baseline
**Document version:** 1.0.0

---

## 1. Purpose

This document defines the REST API connecting the CyberShield-Auto web frontend with the Python backend services.

The API exposes endpoints for event intake, threat detection findings, incident records, risk assessments, controlled response evaluations, and system health status. It establishes the communication contract between the decoupled React frontend and the FastAPI backend.

---

## 2. Architecture and Design Principles

### 2.1 Frontend and Backend Separation

CyberShield-Auto separates the user interface from backend application logic:

* **Frontend client (React, TypeScript, Tailwind CSS):** Renders the security dashboard, incident investigation views, alert feeds, and response history. The frontend communicates with backend services exclusively through structured HTTP requests.
* **Backend service (Python, FastAPI, Pydantic):** Executes event validation, rule-based detection, forensic correlation, risk scoring, response policy evaluation, restricted action execution, and audit logging.

### 2.2 Security and Validation Principles

1. **Backend authority:** The frontend interface never receives direct operating-system access or administrative execution privileges. All permissions, policy checks, and system interactions remain within the backend service.
2. **Strict schema validation:** All incoming request payloads and outgoing responses are validated by Pydantic schemas. Malformed inputs are rejected before reaching core processing modules.
3. **Safe defaults:** System-changing response endpoints require explicit policy authorization and are disabled by default in simulation or detection-only mode.
4. **Advisory AI boundary:** AI-generated investigation notes and recommendations cannot directly invoke action endpoints or alter response policies.
5. **Fail-safe error handling:** Failures return structured error responses without leaking internal filesystem paths, stack traces, or credentials.

### 2.3 Real-Time Communication Strategy

REST polling serves as the primary communication mechanism for dashboard views, incident records, and health checks.

Push notification technologies, such as Server-Sent Events (SSE) or WebSocket, are under technical evaluation for streaming high-priority alerts to the dashboard. They remain optional and will be documented as confirmed design choices only upon formal architectural approval.

---

## 3. Communication Standards

### 3.1 Transport and Encoding

* **Protocol:** HTTP/1.1 (HTTP/2 supported via reverse proxy where configured).
* **Content type:** `application/json`.
* **Character encoding:** UTF-8.
* **Local development base URL:** `http://127.0.0.1:8000`

### 3.2 Authentication and Authorization

* **Local single-user mode:** The API binds to localhost (`127.0.0.1`) by default, restricting access to the local machine.
* **Header-based authentication:** Protected management and response endpoints require a pre-shared API key or token passed in the `X-API-Key` or `Authorization: Bearer <token>` header.
* **CORS policy:** Cross-Origin Resource Sharing is restricted to authorized frontend origins (e.g., `http://localhost:5173` for the local Vite development server).

### 3.3 HTTP Status Codes

The API uses standard HTTP response status codes:

| Code | Meaning | Usage |
| :--- | :--- | :--- |
| `200 OK` | Request succeeded | Standard response for successful retrieval and synchronous updates. |
| `201 Created` | Resource created | Returned when a new event or incident record is generated. |
| `400 Bad Request` | Invalid request | Returned when request syntax or query parameters are malformed. |
| `401 Unauthorized` | Missing authentication | Returned when required credentials are absent or invalid. |
| `403 Forbidden` | Access denied | Returned when policy rejects an action or emergency stop is engaged. |
| `404 Not Found` | Resource missing | Returned when an incident, detection, or event identifier does not exist. |
| `422 Unprocessable Entity`| Schema failure | Returned by FastAPI when Pydantic payload validation fails. |
| `500 Internal Error` | Server error | Returned upon unhandled internal failures. |

---

## 4. API Endpoints

### 4.1 System and Health

#### `GET /`
Returns service status and metadata.

* **Status:** Implemented (prototype)
* **Response `200 OK`:**
  ```json
  {
    "message": "CyberShield-Auto API is running"
  }
  ```

#### `GET /health`
Returns health indicators for monitoring adapters, database storage, and the policy engine.

* **Status:** Planned
* **Response `200 OK`:**
  ```json
  {
    "status": "healthy",
    "version": "0.1.0",
    "operating_mode": "detection_only",
    "emergency_stop_active": false,
    "components": {
      "monitoring": "active",
      "detection_engine": "active",
      "policy_engine": "active",
      "storage": "connected"
    }
  }
  ```

---

### 4.2 Event Intake

#### `POST /events`
Accepts security events from monitoring adapters or test harnesses for schema validation and processing.

* **Status:** Partially implemented (basic prototype with `NetworkEvent` schema in `src/api/`)
* **Request Body (`NetworkEvent` prototype):**
  ```json
  {
    "source_ip": "192.168.1.50",
    "destination_port": 445,
    "packet_count": 120
  }
  ```
* **Planned Endpoint Event Payload:**
  ```json
  {
    "event_id": "evt-20261022-001",
    "timestamp": "2026-10-22T10:15:30Z",
    "source": "windows_security",
    "event_code": 4688,
    "host": "SEC-WORKSTATION",
    "details": {
      "process_name": "powershell.exe",
      "process_id": 4820,
      "parent_process": "cmd.exe",
      "user": "DOMAIN\\user1"
    }
  }
  ```
* **Response `201 Created` / `200 OK`:** Echoes validated event structure with assigned identifier.

---

### 4.3 Threat Detections

#### `GET /detections`
Lists threat detections produced by the rule engine, with optional filters.

* **Status:** Planned
* **Query parameters:**
  * `severity` (optional): `low`, `medium`, `high`, `critical`
  * `rule_id` (optional): Filter by specific detection rule
  * `limit` (optional, default: 50): Maximum items to return
* **Response `200 OK`:**
  ```json
  [
    {
      "detection_id": "det-20261022-101",
      "timestamp": "2026-10-22T10:15:32Z",
      "rule_id": "RULE-WIN-001",
      "rule_name": "Suspicious Process Creation",
      "severity": "high",
      "confidence": 0.85,
      "evidence_event_ids": ["evt-20261022-001"],
      "summary": "PowerShell spawned from CMD with encoded parameters"
    }
  ]
  ```

#### `GET /detections/{detection_id}`
Retrieves full detection details, including rule logic, triggering fields, and forensic telemetry.

* **Status:** Planned
* **Response `200 OK`:** Full detection record.
* **Response `404 Not Found`:** Detection ID does not exist.

---

### 4.4 Incident Management

#### `GET /incidents`
Returns a list of correlated incidents for the dashboard.

* **Status:** Planned
* **Query parameters:**
  * `status` (optional): `detected`, `investigating`, `responding`, `verified`, `closed`
  * `min_severity` (optional): Minimum severity threshold
  * `page` (optional, default: 1): Page number
  * `page_size` (optional, default: 20): Items per page
* **Response `200 OK`:** Paginated list of incident summaries.

#### `GET /incidents/{incident_id}`
Returns comprehensive incident context for the investigation view.

* **Status:** Planned
* **Response `200 OK`:**
  ```json
  {
    "incident_id": "inc-20261022-005",
    "status": "investigating",
    "severity": "high",
    "confidence": 0.90,
    "created_at": "2026-10-22T10:15:35Z",
    "title": "Suspected Credential Access Activity",
    "detections": ["det-20261022-101"],
    "evidence_events": ["evt-20261022-001"],
    "investigation_notes": "Advisory summary: multiple encoded PowerShell invocations observed.",
    "response_state": "pending_evaluation"
  }
  ```

---

### 4.5 Response Policy and Control

#### `POST /incidents/{incident_id}/actions/evaluate`
Submits a proposed defensive response to the policy engine for dry-run evaluation.

* **Status:** Planned
* **Request Body:**
  ```json
  {
    "action_type": "terminate_process",
    "target_identifier": "4820",
    "reason": "Matched RULE-WIN-001 high confidence detection"
  }
  ```
* **Response `200 OK`:**
  ```json
  {
    "allowed": true,
    "operating_mode": "simulation",
    "policy_rule": "POL-PROC-TERMINATE-ALLOW",
    "evaluation_notes": "Action permitted under configured policy allowlist.",
    "simulated_execution": true
  }
  ```

#### `POST /incidents/{incident_id}/actions/execute`
Executes an approved defensive action when live response mode is explicitly enabled.

* **Status:** Planned
* **Safety constraints:**
  * Denied if operating mode is `detection_only` or `simulation`.
  * Denied if emergency stop is engaged.
  * Denied if action type is not on the policy allowlist.
  * Target parameters undergo validation against active process lists.
* **Response `200 OK` / `202 Accepted`:** Action status and execution task reference.
* **Response `403 Forbidden`:** Policy check failed, or simulation mode is active.

#### `POST /system/emergency-stop`
Engages the global emergency kill-switch, instantly halting and disallowing automated responses.

* **Status:** Planned
* **Response `200 OK`:**
  ```json
  {
    "emergency_stop_active": true,
    "timestamp": "2026-10-22T10:20:00Z",
    "message": "Emergency stop engaged. All automated responses halted."
  }
  ```

---

### 4.6 Audit History

#### `GET /audit/records`
Retrieves tamper-evident audit logs documenting policy decisions, response executions, and verification checks.

* **Status:** Planned
* **Query parameters:** `start_time`, `end_time`, `action_type`, `limit`
* **Response `200 OK`:** Array of structured audit log entries.

---

## 5. Implementation Roadmap and Status

| Endpoint | Method | Component Role | Current Repository Status |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | Root status message | Implemented prototype (`src/api/main.py`) |
| `/events` | `POST` | Event intake | Partially implemented prototype (`src/api/main.py`) |
| `/health` | `GET` | System health check | Planned |
| `/detections` | `GET` | Detection list | Planned |
| `/detections/{id}`| `GET` | Detection details | Planned |
| `/incidents` | `GET` | Incident list | Planned |
| `/incidents/{id}` | `GET` | Incident details | Planned |
| `/incidents/{id}/actions/evaluate` | `POST` | Policy evaluation | Planned |
| `/incidents/{id}/actions/execute` | `POST` | Response execution | Planned |
| `/system/emergency-stop` | `POST` | Emergency stop switch | Planned |
| `/audit/records` | `GET` | Decision and audit trail | Planned |

---

## 6. Testing and Acceptance Criteria

1. **Schema validation:** Invalid field types, missing required attributes, and unexpected fields return HTTP 422.
2. **Authorization enforcement:** Attempts to execute unapproved response actions return HTTP 403.
3. **No direct OS access:** All interaction occurs through HTTP requests; no shell or raw OS commands are accepted.
4. **Deterministic response:** Every endpoint produces structured JSON matching the defined Pydantic schema.
5. **Traceability:** Every detection, incident, and action execution contains stable, unique identifiers.
