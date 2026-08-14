
# PEAS and Formal AI Problem Formulation

## PEAS

**Performance measure:** The system is successful as it suggests walking path that is safe to walk and has the reasonable time.
Route safety score, travel time, successful completion of the route, user preference satisfaction, and rate of route recalculation in the event of change will be used to assess the performance.

**Environment:** The intelligent simulated agent acts on a campus or city map. It relies on data on distances of the roads, lighting, CCTV, pedestrian traffic, road construction and crime risk in order to determine the safest route.

**Actuators** The agent suggests the safest walking route, shows the route safety scores, alerts users potential safety dangers, recalculates the route when conditions change, enables Guardian mode during the trip, and enables the SOS feature when necessary.

**Sensors:** The agent is given the user's current position, destination, safety requirements, estimated travel time, and environmental data including ambient light, CCTV, pedestrian traffic, road closures and simulated crime-risk data.

## Environment properties

- **Observable:** *Partially*
  The same action (walking the same road) may not always result in the same outcome because real world safety conditions may differ between trips even on the same roadway, for example pedestrian activity or crime risk.
- **Deterministic:** *No*
  Future decisions depend on the decision made in the previous step (which road the agent will take on next): decisions are interdependent, as the agent's available options on each step depend on the one he has made on the previous step.
- **Episodic or sequential:** *Sequential*
  The environment may change as the agent is deliberating, or the user may be travelling, and new road closures or construction zones might appear in the middle of the way.
- **Static or dynamic:** Dynamic
  The map is not continuous, but a finite set of intersections (nodes), and road segments (edges), and the state space and action space are both finite.
- **Discrete or continuous:** *Discrete*
  The state comprises the user's location, destination, and the safety information of each road segment. Each road has a set of attributes, including walking distance, lighting conditions, CCTV, pedestrian activity, construction status and crime-risk level. User's safety desire (such as safety as a top priority) is also taken into account in route evaluation.

## State or variables

The state consists of the user's current location, destination, and the safety information of each road segment. Each road contains attributes such as walking distance, lighting conditions, CCTV availability, pedestrian activity, construction status, and crime-risk level. The user's safety preference (e.g., prioritising safety over speed) is also considered during route evaluation.

## Initial state

The first state is where the users are at the beginning of their trip. The AI is set to search for the safest route after you enter the destination and the preferences.

## Actions or domains

The available actions are to move from one intersection to another on the map by using connected roads. The AI will look at all possible routes to take and choose the next road, using a heuristic evaluation.

## Transition model or constraints

The AI's choice of road causes the player's position to be changed to the next road junction connected to it.**When the user deviates from the path suggested by the AI, the AI updates the path, if there are changes in the road, such as closing and construction.

## Goal test

The goal is achieved if the user is able to reach the destination using the route with a reasonable travel time, which is safe according to the safety preferences chosen by the user.

## Path cost

The path cost is not just based on the distance although it is also taken into account. Poor lighting, low pedestrian volume, increased crime-risk, construction sites and no CCTV cameras are assigned higher costs, and safer roads lower costs.This will help to make the AI choose safer routes instead of just the shortest route.

## Heuristic, where applicable

The heuristic estimates a safest remaining route to the destination, taking into account the remaining walking distance and safety factors. The AI gives higher value on routes with greater lighting, CCTV coverage and increased pedestrian traffic and penalizes routes with increased crime-risk levels or unsafe conditions.This enables the A algorithm to efficiently search for the safest practical route.

## Testing strategy

The formulation will then be tested on at least three different map scenarios with different levels of map density and different map layouts, with a shortest path route (safety weight of zero) compared with a safety optimized route. Three measures are collected for each scenario: the extra distance walked due to prioritising safety, the overall decrease in route risk score, and the number of nodes expanded during the search, as an indicator of computational efficiency.This will enable assessment of the trade-off between distance, safety, and search cost directly, instead of assuming it.

## Appendix: draft simple reflex agent rules (early sketch, Part D)

**Rule 1**
If: The selected route has a road segment that scores highly for crime-risk or has poor lighting.
Then: Propose an alternate route that has a better safety score.

**Rule 2**
If: User takes a path that is not recommended for safety.
Then: Re-calculate and suggest the safest route between the user's current position and the target.

**Rule 3**
If: The user's arrival at the destination is delayed by the time expected for the journey and the user fails to answer a Guardian Mode safety check.
If so: Arm SOS and inform the user's emergency contact of the user's last known location.
