"""
Z16 Omni - Global Maritime Ports & Geospatial Corridors Engine.
Tracks international port hubs, container throughput, maritime choke points, and transit latency.
"""

from typing import Dict, Any, List

GLOBAL_PORT_HUBS = [
    {
        "port_name": "Port of Singapore",
        "country": "Singapore",
        "coordinates": {"lat": 1.2902, "lng": 103.8519},
        "annual_throughput_teu": "37.2 Million TEU",
        "key_chokepoint": "Strait of Malacca",
        "strategic_role": "Primary transshipment hub connecting Northeast India / Bay of Bengal to Far East Asia.",
        "congestion_index": "NORMAL (1.2 days wait)"
    },
    {
        "port_name": "Jebel Ali Port (Dubai)",
        "country": "United Arab Emirates",
        "coordinates": {"lat": 25.0069, "lng": 55.0617},
        "annual_throughput_teu": "14.1 Million TEU",
        "key_chokepoint": "Strait of Hormuz",
        "strategic_role": "India-Middle East Corridor (IMEC) anchor port; principal destination for Indian specialty commodities.",
        "congestion_index": "LOW (0.8 days wait)"
    },
    {
        "port_name": "Port of Rotterdam",
        "country": "Netherlands",
        "coordinates": {"lat": 51.9244, "lng": 4.4777},
        "annual_throughput_teu": "14.5 Million TEU",
        "key_chokepoint": "English Channel / North Sea",
        "strategic_role": "Gateway to Western Europe for high-value agricultural exports and manufacturing.",
        "congestion_index": "MODERATE (2.1 days wait)"
    },
    {
        "port_name": "Jawaharlal Nehru Port (JNPT Mumbai)",
        "country": "India",
        "coordinates": {"lat": 18.9499, "lng": 72.9515},
        "annual_throughput_teu": "6.0 Million TEU",
        "key_chokepoint": "Arabian Sea",
        "strategic_role": "India's premier container gateway with Dedicated Freight Corridor (DFC) rail links.",
        "congestion_index": "NORMAL (1.5 days wait)"
    },
    {
        "port_name": "Chittagong Port",
        "country": "Bangladesh",
        "coordinates": {"lat": 22.3167, "lng": 91.8000},
        "annual_throughput_teu": "3.1 Million TEU",
        "key_chokepoint": "Bay of Bengal",
        "strategic_role": "Closest maritime access point for Northeast India (Tripura & Barak Valley transit corridor).",
        "congestion_index": "ELEVATED (3.4 days wait)"
    },
    {
        "port_name": "Mundra Port (Adani)",
        "country": "India",
        "coordinates": {"lat": 22.8395, "lng": 69.7213},
        "annual_throughput_teu": "7.4 Million TEU",
        "key_chokepoint": "Gulf of Kutch / Arabian Sea",
        "strategic_role": "India's largest commercial container port serving Northern & Western industrial corridors.",
        "congestion_index": "NORMAL (1.1 days wait)"
    },
    {
        "port_name": "Paradip Port",
        "country": "India",
        "coordinates": {"lat": 20.2644, "lng": 86.6708},
        "annual_throughput_teu": "145 MMT Cargo",
        "key_chokepoint": "Bay of Bengal (Odisha)",
        "strategic_role": "East coast energy, coal, iron ore & refinery terminal.",
        "congestion_index": "NORMAL (1.3 days wait)"
    },
    {
        "port_name": "Pandu Inland Port (Guwahati)",
        "country": "India",
        "coordinates": {"lat": 26.1714, "lng": 91.6820},
        "annual_throughput_teu": "NW-2 Brahmaputra Multimodal",
        "key_chokepoint": "National Waterway 2 (Brahmaputra)",
        "strategic_role": "Northeast India's anchor riverine terminal connecting Assam to Haldia/Kolkata via Indo-Bangladesh Protocol Route.",
        "congestion_index": "OPTIMAL (0.5 days wait)"
    }
]

class GeospatialEngine:
    """Manages spatial coordinate resolution and maritime logistics tracking."""

    def get_port_telemetry(self, query: str = "") -> List[Dict[str, Any]]:
        if not query:
            return GLOBAL_PORT_HUBS
        import re
        words = [w for w in re.findall(r'[a-z0-9]+', query.lower()) if len(w) >= 4]
        def _score(p: Dict[str, Any]) -> int:
            hay = f"{p['port_name']} {p['country']} {p['strategic_role']} {p['key_chokepoint']}".lower()
            return sum(1 for w in words if w in hay)
        return sorted(GLOBAL_PORT_HUBS, key=_score, reverse=True)

geospatial_engine = GeospatialEngine()

