# CyberShield-Auto Development Guide

## 1. Purpose

This guide explains how to develop, test, review, and maintain CyberShield-Auto.

It establishes a consistent workflow for working on the codebase, implementing features, handling security-sensitive changes, and verifying results before marking work complete.

The guide complements the following project documents:

* `docs/PROJECT_OVERVIEW.md`
* `docs/PROJECT_REQUIREMENTS.md`
* `docs/DEVELOPMENT_ROADMAP.md`
* `docs/SYSTEM_ARCHITECTURE.MD`
* `docs/THREAT_MODEL.md`
* `docs/THREAT_DETECTION_ENGINE.md`
* `docs/AUTOMATED_RESPONSE_POLICY.md`
* `docs/AI_AGENT_DESIGN.md`
* `docs/TESTING_STRATEGY.md`
* `docs/DATA_STORAGE_AND_PRIVACY.md`
* `docs/API_SPECIFICATION.md`
* `docs/DATASET.md`
* `docs/ARCHITECTURAL_DECISION_LOG.md`

The existing repository structure and verified implementation take precedence over assumptions made in planning documents. If a documented path, command, interface, or feature does not match the repository, inspect the actual implementation and resolve the discrepancy before proceeding.

## 2. Development principles

### 2.1 Inspect before changing

Before modifying a component, inspect its source code, tests, dependencies, and related documentation.

Check whether the required functionality already exists. Extend working code where appropriate instead of creating duplicate implementations.

### 2.2 Work in small steps

Implement one well-defined task at a time.

Avoid combining unrelated features, broad refactoring, and security-sensitive changes in a single change set.

### 2.3 Follow the requirements

Every significant feature should trace back to a documented requirement or an approved architectural decision.

If implementation reveals a missing requirement, document the decision before expanding the scope.

### 2.4 Keep security controls independent

Threat detection, investigation, risk assessment, response authorization, execution, and verification must have clear responsibilities.

AI-generated recommendations must not bypass the response policy.

### 2.5 Test before declaring completion

A feature is complete only when its acceptance criteria have been checked and the required tests pass.

The existence of a source file does not prove that its functionality works.

### 2.6 Document meaningful changes

Update documentation when a change affects public interfaces, configuration, security behavior, data formats, setup instructions, or supported functionality.

## 3. Development environment

The initial target platform is Windows, and Python is the primary language.

The developer uses Antigravity IDE with its integrated PowerShell terminal.

Before implementation begins, confirm the supported Python version, dependency manager, project package layout, and test commands from the actual repository.

### 3.1 Inspect the environment

Run the following commands in the repository root.

Check the current directory:

```powershell
Get-Location
```

Check the Python installation:

```powershell
python --version
```

Check Git:

```powershell
git --version
```

Check the current branch and working tree:

```powershell
git branch --show-current
git status --short
```

Inspect the project files:

```powershell
Get-ChildItem
Get-ChildItem ".\docs"
```

These commands help establish the current environment. They do not prove that the application or its dependencies are configured correctly.

### 3.2 Virtual environment

Use the virtual environment and dependency workflow established by the repository.

If the project uses a local `.venv` directory and it does not already exist, create it with:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation is blocked by the current PowerShell policy, follow the project's approved setup instructions rather than changing machine-wide security settings unnecessarily.

Verify the active interpreter:

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

Do not create additional virtual environments without a clear reason.

### 3.3 Dependency management

Inspect `pyproject.toml` and any existing lockfiles before installing dependencies.

Use the package manager and installation command documented by the project.

Do not install arbitrary packages merely to resolve an error without first identifying the missing dependency and checking compatibility.

Dependency changes must be reflected in the appropriate project configuration.

## 4. Repository workflow

### Step 1: Understand the task

Before coding, identify:

* The requirement being implemented.
* The expected behavior.
* The affected components.
* Existing tests.
* Security implications.
* Dependencies on unfinished work.
* The acceptance criteria.

