# Testing Strategy

## 1. Purpose

This document defines how CyberShield-Auto will be tested during development. It describes the test levels, tools, security checks, and acceptance criteria used to verify the application's behavior.

Testing will begin with synthetic events and isolated components. Tests that could affect a real system must remain disabled until the relevant safeguards have been implemented and verified.

## 2. Testing objectives

Testing must establish that:

* Event data is validated before processing.
* Detection rules produce the expected findings for known inputs.
* Invalid or incomplete data does not crash the application.
* The AI component cannot authorize or execute response actions.
* The response policy denies actions that are not explicitly permitted.
* API endpoints enforce validation and access controls.
* Stored records remain consistent and sensitive information is handled appropriately.
* Failures are logged without exposing secrets.
* The application behaves predictably when a component or external service is unavailable.

## 3. Testing environment

The initial development environment is Windows with Python.

The proposed test tools are:

| Tool                    | Purpose                                                        |
| ----------------------- | -------------------------------------------------------------- |
| `pytest`                | Run automated tests                                            |
| Pydantic                | Validate event and API data models                             |
| FastAPI test client     | Test API endpoints                                             |
| SQLite test database    | Test storage operations                                        |
| Python standard library | Create temporary files, mock dependencies, and inspect results |

The exact dependency versions will be recorded in the project's dependency configuration.

Tests should run locally without requiring paid services, real malware samples, or an external AI provider.

## 4. Test levels

### 4.1 Unit tests

Unit tests will verify individual functions and classes in isolation.

Examples include:

* Event schema validation
* Rule evaluation
* Severity and confidence calculation
* Finding deduplication
* Alert grouping
* Response policy decisions
* Target validation
* Data retention logic
* AI output validation

Each test should use controlled inputs and check the expected result.

### 4.2 Integration tests

Integration tests will check how components work together.

Examples include:

* Normalized events reaching the detection engine
* Findings creating or updating alerts
* The policy engine evaluating a proposed response
* Approved simulated actions reaching the response executor
* Results being stored in SQLite
* API requests returning the expected response models

External services should be mocked unless a test specifically checks a configured integration.

### 4.3 API tests

API tests will cover successful requests, invalid requests, missing records, unauthorized access, and internal errors.

Tests should check HTTP status codes, response structures, validation behavior, and whether failed requests leave the system in a consistent state.

### 4.4 Security tests

Security tests will check the controls that protect the application and the endpoint.

They should include:

* Malformed and oversized input
* Attempts to bypass response policies
* Unapproved response actions
* Invalid or unexpected AI output
* Prompt injection in event descriptions and other untrusted text
* Unauthorized API access
* Attempts to access files outside approved locations
* Secret exposure in logs
* Audit records for response decisions

Security tests must use an isolated test environment.

### 4.5 End-to-end tests

End-to-end tests will exercise a complete workflow using synthetic data.

A representative scenario is:

1. Submit a synthetic event.
2. Validate and normalize the event.
3. Run the detection rules.
4. Create a finding when a rule matches.
5. Generate or update the corresponding alert.
6. Evaluate any proposed response through the policy engine.
7. Simulate the response when simulation mode is enabled.
8. Verify that the result and audit record are stored.

The test must confirm that detection alone cannot trigger an unrestricted system-changing action.

## 5. Test data

Tests should use synthetic events representing both ordinary and suspicious activity.

The dataset should include:

* Normal process activity
* Repeated authentication failures
* Suspicious process behavior
* Known test file indicators
* Unusual network activity
* Possible persistence changes
* Duplicate events
* Missing fields
* Invalid timestamps
* Unexpected data types
* Oversized text fields
* Conflicting or incomplete evidence

Test cases must document their expected results. A suspicious-looking event should not automatically be treated as proof of a real attack.

Real personal data and live malware samples are not required for the initial test suite.

## 6. Detection engine tests

Each detection rule should have tests for matching and non-matching inputs.

Tests should verify:

* The rule matches when its conditions are satisfied.
* The rule does not match when its conditions are not satisfied.
* Missing or invalid fields are handled safely.
* Findings contain the required evidence and metadata.
* Repeated events do not create uncontrolled duplicate findings.
* Rule failures do not silently stop unrelated rules from running.
* Severity and confidence values remain within their defined ranges.

