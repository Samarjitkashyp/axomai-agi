"""
AxomAI Cognition Engine - Cognitive Intent & Language Resonance Profiler.
Analyzes user queries across multi-level dimensions:
1. Language & Cultural Tone (Hinglish, Hindi, Assamese, English) for authentic resonance.
2. Intent Archetype (Strategic Consultation vs Implementation vs Conceptual vs Execution).
3. Domain Ontology & Ground Realities (Injecting real-world constraints like e-commerce variants,
   payment gateways, and shipping logistics into reasoning).
4. Progressive Disclosure Strategy (Consultative dialogue first, deep implementation upon request).
"""

import re
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class CognitiveProfile:
    query: str
    language: str  # "hinglish" | "hindi" | "assamese_bengali" | "english"
    language_prompt_directive: str
    intent_archetype: str  # "ADVISORY_STRATEGY" | "IMPLEMENTATION_CODE" | "CONCEPTUAL_EXPLANATION" | "TASK_EXECUTION" | "GENERAL_CONVERSATION"
    target_role: str  # "Chief Technology Officer / Solution Strategist" | "Lead Software Engineer" | "Domain Mentor"
    domain: str  # "ecommerce" | "fintech" | "healthcare" | "edtech" | "logistics" | "general_software" | "general"
    domain_invariants: List[str] = field(default_factory=list)
    prohibit_code_dump: bool = False
    requires_progressive_disclosure: bool = False
    consultation_roadmap: Optional[Dict[str, Any]] = None

