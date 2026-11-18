import sqlite3
from axomai.config import settings

db_path = settings.STORAGE_DIR / "cognitive_memory.db"
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute("DELETE FROM semantic_triples WHERE subject_name IN ('Orthodox Tea', 'Changsari Logistics Hub', 'Solar Rooftop PPA', 'FIDIC Clause 20.1')")
    c.execute("DELETE FROM semantic_entities WHERE entity_name IN ('Orthodox Tea', 'Changsari Logistics Hub', 'Siliguri Corridor', 'Solar Rooftop PPA', 'FIDIC Clause 20.1')")
    conn.commit()
    print("Cleaned regional seed from cognitive_memory.db, total changes:", conn.total_changes)
    conn.close()
