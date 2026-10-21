# API specification

**Project:** CyberShield-Auto
**Document status:** Draft
**Proposed framework:** FastAPI
**Target platform:** Windows

## 1. Purpose

The API provides a defined interface for accessing security findings, reviewing alerts, checking application health, and managing investigations.

FastAPI is the proposed framework for the initial backend. The API should use validated request and response models so that each endpoint has a clear contract.

The API is a communication layer. It must enforce access controls and route security-sensitive requests through the appropriate policy checks.

## 2. Scope

The initial API design covers:

* Application health checks.
* Retrieval of security events.
* Retrieval and filtering of detection findings.
* Alert and incident management.
* Inspection of detection rules.
* Access to authorized audit records.
* Submission of proposed response actions for policy evaluation.

These are proposed capabilities. An endpoint must not be considered implemented until its route, validation, authorization, and tests exist.

## 3. API design principles

The API should follow these principles:

* Use typed request and response models.
* Validate all client-supplied data.
* Return consistent HTTP status codes.
* Avoid exposing stack traces or sensitive internal details.
* Apply access controls to sensitive operations.
* Use pagination for potentially large result sets.
* Keep detection, investigation, and response policy in separate components.
* Record security-relevant operations.
* Reject unsupported actions and malformed targets.

The server must not rely on the dashboard to enforce security. Every request must be validated on the backend.

## 4. Base path and versioning

The proposed API base path is:

```text
/api/v1
```

The version prefix allows the interface to evolve without silently changing the contract expected by clients.

A later API version should be introduced when a change would break existing clients.

## 5. Proposed endpoints

The following endpoints describe the initial design. They are not implemented routes unless confirmed in the source code.

### 5.1 Health

| Method | Endpoint  | Purpose                   |
| ------ | --------- | ------------------------- |
| `GET`  | `/health` | Report application health |

The health response should indicate whether the application is running and identify relevant dependency problems.

The endpoint must not expose credentials, private configuration, or detailed internal error messages.

A simple liveness check may return success while a separate readiness check reports that a required dependency is unavailable.

### 5.2 Security events

| Method | Endpoint                    | Purpose                       |
| ------ | --------------------------- | ----------------------------- |
| `GET`  | `/api/v1/events`            | List authorized event records |
| `GET`  | `/api/v1/events/{event_id}` | Retrieve one event            |

List endpoints should support pagination and approved filters, such as event type or time range.

The API must restrict access to sensitive event details.

### 5.3 Detection findings

| Method | Endpoint                        | Purpose                                        |
| ------ | ------------------------------- | ---------------------------------------------- |
| `GET`  | `/api/v1/findings`              | List detection findings                        |
| `GET`  | `/api/v1/findings/{finding_id}` | Retrieve a finding and its evidence references |

The response should include the detection rule, severity, confidence, timestamps, and references to supporting events.

The API must distinguish a detection finding from a confirmed security incident.

### 5.4 Alerts and incidents

| Method  | Endpoint                          | Purpose                       |
| ------- | --------------------------------- | ----------------------------- |
| `GET`   | `/api/v1/alerts`                  | List alerts                   |
| `GET`   | `/api/v1/alerts/{alert_id}`       | Retrieve an alert             |
| `PATCH` | `/api/v1/alerts/{alert_id}`       | Update permitted alert fields |
| `GET`   | `/api/v1/incidents/{incident_id}` | Retrieve an incident          |

Updates must validate allowed status transitions. Clients must not be able to modify protected evidence, overwrite audit history, or assign arbitrary fields.

The final incident model should be documented before these routes are implemented.

### 5.5 Detection rules

| Method | Endpoint                  | Purpose                        |
| ------ | ------------------------- | ------------------------------ |
| `GET`  | `/api/v1/rules`           | List available detection rules |
| `GET`  | `/api/v1/rules/{rule_id}` | Retrieve a rule definition     |

The initial API may provide read-only access to rules. If rule modification is added later, it must require appropriate authorization, validation, and audit records.

### 5.6 Audit records

| Method | Endpoint        | Purpose                           |
| ------ | --------------- | --------------------------------- |
| `GET`  | `/api/v1/audit` | Retrieve authorized audit records |

Audit access should be restricted to authorized users or administrative operations.

The API must not provide ordinary clients with a way to rewrite or delete audit history.

### 5.7 Response policy

| Method | Endpoint                    | Purpose                                   |
| ------ | --------------------------- | ----------------------------------------- |
| `POST` | `/api/v1/response/evaluate` | Evaluate a proposed action against policy |

This endpoint evaluates a proposed action. It does not automatically authorize the caller to execute it.

If a separate execution endpoint is introduced, it must accept only approved action types and enforce authorization independently. It must not allow clients to bypass the response-policy engine.

The initial implementation should support detection-only or simulation behavior until the response controls have been tested.

## 6. Request validation

Every endpoint must validate its input before performing an operation.

Validation should cover:

* Identifier formats.
* Required fields.
* Allowed values.
* Timestamp formats and ranges.
* Pagination limits.
* Filter parameters.
* Alert status transitions.
* Proposed action types.
* Target identifiers and paths.

The API should reject unknown or unsupported fields where appropriate.

Client-supplied identifiers must not be treated as proof of authorization. The backend must verify that the caller may access the referenced record.

## 7. Response format

Responses should use consistent JSON structures.

