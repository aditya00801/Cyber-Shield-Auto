---
description: Develop CyberShield-Auto incrementally, validate every change, and automatically create safe Git commits after each completed change.
---

CyberShield-Auto Development Workflow
Objective

Develop CyberShield-Auto as a modular defensive cybersecurity application for Windows endpoint monitoring, threat detection, investigation, risk assessment, and controlled response.

Work in small increments. Inspect the repository before changing files, follow the project documentation, test changes, and create a Git commit after every completed, validated change.

Default workflow: Inspect → Plan → Modify one logical change → Test → Review → Commit → Verify.

Do not accumulate multiple unrelated completed changes before committing.

1. Load Project Context

Before making changes:

Read AGENTS.md and PROJECT_MEMORY.md if they exist.
Read README.md.
Review the relevant documentation in docs/, including:
PROJECT_OVERVIEW.md
PROJECT_REQUIREMENTS.md
SYSTEM_ARCHITECTURE.MD
DEVELOPMENT_ROADMAP.md
DEVELOPMENT_GUIDE.md
SECURITY_REQUIREMENTS.md
THREAT_MODEL.md
TESTING_STRATEGY.md
AUTOMATED_RESPONSE_POLICY.md
DATA_STORAGE_AND_PRIVACY.md
ARCHITECTURAL_DECISION_LOG.md

Read additional documents when required by the task.

If a referenced file does not exist, report that fact instead of inventing its contents.

2. Inspect Git Before Every Change

Before editing any file, inspect:

git branch --show-current
git status --short

Determine which changes already existed before the task.

Inspect relevant files, tests, and diffs before editing. Do not recreate existing files or overwrite working implementations unnecessarily.

Never discard, reset, revert, or overwrite unrelated user changes.

Keep track of which files and modifications belong to the current task so they can be committed separately.

3. Work on One Logical Change at a Time

Break large tasks into small, independently verifiable changes.

Examples:

Add one event-validation function.
Fix one detection defect.
Add tests for one policy rule.
Update one documentation section.
Modify one configuration behavior.

For each change:

Identify the expected behavior.
Identify affected files.
Implement the smallest coherent change.
Add or update relevant tests.
Update documentation if necessary.
Validate the change.
Review the diff.
Create a Git commit.
Verify the commit before starting the next change.

A single logical change may require modifying several files. Commit those files together when they are necessary for the same completed change.

Do not create meaningless commits for every individual line or intermediate edit.

The commit boundary is one completed logical change, not necessarily one physical file.

4. Automatically Commit Completed Changes

Automatic local Git commits are enabled by this workflow.

After completing and validating a logical change, create a commit without asking for routine approval each time.

Before committing:

Run the relevant tests.
Check formatting and whitespace.
Review the actual diff.
Inspect the staged file list.
Check for secrets and unrelated changes.
Confirm that the change is ready to preserve in Git.

Run:

git diff --check
git status --short

Stage only the files belonging to the current logical change.

Use explicit paths, for example:

git add src/factoryverse/example.py tests/test_example.py

The paths above are examples. Determine the actual paths from the repository before running commands.

Never use git add . or git add -A as a shortcut for automatic commits.

After staging, run:

git diff --cached --check
git diff --cached --stat
git status --short

Inspect the staged patch when necessary:

git diff --cached

Only commit files that have been reviewed and belong to the completed change.

5. Commit Message Convention

Use clear, descriptive commit messages in this format:

type(scope): concise description

Common types:

feat: new functionality.
fix: bug fixes.
docs: documentation changes.
test: test changes.
refactor: internal restructuring.
chore: maintenance and tooling.
security: security-focused changes, when appropriate for the repository conventions.

Examples:

feat(events): add event schema validation
fix(detection): handle malformed event records
test(policy): cover denied response actions
docs(workflow): document automatic commit process
chore(config): update development configuration

Choose a message that accurately describes the actual change.

Never describe planned functionality as implemented functionality.

6. Verify Every Commit

After committing, inspect the latest commit:

git log -1 --oneline

Then inspect the working tree:

git status --short

Confirm that:

The commit was created successfully.
The intended files were committed.
No unrelated changes were included.
Any remaining changes are understood.
The working tree is clean only if the command confirms it.

If verification fails, stop and investigate before starting another change.

Do not create duplicate commits to compensate for uncertainty.

7. Test Every Meaningful Change

Follow docs/TESTING_STRATEGY.md and the existing test layout.

Use appropriate tests, including:

Unit tests.
Input-validation tests.
Integration tests.
API tests.
Security tests.
Failure-path tests.
Regression tests.
End-to-end tests when the required components are available.