### Step 2: Inspect existing code

Use Antigravity to inspect the relevant files and follow the existing interfaces.

Search for related functions, models, configuration variables, tests, and documentation.

Do not assume that a planned component has already been implemented.

### Step 3: Create a focused implementation plan

Write down the smallest set of changes that can satisfy the requirement.

Identify the files that need to change and the tests that will demonstrate correct behavior.

For complex tasks, divide the work into smaller checkpoints.

### Step 4: Implement the change

Follow the project's existing conventions.

Prefer clear interfaces, explicit error handling, validated inputs, and predictable behavior.

Avoid unrelated modifications.

### Step 5: Test the change

Run the focused tests first, followed by relevant integration and regression tests.

For security-sensitive code, include negative tests that demonstrate how prohibited behavior is rejected.

### Step 6: Review the changes

Inspect the final diff:

```powershell
git diff
```

Check for whitespace errors:

```powershell
git diff --check
```

Check the working tree:

```powershell
git status --short
```

If changes have already been staged, also inspect the staged diff:

```powershell
git diff --cached
```

Review the output before proceeding.

### Step 7: Update documentation

Update relevant documentation if behavior, interfaces, configuration, or security assumptions have changed.

Keep the documentation aligned with the verified implementation.

### Step 8: Commit the milestone

Commit a coherent, tested change when the milestone is ready.

### Step 9: Update progress

Record the completed work, test evidence, outstanding issues, and next task.

Do not mark a roadmap phase complete until its required acceptance criteria have been verified.

## 5. Python coding standards

### 5.1 Readability

Write code that clearly communicates its purpose.

Prefer descriptive names and focused functions over large functions that combine unrelated responsibilities.

### 5.2 Type annotations

Use type annotations for public functions, important data structures, and component interfaces where appropriate.

Keep annotations consistent with the supported Python version.

### 5.3 Input validation

Validate external data at system boundaries.

This includes collected events, API requests, configuration, policy definitions, and response requests.

Do not assume that external data is trustworthy simply because it came from a local source.

### 5.4 Error handling

Handle expected failures explicitly.

Examples include:

* Invalid input.
* Missing configuration.
* Permission errors.
* Unavailable event sources.
* Database failures.
* API timeouts.
* Invalid AI responses.
* Failed response execution.
* Inconclusive verification.

Errors should be reported accurately without exposing credentials or unnecessary sensitive information.

### 5.5 Configuration

Keep environment-specific settings outside application source code.

Use the configuration mechanism already established by the repository.

Document required and optional settings, defaults, and validation behavior.

Never commit real API keys, passwords, access tokens, or other secrets.

### 5.6 Dependencies

Add dependencies only when they provide a clear benefit.

Review compatibility, maintenance, licensing, and security implications before introducing a new package.

## 6. Component boundaries

CyberShield-Auto is planned as a modular application.

The following responsibilities should remain distinct.

| Component           | Responsibility                                   |
| ------------------- | ------------------------------------------------ |
| Monitoring          | Collects events from supported sources           |
| Event processing    | Validates and normalizes event data              |
| Detection engine    | Applies documented detection rules               |
| Investigation       | Collects supporting evidence                     |
| Risk assessment     | Evaluates severity, confidence, and impact       |
| Policy engine       | Determines whether an action is permitted        |
| Response executor   | Performs approved operations                     |
| Verification        | Checks the result of an action                   |
| Incident management | Maintains incident state and history             |
| Storage             | Persists required records                        |
| Alerting            | Reports incidents and status changes             |
| API                 | Exposes documented application operations        |
| Dashboard           | Displays incidents and system status             |
| AI integration      | Assists with evidence summaries and explanations |

These are architectural responsibilities. The actual module paths and interfaces must be confirmed from the repository.

A component should not take ownership of another component's security decisions.

## 7. Security-sensitive development

CyberShield-Auto can perform operations that affect a computer's security and availability. Changes to response behavior therefore require additional care.

### 7.1 Safe operating modes

