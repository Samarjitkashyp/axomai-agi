import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from axomai.memory.session_memory import session_conversation_memory
from axomai.agents.master_orchestrator import master_orchestrator

def test_multi_turn_conversation_recall():
    print("--- [TEST 1: Multi-Turn Conversation Memory Recall] ---", flush=True)
    test_session = "sess_tea_research_01"

    # Turn 1: User mentions a specific factual topic
    query1 = "Assam tea auction prices in Guwahati are soaring to 350 INR per kg due to weather disruptions."
    events1 = list(master_orchestrator.orchestrate_stream(query1, session_id=test_session))
    ans1 = ""
    for ev in events1:
        if ev.get("type") == "done":
            ans1 = ev.get("answer", "")

    sess = session_conversation_memory.get_session(test_session)
    assert sess is not None, "Session should exist"
    assert len(sess.turns) >= 2, f"Expected at least 2 turns (user + assistant), got {len(sess.turns)}"
    print(f"Turn 1 Recorded. Session Turns: {len(sess.turns)}, Tokens: {sess.total_tokens}", flush=True)

    # Turn 2: Follow-up referencing "iss topic par aur batao"
    query2 = "iss topic par aur batao, what are the supply chain impacts?"
    ctx_data = session_conversation_memory.get_conversation_context(test_session, query2)
    assert "Assam tea auction" in ctx_data["context_prompt"], "Prior context must be present in prompt"
    print("Multi-turn context prompt verified: includes prior discussion facts.", flush=True)

    events2 = list(master_orchestrator.orchestrate_stream(query2, session_id=test_session))
    ans2 = ""
    for ev in events2:
        if ev.get("type") == "done":
            ans2 = ev.get("answer", "")

    sess2 = session_conversation_memory.get_session(test_session)
    print(f"Turn 2 Completed. Total Turns: {len(sess2.turns)}, Tokens: {sess2.total_tokens}", flush=True)
    print("TEST 1 PASSED: Context retention across multiple turns works cleanly.\n", flush=True)


def test_100k_context_limit_and_new_chat_prompt():
    print("--- [TEST 2: 100k Context Token Limit & ChatGPT-Style New Chat Redirection] ---", flush=True)
    test_session = "sess_heavy_load_99"

    # Inject mock large turns to push past 100,000 tokens
    # E.g., 20 turns of 5,000 words each = ~135,000 tokens
    for i in range(22):
        session_conversation_memory.record_turn(
            session_id=test_session,
            role="user" if i % 2 == 0 else "assistant",
            content=f"Comprehensive financial audit analysis section {i}: " + ("data metric forecast revenue " * 1000)
        )

    sess = session_conversation_memory.get_session(test_session)
    print(f"Simulated High-Context Session Tokens: {sess.total_tokens:,} tokens", flush=True)
    assert sess.total_tokens >= 100_000, f"Expected >= 100k tokens, got {sess.total_tokens}"
    assert session_conversation_memory.is_context_exhausted(test_session), "Session must report exhausted at >= 100k tokens"

    # Now attempt a stream request with exhausted session
    events = list(master_orchestrator.orchestrate_stream("Can we continue with another query?", session_id=test_session))
    status_events = [e for e in events if e.get("stage") == "context_limit_reached"]
    done_events = [e for e in events if e.get("type") == "done"]

    assert len(status_events) > 0, "Expected context_limit_reached status event"
    done_ans = done_events[0].get("answer", "")
    assert "Session Context Limit Reached" in done_ans or "New Chat" in done_ans, "Exhaustion message must recommend New Chat"
    print("Exhaustion message received successfully:\n", done_ans[:350], "...", flush=True)

    # Verify session summary was archived to episodic memory
    from axomai.memory import unified_memory_hub
    with unified_memory_hub.episodic._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT episode_id, query, lesson_learned FROM episodic_episodes WHERE query LIKE ?", (f"%{test_session}%",))
        rows = cursor.fetchall()
        assert len(rows) > 0, "Session should be archived to episodic memory upon context exhaustion"
        print(f"Archived Episode Lesson: {rows[0]['lesson_learned'][:150]}...", flush=True)

    print("TEST 2 PASSED: 100k context limit and New Chat prompt work perfectly.\n", flush=True)


if __name__ == "__main__":
    test_multi_turn_conversation_recall()
    test_100k_context_limit_and_new_chat_prompt()
    print("=== ALL LONG CONTEXT MEMORY TESTS PASSED SUCCESSFULLY! ===", flush=True)
