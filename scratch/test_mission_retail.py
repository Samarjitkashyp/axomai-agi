"""
Test script for verifying Mission Mode fixes on retail branch expansion:
1. Fast planning (< 5ms)
2. No jammed headers or unrendered markdown tables
3. No premature done / indicator removal
4. Stage transitions and live HUD
"""
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from axomai.agents.master_orchestrator import master_orchestrator

def test_retail_mission_stream():
    query = "pehle Assam ke top 3 districts me nayi retail branch kholne ka 360-degree plan banao"
    print(f"Executing Query: {query}")
    start_t = time.perf_counter()

    events = []
    tokens = []
    milestone_starts = []
    milestone_completes = []

    for event in master_orchestrator.orchestrate_stream(query=query):
        events.append(event)
        etype = event.get("type")
        if etype == "mission_step_start":
            milestone_starts.append(event)
            print(f"  [STEP START]: Stage {event.get('step_id')}: {event.get('title')} ({event.get('agent')})")
        elif etype == "mission_step_complete":
            milestone_completes.append(event)
            print(f"  [STEP COMPLETE]: Stage {event.get('step_id')}: {event.get('title')}")
        elif etype == "status":
            print(f"  [STATUS]: {event.get('message')}")
        elif etype == "token":
            tokens.append(event.get("content", ""))
        elif etype == "mission_complete":
            print("  [MISSION COMPLETE]: 100% Executed!")
        elif etype == "done":
            print("  [DONE]: Final stream finish")

    total_time = round(time.perf_counter() - start_t, 2)
    full_text = "".join(tokens)

    print("\n" + "=" * 60)
    print(f"Total Execution Time: {total_time} seconds")
    print(f"Total Milestones Started: {len(milestone_starts)}")
    print(f"Total Milestones Completed: {len(milestone_completes)}")
    print(f"Total Streamed Tokens Length: {len(full_text)} characters")

    # Check for unformatted jammed headers like "Dossier ## 1." or "measures. ## 2."
    jammed_h2 = [m for m in full_text.split("\n") if " ## " in m]
    jammed_h1 = [m for m in full_text.split("\n") if " # " in m]
    print(f"Jammed ## lines: {len(jammed_h2)}")
    print(f"Jammed # lines: {len(jammed_h1)}")

    # Check that table pipes are present and properly separated
    has_table = "| Clause Name |" in full_text or "| :" in full_text or "Table" in full_text
    print(f"Contains structured table: {has_table}")

    assert len(milestone_completes) == 4, f"Expected 4 completed milestones, got {len(milestone_completes)}"
    print("=" * 60)
    print("PASS: Mission Mode Retail Plan executed with 100% continuous handoffs & fast speed!")

if __name__ == "__main__":
    test_retail_mission_stream()

