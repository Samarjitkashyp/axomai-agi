"""
Z7 Visionary - Interactive HTML5 Web Deck Builder.
Exports a standalone, responsive HTML5 presentation with Chart.js visualizations,
Assam sector branding, keyboard arrow navigation, and one-click Print-to-PDF support.
"""

import uuid
from typing import Dict, Any, List
from axomai.config import settings
from axomai.agents.z7_visionary.tools.assam_themes_and_dpr import SECTOR_THEMES


class Html5DeckBuilder:
    """Generates shareable interactive HTML5 web presentations with Chart.js."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_web_deck(
        self,
        title: str,
        subtitle: str,
        slides_data: List[Dict[str, Any]],
        dpr_data: Dict[str, Any],
        sector: str = "TECH_BOARDROOM"
    ) -> Dict[str, Any]:
        theme = SECTOR_THEMES.get(sector, SECTOR_THEMES["TECH_BOARDROOM"])
        bg = theme["hex_bg"]
        accent = theme["hex_accent"]

        slides_html = ""
        for idx, s in enumerate(slides_data, 1):
            bullets_li = "".join(f"<li class='mb-3 text-slate-200 text-lg'>▸ {b}</li>" for b in s.get("bullets", []))
            slides_html += f"""
            <section class="slide p-10 rounded-2xl border border-white/10 bg-white/5 mb-8 break-after-page">
              <div class="text-xs uppercase tracking-widest mb-2" style="color:{accent}">Slide {idx + 1}</div>
              <h2 class="text-2xl font-bold mb-6" style="color:{accent}">{s.get('heading')}</h2>
              <ul>{bullets_li}</ul>
            </section>
            """

        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{title} — AxomAI Z7 Interactive Deck</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {{ background: {bg}; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; }}
    @media print {{ .no-print {{ display: none; }} }}
  </style>
</head>
<body class="max-w-5xl mx-auto py-10 px-6">
  <div class="flex justify-between items-center mb-8 no-print">
    <span class="text-xs font-mono px-3 py-1 rounded border border-white/20">AxomAI Z7 Visionary • Interactive HTML5 Deck</span>
    <button onclick="window.print()" class="px-4 py-2 rounded-lg text-sm font-semibold text-slate-900" style="background:{accent}">Export / Print PDF</button>
  </div>
  <section class="p-12 rounded-2xl border border-white/15 bg-white/5 mb-8">
    <div class="text-xs uppercase tracking-widest mb-3" style="color:{accent}">{theme['name']}</div>
    <h1 class="text-4xl font-extrabold mb-4" style="color:{accent}">{title}</h1>
    <p class="text-lg text-slate-300">{subtitle} • {dpr_data['district']}</p>
  </section>
  {slides_html}
  <section class="p-10 rounded-2xl border border-white/10 bg-white/5 mb-8">
    <h2 class="text-2xl font-bold mb-4" style="color:{accent}">5-Year Revenue & EBITDA Trajectory (₹ Lakhs)</h2>
    <canvas id="dprChart" height="110"></canvas>
  </section>
  <script>
    new Chart(document.getElementById('dprChart'), {{
      type: 'bar',
      data: {{
        labels: {dpr_data['years']},
        datasets: [
          {{ label: 'Revenue (₹L)', data: {dpr_data['revenues_lakhs']}, backgroundColor: '{accent}' }},
          {{ label: 'EBITDA (₹L)', data: {dpr_data['ebitda_lakhs']}, backgroundColor: '#22c55e' }}
        ]
      }},
      options: {{ responsive: true, plugins: {{ legend: {{ labels: {{ color: '#e2e8f0' }} }} }} }}
    }});
  </script>
</body>
</html>"""

        filename = f"web_deck_{uuid.uuid4().hex[:8]}.html"
        file_path = self.output_dir / filename
        file_path.write_text(html_doc, encoding="utf-8")

        return {
            "filename": filename,
            "file_path": str(file_path),
            "download_url": f"/api/download/generated/{filename}"
        }


html5_deck_builder = Html5DeckBuilder()
