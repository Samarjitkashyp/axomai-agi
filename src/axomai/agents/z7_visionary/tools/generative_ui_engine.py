"""
Z7 Visionary - Dynamic Multi-App Generative UI & Micro-App Engine.
Generates self-contained interactive HTML/JS widgets tailored to the user's request:
1. ASSAM_LAND_CONVERTER (Exact Assam standard: 1 Bigha = 5 Katha = 100 Lessa = 14,400 sq.ft)
2. LOAN_SUBSIDY_EMI (CMAAA / UNNATI / PMEGP Subsidy + Bank EMI Calculator)
3. TEA_YIELD_SIMULATOR (Assam Tea Estate Green Leaf -> Made Tea -> Revenue Simulator)
4. KPI_DASHBOARD (Interactive Executive Metric Cards)
5. ROI_SIMULATOR (Enterprise Automation ROI Calculator)
"""

import uuid
from typing import Dict, Any, Optional
from axomai.config import settings
from axomai.core.llm import llm_brain


class GenerativeUIEngine:
    """Produces dynamic, executable HTML/JS micro-app components & arbitrary prompt-to-code apps."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_widget(self, widget_type: str = "ROI_SIMULATOR", project_name: str = "AxomAI Interactive App", raw_query: str = "") -> Dict[str, Any]:
        if widget_type == "ASSAM_LAND_CONVERTER":
            res = self._assam_land_converter(project_name)
        elif widget_type == "LOAN_SUBSIDY_EMI":
            res = self._loan_subsidy_emi_calculator(project_name)
        elif widget_type == "TEA_YIELD_SIMULATOR":
            res = self._tea_yield_simulator(project_name)
        elif widget_type == "KPI_DASHBOARD":
            res = self._kpi_dashboard(project_name)
        elif widget_type == "CUSTOM_DYNAMIC_APP" and raw_query:
            res = self._compile_arbitrary_micro_app(raw_query, project_name)
        else:
            res = self.generate_roi_calculator(project_name)

        # Save standalone downloadable HTML widget
        fname = f"micro_app_{uuid.uuid4().hex[:8]}.html"
        fpath = self.output_dir / fname
        standalone_html = (
            f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>{project_name}</title>"
            f"<script src='https://cdn.tailwindcss.com'></script></head>"
            f"<body class='bg-slate-950 min-h-screen flex items-center justify-center p-6'>{res['html']}</body></html>"
        )
        fpath.write_text(standalone_html, encoding="utf-8")
        res["download_url"] = f"/api/download/generated/{fname}"
        res["filename"] = fname
        return res

    def _compile_arbitrary_micro_app(self, raw_query: str, project_name: str) -> Dict[str, Any]:
        """Uses LLM to compile an arbitrary custom interactive HTML/Tailwind/JS micro-app."""
        if llm_brain.is_available:
            prompt = (
                f"Build a self-contained interactive HTML + TailwindCSS + inline <script> micro-app widget for:\n"
                f"Request: '{raw_query}'\n"
                "Requirements:\n"
                "- Wrap inside a single <div class='p-4 rounded-xl bg-gray-900 border border-cyan-700 text-white max-w-xl'>.\n"
                "- Include interactive <input> sliders or number fields with real-time JS calculation.\n"
                "- Output ONLY raw HTML+JS code (no markdown fences, no explanation)."
            )
            try:
                raw_html = llm_brain.generate("You are an expert Frontend Micro-App Compiler. Output raw HTML only.", prompt, temperature=0.2).strip()
                if "```html" in raw_html:
                    raw_html = raw_html.split("```html")[1].split("```")[0].strip()
                elif "```" in raw_html:
                    raw_html = raw_html.split("```")[1].split("```")[0].strip()
                if "<div" in raw_html and "<script" in raw_html:
                    return {"widget_type": "CUSTOM_DYNAMIC_APP", "html": raw_html, "project_name": project_name}
            except Exception:
                pass
        return self.generate_roi_calculator(project_name)

    def _assam_land_converter(self, project_name: str) -> Dict[str, Any]:
        html = """
