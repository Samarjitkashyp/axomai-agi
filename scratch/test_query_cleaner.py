import re

def clean_conversational_query(q: str) -> str:
    if ":" in q:
        parts = q.split(":")
        q = parts[0] if len(parts[0].split()) >= 3 else parts[1]

    cleaned = re.sub(
        r'^(can you tell me|can you please tell me|tell me|please tell me|what is|what are|batao|kya hai|kuch batao|perform deep market research on|analyze|assess|conduct|model|audit)\s*',
        '',
        q.strip(),
        flags=re.IGNORECASE
    )
    cleaned = re.sub(r'[,;:\"\'\(\)\[\]{}]+', ' ', cleaned).strip()

    words = cleaned.split()
    if len(words) > 6:
        stop_words = {'the', 'a', 'an', 'and', 'or', 'for', 'with', 'in', 'on', 'at', 'to', 'from', 'of', 'pehle', 'ka', 'ke', 'me', 'nayi', 'banao', 'perform', 'deep', 'top', 'conduct', 'model', 'assess', 'district', 'districts'}
        meaningful = [w for w in words if w.lower() not in stop_words]
        cleaned = ' '.join(meaningful[:5]) if meaningful else ' '.join(words[:5])

    return cleaned or q

for t in [
    'Kamrup Metropolitan commercial district population density consumer spending footfall density competitor presence commercial real estate pricing 2026',
    'Nagaon commercial district market analysis population density consumer spending footfall density competitor presence 2026',
    'Dibrugarh commercial district commercial real estate pricing population density consumer spending competitor presence 2026'
]:
    print(t[:30], '->', repr(clean_conversational_query(t)))

