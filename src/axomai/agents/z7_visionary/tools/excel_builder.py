"""
Z7 Visionary - Dynamic Excel Financial & Bankable DPR Workbook Builder.
Generates styled, multi-tab Microsoft Excel (.xlsx) workbooks with live Excel formulas
(SUM, DSCR, Margin %) and embedded native openpyxl BarCharts.
"""

import uuid
from typing import Dict, Any, Optional
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference

from axomai.config import settings


class ExcelModelBuilder:
    """Builds dynamic formula-driven .xlsx financial models and Bankable DPR spreadsheets."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_bankable_dpr_excel(
        self,
        project_name: str,
        dpr_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Creates a dynamic 3-tab Bankable DPR & Financial Model (.xlsx) with embedded BarChart."""
        wb = openpyxl.Workbook()

        navy_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
        accent_fill = PatternFill(start_color="0284C7", end_color="0284C7", fill_type="solid")
        zebra_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
        white_bold = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        dark_bold = Font(name="Calibri", size=11, bold=True, color="0F172A")
        thin_border = Border(
            left=Side(style="thin", color="CBD5E1"),
            right=Side(style="thin", color="CBD5E1"),
            top=Side(style="thin", color="CBD5E1"),
            bottom=Side(style="thin", color="CBD5E1")
        )

        # TAB 1: Means of Finance & Capex Breakdown
        ws1 = wb.active
        ws1.title = "Means of Finance"
        ws1.merge_cells("A1:D1")
        ws1["A1"] = f"{project_name} — Bankable DPR Means of Finance ({dpr_data['district']})"
        ws1["A1"].font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
        ws1["A1"].fill = navy_fill
        ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws1.row_dimensions[1].height = 32

        headers1 = ["Funding Source / Component", "Scheme / Terms", "Amount (₹ Lakhs)", "Share (%)"]
        for col, h in enumerate(headers1, 1):
            c = ws1.cell(row=3, column=col, value=h)
            c.font = white_bold
            c.fill = accent_fill
            c.border = thin_border

        rows1 = [
            ("Promoter Equity Margin", "15% Mandatory Promoter Contribution", dpr_data["promoter_equity_lakhs"]),
            ("Government Capital Subsidy", dpr_data["scheme"], dpr_data["govt_subsidy_lakhs"]),
            ("Bank Term Loan", "9.5% p.a. 5-Year Repayment", dpr_data["bank_term_loan_lakhs"]),
        ]
        for idx, (src, desc, amt) in enumerate(rows1, 4):
            ws1.cell(row=idx, column=1, value=src).border = thin_border
            ws1.cell(row=idx, column=2, value=desc).border = thin_border
            c_amt = ws1.cell(row=idx, column=3, value=amt)
            c_amt.number_format = "#,##0.00"
            c_amt.border = thin_border
            c_pct = ws1.cell(row=idx, column=4, value=f"=C{idx}/$C$7")
            c_pct.number_format = "0.0%"
            c_pct.border = thin_border

        ws1.cell(row=7, column=1, value="TOTAL PROJECT COST").font = dark_bold
        ws1.cell(row=7, column=2, value="Verified Bankable Outlay").font = dark_bold
        c_tot = ws1.cell(row=7, column=3, value="=SUM(C4:C6)")
        c_tot.font = dark_bold
        c_tot.number_format = "#,##0.00"
        c_tot_pct = ws1.cell(row=7, column=4, value="=SUM(D4:D6)")
        c_tot_pct.font = dark_bold
        c_tot_pct.number_format = "0.0%"

        for col, w in enumerate([30, 38, 20, 14], 1):
            ws1.column_dimensions[openpyxl.utils.get_column_letter(col)].width = w

        # TAB 2: 5-Year P&L, DSCR & Embedded Chart
        ws2 = wb.create_sheet("5-Year Projections & Chart")
        ws2.merge_cells("A1:F1")
        ws2["A1"] = f"{project_name} — 5-Year Financial Projections & DSCR (₹ Lakhs)"
        ws2["A1"].font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
        ws2["A1"].fill = navy_fill
        ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws2.row_dimensions[1].height = 32

        headers2 = ["Year", "Revenue (₹L)", "EBITDA (₹L)", "Net Profit PAT (₹L)", "Debt Service (₹L)", "DSCR (x)"]
        for col, h in enumerate(headers2, 1):
            c = ws2.cell(row=3, column=col, value=h)
            c.font = white_bold
            c.fill = accent_fill
            c.border = thin_border

        for i in range(5):
            r = 4 + i
            ws2.cell(row=r, column=1, value=dpr_data["years"][i]).border = thin_border
            c_rev = ws2.cell(row=r, column=2, value=dpr_data["revenues_lakhs"][i])
            c_eb = ws2.cell(row=r, column=3, value=dpr_data["ebitda_lakhs"][i])
            c_pat = ws2.cell(row=r, column=4, value=dpr_data["pat_lakhs"][i])
            c_ds = ws2.cell(row=r, column=5, value=dpr_data["annual_debt_service_lakhs"])
            c_dscr = ws2.cell(row=r, column=6, value=f"=C{r}/E{r}")
            for cell in (c_rev, c_eb, c_pat, c_ds):
                cell.number_format = "#,##0.00"
                cell.border = thin_border
                if i % 2 == 1:
                    cell.fill = zebra_fill
            c_dscr.number_format = "0.00"
            c_dscr.border = thin_border

        # Add Native Excel BarChart
        chart = BarChart()
        chart.type = "col"
        chart.title = "5-Year Revenue vs EBITDA (₹ Lakhs)"
        chart.y_axis.title = "INR Lakhs"
        chart.x_axis.title = "Projection Year"
        data_ref = Reference(ws2, min_col=2, min_row=3, max_col=3, max_row=8)
        cats_ref = Reference(ws2, min_col=1, min_row=4, max_row=8)
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
        chart.width = 16
        chart.height = 9
        ws2.add_chart(chart, "A10")

        for col, w in enumerate([14, 18, 18, 22, 20, 14], 1):
            ws2.column_dimensions[openpyxl.utils.get_column_letter(col)].width = w

        filename = f"dpr_model_{uuid.uuid4().hex[:8]}.xlsx"
        file_path = self.output_dir / filename
        wb.save(str(file_path))

        return {
            "filename": filename,
            "file_path": str(file_path),
            "download_url": f"/api/download/generated/{filename}",
            "tabs": ["Means of Finance", "5-Year Projections & Chart"]
        }

    def generate_retail_expansion_model(self, project_name: str = "Commercial Retail Expansion") -> Dict[str, Any]:
        """Backward-compatible wrapper using dynamic DPR generator."""
        from axomai.agents.z7_visionary.tools.assam_themes_and_dpr import compute_bankable_dpr_financials
        dpr = compute_bankable_dpr_financials(capex_lakhs=75.0, scheme=None, district="Guwahati")
        return self.generate_bankable_dpr_excel(project_name, dpr)


excel_model_builder = ExcelModelBuilder()