<div class="p-4 rounded-xl bg-gray-900 border border-emerald-700/80 shadow-2xl text-white font-sans max-w-xl">
  <div class="flex items-center justify-between pb-3 mb-3 border-b border-gray-800">
    <h4 class="text-xs font-bold text-emerald-300 font-mono">🏞️ Assam Land Unit Converter (Bigha • Katha • Lessa • Sq.ft)</h4>
    <span class="text-[10px] bg-emerald-950 text-emerald-300 border border-emerald-700 px-2 py-0.5 rounded font-mono">ASSAM REVENUE STD</span>
  </div>
  <div class="grid grid-cols-3 gap-2 text-xs mb-3">
    <div>
      <label class="text-gray-400 block mb-1">Bigha (বিঘা)</label>
      <input type="number" id="in-bigha" value="1" min="0" step="0.5" class="w-full bg-black/60 border border-gray-700 rounded px-2 py-1 text-emerald-300 font-mono" oninput="calcAssamLand()">
    </div>
    <div>
      <label class="text-gray-400 block mb-1">Katha (কঠা)</label>
      <input type="number" id="in-katha" value="0" min="0" step="1" class="w-full bg-black/60 border border-gray-700 rounded px-2 py-1 text-emerald-300 font-mono" oninput="calcAssamLand()">
    </div>
    <div>
      <label class="text-gray-400 block mb-1">Lessa (লেছা)</label>
      <input type="number" id="in-lessa" value="0" min="0" step="1" class="w-full bg-black/60 border border-gray-700 rounded px-2 py-1 text-emerald-300 font-mono" oninput="calcAssamLand()">
    </div>
  </div>
  <div class="p-3 rounded-lg bg-black/60 border border-gray-800 grid grid-cols-3 gap-2 text-xs">
    <div><span class="text-[10px] text-gray-400 block">Total Sq. Ft</span><span id="out-sqft" class="text-sm font-bold text-emerald-400 font-mono">14,400</span></div>
    <div><span class="text-[10px] text-gray-400 block">Total Acres</span><span id="out-acre" class="text-sm font-bold text-cyan-300 font-mono">0.3306</span></div>
    <div><span class="text-[10px] text-gray-400 block">Sq. Meters</span><span id="out-sqm" class="text-sm font-bold text-amber-300 font-mono">1,337.8</span></div>
  </div>
  <script>
    function calcAssamLand() {
      const b = parseFloat(document.getElementById('in-bigha').value) || 0;
      const k = parseFloat(document.getElementById('in-katha').value) || 0;
      const l = parseFloat(document.getElementById('in-lessa').value) || 0;
      const sqft = (b * 14400) + (k * 2880) + (l * 144);
      document.getElementById('out-sqft').innerText = Math.round(sqft).toLocaleString();
      document.getElementById('out-acre').innerText = (sqft / 43560).toFixed(4);
      document.getElementById('out-sqm').innerText = (sqft * 0.092903).toFixed(1);
    }
  </script>
</div>"""
        return {"widget_type": "ASSAM_LAND_CONVERTER", "html": html.strip(), "project_name": project_name}

    def _loan_subsidy_emi_calculator(self, project_name: str) -> Dict[str, Any]:
        html = """
<div class="p-4 rounded-xl bg-gray-900 border border-sky-700/80 shadow-2xl text-white font-sans max-w-xl">
  <div class="flex items-center justify-between pb-3 mb-3 border-b border-gray-800">
    <h4 class="text-xs font-bold text-sky-300 font-mono">🏦 Assam Govt Subsidy & Bank Term Loan EMI Simulator</h4>
    <span class="text-[10px] bg-sky-950 text-sky-300 border border-sky-700 px-2 py-0.5 rounded font-mono">CMAAA / UNNATI</span>
  </div>
  <div class="space-y-3 text-xs">
    <div>
      <div class="flex justify-between mb-1"><span>Project Capex (₹ Lakhs):</span><span id="capex-lbl" class="text-sky-300 font-mono font-bold">₹50 L</span></div>
      <input type="range" min="10" max="500" value="50" id="capex-sl" class="w-full accent-sky-400" oninput="document.getElementById('capex-lbl').innerText='₹'+this.value+' L'; calcEmi()">
    </div>
    <div>
      <div class="flex justify-between mb-1"><span>Govt Subsidy (%):</span><span id="sub-lbl" class="text-emerald-300 font-mono font-bold">35%</span></div>
      <input type="range" min="0" max="50" value="35" id="sub-sl" class="w-full accent-emerald-400" oninput="document.getElementById('sub-lbl').innerText=this.value+'%'; calcEmi()">
    </div>
    <div class="p-3 rounded-lg bg-black/60 border border-gray-800 grid grid-cols-3 gap-2">
      <div><span class="text-[10px] text-gray-400 block">Govt Subsidy</span><span id="out-sub" class="text-sm font-bold text-emerald-400 font-mono">₹17.5 L</span></div>
      <div><span class="text-[10px] text-gray-400 block">Net Bank Loan</span><span id="out-loan" class="text-sm font-bold text-sky-300 font-mono">₹25.0 L</span></div>
      <div><span class="text-[10px] text-gray-400 block">Est. Monthly EMI</span><span id="out-emi" class="text-sm font-bold text-amber-300 font-mono">₹52,505</span></div>
    </div>
  </div>
  <script>
    function calcEmi() {
      const cap = parseFloat(document.getElementById('capex-sl').value);
      const subPct = parseFloat(document.getElementById('sub-sl').value);
      const subAmt = cap * (subPct / 100);
      const margin = cap * 0.15;
      const loanL = Math.max(0, cap - subAmt - margin);
      const P = loanL * 100000;
      const r = 0.095 / 12, n = 60;
      const emi = P > 0 ? Math.round((P * r * Math.pow(1+r, n)) / (Math.pow(1+r, n) - 1)) : 0;
      document.getElementById('out-sub').innerText = '₹' + subAmt.toFixed(1) + ' L';
      document.getElementById('out-loan').innerText = '₹' + loanL.toFixed(1) + ' L';
      document.getElementById('out-emi').innerText = '₹' + emi.toLocaleString();
    }
  </script>