Development and testing must begin with detection-only behavior and simulated responses.

Detection-only mode must not perform real system-changing actions.

Simulation mode must evaluate and record proposed actions without executing their real-world effects.

The current mode must be visible and validated.

### 7.2 Response authorization

Every system-changing action must pass through the independent response policy engine.

The executor must reject:

* Unsupported action types.
* Unauthorized targets.
* Invalid action parameters.
* Actions prohibited by the current operating mode.
* Actions blocked by the emergency stop.
* Requests for which authorization cannot be established.

Policy-engine failures must not grant permission.

### 7.3 Target validation

Validate the intended target before performing an action.

Do not allow untrusted event fields, file contents, or AI-generated text to determine an unrestricted command or target.

### 7.4 Restricted execution

The executor must implement only explicitly supported defensive operations.

Avoid arbitrary shell execution and unrestricted command construction.

Use the narrowest available operation and the minimum required permissions.

### 7.5 Failure behavior

A failed action must not be reported as successful.

If the result cannot be verified, record the outcome as uncertain.

Do not trigger unrestricted alternative actions when verification or authorization fails.

### 7.6 Audit records

Record significant policy decisions, execution attempts, errors, and verification outcomes.

Do not include credentials or unnecessary sensitive data in audit messages.

### 7.7 Emergency stop

Test the emergency stop independently from normal response execution.

When active, it must block new automated actions while preserving detection and logging where possible.

## 8. AI development rules

AI integration is optional for the core detection workflow.

When implemented, AI may assist with:

* Summarizing collected evidence.
* Explaining why a documented rule matched.
* Identifying missing information.
* Preparing investigation notes.
* Suggesting further investigation.

AI must not:

* Execute arbitrary commands.
* Modify response policies.
* Grant itself permissions.
* Authorize its own recommendations.
* Bypass the policy engine.
* Convert untrusted event content into executable instructions.
* Present unsupported conclusions as confirmed facts.

Validate model output against a defined schema.

Handle unavailable providers, timeouts, malformed output, and unsupported responses.

Core deterministic detection and policy checks must continue to behave predictably when the AI service is unavailable.

## 9. Dataset development

CICIDS2017 is intended for network intrusion detection evaluation.

It must not be treated as a substitute for Windows endpoint telemetry.

### 9.1 Dataset inspection

Before building the processing pipeline:

1. Inspect the actual dataset files.
2. Confirm their formats and available fields.
3. Identify the target labels.
4. Check missing values and duplicates.
5. Examine class distribution.
6. Document preprocessing decisions.
7. Define the evaluation method.

### 9.2 Model evaluation

When machine learning is used:

* Establish a baseline.
* Separate features from labels.
* Choose an appropriate data-splitting strategy.
* Check for data leakage.
* Evaluate false positives and false negatives.
* Record the selected metrics.
* Document the limitations of the evaluation.
* Preserve enough configuration to reproduce the experiment.

Do not claim that strong dataset performance proves effectiveness against live attacks.

### 9.3 Data management

Follow the dataset's applicable usage terms.

Avoid committing large raw datasets or generated model artifacts unless the repository explicitly requires them.

Document the location and handling of any required local data.

## 10. Testing workflow

Testing is part of implementation, not a final activity performed only before release.

### 10.1 Unit tests

Use unit tests to verify individual functions and components.

Cover normal inputs, invalid inputs, boundary conditions, and expected failures.

### 10.2 Integration tests

Verify that connected components exchange the correct data and preserve the required security boundaries.

### 10.3 Regression tests

After changing shared models, policies, interfaces, or configuration, run relevant existing tests to detect unintended behavior changes.

### 10.4 Security tests

Test both permitted and prohibited behavior.

For response functionality, verify that invalid targets, unsupported actions, and unauthorized requests are rejected.

### 10.5 Failure tests

Test missing permissions, unavailable services, timeouts, malformed input, storage failures, and inconclusive verification.