A successful response might look like this:

```json
{
  "finding_id": "finding-example-001",
  "severity": "high",
  "confidence": 0.91,
  "status": "new"
}
```

This is an illustrative example, not a real finding from the application.

The actual response schema must match the validated models used by the backend.

For list endpoints, responses should include pagination information when needed. Error responses should provide a clear error code and message without exposing secrets or internal stack traces.

## 8. HTTP status codes

The API should use status codes consistently.

| Status                      | Meaning                                               |
| --------------------------- | ----------------------------------------------------- |
| `200 OK`                    | The request succeeded                                 |
| `201 Created`               | A resource was created                                |
| `204 No Content`            | The request succeeded without a response body         |
| `400 Bad Request`           | The request is invalid                                |
| `401 Unauthorized`          | Authentication is required or invalid                 |
| `403 Forbidden`             | The caller is not permitted to perform the operation  |
| `404 Not Found`             | The resource does not exist or is not accessible      |
| `409 Conflict`              | The request conflicts with the current resource state |
| `422 Unprocessable Entity`  | The request fails schema or semantic validation       |
| `429 Too Many Requests`     | The caller exceeded an applicable rate limit          |
| `500 Internal Server Error` | An unexpected server error occurred                   |
| `503 Service Unavailable`   | A required service is unavailable                     |

The API should avoid revealing whether a protected resource exists when that information could expose sensitive data.

## 9. Authentication and authorization

Authentication requirements depend on how the application is deployed.

For a local prototype, the API should still be protected against unauthorized access from other users or processes. Binding the service to localhost reduces network exposure but does not replace authorization controls.

If remote access is introduced, the project must define an authentication mechanism, transport protection, access roles, and credential management before enabling it.

Authorization must be enforced by the backend for every sensitive endpoint.

## 10. Rate limits and request limits

The API should limit request sizes and pagination values to reduce accidental resource exhaustion.

Endpoints that trigger expensive processing or external AI requests may require rate limits and request timeouts.

The application should avoid unbounded retries and should return a controlled error when a request cannot be processed safely.

## 11. Error handling and logging

The API should return structured errors and record relevant failures.

Logs may include the endpoint, timestamp, request identifier, operation result, and a safe error category.

They must not contain API keys, passwords, authentication tokens, or unnecessary sensitive event data.

Unexpected errors should be logged for diagnosis while clients receive a controlled response.

## 12. Response-policy integration

The API must preserve the separation between detection and action execution.

A request to evaluate or execute a proposed action must pass through the response-policy component.

The backend must deny an action if:

* The action type is not supported.
* The target fails validation.
* Required evidence is missing.
* The operating mode does not permit the action.
* Required approval is absent.
* The policy engine is unavailable.

An AI-generated recommendation must not bypass these checks.

## 13. Testing requirements

The API test suite should cover:

### Functional tests

* Health responses.
* Finding and alert retrieval.
* Pagination and filtering.
* Valid status updates.
* Structured error responses.

### Validation tests

* Missing required fields.
* Invalid identifiers.
* Unsupported values.
* Invalid timestamps.
* Excessive pagination values.
* Malformed response-action requests.

### Security tests

* Unauthorized access.
* Attempts to retrieve protected records.
* Attempts to modify restricted fields.
* Attempts to bypass response policy.
* Oversized requests.
* Secret exposure through errors or logs.

### Failure tests

* Database unavailable.
* Policy engine unavailable.
* AI provider timeout.
* Invalid stored data.
* Unexpected internal errors.

Tests should use synthetic records and isolated test dependencies.

## 14. Acceptance criteria

The API specification is ready for implementation when:

* [ ] Endpoint paths and methods are documented.
* [ ] Request and response schemas are defined.
* [ ] Backend validation is enforced.
* [ ] Error responses follow a consistent format.
* [ ] Sensitive endpoints have documented authorization requirements.
* [ ] List endpoints support bounded pagination where needed.
* [ ] Audit records are protected from unauthorized modification.
* [ ] Response requests cannot bypass policy evaluation.
* [ ] Dependency failures are handled explicitly.
* [ ] Unit and integration tests cover normal and failure cases.

These criteria describe the intended behavior. They do not indicate that the routes have been implemented or tested.

## 15. Implementation sequence

The implementation should proceed in this order:

1. Define shared request and response models.
2. Implement the health endpoint.
3. Add read-only finding and alert endpoints.
4. Add pagination and filtering.
5. Implement authorized alert status updates.
6. Add authentication and authorization as required by the deployment.
7. Integrate the response-policy evaluation endpoint.
8. Add structured error handling and audit logging.
9. Test validation, authorization, and dependency failures.
10. Update the documentation to match the tested implementation.

## 16. Open decisions

The following decisions remain for implementation:

* Will the first release use FastAPI for all backend routes?
* Which authentication method will be used?
* Will the dashboard run in the same process or as a separate client?
* Which filters and pagination limits are required?
* Which endpoints may modify records?
* How will API versions be maintained?
* Will remote access be supported in a future release?

Record accepted decisions in `ARCHITECTURAL_DECISION_LOG.md`.

## 17. Current status

This document defines the proposed API contract for CyberShield-Auto.

The first implementation should focus on health checks and read-only access to findings and alerts. Sensitive operations should be added only after their validation, authorization, and audit requirements have been tested.