</div>"""
        return {"widget_type": "LOAN_SUBSIDY_EMI", "html": html.strip(), "project_name": project_name}

    def _tea_yield_simulator(self, project_name: str) -> Dict[str, Any]:
        html = """
<div class="p-4 rounded-xl bg-gray-900 border border-amber-700/80 shadow-2xl text-white font-sans max-w-xl">
  <div class="flex items-center justify-between pb-3 mb-3 border-b border-gray-800">
    <h4 class="text-xs font-bold text-amber-300 font-mono">🍃 Assam Tea Estate Yield & GTAC Auction Simulator</h4>
    <span class="text-[10px] bg-amber-950 text-amber-300 border border-amber-700 px-2 py-0.5 rounded font-mono">ASSAM TEA</span>
  </div>
  <div class="space-y-3 text-xs">
    <div>
      <div class="flex justify-between mb-1"><span>Estate Area (Hectares):</span><span id="ha-lbl" class="text-amber-300 font-mono font-bold">50 Ha</span></div>
      <input type="range" min="5" max="300" value="50" id="ha-sl" class="w-full accent-amber-400" oninput="document.getElementById('ha-lbl').innerText=this.value+' Ha'; calcTea()">
    </div>
    <div>
      <div class="flex justify-between mb-1"><span>Auction Price (₹ / kg Made Tea):</span><span id="px-lbl" class="text-emerald-300 font-mono font-bold">₹265</span></div>
      <input type="range" min="140" max="600" value="265" id="px-sl" class="w-full accent-emerald-400" oninput="document.getElementById('px-lbl').innerText='₹'+this.value; calcTea()">
    </div>
    <div class="p-3 rounded-lg bg-black/60 border border-gray-800 grid grid-cols-2 gap-2">
      <div><span class="text-[10px] text-gray-400 block">Annual Made Tea Output</span><span id="out-tea" class="text-base font-bold text-emerald-400 font-mono">105,000 kg</span></div>
      <div><span class="text-[10px] text-gray-400 block">Annual Gross Revenue</span><span id="out-rev" class="text-base font-bold text-amber-300 font-mono">₹2.78 Cr</span></div>
    </div>
  </div>
  <script>
    function calcTea() {
      const ha = parseFloat(document.getElementById('ha-sl').value);
      const px = parseFloat(document.getElementById('px-sl').value);
      const kg = Math.round(ha * 2100);
      const revCr = (kg * px) / 10000000;
      document.getElementById('out-tea').innerText = kg.toLocaleString() + ' kg';
      document.getElementById('out-rev').innerText = '₹' + revCr.toFixed(2) + ' Cr';
    }
  </script>
</div>"""
        return {"widget_type": "TEA_YIELD_SIMULATOR", "html": html.strip(), "project_name": project_name}

    def _kpi_dashboard(self, project_name: str) -> Dict[str, Any]:
        html = f"""
