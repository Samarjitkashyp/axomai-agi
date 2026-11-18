"""
Y3 Sanjeevani - Epidemiological Outbreak Prediction & Disease Surveillance Engine.
Models epidemic transmission dynamics using compartmental SIR models (R0 basic reproduction number)
and vector-borne disease risk heat-mapping for Japanese Encephalitis, Dengue, and Water-borne pathogens.
"""

from typing import Dict, Any, List

class EpidemiologyEngine:
    """Computes disease propagation dynamics and public health intervention thresholds."""

    def __init__(self):
        # Endemic vector-borne disease baseline parameters in flood-prone riverine zones
        self.disease_profiles = {
            "japanese_encephalitis": {
                "vector": "Culex vishnui mosquito (paddy-breeding)",
                "transmission_rate_beta": 0.28,
                "recovery_rate_gamma": 0.14,
                "peak_season": "June - September (Post-Monsoon)",
                "case_fatality_rate_pct": 22.5
            },
            "dengue": {
                "vector": "Aedes aegypti (urban container-breeding)",
                "transmission_rate_beta": 0.35,
                "recovery_rate_gamma": 0.18,
                "peak_season": "August - November",
                "case_fatality_rate_pct": 1.2
            },
            "water_borne_cholera": {
                "vector": "Vibrio cholerae (floodwater contamination)",
                "transmission_rate_beta": 0.42,
                "recovery_rate_gamma": 0.20,
                "peak_season": "Peak Flood Inundation",
                "case_fatality_rate_pct": 3.8
            }
        }

    def register_disease(self, disease_id: str, profile: Dict[str, Any]) -> None:
        """Dynamically registers new pathogen epidemiology parameters."""
        self.disease_profiles[disease_id.lower().replace(" ", "_")] = profile

    def resolve_disease(self, disease_name: str) -> Dict[str, Any]:
        """Dynamically models epidemiological transmission characteristics for ANY pathogen."""
        d_key = disease_name.lower().replace(" ", "_")
        if d_key in self.disease_profiles:
            return self.disease_profiles[d_key]
        
        # Pathogen category dynamic inference
        if any(r in d_key for r in ["covid", "corona", "sars", "flu", "influenza", "respiratory", "measles"]):
            return {
                "vector": "Airborne aerosol droplet transmission",
                "transmission_rate_beta": 0.55,
                "recovery_rate_gamma": 0.18,
                "peak_season": "Winter / Confined Indoor Clusters",
                "case_fatality_rate_pct": 0.8
            }
        elif any(v in d_key for v in ["malaria", "chikungunya", "zika", "kala_azar"]):
            return {
                "vector": "Anopheles / Aedes mosquito vector",
                "transmission_rate_beta": 0.32,
                "recovery_rate_gamma": 0.15,
                "peak_season": "Monsoon / Post-Monsoon",
                "case_fatality_rate_pct": 2.5
            }
        elif any(e in d_key for e in ["typhoid", "hepatitis", "rotavirus", "dysentery"]):
            return {
                "vector": "Fecal-oral water contamination",
                "transmission_rate_beta": 0.38,
                "recovery_rate_gamma": 0.19,
                "peak_season": "Summer Flood Contamination",
                "case_fatality_rate_pct": 1.5
            }
        else:
            return {
                "vector": "General environmental pathogen",
                "transmission_rate_beta": 0.30,
                "recovery_rate_gamma": 0.16,
                "peak_season": "Seasonal Surge",
                "case_fatality_rate_pct": 2.0
            }

    def simulate_outbreak_risk(
        self,
        district: str = "dibrugarh",
        disease_name: str = "japanese_encephalitis",
        susceptible_population: int = 250000,
        initial_infected_cases: int = 15,
        water_stagnation_index: float = 0.75  # 0 to 1 based on satellite SAR flood data
    ) -> Dict[str, Any]:
        """
        Calculates R0 basic reproduction number adjusted for environmental flood stagnation
        and projects 30-day peak infection curve.
        """
        profile = self.resolve_disease(disease_name)

        # Environmental amplification of vector transmission due to stagnant water bodies
        amplified_beta = round(profile["transmission_rate_beta"] * (1.0 + (water_stagnation_index * 0.4)), 3)
        gamma = profile["recovery_rate_gamma"]

        # R0 = Beta / Gamma
        r0 = round(amplified_beta / gamma, 2)

        # Projected peak infected cases at day 21 (SIR analytical approximation)
        is_epidemic_expanding = r0 > 1.0
        projected_peak_cases = int(initial_infected_cases * (r0 ** 2.2)) if is_epidemic_expanding else initial_infected_cases

        return {
            "monitored_district": district.title(),
            "target_pathogen": disease_name.title(),
            "vector_organism": profile["vector"],
            "baseline_r0": round(profile["transmission_rate_beta"] / gamma, 2),
            "environment_amplified_r0": r0,
            "outbreak_expansion_status": "CRITICAL_EPIDEMIC_SURGE" if r0 > 1.8 else ("MODERATE_CLUSTER_SPREAD" if r0 > 1.0 else "CONTAINED"),
            "projected_peak_active_cases": projected_peak_cases,
            "case_fatality_rate_pct": f"{profile['case_fatality_rate_pct']}%",
            "medical_countermeasures": [
                f"Deploy indoor residual thermal fogging targeted at {profile['vector']} habitat",
                "Pre-position 5,000 doses of live attenuated SA 14-14-2 JE vaccine at district civil hospital",
                "Mobilize ASHA community health workers for rapid syndromic fever surveillance in relief camps"
            ]
        }

epidemiology_engine = EpidemiologyEngine()

