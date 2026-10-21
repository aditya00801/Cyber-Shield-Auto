# AI Agent Design

**Project:** CyberShield-Auto
**Document status:** Draft
**Target platform:** Windows
**Implementation language:** Python

## 1. Purpose

The AI agent helps investigate security findings produced by the Threat Detection Engine. It reviews the available evidence, explains suspicious activity in plain language, and suggests appropriate investigation steps.

The agent operates within defined security boundaries. It cannot independently authorize system changes or execute arbitrary operating-system commands.

## 2. Scope

The first version will focus on evidence analysis and investigation assistance.

The AI agent should:

* Summarize security findings.
* Explain which evidence supports a detection.
* Identify missing information that may affect an investigation.
* Review related findings provided by the application.
* Suggest investigation steps from an approved set of recommendations.
* Return structured results that the application can validate.
* Explain uncertainty when the evidence is incomplete.

The first version will not independently monitor the operating system, replace the detection engine, or execute defensive actions.

## 3. Position in the architecture

The AI agent receives findings from the investigation workflow and returns an analysis result.

The intended flow is:

1. The monitoring layer collects security events.
2. The Threat Detection Engine evaluates the events.
3. The investigation component gathers relevant findings and evidence.
4. The AI agent analyzes the supplied information.
5. The application validates the AI response.
6. The investigation component records the analysis.
7. The alerting component presents the findings and relevant explanation to the user.
8. Any proposed defensive action goes through the separate response-policy engine.

The AI agent must not bypass this workflow.

## 4. Inputs

The agent should receive only the information needed for the current investigation.

Potential inputs include:

| Input                 | Purpose                                                            |
| --------------------- | ------------------------------------------------------------------ |
| Finding ID            | Identifies the finding being investigated                          |
| Detection rule        | Explains which rule matched                                        |
| Event metadata        | Provides context about the observed activity                       |
| Evidence references   | Links the analysis to its supporting data                          |
| Severity              | Communicates the potential impact assigned by the detection system |
| Confidence            | Communicates the detection system's confidence assessment          |
| Related findings      | Provides relevant context from other detections                    |
| Investigation history | Shows previously recorded investigation results                    |
| Approved guidance     | Defines the investigation steps available to the agent             |

The agent must not assume that an omitted field has a particular value. If important evidence is missing, it should identify the limitation in its analysis.

## 5. Output specification

The agent should return a validated, structured response rather than unrestricted text alone.

A proposed response model is:

```python
from pydantic import BaseModel, Field


class AgentAnalysis(BaseModel):
    finding_id: str
    summary: str
    supporting_evidence: list[str]
    missing_information: list[str] = Field(
        default_factory=list
    )
    recommended_steps: list[str] = Field(
        default_factory=list
    )
    assessment: str
    requires_human_review: bool = True
```

This model is a proposed interface. It must be implemented and tested before it is treated as part of the working application.

### 5.1 Output requirements

The agent must:

* Reference the finding it analyzed.
* Explain its conclusions using supplied evidence.
* Distinguish observed facts from possible interpretations.
* Identify missing or conflicting information.
* Recommend investigation steps that fit the approved workflow.
* Avoid inventing events, indicators, or system state.
* Flag cases that require human review.

The application must validate every response before storing or displaying it.

## 6. Evidence-based reasoning

The agent must base its analysis on the evidence supplied by CyberShield-Auto.

For example, if a detection rule identifies repeated authentication failures, the agent may explain the observed pattern and recommend reviewing the affected account and source information.

It must not claim that an account was compromised unless the supplied evidence supports that conclusion.

The agent should distinguish among:

* **Observed evidence:** Information directly present in the event records.
* **Interpretation:** A possible explanation for the observed behavior.
* **Recommendation:** A proposed next step that requires evaluation by the relevant application component.

This distinction helps investigators understand how the agent reached its conclusions.

## 7. Security boundaries

The AI agent must operate with restricted permissions.

It must not:

* Execute shell commands or arbitrary Python code.
* Terminate processes.
* Delete or quarantine files.
* Modify registry entries or system settings.
* Change account permissions.
* Disable security controls.
* Modify detection rules without an authorized configuration workflow.
* Approve its own recommendations for execution.
* Access files, credentials, or data outside its assigned scope.

The application must enforce these restrictions. A prompt telling the model to behave safely is not sufficient protection.

### 7.1 Response-policy integration

If the agent recommends a defensive action, it must return that recommendation as data.

The response-policy engine must independently validate the action, its target, the supporting evidence, and the applicable policy.

An AI recommendation does not constitute authorization.

If policy evaluation fails, the action must be denied.

## 8. Handling untrusted input

Security events may contain text controlled by an external user or process. Such text could include instructions intended to manipulate the AI agent.

