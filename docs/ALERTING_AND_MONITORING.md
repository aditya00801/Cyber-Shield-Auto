# Alerting and Monitoring

**Project:** CyberShield-Auto
**Document status:** Draft
**Target platform:** Windows

## 1. Purpose

The alerting and monitoring component informs users when the Threat Detection Engine identifies suspicious activity. It also reports problems that affect the application's ability to monitor the system or process security events.

Users should be able to understand what triggered an alert, which evidence supports it, how serious it may be, and whether further investigation is needed.

The component must distinguish security findings from application health warnings. A monitoring failure, for example, should generate an operational warning rather than being treated as evidence of a threat.

## 2. Scope

The component is responsible for:

* Receiving detection findings.
* Creating and updating alerts.
* Grouping duplicate or related alerts.
* Tracking investigation status.
* Displaying severity and supporting evidence.
* Reporting monitoring and processing failures.
* Recording notification attempts and their outcomes.
* Supporting dashboard views of security activity.

External notifications, such as email, may be added when a suitable provider has been selected and configured.

## 3. Alert lifecycle

An alert follows a defined lifecycle from creation to resolution.

1. The detection engine produces a finding.
2. The alerting component validates the finding.
3. The component checks for an existing alert that represents the same activity.
4. It creates a new alert or updates an existing one.
5. The alert is stored with references to its supporting evidence.
6. The dashboard displays the alert.
7. An investigator reviews the evidence and updates the status.
8. The alert is resolved, marked as a false positive, or left open for further investigation.

The application should preserve the original finding even when an alert is updated or grouped with other findings.

## 4. Alert data model

Each alert should contain enough information for an investigator to understand and track the event.

| Field              | Purpose                                                 |
| ------------------ | ------------------------------------------------------- |
| `alert_id`         | Unique identifier for the alert                         |
| `finding_id`       | Reference to the detection finding                      |
| `title`            | Short description of the detected activity              |
| `description`      | Explanation of why the alert was generated              |
| `severity`         | Potential impact assigned to the finding                |
| `confidence`       | Confidence in the detection result                      |
| `host_id`          | Identifier of the affected computer                     |
| `created_at`       | Time the alert was created                              |
| `updated_at`       | Time the alert was last updated                         |
| `status`           | Current investigation status                            |
| `event_ids`        | References to relevant source events                    |
| `occurrence_count` | Number of matching occurrences represented by the alert |

The final data model should use validated types and documented constraints. The application must preserve the link between an alert and its source findings.

## 5. Severity and priority

The alerting component should display the severity assigned by the detection system.

The initial severity levels are:

* **Informational:** Activity recorded for reference.
* **Low:** Limited suspicious evidence that may need review.
* **Medium:** Activity that warrants investigation.
* **High:** Strong evidence of potentially serious suspicious behavior.
* **Critical:** Evidence of a potentially severe security incident.

Severity and confidence must remain separate. A critical alert with incomplete evidence may require urgent investigation, but it does not automatically authorize a system-changing response.

The application should not silently increase or decrease severity merely to change the number of alerts displayed.

## 6. Deduplication and grouping

Repeated detections can generate many alerts about the same activity. The system should reduce unnecessary duplication while preserving the evidence needed for investigation.

Deduplication may consider:

* The detection rule.
* The affected host.
* Relevant process, file, account, or network identifiers.
* The time window.
* The existing alert's status.

When another matching event occurs, the application may update the occurrence count, last-seen time, and evidence references.

Grouping must not combine unrelated events simply because their timestamps are close. Every grouped event should remain traceable to its original record.

## 7. Investigation status

The initial alert workflow should support these statuses:

| Status                | Meaning                                                                     |
| --------------------- | --------------------------------------------------------------------------- |
| `new`                 | The alert has been created and has not yet been reviewed                    |
| `under_investigation` | An investigator is reviewing the alert                                      |
| `resolved`            | The investigation is complete                                               |
| `false_positive`      | The alert was reviewed and determined not to represent the suspected threat |

The application should record status changes and their timestamps. Where user accounts are supported, it should also record who made the change.

Closing an alert must not delete its evidence or erase its audit history.

## 8. Dashboard requirements

The dashboard should provide a clear view of current security activity and application health.

The initial interface should support:

* A list of recent alerts.
* Filtering by severity and status.
* Searching by alert or finding identifier.
* Viewing the evidence associated with an alert.
* Inspecting the rule that triggered the finding.
* Reviewing the detection timestamp and affected host.
* Updating investigation status.
* Viewing monitoring and processing errors.

The dashboard should distinguish verified evidence from AI-generated summaries or recommendations.

Actions that change the monitored system must follow the response-policy workflow. A dashboard button must not bypass policy evaluation.

## 9. Operational monitoring

CyberShield-Auto must report failures that affect its security coverage.

Operational events may include:

* A Windows event source becoming unavailable.
* Event ingestion failures.
* Invalid event data.
* Detection rule evaluation errors.
* Database connection or write failures.
* Notification delivery failures.
* AI provider timeouts.
* Policy engine errors.
* Unexpected application shutdowns.

The application should record the affected component, the time of the failure, and any available diagnostic information.

If a monitoring source stops working, the dashboard must not continue to imply that the endpoint is being monitored normally.

## 10. Notification delivery

External notifications may be introduced after the local alert workflow is working reliably.

Potential delivery channels include email or another explicitly configured notification service.

Each notification should contain only the information needed to direct the recipient to the relevant alert. Sensitive event details should remain in the protected application unless there is an approved reason to transmit them.

The notification component should:

* Validate the destination configuration.
* Record each delivery attempt.
* Handle provider errors and timeouts.
* Apply controlled retry limits.
* Avoid sending repeated notifications for the same unchanged alert.
* Never log API keys or other credentials.

A failed notification must not delete the alert or prevent it from appearing in the dashboard.

## 11. Logging and auditability

The application should maintain records of alert creation, grouping, status changes, notification attempts, and relevant operational failures.

Audit records should contain enough information to reconstruct important decisions without storing unnecessary sensitive data.

Logs must not contain passwords, API keys, or unrelated personal information.

The application should distinguish between:

* Security findings.
* Alert lifecycle events.
* Operational errors.
* Response-policy decisions.
* Diagnostic logs.

These records may have different access and retention requirements.

## 12. Failure handling

| Failure                           | Expected behavior                                                      |
| --------------------------------- | ---------------------------------------------------------------------- |
| Invalid finding                   | Reject it and record the validation error                              |
| Database write fails              | Report that the alert was not durably stored                           |
| Dashboard unavailable             | Preserve stored findings and report the service failure where possible |
| Notification provider unavailable | Keep the alert and record the delivery failure                         |
| Duplicate finding arrives         | Update the existing alert when the deduplication rules match           |
| Monitoring source unavailable     | Report degraded monitoring status                                      |
| AI explanation unavailable        | Display the rule-based finding without an AI summary                   |
| Alert status update fails         | Preserve the previous status and report the error                      |

The application must not report that an alert was successfully stored when the database operation failed.

## 13. Testing requirements

Testing should cover the alert lifecycle and the operational failures that could hide security activity.

### Unit tests

Test alert creation, validation, severity display, deduplication keys, occurrence counts, status transitions, and notification configuration.

### Integration tests

Verify that a detection finding produces a stored alert, that the dashboard can retrieve it, and that status changes are recorded.

### Failure tests

Test database outages, notification timeouts, unavailable event sources, malformed findings, and unavailable AI services.

### Security tests

Verify that unauthorized users cannot access restricted alert details or change investigation status without permission.

Test that dashboard requests cannot bypass response-policy checks.

### Acceptance tests

Use synthetic security events to confirm that expected alerts appear and benign events do not generate alerts unless a configured rule requires them.

## 14. Acceptance criteria

The alerting and monitoring component is ready for integration when:

* [ ] Valid findings produce structured alerts.
* [ ] Alerts reference their source findings and evidence.
* [ ] Severity and confidence are displayed separately.
* [ ] Duplicate findings are handled according to documented rules.
* [ ] Investigation status changes are recorded.
* [ ] The dashboard displays alerts and operational health.
* [ ] Monitoring failures are visible to the user.
* [ ] Notification failures do not remove stored alerts.
* [ ] Sensitive information is excluded from ordinary logs.
* [ ] AI unavailability does not prevent rule-based alerts.
* [ ] Dashboard operations cannot bypass response policy.
* [ ] Unit and integration tests cover normal and failure conditions.

These criteria define the expected behavior. They do not indicate that the functionality has already been implemented.

## 15. Implementation sequence

The implementation should proceed in this order:

1. Define the alert data model.
2. Implement alert creation from detection findings.
3. Add persistence and evidence references.
4. Implement deduplication and occurrence tracking.
5. Add investigation status transitions.
6. Display alerts in the dashboard.
7. Add application health reporting.
8. Integrate optional external notifications.
9. Add access controls and audit records.
10. Test normal operation, failure recovery, and security boundaries.

## 16. Open decisions

The following decisions remain for implementation:

* Which notification channel should be supported first?
* How should the system identify duplicate alerts for each detection category?
* What retention period should apply to alert records?
* Will the first dashboard support multiple users?
* Which operational health checks should be mandatory?
* How should notification retries and rate limits be configured?
* Which alert fields may be included in external notifications?

Record accepted architectural decisions in `ARCHITECTURAL_DECISION_LOG.md`.

## 17. Current status

This document defines the intended alerting and monitoring behavior for CyberShield-Auto.

The initial implementation should focus on reliable alert creation, evidence references, status tracking, and visible reporting of monitoring failures. External notifications can be added after the local alert workflow has been tested.
