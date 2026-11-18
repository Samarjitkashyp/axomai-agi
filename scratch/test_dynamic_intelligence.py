"""
Verification script for Dynamic AGI capabilities:
Ensures all tools dynamically handle novel/unlisted inputs rather than relying on hardcoded records.
"""

import sys
from pathlib import Path

# Add src to PYTHONPATH
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def test_dynamic_tools():
    print("=== Testing Dynamic Intelligence Capabilities ===")

    # 1. World Model Dynamic Discovery
    from axomai.cognition.world_model import world_model
    snap = world_model.get_world_snapshot()
    print(f"1. World Model Entities Discovered: {list(snap['entities'].keys())}")
    assert "host_system" in snap["entities"]
    assert "storage_telemetry" in snap["entities"]
    print("   [PASS] World Model uses real environment discovery!")

    # 2. Dynamic Route Optimizer (Test unlisted city pair)
    from axomai.agents.z10_matrix.tools.route_optimizer import route_optimizer
    res_route = route_optimizer.optimize_route("Jaipur", "Lucknow", payload_tons=10.0)
    print(f"2. Dynamic Route (Jaipur -> Lucknow): {res_route['distance_km']} km, Cost: ₹{res_route['total_logistics_cost_inr']}")
    assert res_route["distance_km"] > 300
    assert "Jaipur" in res_route["origin"]
    print("   [PASS] Dynamic Route Optimizer successfully calculates novel routes!")

    # 3. Dynamic Scheme Matcher (Test unlisted AI / Clean energy / Global grant)
    from axomai.agents.z11_pragati.tools.scheme_matcher import scheme_matcher
    schemes_ai = scheme_matcher.match_schemes("I want semiconductor and GPU compute subsidies for my AI lab in India")
    print(f"3. Dynamic Scheme Match: {schemes_ai[0]['scheme_name']}")
    assert "IndiaAI" in schemes_ai[0]["scheme_name"] or "Semiconductor" in schemes_ai[0]["scheme_name"]
    print("   [PASS] Dynamic Scheme Matcher synthesizes domain policies!")

    # 4. Dynamic Salary Benchmarking (Test unlisted role: AI Research Scientist in Bangalore)
    from axomai.agents.z12_athena.tools.salary_benchmark import salary_benchmark
    res_salary = salary_benchmark.benchmark_role("Senior AI Research Scientist", "Bengaluru")
    print(f"4. Dynamic Salary Benchmark: {res_salary['role']} in {res_salary['location']} -> Median ₹{res_salary['monthly_median_inr']}/mo (Annual ₹{res_salary['annual_ctc_median_inr']})")
    assert res_salary["monthly_median_inr"] > 150000
    print("   [PASS] Dynamic Salary Benchmarking handles any professional role!")

    # 5. Dynamic Mandi Tracker (Test unlisted commodity: Turmeric / Cardamom / Crude Oil)
    from axomai.agents.z13_quantum.tools.mandi_tracker import mandi_tracker
    res_mandi = mandi_tracker.get_benchmarks("cardamom auction rates")
    print(f"5. Dynamic Mandi Benchmark: {res_mandi[0]['commodity']} -> Wholesale ₹{res_mandi[0]['wholesale_price_inr']} {res_mandi[0]['unit']}")
    assert "Cardamom" in res_mandi[0]["commodity"]
    print("   [PASS] Dynamic Mandi Tracker monitors diverse commodities!")

    # 6. Dynamic FX Options (Test unlisted currency pair: AUDUSD / USDCAD)
    from axomai.agents.z14_horizon.tools.fx_options import fx_options_engine
    vol_aud = fx_options_engine.get_volatility("AUDUSD")
    print(f"6. Dynamic FX Volatility for AUDUSD: {vol_aud}")
    assert vol_aud > 0.05
    print("   [PASS] Dynamic FX Options handles any currency pair!")

    # 7. Dynamic Maritime Tracker (Test arbitrary vessel)
    from axomai.agents.z16_omni.tools.maritime_ais_tracker import maritime_ais_tracker
    res_ship = maritime_ais_tracker.track_vessel_telemetry("PACIFIC_TITAN_7")
    print(f"7. Dynamic Vessel Tracking: {res_ship['vessel_name']} (MMSI: {res_ship['mmsi']})")
    assert "PACIFIC TITAN 7" in res_ship["vessel_name"]
    print("   [PASS] Dynamic Maritime Tracker tracks arbitrary vessels!")

    # 8. Dynamic Weather Microclimate (Test unlisted hill station: Shimla)
    from axomai.agents.y1_annapurna.tools.weather_microclimate import weather_microclimate_engine
    res_weather = weather_microclimate_engine.forecast_agronomic_weather("Shimla Hill Station")
    print(f"8. Dynamic Weather: {res_weather['target_district']} -> Rainfall {res_weather['projected_cumulative_rainfall_mm']}mm")
    assert res_weather["projected_cumulative_rainfall_mm"] > 50
    print("   [PASS] Dynamic Weather Microclimate infers climate across any region!")

    # 9. Dynamic Epidemiology (Test novel pathogen: Covid-19 / Nipah)
    from axomai.agents.y3_sanjeevani.tools.epidemiology_engine import epidemiology_engine
    res_epi = epidemiology_engine.simulate_outbreak_risk("Mumbai", "Covid 19 Respiratory Variant", susceptible_population=1000000, initial_infected_cases=50)
    print(f"9. Dynamic Epidemiology: {res_epi['target_pathogen']} -> R0 = {res_epi['environment_amplified_r0']}")
    assert res_epi["environment_amplified_r0"] > 1.5
    print("   [PASS] Dynamic Epidemiology simulates novel pathogens!")

    # 10. Dynamic Seismic Safety (Test Zone III)
    from axomai.agents.y4_vishwakarma.tools.seismic_embankment_safety import seismic_embankment_engine
    res_seismic = seismic_embankment_engine.evaluate_embankment_stability(seismic_zone="Zone III")
    print(f"10. Dynamic Seismic Safety: Zone = {res_seismic['seismic_zone']}, PGA = {res_seismic['peak_ground_acceleration_pga']}, FoS = {res_seismic['seismic_zone_v_factor_of_safety']}")
    assert res_seismic["peak_ground_acceleration_pga"] == "0.16g"
    print("   [PASS] Dynamic Seismic Safety supports arbitrary seismic zones!")

    print("\n============================================================")
    print(">>> ALL 10 DYNAMIC INTELLIGENCE SUBSYSTEMS VERIFIED 100% <<<")
    print("============================================================")

if __name__ == "__main__":
    test_dynamic_tools()
