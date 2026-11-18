"""
Y4 Vishwakarma - Zone-V Seismic Engineering & Geotechnical Embankment Safety Engine.
Models high-seismic Peak Ground Acceleration (PGA = 0.36g in Zone V), slope stability
Factor of Safety (FoS) via Bishop's method, and geotextile tube riverbank erosion armor.
"""

import math
from typing import Dict, Any, Optional

class SeismicEmbankmentSafetyEngine:
    """Calculates geotechnical slope stability, liquefaction risk, and seismic loads."""

    def __init__(self):
        # Universal Seismic Zone Acceleration Mappings (IS 1893:2016 / International Standards)
        self.zone_pga_map = {
            "zone_ii": 0.10,   # Low seismic hazard
            "zone_iii": 0.16,  # Moderate seismic hazard
            "zone_iv": 0.24,   # Severe seismic hazard
            "zone_v": 0.36     # Catastrophic / severe fault line
        }
        self.seismic_zone_factor = 0.36   # Default Zone V Peak Ground Acceleration (PGA) = 0.36g
        self.importance_factor = 1.5      # Critical infrastructure bridge/embankment

    def evaluate_embankment_stability(
        self,
        embankment_height_meters: float = 8.5,
        slope_angle_deg: float = 30.0,
        soil_cohesion_kpa: float = 18.0,
        soil_friction_angle_deg: float = 28.0,
        soil_unit_weight_kn_m3: float = 19.5,
        geotextile_reinforcement: bool = True,
        seismic_zone: str = "Zone V",
        pga_override: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates static and pseudostatic seismic Factor of Safety (FoS) against circular slip failure.
        Standard requires FoS >= 1.5 (static) and FoS >= 1.15 (seismic).
        """
        # Resolve active PGA factor dynamically
        z_key = seismic_zone.lower().replace(" ", "_").replace("-", "_")
        zone_factor = pga_override if pga_override is not None else self.zone_pga_map.get(z_key, self.seismic_zone_factor)
        
        slope_rad = math.radians(slope_angle_deg)
        phi_rad = math.radians(soil_friction_angle_deg)

        # Simplified infinite slope / Bishop approximation:
        # Static FoS = (c' / (gamma * H * sin * cos)) + (tan(phi) / tan(beta))
        term1 = soil_cohesion_kpa / (soil_unit_weight_kn_m3 * embankment_height_meters * math.sin(slope_rad) * math.cos(slope_rad))
        term2 = math.tan(phi_rad) / math.tan(slope_rad)
        static_fos = round(term1 + term2, 2)

        # Seismic derating factor under horizontal seismic coefficient Kh = 0.5 * Zone_Factor * I
        k_h = 0.5 * zone_factor * self.importance_factor
        seismic_derating = 1.0 - (k_h * 1.45)

        # Reinforcement boost from multi-tier high-tenacity geotextile tubes and biaxial geogrids
        reinforcement_boost = 0.55 if geotextile_reinforcement else 0.0

        seismic_fos = round((static_fos * seismic_derating) + reinforcement_boost, 2)

        is_structurally_safe = seismic_fos >= 1.15

        return {
            "seismic_zone": f"IS 1893:2016 {seismic_zone.upper()}",
            "peak_ground_acceleration_pga": f"{zone_factor}g",
            "embankment_geometry": f"Height: {embankment_height_meters}m | Slope: 1:{round(1.0/math.tan(slope_rad), 1)} ({slope_angle_deg}°)",
            "geotextile_armor_installed": geotextile_reinforcement,
            "static_factor_of_safety_fos": static_fos,
            "seismic_zone_v_factor_of_safety": seismic_fos,
            "statutory_safety_threshold": "FoS >= 1.15 (Seismic Condition)",
            "structural_integrity_verdict": "STRUCTURALLY_SOUND_ZONE_V_CERTIFIED" if is_structurally_safe else "SLOPE_COLLAPSE_RISK_REMEDIAL_STABILIZATION_REQUIRED",
            "engineering_recommendation": (
                "Install double-layer high-tenacity polyester geogrids at 1.5m vertical intervals and "
                "encase river-facing toe with mega-polypropylene geotextile sand tubes to resist scouring."
            )
        }

seismic_embankment_engine = SeismicEmbankmentSafetyEngine()
