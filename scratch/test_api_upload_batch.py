import sys
import io
sys.path.insert(0, r"e:\axomai_agi\src")

from fastapi.testclient import TestClient
from axomai.api.app import app

client = TestClient(app)

print("--- 1. Testing GET / (HTML response, check aside removed) ---")
res = client.get("/")
assert res.status_code == 200
html = res.text
assert "<aside" not in html, "<aside> should not be present in HTML"
assert "attached-files-tray" in html, "attached-files-tray should be present"
assert "file-input" in html, "file-input should be present"
print("HTML verified: Left sidebar is completely removed and attached files tray is present!")

print("\n--- 2. Testing POST /api/upload with Malicious File (.exe) ---")
bad_file = ("trojan.exe", b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00", "application/octet-stream")
res = client.post("/api/upload", files={"file": bad_file})
print(f"Malicious upload response status: {res.status_code}, detail: {res.json().get('detail')}")
assert res.status_code == 400, "Should reject malicious file with 400"
assert "Security Alert" in res.json().get("detail", ""), "Should have Security Alert in detail"

print("\n--- 3. Testing POST /api/upload-batch with Safe Text and CSV Files ---")
f1 = ("doc1.txt", b"AxomAI AGI Document 1 content: Q1 revenue was 150 crore INR.", "text/plain")
f2 = ("doc2.csv", b"Quarter,Revenue\nQ1,150\nQ2,180\nQ3,210", "text/csv")
res = client.post("/api/upload-batch", files=[("files", f1), ("files", f2)])
print(f"Batch upload status: {res.status_code}")
data = res.json()
print(f"Uploaded count: {data.get('count')}, documents: {[d['filename'] for d in data.get('documents', [])]}")
assert res.status_code == 200
assert data.get("count") == 2

print("\n--- 4. Testing Multi-Document Master Stream ---")
doc_ids = [d["document_id"] for d in data.get("documents", []) if d.get("document_id")]
print(f"Testing master-stream with document_ids: {doc_ids}")
res_stream = client.post("/api/master-stream", json={
    "query": "Compare the revenue metrics across both documents",
    "document_ids": doc_ids,
    "manual_agent": "auto"
})
assert res_stream.status_code == 200
body = res_stream.text
print(f"Stream response sample: {body[:300]}...")
assert "Comparing 2 Files" in body or "data: " in body, "Stream should contain events"

print("\nAll API Batch Upload & Security Tests Passed 100%!")