class CognitiveIntentProfiler:
    """Universal Zero-Shot Cognitive Intent & Language Resonance Engine."""

    def __init__(self):
        # Hinglish indicators (Latin-script conversational Hindi/Urdu keywords)
        self.hinglish_keywords = {
            "kya", "kaise", "kaisa", "kaisi", "kyu", "kyun", "kyo", "kis", "kisko", "kisme",
            "muje", "mujhe", "mera", "meri", "mere", "hume", "humko", "humara", "humari",
            "karna", "kare", "karega", "karenge", "karti", "karta", "karu", "karun", "kar", "karke",
            "banana", "banaye", "banayenge", "banau", "banaun", "banayein",
            "chahiye", "chiye", "chaiye", "chahie", "batao", "bataiye", "bata",
            "hoga", "hogi", "hoge", "honge", "hai", "hain", "he", "tha", "thi", "the",
            "par", "mai", "main", "me", "mein", "se", "ko", "ke", "ki", "ka", "liye", "bhi",
            "aur", "ya", "toh", "to", "matlab", "mtlb", "mtalab",
            "thik", "theek", "sahi", "accha", "achha", "behtar", "acha",
            "dukan", "saman", "bechna", "kharidna", "lena", "dena", "daal",
            "karo", "kijiye", "mat", "nahi", "nhi", "haan", "ha", "sirf", "bas",
            "likh", "likho", "likhkar", "de", "do",
            "aage", "pehle", "pehla", "dono", "sabse", "badlo", "hatao", "batao"
        }

        # Intent Archetype Rules
        self.code_keywords = [
            "code likh", "code do", "code bana", "write code", "implement code", "give code",
            "script likho", "script do", "write script", "create script", "function likho",
            "boilerplate code", "full code", "code snippet", "code generate", "debug this code",
            "write python", "write javascript", "write react", "write sql", "syntax do"
        ]

        self.advice_keywords = [
            "kya use karu", "kya use kare", "kya use karna", "konsi technology", "kis technology",
            "konsa stack", "which technology", "what technology", "what stack", "which framework",
            "which language", "advice", "recommend", "guide me", "kaise shuru karu", "kaise start karu",
            "kaise kare", "best way to", "pros and cons", "options", "comparison", "kya behtar hai",
            "suggest karo", "batao muje kis", "batao konsa", "architecture advice", "solution design",
            "which is better", "should i use", "guide karo", "suggestions", "kaunsa use karu"
        ]

        self.concept_keywords = [
            "kya hota hai", "kya hai", "explain", "samjhao", "what is", "meaning of",
            "difference between", "kaise kaam karta", "how it works", "definition of",
            "overview of", "deep dive into"
        ]

        self.exec_keywords = [
            "deploy", "run", "execute", "scan", "benchmark", "profile", "scrape",
            "crawl", "reverse engineer", "clone app", "test e2e", "audit cve"
        ]

    def detect_language(self, query: str) -> Dict[str, Any]:
        """Detects language script and stylistic resonance."""
        q_lower = query.lower().strip()
        
        # Devanagari Script (Hindi)
        if re.search(r'[\u0900-\u097F]', query):
            return {
                "language": "hindi",
                "directive": (
                    "User is writing in Hindi (Devanagari). "
                    "Respond exclusively in fluent, elegant, and natural Hindi (Devanagari script)."
                )
            }

        # Bengali/Assamese Script
        if re.search(r'[\u0980-\u09FF]', query):
            return {
                "language": "assamese_bengali",
                "directive": (
                    "User is writing in Assamese/Bengali script. "
                    "Respond gracefully in the respective language."
                )
            }

        # Check Latin-script tokens for Hinglish
        words = re.findall(r'\b[a-zA-Z]+\b', q_lower)
        hinglish_count = sum(1 for w in words if w in self.hinglish_keywords)
        is_hinglish = (hinglish_count >= 2) or (len(words) <= 5 and hinglish_count >= 1)

        if is_hinglish:
            return {
                "language": "hinglish",
                "directive": (
                    "CRITICAL LANGUAGE DIRECTIVE: The user communicates in natural Hinglish (Hindi in Roman script). "
                    "You MUST respond in natural, professional, intelligent Hinglish (Hindi words in clean Latin script). "
                    "DO NOT SWITCH TO FORMAL TEXTBOOK ENGLISH. "
                    "Speak like a world-class CTO / strategic advisor chatting with a founder — warm, sharp, authoritative, and consultative."
                )
            }

        return {
            "language": "english",
            "directive": (
                "User communicates in English. Respond in clear, articulate, and well-structured professional English."
            )
        }

    def detect_domain(self, query: str) -> Dict[str, Any]:
        """Maps query to domain ontology and extracts real-world non-toy constraints."""
        q = query.lower()

        # 1. E-Commerce & Retail
        if any(k in q for k in ["shoes", "shoe", "clothes", "clothing", "tshirt", "store", "shop", "ecommerce", "e-commerce", "sell", "buy", "cart", "checkout", "inventory", "products", "mens", "womens", "kids", "sneakers", "footwear", "retail", "dukan"]):
            return {
                "domain": "ecommerce",
                "invariants": [
                    "Variant Management: Shoes require a multi-dimensional matrix (Brand -> Model -> Color -> Sizes like UK 6-11) with independent SKU stock per variant, not a single scalar size.",
                    "Payment Infrastructure: Instant integration with payment gateways (Razorpay, Stripe, Cash on Delivery verification) with webhook status handling.",
                    "Logistics & Shipping: Automated integration with shipping aggregators (Shiprocket, Delhivery, Bluedart) for pin-code serviceability, label generation, and real-time tracking.",
                    "Statutory Tax & Invoicing: Automated GST invoicing (CGST, SGST, IGST) and compliance.",
                    "Cart & Inventory Reservation: Atomic stock locking to prevent overselling high-demand sizes during simultaneous checkout."
                ],
                "fast_track_solution": "Shopify / WooCommerce (Ready in 24-48 hours, built-in payments & logistics)",
                "custom_scale_solution": "Next.js App Router (Storefront) + Headless Engine (MedusaJS / Shopify Storefront API) + PostgreSQL + Redis"
            }

        # 2. Fintech & Banking
        if any(k in q for k in ["bank", "payment", "loan", "emi", "transaction", "wallet", "transfer", "ledger", "balance", "crypto", "trading", "stock"]):
            return {
                "domain": "fintech",
                "invariants": [
                    "Double-Entry Ledger: Every monetary transfer must have an immutable debit and credit pair; zero balance drift.",
                    "PCI-DSS & Security: Cardholder data tokenization, zero plain-text storage.",
                    "Idempotency: Every financial API endpoint must mandate unique idempotency keys to prevent duplicate billing on network retry."
                ]
            }

        # 3. Healthcare & Medicine
        if any(k in q for k in ["doctor", "hospital", "clinic", "patient", "disease", "symptom", "medicine", "pharmacy", "health"]):
            return {
                "domain": "healthcare",
                "invariants": [
                    "Regulatory Disclaimer: Clear clinical guidance disclaimers.",
                    "HIPAA & Data Privacy: End-to-end encrypted electronic health records (EHR).",
                    "Authentic Medical Evidence: Grounded in peer-reviewed clinical knowledge."
                ]
            }

        # 4. Logistics & Fleet
        if any(k in q for k in ["freight", "truck", "corridor", "demurrage", "warehouse", "depot", "fleet", "shipping container", "multimodal"]):
            return {
                "domain": "logistics",
                "invariants": [
                    "Dynamic Corridors: Turnaround times, fuel surcharges, toll optimization.",
                    "Geofencing & Telematics: Live GPS tracking and detention alerting."
                ]
            }

        # 5. Search, AEO, GEO & Digital Visibility
        if any(k in q for k in ["seo", "aeo", "geo", "audit", "meta tag", "search engine", "ranking", "perplexity", "schema", "sitemap", "backlink"]):
            return {
                "domain": "digital_marketing_seo",
                "invariants": [
                    "Multi-Pillar Auditing: Balance Traditional SEO, Conversational AEO, and Generative GEO.",
                    "Schema.org Validation: Ensure strict JSON-LD syntax compliance.",
                    "Actionable Code Fixes: Provide ready-to-paste drop-in tags and blueprints."
                ]
            }

        # 6. Default General Software
        return {
            "domain": "general_software",
            "invariants": [
                "Scalability & Decoupling: Stateless API layer with durable persistence.",
                "Zero-Tolerance for Hallucination: Grounded architecture and clear trade-offs."
            ]
        }

    def profile_query(self, query: str) -> CognitiveProfile:
        """Computes the full 5-tier cognitive profile of the incoming user request."""
        lang_info = self.detect_language(query)
        dom_info = self.detect_domain(query)
        q_lower = query.lower().strip()

        # Detect Archetype
        has_code_intent = any(k in q_lower for k in self.code_keywords)
        has_advice_intent = any(k in q_lower for k in self.advice_keywords)
        has_concept_intent = any(k in q_lower for k in self.concept_keywords)
        has_exec_intent = any(k in q_lower for k in self.exec_keywords)

        # Disambiguation: If user asks "kaise banaye" or "kis technology ko use kare", this is ADVISORY_STRATEGY, NOT CODE DUMP
        if has_advice_intent or ("website banana" in q_lower and not has_code_intent) or ("app banana" in q_lower and not has_code_intent):
            archetype = "ADVISORY_STRATEGY"
            target_role = "Chief Technology Officer / Solution Strategist"
            prohibit_code_dump = True
            requires_progressive_disclosure = True
        elif has_code_intent:
            archetype = "IMPLEMENTATION_CODE"
            target_role = "Lead Software Engineer & Code Architect"
            prohibit_code_dump = False
            requires_progressive_disclosure = False
        elif has_concept_intent:
            archetype = "CONCEPTUAL_EXPLANATION"
            target_role = "Principal Domain Mentor"
            prohibit_code_dump = True
            requires_progressive_disclosure = False
        elif has_exec_intent:
            archetype = "TASK_EXECUTION"
            target_role = "Autonomous Systems Operator"
            prohibit_code_dump = False
            requires_progressive_disclosure = False
        else:
            archetype = "GENERAL_CONVERSATION"
            target_role = "AxomAI Autonomous Intelligence Partner"
            prohibit_code_dump = True
            requires_progressive_disclosure = False

        return CognitiveProfile(
            query=query,
            language=lang_info["language"],
            language_prompt_directive=lang_info["directive"],
            intent_archetype=archetype,
            target_role=target_role,
            domain=dom_info["domain"],
            domain_invariants=dom_info["invariants"],
            prohibit_code_dump=prohibit_code_dump,
            requires_progressive_disclosure=requires_progressive_disclosure,
            consultation_roadmap=dom_info if archetype == "ADVISORY_STRATEGY" else None
        )

cognitive_intent_profiler = CognitiveIntentProfiler()