Run the relevant tests before committing implementation changes.

For documentation-only changes, inspect the diff and validate relevant paths, commands, and references. Do not claim that code tests passed when no tests were run.

If a test fails:

Investigate the failure.
Fix it if the correction is safe and within the task's scope.
Rerun the relevant tests.
Commit only after the change meets its acceptance criteria.

If a meaningful failure remains unresolved, do not automatically commit the affected implementation as a completed change. Report the blocker and preserve the work safely.

Never disable tests or weaken security controls simply to obtain a passing result.

8. Protect Existing and Unrelated Changes

Before staging, compare the current working tree with the initial Git state.

Do not include:

Unrelated user modifications.
Unreviewed files.
API keys, passwords, tokens, or private keys.
.env files containing real secrets.
Local virtual environments.
Generated logs or temporary files.
Local datasets or model artifacts that should not be version-controlled.
Files excluded by project policy.

If a file contains both task-related and unrelated modifications, do not stage the entire file blindly. Separate the changes safely or stop and report the issue.

Never delete or discard unrelated work merely to produce a clean working tree.

If a safe commit cannot be isolated, explain the reason and ask for help only when necessary.

9. Defensive Security Requirements

Keep security controls enabled throughout development.

Default to detection-only mode.
Use simulation or dry-run mode for response development.
Require independent policy authorization for response actions.
Use an explicit allowlist of permitted actions.
Deny unknown or unapproved actions.
Validate targets before taking action.
Apply least privilege.
Record response decisions and actions.
Verify response outcomes.
Preserve emergency-stop controls.
Fail safely when validation, authorization, or verification fails.

Do not implement unrestricted command execution, arbitrary script execution, unauthorized persistence, stealth, credential theft, security-control bypasses, or uncontrolled remote access.

AI may assist with investigation and recommendations, but it must not independently authorize or execute response actions.

Treat event data, logs, filenames, and network payloads as untrusted input.

10. Dataset Handling

Keep Windows endpoint telemetry separate from network-flow datasets.

CICIDS2017 is for network intrusion detection evaluation. Do not represent its rows as genuine Windows process, file, authentication, or system-event telemetry.

Check dataset schemas, labels, missing values, class imbalance, preprocessing, data leakage, and evaluation methodology.

Never invent experimental results or claim production effectiveness from dataset metrics alone.

11. Documentation Maintenance

Update existing documentation when a change affects requirements, architecture, behavior, configuration, APIs, security, testing, deployment, or project status.

Do not create duplicate documents.

Keep technical documentation clear and natural. Preserve requirement IDs, file paths, commands, and factual details.

Clearly distinguish planned, implemented, tested, deferred, and incomplete functionality.

Commit documentation changes automatically after they have been reviewed and validated.

12. Git Safety

Never execute these commands without explicit authorization:

git reset --hard
git clean -fd
git push --force

Also require explicit authorization before destructive branch deletion, discarding user work, overwriting remote history, or amending an existing commit.

Do not bypass Git hooks or verification checks to force a commit.

Do not change branches when uncommitted changes could be affected.

Use the current branch unless a branch change is explicitly requested.

13. Automatic GitHub Push

Automatic local commits are enabled. Automatic pushing is disabled by default.

After a successful commit:

Verify the commit hash and message.
Verify the current branch.
Check whether the branch has an upstream.
Report whether the local commit is ready to push.

Do not push automatically unless the user has separately authorized automatic pushing.

When automatic pushing is explicitly enabled, use a normal push to the verified upstream. Never force-push.

If a push fails, report the error and investigate without attempting destructive recovery.

14. Definition of Done

A logical change is complete when:

The requested behavior is implemented.
Relevant requirements are satisfied.
Security controls remain intact.
Appropriate validation has been performed.
Relevant tests have passed, or limitations have been explicitly documented.
The diff has been reviewed.
Only intended files have been staged.
A meaningful Git commit has been created.
The commit has been verified.
Remaining uncommitted changes have been identified.

A roadmap phase must not be marked complete until its acceptance criteria have been verified.

15. Final Report

After each logical change, provide a concise report.

Change

Describe what was changed.

Files

List the files included in the change.

Validation

Report commands and tests actually executed, including failures.

Commit

Report the commit hash and message.

Git Status

Report the branch, remaining changes, and whether the working tree is clean.

Next Step

Identify the next logical task.

Never invent command output or claim success without verification.

Operating Rule

Inspect first. Change one logical unit at a time. Validate it. Review the diff. Commit automatically. Verify the commit. Preserve unrelated work. Never sacrifice security for convenience.