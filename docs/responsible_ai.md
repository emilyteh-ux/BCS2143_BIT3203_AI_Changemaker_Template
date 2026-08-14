
# Responsible AI

**Fairness and bias.** The system scores routes using infrastructure and environmental. The lighting, CCTV coverage, pedestrian activity, and simulated crime-risk, rather than the actual risk of crime, which is hard to measure, and were considered in determining the attributes.
More than demographic or identity-based user profiling or neighbourhood profiling. A risk in a real deployment: incomplete or obsolete safety information (e.g. a broken street light but one that is not known to be broken) Mediation, if it is reported, or a CCTV camera that is off-line; mitigation would be a user-reporting channel and regular data reviews to ensure that no region is over-penalised or under-penalised because of the crime-risk
factor.

**Privacy.** The agent handles sensitive real-time information, such as the user's real-time location, destination, via Guardian Mode, and emergency contact. On a real deployment, this would be the case.
Removes location data after journey has completed, only use location with emergency contact if SOS does trigger, but don't log individual users' routes or journey history
without consent.

**Safety.** A user may be directed to a false, or incorrect, lighting, CCTV or crime risk label. A road that is not as safe as the score indicates. Recalculating routes when: Mitigation.
Safety attributes from conditions change (e.g. a road closure or construction). Where possible, verified data and use Guardian mode and SOS as a last resort. Even if the recommended route is taken, there is still an unsafe situation.

**Security.** Guardian Mode is shared real-time location and can reach a third party, SOS pathway is a high-value target if the system is compromised. A production version will must only allow location-sharing and SOS to be activated when users explicitly opt-in per journey, encrypt any location data that is being transmitted, particularly if it receives user-entered safety information later on.
Reports which require validation and moderation before being trusted.

**Transparency.** Options are displayed, giving the agent a breakdown of safety scores for each recommended route.
Describes why the recalculation has been made (e.g., road closure detected) to make it easier for the user to understand what
The consequence that was chosen, distance versus safety was not just unexplained but also made.

**Accessibility.** The routes suggested should also consider individuals who may have reduced mobility,
Safety scoring as well as measures such as avoiding stairs or poorly maintained pavements.**Offering
navigability as an extra filter, then eventually a screen-reader friendly/voice
To extend the current prototype would be an obvious real world extension to the interface.

**Environmental sustainability.** By making walking feel safer, SafeRoute AI is helping to support walking.
As an alternative low emission transport in urban areas. The algorithms used are also light-weight.
There are negligible computational and energy costs (s small graph, no training required), a minor
It's not a major sustainability discovery, of course, but a positive one.

**Limitations.** This project is not based on real safety data, but rather, a prototype. The outputs should be interpreted as an example of the from city infrastructure, its outputs are feed. It is not a proven safety measure, but rather an approach. For a real deployment, agreements with would need to be hammered out.
City authorities, or facilities offices, as far as actual lighting, CCTV, and crime risk information. Having a straightforward procedure to maintain this data up to date as ground conditions change.
