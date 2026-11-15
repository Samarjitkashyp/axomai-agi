import sys
from pathlib import Path

sys.path.insert(0, r"e:\axomai_agi\src")

from axomai.agents.mission_control import mission_planner, mission_executor
from axomai.agents.master_orchestrator import master_orchestrator

print("--- 1. Testing Mission Decomposition & Planning ---")
goal = "Launch complete autonomous expansion strategy for Assam EV market: analyze competitor teardown, revenue forecast, DPDP statutory compliance, and generate executive presentation deck"

plan = mission_planner.plan_mission(goal)
print(f"Mission ID: {plan.mission_id}")
print(f"Mission Title: {plan.title}")
print(f"Total Stages: {plan.total_steps}")
assert plan.total_steps >= 3, "Plan should have at least 3 stages"
for m in plan.milestones:
    print(f"  Stage {m.step_id}: {m.title} -> Assigned to: {m.agent_name} ({m.target_agent})")

print("\n--- 2. Testing Master Orchestrator Routing for Mission ---")
route_res = master_orchestrator.classify_and_route(goal)
print(f"Routed agent: {route_res['agent']}, Name: {route_res['name']}, Reason: {route_res['reason']}")
assert route_res['agent'] == "mission", f"Expected 'mission', got '{route_res['agent']}'"

print("\n--- 3. Testing Mission Execution Stream (Mocking / Running Pipeline) ---")
event_types = []
token_count = 0

for event in mission_executor.execute_mission_stream(goal):
    etype = event.get("type")
    if etype not in event_types:
        event_types.append(etype)
    if etype == "token":
        token_count += 1
    elif etype in ["mission_init", "mission_step_start", "mission_step_complete", "mission_complete"]:
        print(f"  [Event: {etype}] Step={event.get('step_id') or 'N/A'}, Title={event.get('title') or event.get('mission_id')}")

print(f"\nTotal Event Types Emitted: {event_types}")
print(f"Total Streamed Tokens: {token_count}")

assert "mission_init" in event_types, "Must emit mission_init"
assert "mission_step_start" in event_types, "Must emit mission_step_start"
assert "mission_step_complete" in event_types, "Must emit mission_step_complete"
assert "mission_complete" in event_types, "Must emit mission_complete"
assert "done" in event_types, "Must emit done"

print("\nPhase 1: Autonomous Mission Mode is 100% Working & Verified!")

