# CyberShield-Auto UI Prototype

This folder contains a dependency-free, static frontend prototype for the CyberShield-Auto project.

## Open it

Open `index.html` in a modern browser. No package installation or build step is required.

## Pages included

- Login demo
- Security dashboard
- Threat monitoring
- Incident investigation
- Endpoint monitoring
- Response center
- Network traffic analysis
- Audit logs and CSV export
- Settings and policies
- About CyberShield-Auto
- Expandable FAQ and shared interaction states

## Implemented frontend interactions

- Form success/error feedback and client-side validation
- Password visibility toggle
- Confirmation modal with Escape handling, focus restoration, and a basic keyboard focus loop
- Dark/light theme toggle, saved locally
- Essential-only cookie preference banner
- Page search and threat/severity filtering
- Mobile navigation menu
- Loading/transition animation with reduced-motion preference support
- Button hover and keyboard focus states
- Scroll progress indicator and back-to-top button
- Copy-to-clipboard controls with status feedback
- Print stylesheet for the current view
- Sticky header and sidebar on desktop
- Skip-to-content link
- Last-updated date on About page
- Expandable FAQ
- Floating contact button
- UTM parameter capture in session storage
- Demo audit CSV export

## Important limitations

This is a frontend-only demo, not an authenticated or operational security product.

- Login validation runs in the browser and does not authenticate users.
- Dashboard metrics and event records are clearly labelled sample data.
- The forms do not call the FastAPI backend.
- No endpoint collector, detection engine, response executor, or audit database is connected by this page.
- Response-related controls demonstrate validation and confirmation states only. They do not execute operating-system actions.
- The current repository documentation targets Windows first; Linux monitoring remains a planned extension.
- CICIDS2017 is a network-flow dataset and is not a substitute for native endpoint telemetry.

Before production use, implement backend authentication, session security, server-side validation, authorization, consent-aware analytics, API integration, and automated accessibility/security tests. Never treat frontend controls as an authorization boundary.

## UTM handling

The prototype reads `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, and `utm_content` from the page query string and stores present values in the browser session. It does not send them to a server or third party.

## Source of project scope

The UI scope follows the repository README and `docs/API_SPECIFICATION.md`. Planned features are labelled as planned rather than presented as completed functionality.
