"""
Comprehensive Automated Verification Suite for Y-Series Agents (Y1 - Y5).
Tests:
1. Y1 Annapurna (Doppler Microclimate, Soil NPK, MCX Futures)
2. Y2 Urja (Solar/Hydro LCOE, VCS Carbon Offsets, Green Open Access PPA)
3. Y3 Sanjeevani (Epidemiology SIR Model, IoT Cold-Chain MKT, CDSCO Schedule M)
4. Y4 Vishwakarma (Primavera 4D EVM Delay, FIDIC Claims, Zone-V Seismic FoS)
5. Y5 Chanakya (OFAC Sanctions, Siliguri Chokepoint, OSINT Synthesis)
6. Master Orchestrator Intent Routing & Auto-Pilot Dispatch
7. Mission Control Planner & Step Verification
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

def test_y1_annapurna():
    print("--- [1/6] Testing Y1 Annapurna (Agri-Science & Commodity Futures) ---")
    from axomai.agents.y1_annapurna.tools.weather_microclimate import weather_microclimate_engine
    from axomai.agents.y1_annapurna.tools.soil_chemistry import soil_chemistry_engine
    from axomai.agents.y1_annapurna.tools.commodity_futures import commodity_futures_engine
    from axomai.agents.y1_annapurna.agent import y1_annapurna_agent

    # 1. Weather Microclimate
    w = weather_microclimate_engine.forecast_agronomic_weather("dibrugarh", 7)
    assert w["projected_cumulative_rainfall_mm"] > 0
    print(f"  ✓ Weather Forecast: {w['target_district']} QPF={w['projected_cumulative_rainfall_mm']}mm, Radar={w['doppler_radar_reflectivity_dbz']}dBZ")

    # 2. Soil NPK
    s = soil_chemistry_engine.prescribe_soil_nutrition(crop_type="tea", soil_ph=4.2)
    assert s["soil_ph"] == 4.2
    assert s["fertilizer_prescriptions_kg_ha"]["commercial_urea_46n"] > 0
    print(f"  ✓ Soil Nutrition: pH={s['soil_ph']} ({s['ph_status']}), Urea needed={s['fertilizer_prescriptions_kg_ha']['commercial_urea_46n']}kg/ha")

    # 3. Commodity Futures
    f = commodity_futures_engine.price_commodity_futures("assam_orthodox_tea", tenor_months=3)
    assert f["theoretical_futures_price_inr_per_kg"] > f["spot_price_inr_per_kg"]
    print(f"  ✓ MCX Futures: Spot=₹{f['spot_price_inr_per_kg']}, 3M Futures=₹{f['theoretical_futures_price_inr_per_kg']}, Beta={f['optimal_hedge_ratio_beta']}")

    # 4. Agent Stream
    events = list(y1_annapurna_agent.agri_stream("Optimize tea estate NPK fertilization and MCX futures hedge"))
    assert any(e.get("type") == "final" for e in events)
    print("  ✓ Y1 Annapurna stream generated successfully.")

def test_y2_urja():
    print("\n--- [2/6] Testing Y2 Urja (Green Energy & Carbon Credits) ---")
    from axomai.agents.y2_urja.tools.solar_hydro_feasibility import solar_hydro_engine
    from axomai.agents.y2_urja.tools.carbon_credits import carbon_credits_engine
    from axomai.agents.y2_urja.tools.ppa_grid_optimizer import ppa_grid_optimizer
    from axomai.agents.y2_urja.agent import y2_urja_agent

    # 1. Solar & Hydro Feasibility
    solar = solar_hydro_engine.evaluate_rooftop_solar_pv(roof_area_sqft=25000.0)
    hydro = solar_hydro_engine.evaluate_micro_hydro(flow_rate_m3_sec=1.2, head_height_meters=15.0)
    assert solar["installed_capacity_kwp"] == 250.0
    assert hydro["continuous_rated_power_kw"] > 0
    print(f"  ✓ Solar & Hydro: Capacity={solar['installed_capacity_kwp']}kWp, LCOE=₹{solar['levelized_cost_of_energy_lcoe_inr_kwh']}/kWh, Hydro={hydro['continuous_rated_power_kw']}kW")

    # 2. Carbon Credits
    carbon = carbon_credits_engine.quantify_carbon_credits(clean_generation_kwh=solar["annual_generation_kwh"])
    assert carbon["annual_carbon_credits_generated_tco2e"] > 0
    print(f"  ✓ Carbon Offsets: {carbon['annual_carbon_credits_generated_tco2e']} tCO2e/yr, Revenue=₹{carbon['annual_carbon_revenue_inr']:,.2f}/yr")

    # 3. PPA Optimizer
    ppa = ppa_grid_optimizer.evaluate_green_open_access_ppa(monthly_consumption_kwh=120000.0)
    assert ppa["annual_cost_savings_inr"] > 0
    print(f"  ✓ Green PPA: Effective Tariff=₹{ppa['blended_effective_tariff_inr_kwh']}/kWh, Annual Savings=₹{ppa['annual_cost_savings_inr']:,.2f}")

    # 4. Agent Stream
    events = list(y2_urja_agent.energy_stream("Evaluate 250kWp rooftop solar and Verra carbon monetization"))
    assert any(e.get("type") == "final" for e in events)
    print("  ✓ Y2 Urja stream generated successfully.")

def test_y3_sanjeevani():
    print("\n--- [3/6] Testing Y3 Sanjeevani (Healthcare & Cold-Chain Pharma) ---")
    from axomai.agents.y3_sanjeevani.tools.epidemiology_engine import epidemiology_engine
    from axomai.agents.y3_sanjeevani.tools.cold_chain_auditor import cold_chain_auditor
    from axomai.agents.y3_sanjeevani.tools.pharma_compliance import pharma_compliance_engine
    from axomai.agents.y3_sanjeevani.agent import y3_sanjeevani_agent

    # 1. Epidemiology SIR
    epi = epidemiology_engine.simulate_outbreak_risk("Dibrugarh", "japanese_encephalitis")
    assert epi["environment_amplified_r0"] > 0
    print(f"  ✓ Epidemiology SIR: Pathogen={epi['target_pathogen']}, Amplified R0={epi['environment_amplified_r0']}, Status={epi['outbreak_expansion_status']}")

    # 2. Cold Chain MKT
    cold = cold_chain_auditor.calculate_mean_kinetic_temperature([4.2, 4.8, 5.1, 5.5, 4.9, 4.3])
    assert cold["arrhenius_mean_kinetic_temp_celsius"] > 0
    assert cold["freezing_breach_detected"] is False
    print(f"  ✓ Cold-Chain MKT: Arrhenius MKT={cold['arrhenius_mean_kinetic_temp_celsius']}°C, Verdict={cold['biological_potency_verdict']}")

    # 3. Pharma Compliance
    gmp = pharma_compliance_engine.audit_manufacturing_facility()
    assert gmp["compliance_readiness_score"] == "100.0%"
    print(f"  ✓ CDSCO GMP Audit: Readiness={gmp['compliance_readiness_score']}, Batch Verdict={gmp['batch_release_authorization']}")

    # 4. Agent Stream
    events = list(y3_sanjeevani_agent.healthcare_stream("Audit JE vaccine cold-chain and CDSCO Schedule M compliance"))
    assert any(e.get("type") == "final" for e in events)
    print("  ✓ Y3 Sanjeevani stream generated successfully.")

def test_y4_vishwakarma():
    print("\n--- [4/6] Testing Y4 Vishwakarma (Mega Infrastructure & EPC Civil) ---")
    from axomai.agents.y4_vishwakarma.tools.primavera_delay_engine import primavera_delay_engine
    from axomai.agents.y4_vishwakarma.tools.fidic_contract_auditor import fidic_contract_auditor
    from axomai.agents.y4_vishwakarma.tools.seismic_embankment_safety import seismic_embankment_engine
    from axomai.agents.y4_vishwakarma.agent import y4_vishwakarma_agent

    # 1. Primavera EVM
    evm = primavera_delay_engine.evaluate_epc_schedule_evm()
    assert evm["schedule_performance_index_spi"] == 0.85
    assert evm["projected_delay_days"] > 0
    print(f"  ✓ Primavera EVM: SPI={evm['schedule_performance_index_spi']}, CPI={evm['cost_performance_index_cpi']}, Delay={evm['projected_completion_duration_months']}")

    # 2. FIDIC Contract Claim
    fidic = fidic_contract_auditor.audit_contractor_claim(notice_served_days_after_event=18)
    assert fidic["dab_adjudication_success_probability"] > 0.70
    print(f"  ✓ FIDIC Claim: Status={fidic['statutory_time_bar_status']}, DAB Probability={int(fidic['dab_adjudication_success_probability']*100)}%, Settlement EoT={fidic['recommended_settlement_eot_days']} Days")

    # 3. Seismic Zone V Stability
    seismic = seismic_embankment_engine.evaluate_embankment_stability()
    assert seismic["seismic_zone_v_factor_of_safety"] >= 1.15
    print(f"  ✓ Seismic Zone V: PGA={seismic['peak_ground_acceleration_pga']}, FoS={seismic['seismic_zone_v_factor_of_safety']} ({seismic['structural_integrity_verdict']})")

    # 4. Agent Stream
    events = list(y4_vishwakarma_agent.infra_stream("Audit bridge EPC Primavera delay, FIDIC Clause 8.4 and Zone-V seismic safety"))
    assert any(e.get("type") == "final" for e in events)
    print("  ✓ Y4 Vishwakarma stream generated successfully.")

def test_y5_chanakya():
    print("\n--- [5/6] Testing Y5 Chanakya (Sovereign Geopolitics & OSINT) ---")
    from axomai.agents.y5_chanakya.tools.sanctions_screening import sanctions_screening_engine
    from axomai.agents.y5_chanakya.tools.chokepoint_radar import chokepoint_radar
    from axomai.agents.y5_chanakya.tools.osint_synthesizer import osint_synthesizer
    from axomai.agents.y5_chanakya.agent import y5_chanakya_agent

    # 1. Sanctions Screening
    clean_party = sanctions_screening_engine.screen_entity("dubai_specialty_tea_llc")
    assert clean_party["ofac_sdn_status"] == "PASSED_CLEAN"
    blocked_party = sanctions_screening_engine.screen_entity("sovcomflot")
    assert blocked_party["ofac_sdn_status"] == "CRITICAL_BLOCKED"
    print(f"  ✓ Sanctions Screening: Clean entity={clean_party['ofac_sdn_status']}, Blocked entity={blocked_party['ofac_sdn_status']}")

    # 2. Chokepoint Radar
    corridor = chokepoint_radar.assess_chokepoint_risk("siliguri_corridor")
    assert corridor["geopolitical_risk_score"] > 50
    print(f"  ✓ Chokepoint Radar: {corridor['corridor_name']} (Risk: {corridor['geopolitical_risk_score']}/100, Contingency: {corridor['redundant_contingency_path'][:35]}...)")

    # 3. OSINT Synthesis
    osint = osint_synthesizer.synthesize_geopolitical_dossier()
    assert len(osint["verified_intelligence_streams"]) == 3
    print(f"  ✓ OSINT Synthesis: Streams={len(osint['verified_intelligence_streams'])}, Index={osint['composite_geopolitical_risk_index']}")

    # 4. Agent Stream
    events = list(y5_chanakya_agent.geopolitics_stream("Screen trade partner against OFAC SDN and assess Siliguri corridor"))
    assert any(e.get("type") == "final" for e in events)
    print("  ✓ Y5 Chanakya stream generated successfully.")

def test_master_routing_and_planner():
    print("\n--- [6/6] Testing Master Orchestrator Routing & Planner ---")
    from axomai.agents.master_orchestrator import master_orchestrator
    from axomai.agents.mission_control.planner import AGENT_NAME_MAP

    test_queries = [
        ("Prescribe tea soil NPK fertilizer and MCX commodity futures hedge", "y1"),
        ("Calculate 250kW rooftop solar LCOE and Verra VCS carbon offset credits", "y2"),
        ("Model encephalitis epidemic outbreak SIR and audit vaccine cold-chain MKT", "y3"),
        ("Analyze bridge EPC Primavera schedule delay and FIDIC Clause 8.4 EoT", "y4"),
        ("Screen trade counterparty against OFAC SDN list and check Siliguri corridor", "y5")
    ]

    for q, expected in test_queries:
        res = master_orchestrator.classify_and_route(q)
        assert res["agent"] == expected, f"Expected {expected} for '{q}', got {res['agent']}"
        print(f"  ✓ Routed correctly: '{q[:45]}...' -> [{res['agent'].upper()}] ({res['name']})")

    # Verify AGENT_NAME_MAP has all Y-series entries
    for y_key in ["y1", "y2", "y3", "y4", "y5"]:
        assert y_key in AGENT_NAME_MAP, f"Key {y_key} missing from AGENT_NAME_MAP"
        print(f"  ✓ Planner Map Verified: [{y_key.upper()}] -> {AGENT_NAME_MAP[y_key]}")

if __name__ == "__main__":
    test_y1_annapurna()
    test_y2_urja()
    test_y3_sanjeevani()
    test_y4_vishwakarma()
    test_y5_chanakya()
    test_master_routing_and_planner()
    print("\n=======================================================")
    print("🎉 ALL 5 Y-SERIES AGENTS PASSED WITH 100% OPERATIONAL SUCCESS!")
    print("=======================================================")

