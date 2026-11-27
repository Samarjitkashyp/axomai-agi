"""
Z7 Visionary - Full Bankable DPR Word Document (.docx) Builder (SBI / AGVB / NEDFi Format).
Generates a comprehensive, print-ready Microsoft Word Project Report (.docx) featuring
White-Label Brand & UDYAM Seal, Multi-Script Assam/Bodo/Bengali Headers,
Assam District Benchmarks (APDCL tariff, wages, UNNATI Zone), Means of Finance table,
5-Year DSCR/PAT projections, BEP & IRR metrics, SWOT table, Scheme Document Checklist,
and embedded high-DPI BEP Chart + Assam Catchment Map PNGs.
"""

import uuid
from typing import Dict, Any, Optional
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from axomai.config import settings


class DocxDprBuilder:
    """Builds SBI / NEDFi / AGVB-ready Bankable Detailed Project Reports (.docx)."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_bankable_dpr_docx(
        self,
        title: str,
        dpr_data: Dict[str, Any],
        benchmarks: Dict[str, Any],
        bep_chart_path: Optional[str] = None,
        map_img_path: Optional[str] = None,
        white_label_brand: str = "AxomAI Sovereign Advisory",
        udyam_seal: Optional[str] = None
    ) -> Dict[str, Any]:
        doc = Document()

        # Header / White-Label Footer Seal
        section = doc.sections[0]
        footer = section.footer
        fp = footer.paragraphs[0]
        seal_txt = f" | UDYAM Seal: {udyam_seal}" if udyam_seal else ""
        fp.text = f"Prepared by: {white_label_brand}{seal_txt} | Bankable DPR (SBI / AGVB / NEDFi Standard)"

        # COVER TITLE
        h1 = doc.add_heading(title, level=0)
        h1.alignment = WD_ALIGN_PARAGRAPH.CENTER

        sub = doc.add_paragraph(
            f"{benchmarks['script_labels']['dpr_title']}\n"
            f"Location: {benchmarks['district_clean']}, Assam ({benchmarks['unnati_zone']})\n"
            f"Applicable Scheme: {dpr_data['scheme']}\n"
            f"Prepared By: {white_label_brand}{seal_txt}"
        )
        sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # CHAPTER 1: EXECUTIVE SUMMARY & MEANS OF FINANCE
        doc.add_heading("1. Executive Summary & Means of Finance", level=1)
        doc.add_paragraph(
            f"This Detailed Project Report (DPR) evaluates the commercial and technical viability of '{title}' "
            f"located in {benchmarks['district_clean']}, Assam along the {benchmarks['highway_corridor']} corridor. "
            f"Total capital outlay is ₹{dpr_data['total_capex_lakhs']} Lakhs with an average Debt Service Coverage Ratio (DSCR) "
            f"of {dpr_data['avg_dscr']}x ({dpr_data['bankability_verdict']}), Break-Even Point at {benchmarks['bep_capacity_pct']}% capacity, "
            f"estimated IRR of {benchmarks['estimated_irr_pct']}%, and Payback Period of {benchmarks['payback_period_years']} years."
        )

        tbl1 = doc.add_table(rows=5, cols=3)
        tbl1.style = "Table Grid"
        hdr1 = ["Funding Component", "Basis / Terms", "Amount (₹ Lakhs)"]
        for c, txt in enumerate(hdr1):
            tbl1.rows[0].cells[c].text = txt
        rows1 = [
            ("Promoter Margin Contribution", "15% Equity Share", f"₹{dpr_data['promoter_equity_lakhs']}"),
            ("Government Capital Subsidy", dpr_data["scheme"], f"₹{dpr_data['govt_subsidy_lakhs']}"),
            ("Bank Term Loan", "9.5% p.a. (5-Yr Tenure)", f"₹{dpr_data['bank_term_loan_lakhs']}"),
            ("TOTAL PROJECT OUTLAY", "100% Bankable Cost", f"₹{dpr_data['total_capex_lakhs']}")
        ]
        for r_i, r_vals in enumerate(rows1, 1):
            for c_i, val in enumerate(r_vals):
                tbl1.rows[r_i].cells[c_i].text = val

        # CHAPTER 2: ASSAM OPERATIONAL & STATUTORY BENCHMARKS
        doc.add_heading("2. Assam Location, Power Tariff & Labor Cost Benchmarks", level=1)
        doc.add_paragraph(
            f"• Industrial Zone Classification: {benchmarks['unnati_zone']}\n"
            f"• APDCL Commercial/Industrial Power Tariff: ₹{benchmarks['apdcl_industrial_tariff_inr_kwh']} / kWh "
            f"(Est. Monthly Bill: ₹{benchmarks['est_monthly_power_bill_inr']:,.2f})\n"
            f"• AIDC / Industrial Estate Benchmark Lease: ₹{benchmarks['aidc_lease_rate_inr_sqft']} / sq.ft/month\n"
            f"• Assam Minimum Wage Norms: Skilled ₹{benchmarks['assam_skilled_wage_inr_month']:,.0f}/mo | "
            f"Unskilled ₹{benchmarks['assam_unskilled_wage_inr_month']:,.0f}/mo\n"
            f"• Break-Even Revenue Threshold: ₹{benchmarks['bep_revenue_lakhs']} Lakhs/yr ({benchmarks['bep_capacity_pct']}% Utilization)"
        )

        # CHAPTER 3: 5-YEAR FINANCIAL PROJECTIONS
        doc.add_heading("3. Five-Year Financial Projections & DSCR Schedule", level=1)
        tbl2 = doc.add_table(rows=6, cols=5)
        tbl2.style = "Table Grid"
        hdr2 = ["Year", "Revenue (₹L)", "EBITDA (₹L)", "Net Profit PAT (₹L)", "DSCR (x)"]
        for c, txt in enumerate(hdr2):
            tbl2.rows[0].cells[c].text = txt
        for i in range(5):
            r = i + 1
            tbl2.rows[r].cells[0].text = dpr_data["years"][i]
            tbl2.rows[r].cells[1].text = f"₹{dpr_data['revenues_lakhs'][i]}"
            tbl2.rows[r].cells[2].text = f"₹{dpr_data['ebitda_lakhs'][i]}"
            tbl2.rows[r].cells[3].text = f"₹{dpr_data['pat_lakhs'][i]}"
            tbl2.rows[r].cells[4].text = f"{dpr_data['dscr_series'][i]}x"

        # CHAPTER 4: EMBEDDED CHARTS & CATCHMENT MAP
        doc.add_heading("4. Break-Even Crossover & Assam Catchment Corridor Visuals", level=1)
        if bep_chart_path:
            doc.add_picture(bep_chart_path, width=Inches(6.0))
        if map_img_path:
            doc.add_picture(map_img_path, width=Inches(6.0))

        # CHAPTER 5: SWOT & MANDATORY SCHEME DOCUMENT CHECKLIST
        doc.add_heading("5. SWOT Analysis & Bank / Subsidy Document Checklist", level=1)
        doc.add_paragraph(
            "Strengths: High regional demand + govt capital subsidy cushion.\n"
            "Weaknesses: Initial working capital cycle during monsoon quarters.\n"
            "Opportunities: Act East cross-border export expansion & UNNATI 2024 benefits.\n"
            "Threats: Flood/transport bottlenecks mitigated via 21-day inventory buffers."
        )
        doc.add_heading("Mandatory Filing Checklist:", level=2)
        for item in benchmarks["scheme_checklist"]:
            doc.add_paragraph(item, style="List Bullet")

        filename = f"bankable_dpr_{uuid.uuid4().hex[:8]}.docx"
        file_path = self.output_dir / filename
        doc.save(str(file_path))

        return {
            "filename": filename,
            "file_path": str(file_path),
            "download_url": f"/api/download/generated/{filename}",
            "white_label_brand": white_label_brand
        }


docx_dpr_builder = DocxDprBuilder()