Tests should also cover false positives and borderline cases. Detection results must retain enough evidence for a reviewer to understand why a rule matched.

## 7. AI component tests

The AI component will be tested independently from the detection and response systems.

Tests should verify that:

* Valid model responses can be parsed into the expected schema.
* Invalid, incomplete, or unexpected responses are rejected.
* Timeouts and provider errors produce controlled failures.
* Event text is treated as untrusted evidence.
* The model cannot change response policy or grant itself permission.
* Unsupported claims are not presented as confirmed facts.
* The system can continue operating when AI assistance is unavailable.
* API keys and other credentials do not appear in prompts, logs, or error messages.

Use mocked responses for routine tests. A separate optional integration test may check a configured AI provider, but the core test suite must not depend on external model availability.

## 8. Automated response tests

Response tests must verify that the policy engine controls every proposed action.

The test suite should cover:

* Detection-only mode
* Simulation mode
* An explicitly permitted action
* An action that is not on the allowlist
* An invalid or out-of-scope target
* A missing approval when approval is required
* An expired or cancelled approval
* A disabled response executor
* An emergency stop
* An executor error
* A failed post-action verification

Denied actions must not reach the system-changing execution step. Simulation mode must not make real system changes.

Tests for disruptive actions should use mocks or isolated fixtures rather than a user's live system.

## 9. Storage and privacy tests

Storage tests should verify that:

* Valid records can be created, retrieved, updated, and deleted where permitted.
* Invalid data is rejected.
* Database errors are handled without corrupting application state.
* Sensitive values are not written to ordinary logs.
* Audit records capture required security decisions.
* Retention rules identify records eligible for deletion.
* Backup and recovery procedures preserve data integrity.

Tests should use a temporary database and clean up their test data.

## 10. Test organization

Tests should be grouped by component. A proposed layout is:

```text
tests/
├── unit/
│   ├── test_event_models.py
│   ├── test_detection_rules.py
│   ├── test_findings.py
│   ├── test_response_policy.py
│   └── test_ai_validation.py
├── integration/
│   ├── test_detection_workflow.py
│   ├── test_alert_workflow.py
│   └── test_storage.py
├── api/
│   └── test_endpoints.py
├── security/
│   ├── test_input_validation.py
│   ├── test_response_controls.py
│   └── test_secret_handling.py
└── end_to_end/
    └── test_synthetic_incident.py
```

This is a proposed structure. Test files should be added as the corresponding application components are implemented.

## 11. Running tests

Once `pytest` is installed and the test suite exists, run the full suite from the repository root:

```powershell
python -m pytest
```

Run a specific test file with:

```powershell
python -m pytest tests/unit/test_detection_rules.py -v
```

Use the actual test paths present in the repository. A command succeeding without discovering tests does not demonstrate that the application has been tested.

Record failed tests, investigate their causes, and rerun the relevant tests after making changes.

## 12. Test quality and maintenance

Tests should be deterministic and independent of execution order. They should avoid fixed delays where a mock or controlled clock can be used instead.

When a bug is fixed, add a regression test when practical. Keep test fixtures small and make expected behavior explicit.

Do not weaken or remove a security test simply to make the suite pass. If a test expectation is incorrect, document the reason for changing it.

## 13. Acceptance criteria

A component is ready for further integration when:

* Its unit tests pass.
* Relevant invalid-input and error-handling cases are covered.
* Security controls have tests for their expected behavior.
* Integration tests pass for its supported workflows.
* Test failures are investigated and documented.
* The documentation accurately describes the behavior that has been verified.

The project must not be described as fully tested based only on successful unit tests. Integration, security, and end-to-end coverage must be assessed separately.

## 14. Open decisions

The following details will be settled during implementation:

* Minimum required test coverage
* Whether continuous integration will run tests on every pull request
* Which test results will block a merge
* Whether performance tests need a dedicated environment
* How optional AI-provider integration tests will be configured

Until these decisions are made, they remain open project requirements.

## 15. Status

This document defines the proposed testing strategy. It does not claim that the test suite or any of the listed components already exists or passes.

Update this document as the implementation and test suite develop.