<div class="p-4 rounded-xl bg-gray-900 border border-indigo-700/80 shadow-2xl text-white font-sans max-w-xl">
  <div class="flex items-center justify-between pb-3 mb-3 border-b border-gray-800">
    <h4 class="text-xs font-bold text-indigo-300 font-mono">📊 Executive KPI Command Panel — {project_name[:32]}</h4>
    <span class="text-[10px] bg-indigo-950 text-indigo-300 border border-indigo-700 px-2 py-0.5 rounded font-mono">LIVE KPI</span>
  </div>
  <div class="grid grid-cols-2 gap-3 text-xs">
    <div class="p-3 rounded-lg bg-black/50 border border-gray-800"><span class="text-gray-400 block">Projected 5Y CAGR</span><span class="text-lg font-bold text-emerald-400 font-mono">24.6%</span></div>
    <div class="p-3 rounded-lg bg-black/50 border border-gray-800"><span class="text-gray-400 block">Target EBITDA Margin</span><span class="text-lg font-bold text-cyan-300 font-mono">26.5%</span></div>
    <div class="p-3 rounded-lg bg-black/50 border border-gray-800"><span class="text-gray-400 block">Payback Period</span><span class="text-lg font-bold text-amber-300 font-mono">2.8 Years</span></div>
    <div class="p-3 rounded-lg bg-black/50 border border-gray-800"><span class="text-gray-400 block">Bankability Rating</span><span class="text-lg font-bold text-indigo-300 font-mono">A+ (DSCR 1.8x)</span></div>
  </div>
</div>"""
        return {"widget_type": "KPI_DASHBOARD", "html": html.strip(), "project_name": project_name}

    def generate_roi_calculator(self, project_name: str = "Enterprise AI Integration") -> Dict[str, Any]:
        widget_html = """
<div class="p-4 rounded-xl bg-gray-900 border border-cyan-800/80 shadow-2xl text-white font-sans max-w-xl">
  <div class="flex items-center justify-between pb-3 mb-3 border-b border-gray-800">
    <h4 class="text-xs font-bold text-cyan-300 font-mono">⚡ Interactive ROI & Cost Savings Simulator</h4>
    <span class="text-[10px] bg-cyan-950 text-cyan-300 border border-cyan-800 px-2 py-0.5 rounded font-mono">LIVE WIDGET</span>
  </div>
  <div class="space-y-3 text-xs">
    <div>
      <div class="flex justify-between text-gray-300 mb-1">
        <span>Monthly Team Hours Saved:</span>
        <span id="hours-val" class="font-mono text-cyan-300 font-bold">120 hrs</span>
      </div>
      <input type="range" min="20" max="500" value="120" id="hours-slider" class="w-full accent-cyan-400" oninput="document.getElementById('hours-val').innerText = this.value + ' hrs'; recalcRoi()">
    </div>
    <div>
      <div class="flex justify-between text-gray-300 mb-1">
        <span>Average Hourly Cost (₹ / hr):</span>
        <span id="rate-val" class="font-mono text-cyan-300 font-bold">₹1,200</span>
      </div>
      <input type="range" min="300" max="5000" value="1200" step="100" id="rate-slider" class="w-full accent-cyan-400" oninput="document.getElementById('rate-val').innerText = '₹' + this.value; recalcRoi()">
    </div>
    <div class="p-3 rounded-lg bg-black/60 border border-gray-800 grid grid-cols-2 gap-2 mt-2">
      <div><span class="text-[10px] text-gray-400 block font-mono">Monthly Savings</span><span id="savings-monthly" class="text-base font-bold text-emerald-400 font-mono">₹1,08,000</span></div>
      <div><span class="text-[10px] text-gray-400 block font-mono">Annualized Value</span><span id="savings-annual" class="text-base font-bold text-cyan-300 font-mono">₹12,96,000</span></div>
    </div>
  </div>
  <script>
    function recalcRoi() {
      const h = parseInt(document.getElementById('hours-slider').value);
      const r = parseInt(document.getElementById('rate-slider').value);
      const monthly = Math.round(h * r * 0.75);
      document.getElementById('savings-monthly').innerText = '₹' + monthly.toLocaleString('en-IN');
      document.getElementById('savings-annual').innerText = '₹' + (monthly * 12).toLocaleString('en-IN');
    }
  </script>
</div>"""
        return {"widget_type": "INTERACTIVE_ROI_SIMULATOR", "html": widget_html.strip(), "project_name": project_name}


generative_ui_engine = GenerativeUIEngine()