### 10.6 Test commands

Use the commands documented by the actual repository.

If the project uses pytest, the following are common examples:

Run the full test suite:

```powershell
python -m pytest
```

Run a specific test file:

```powershell
python -m pytest tests/test_example.py -v
```

These are examples, not confirmation that the named test file exists or that pytest is configured. Inspect the repository and use its actual test paths.

If the project uses a different test framework, follow its established commands.

### 10.7 Recording results

When reporting test results, include:

* The command executed.
* The number of tests passed and failed, when available.
* Any skipped tests.
* Relevant errors.
* Known limitations.

Never report tests as passing if they were not run.

## 11. Git workflow

Use milestone-based commits to preserve a clear development history.

### 11.1 Before starting work

Check the current branch:

```powershell
git branch --show-current
```

Check for existing changes:

```powershell
git status --short
```

Do not overwrite unrelated or uncommitted work.

### 11.2 Before committing

Review changed files:

```powershell
git status --short
git diff
git diff --check
```

Run the relevant tests and inspect the staged changes.

Stage only the intended files.

### 11.3 Commit conventions

Use descriptive commit messages with a consistent prefix.

Examples:

```text
docs: update development guide
feat: add event validation
test: cover detection rule boundaries
fix: handle missing event metadata
security: reject unauthorized response targets
```

These are examples. Use a message that accurately describes the actual change.

### 11.4 After committing

Verify the repository status and confirm that the commit contains the intended changes.

Push only to the intended remote branch after checking the repository's workflow and branch requirements.

Do not commit secrets, local environment files containing credentials, or unrelated changes.

## 12. Documentation maintenance

Update documentation when a change affects:

* Project scope.
* Requirements.
* Architecture.
* Module interfaces.
* Configuration.
* API behavior.
* Dataset processing.
* Security policies.
* Testing procedures.
* Installation or deployment.
* Known limitations.

Record important architectural choices in `docs/ARCHITECTURAL_DECISION_LOG.md`.

Keep the development guide focused on implementation workflow. Keep the roadmap focused on development phases and milestones. Keep deployment instructions in `docs/DEPLOYMENT_GUIDE.md`.

Avoid creating duplicate documents that describe the same responsibilities.

## 13. Troubleshooting

### Dependency installation fails

Check the active Python interpreter, supported Python version, dependency declarations, and package compatibility.

Do not resolve a dependency conflict by installing arbitrary versions without understanding the cause.

### Tests fail after a change

Read the complete error message.

Identify whether the failure comes from the new code, an existing regression, incorrect test configuration, or an environmental dependency.

Reproduce the failure before changing the implementation.

### A Windows event source is unavailable

Check its availability and required permissions.

Report the source as unavailable when appropriate. Do not silently substitute unrelated data and claim equivalent monitoring coverage.

### AI integration fails

Check configuration, credentials, network availability, timeouts, and response validation.

The core detection and policy components must remain independent of AI availability.

### A response action fails

Record the failure and preserve the actual action status.

Do not retry indefinitely or launch a different system-changing action without authorization.

### Documentation disagrees with the implementation

Inspect the code and tests, identify the intended behavior, and update the relevant documentation through the project's change process.

Do not silently treat a planned feature as implemented.

## 14. Definition of done

A development task is complete when:

1. The intended behavior is implemented.
2. Relevant acceptance criteria are satisfied.
3. Appropriate tests have been run.
4. Security implications have been reviewed.
5. Failure behavior has been checked.
6. Documentation reflects the actual behavior.
7. The changes have been reviewed.
8. The Git milestone has been committed when required.

If an essential criterion remains unverified, record the task as incomplete, blocked, or awaiting review.

## 15. Current status

**Document status:** Draft.

**Purpose:** Establish a repeatable workflow for implementing and maintaining CyberShield-Auto.

**Implementation status:** This guide does not establish that any application component or development phase is complete.

The workflow and commands must be checked against the actual repository before they are treated as authoritative instructions.
