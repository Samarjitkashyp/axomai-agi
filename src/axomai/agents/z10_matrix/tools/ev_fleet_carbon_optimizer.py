"""
Z10 Matrix - EV vs Diesel Fleet TCO & Scope 3 Carbon Credit Optimizer.
Compares Diesel HCV vs Electric Commercial Truck Total Cost of Ownership (TCO) per km,
calculates Scope 3 CO2 emissions avoided, and estimates Carbon Credit revenue (INR).
"""

from typing import Dict, Any


class EvFleetCarbonOptimizer:
    """Computes Electric vs Diesel Freight Economics and Scope 3 Carbon Credits."""

    def compare_ev_vs_diesel(
        self,
        total_distance_km: float = 350.0,
        cargo_tons: float = 12.0,
        diesel_cost_inr: float = 8500.0,
        electricity_inr_per_kwh: float = 8.5,
        carbon_credit_inr_per_ton: float = 1200.0
    ) -> Dict[str, Any]:
        # Medium/Heavy EV Truck consumes ~1.35 kWh/km
        ev_energy_kwh = round(total_distance_km * 1.35, 1)
        ev_energy_cost_inr = round(ev_energy_kwh * electricity_inr_per_kwh, 2)
        opex_savings_inr = round(max(0.0, diesel_cost_inr - ev_energy_cost_inr), 2)

        # Diesel CO2: ~0.096 kg per ton-km; India grid EV Scope 2: ~0.038 kg per ton-km
        diesel_co2_kg = round(total_distance_km * cargo_tons * 0.096, 1)
        ev_co2_kg = round(total_distance_km * cargo_tons * 0.038, 1)
        co2_saved_tons = round(max(0.0, (diesel_co2_kg - ev_co2_kg) / 1000.0), 3)
        carbon_credit_value_inr = round(co2_saved_tons * carbon_credit_inr_per_ton, 2)

        return {
            "total_distance_km": total_distance_km,
            "diesel_energy_cost_inr": diesel_cost_inr,
            "ev_energy_kwh_required": ev_energy_kwh,
            "ev_charging_cost_inr": ev_energy_cost_inr,
            "direct_fuel_savings_inr": opex_savings_inr,
            "diesel_co2_kg": diesel_co2_kg,
            "ev_co2_kg": ev_co2_kg,
            "net_co2_saved_tons": co2_saved_tons,
            "carbon_credit_revenue_inr": carbon_credit_value_inr,
            "green_verdict": "HIGH_EV_SAVINGS" if opex_savings_inr > 0 else "DIESEL_PARITY"
        }


ev_carbon_optimizer = EvFleetCarbonOptimizer()