The application must treat event contents, filenames, process arguments, network metadata, and other externally sourced strings as untrusted data.

The agent must not follow instructions embedded in those fields.

Additional safeguards should include:

* Separating system instructions from event data.
* Restricting the data supplied to each investigation.
* Validating the structure of model responses.
* Rejecting unsupported action types.
* Preventing model output from becoming executable code.
* Recording relevant validation failures.

Testing must include events containing malicious or misleading instructions.

## 9. Provider integration

The agent should communicate through a provider-independent client interface.

This allows the project to change AI providers without rewriting the investigation workflow.

The client should support:

* Configurable provider endpoint and model.
* Authentication through protected configuration.
* Request timeouts.
* Error handling.
* Response validation.
* Controlled retry behavior.
* Logging that excludes credentials and unnecessary sensitive data.

Provider-specific details should remain inside the client integration layer.

API keys must not be hardcoded or committed to the repository.

## 10. Failure handling

AI services may be unavailable, slow, or return unusable responses. The application must handle these conditions without disabling rule-based detection.

| Failure                              | Expected behavior                                   |
| ------------------------------------ | --------------------------------------------------- |
| Provider unavailable                 | Record the failure and continue without AI analysis |
| Request timeout                      | Stop waiting after the configured timeout           |
| Invalid response                     | Reject the response and record a validation error   |
| Missing required output              | Mark the analysis as incomplete                     |
| Unsupported recommendation           | Reject the recommendation                           |
| Untrusted instructions in event data | Treat them as data, not instructions                |
| AI confidence is unclear             | Avoid inventing a confidence score                  |
| Policy engine unavailable            | Deny proposed defensive actions                     |

The application may provide a deterministic explanation based on the detection rule and evidence when AI analysis is unavailable.

## 11. Privacy and data handling

The agent should receive the minimum information required to investigate a finding.

Before sending data to an external AI provider, the application must follow the project's approved data-handling policy.

Credentials, passwords, and unrelated personal information must not be included in prompts.

The project should document:

* Which event fields may be sent to the provider.
* Whether external processing is enabled.
* How requests and responses are logged.
* Which data is retained.
* How sensitive information is removed or restricted.

External AI processing should be disabled unless the required configuration is explicitly provided.

## 12. Testing requirements

The AI agent must be tested independently from the detection engine and response executor.

### Unit tests

Test response validation, input preparation, configuration handling, timeout behavior, and error mapping.

### Integration tests

Verify that the investigation component can submit a finding, receive an analysis, validate it, and store the result.

### Security tests

Test prompt-injection attempts, malformed responses, unsupported recommendations, secret leakage, and attempts to bypass response policy.

### Reliability tests

Test unavailable providers, slow responses, repeated failures, and recovery after the service becomes available.

### Evidence tests

Provide known event records and verify that the agent's output does not introduce unsupported facts.

Tests should use mocked provider responses or controlled test services. Real defensive actions must remain disabled during these tests.

## 13. Acceptance criteria

The AI agent specification can be considered implemented when:

* [ ] The agent accepts a validated investigation input.
* [ ] Its output conforms to the approved response schema.
* [ ] Analysis references the supplied finding.
* [ ] Supporting evidence is traceable to the original records.
* [ ] Missing information is reported when relevant.
* [ ] Invalid model responses are rejected.
* [ ] Provider failures do not stop rule-based detection.
* [ ] Credentials are excluded from logs.
* [ ] Untrusted event content cannot authorize actions.
* [ ] Recommendations pass through the response-policy engine.
* [ ] The agent has no direct authority to execute system-changing operations.
* [ ] Unit, integration, and security tests pass.

These criteria describe the required behavior. They do not mean the functionality has already been implemented.

## 14. Implementation sequence

Implementation should follow this order:

1. Define the input and output models.
2. Create the provider-independent client interface.
3. Add configuration and secret handling.
4. Implement request construction and response validation.
5. Add deterministic fallback explanations.
6. Integrate the agent with the investigation workflow.
7. Add security, failure, and evidence-validation tests.
8. Verify that recommendations cannot bypass response policy.

## 15. Open decisions

The following decisions remain for implementation:

* Which AI provider will the initial version use?
* Which event fields are permitted in external requests?
* What timeout and retry limits should apply?
* Should analysis run automatically for every finding or only selected findings?
* How will investigators mark an AI summary as useful, incorrect, or incomplete?
* What retention policy will apply to AI requests and responses?

Record significant decisions in `ARCHITECTURAL_DECISION_LOG.md`.

## 16. Current status

This document defines the intended design for AI-assisted investigation in CyberShield-Auto.

The initial implementation should focus on validated inputs, evidence-based summaries, structured outputs, and safe failure handling. The AI agent must remain an advisory component, with all system-changing actions controlled by the separate response-policy engine.
