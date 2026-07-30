# Responsible AI

Discuss fairness, privacy, safety, security, transparency, accessibility and sustainability where relevant, together with practical mitigation.

=================================================

**Fairness:** Uses infrastructure data (lighting, CCTV coverage, foot traffic) rather than demographic or crime-profiling data, avoiding bias against specific neighborhoods or groups. Mitigation: regularly audit risk scores across different areas to check no district is unfairly over-penalized.

**Privacy:** No personal location history is stored. Start/end points are used only for the duration of a single route request. Mitigation: process routes in-session and discard user location data after the route is generated.

**Safety:** A safety-optimized route is only a risk estimate, not a guarantee — real-time conditions (a broken streetlight, a temporary crowd) aren't reflected. Mitigation: clearly label routes as guidance, not a safety promise, and allow users to report outdated or incorrect risk data.

**Security:** Street safety data (lighting, CCTV) could be misused if exposed publicly at a granular level. Mitigation: restrict access to raw risk-scoring data and only expose the final computed route to users.

**Transparency:** The system shows a safety breakdown alongside the route, so users understand why a path was chosen over the shortest option, rather than trusting a black-box decision.

**Accessibility:** Route suggestions should account for users with mobility constraints (e.g. avoiding stairs, unlit stretches with uneven pavement). Mitigation: allow accessibility as an additional filter alongside safety preference.

**Sustainability:** Encouraging walking over other transport modes supports lower-emission urban mobility, aligning with broader sustainable city goals.