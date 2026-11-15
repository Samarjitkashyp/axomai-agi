"""
Z7 Visionary - Autonomous Excel Financial Model Builder Tool.
Generates styled, multi-tab Microsoft Excel (.xlsx) financial workbooks
with formatted tables, formulas, and Capex/P&L breakdowns.
"""

import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from axomai.config import settings

class ExcelModelBuilder:
    """Builds styled multi-tab financial models in Microsoft Excel (.xlsx)."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_retail_expansion_model(self, project_name: str = "Assam Retail Expansion") -> Dict[str, Any]:
        """Creates an executive-grade 3-tab financial model for retail branch expansion."""
        wb = openpyxl.Workbook()

        # Styles
        navy_header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
        cyan_accent_fill = PatternFill(start_color="0284C7", end_color="0284C7", fill_type="solid")
        gray_sub_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
        
        white_bold = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        cyan_bold = Font(name="Calibri", size=11, bold=True, color="00E5FF")
        dark_bold = Font(name="Calibri", size=11, bold=True, color="0F172A")
        dark_regular = Font(name="Calibri", size=11, color="1E293B")
        
        thin_border = Border(
            left=Side(style='thin', color="CBD5E1"),
            right=Side(style='thin', color="CBD5E1"),
            top=Side(style='thin', color="CBD5E1"),
            bottom=Side(style='thin', color="CBD5E1")
        )

        # TAB 1: Capex & District Allocation
        ws1 = wb.active
        ws1.title = "Capex Allocation"
        ws1.views.sheetView[0].showGridLines = True

        ws1.merge_cells("A1:G1")
        ws1["A1"] = f"{project_name} — District Capex & Setup Outlay (₹ Lakhs)"
        ws1["A1"].font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
        ws1["A1"].fill = navy_header_fill
        ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws1.row_dimensions[1].height = 35

        headers_1 = [
            "District / City", "Format", "Carpet Area (sq.ft)", "Lease Deposit (₹L)",
            "Interior Fit-Outs (₹L)", "IT & Hardware (₹L)", "Total Capex (₹L)"
        ]
        for col_idx, h in enumerate(headers_1, start=1):
            cell = ws1.cell(row=3, column=col_idx, value=h)
            cell.font = white_bold
            cell.fill = cyan_accent_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border
        ws1.row_dimensions[3].height = 25

        data_1 = [
            ["Kamrup Metro (Guwahati)", "Flagship Experiential", 2500, 12.0, 22.0, 8.0, "=SUM(D4:F4)"],
            ["Dibrugarh", "Commercial Trade Center", 1800, 8.0, 15.0, 5.0, "=SUM(D5:F5)"],
            ["Nagaon", "Agro-Consumer Hub", 1500, 6.0, 12.0, 4.0, "=SUM(D6:F6)"],
        ]

        for r_idx, row_values in enumerate(data_1, start=4):
            for c_idx, val in enumerate(row_values, start=1):
                cell = ws1.cell(row=r_idx, column=c_idx, value=val)
                cell.font = dark_regular
                cell.border = thin_border
                cell.alignment = Alignment(horizontal="left" if c_idx <= 2 else "right", vertical="center")
            ws1.row_dimensions[r_idx].height = 20

        # Totals Row
        ws1.cell(row=7, column=1, value="Total Network Outlay").font = white_bold
        ws1.cell(row=7, column=1).fill = navy_header_fill
        ws1.cell(row=7, column=2, value="3 Branches").font = white_bold
        ws1.cell(row=7, column=2).fill = navy_header_fill
        ws1.cell(row=7, column=3, value="=SUM(C4:C6)").font = white_bold
        ws1.cell(row=7, column=3).fill = navy_header_fill
        ws1.cell(row=7, column=4, value="=SUM(D4:D6)").font = white_bold
        ws1.cell(row=7, column=4).fill = navy_header_fill
        ws1.cell(row=7, column=5, value="=SUM(E4:E6)").font = white_bold
        ws1.cell(row=7, column=5).fill = navy_header_fill
        ws1.cell(row=7, column=6, value="=SUM(F4:F6)").font = white_bold
        ws1.cell(row=7, column=6).fill = navy_header_fill
        ws1.cell(row=7, column=7, value="=SUM(G4:G6)").font = cyan_bold
        ws1.cell(row=7, column=7).fill = navy_header_fill
        for c in range(1, 8):
            ws1.cell(row=7, column=c).border = thin_border
        ws1.row_dimensions[7].height = 24

        # TAB 2: 12-Month Network Cashflow & EBITDA
        ws2 = wb.create_sheet(title="12-Month P&L")
        ws2.views.sheetView[0].showGridLines = True

        ws2.merge_cells("A1:M1")
        ws2["A1"] = "Consolidated 12-Month Operating Cashflow & EBITDA Forecast (₹ Lakhs)"
        ws2["A1"].font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
        ws2["A1"].fill = navy_header_fill
        ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws2.row_dimensions[1].height = 35

        months = [f"M{i}" for i in range(1, 13)]
        pnl_headers = ["Metric / Month"] + months
        for col_idx, h in enumerate(pnl_headers, start=1):
            cell = ws2.cell(row=3, column=col_idx, value=h)
            cell.font = white_bold
            cell.fill = cyan_accent_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border

        pnl_metrics = [
            ("Gross Sales (All 3 Branches)", [18.5, 21.2, 24.8, 28.5, 31.0, 34.5, 37.8, 41.2, 44.0, 47.5, 51.0, 55.0]),
            ("Cost of Goods Sold (COGS 60%)", [f"=B4*0.6" for _ in range(12)]),
            ("Gross Margin (40%)", [f"=B4-B5" for _ in range(12)]),
            ("Store Rent & Utilities", [4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5]),
            ("Staff Salaries & Wages", [3.8, 3.8, 3.8, 3.8, 4.0, 4.0, 4.0, 4.2, 4.2, 4.2, 4.5, 4.5]),
            ("Marketing & Logistics", [2.5, 2.0, 1.8, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.8, 2.0]),
            ("Store Operating EBITDA", [f"=B6-SUM(B7:B9)" for _ in range(12)])
        ]

        # Populate P&L data
        for r_offset, (m_label, vals) in enumerate(pnl_metrics, start=4):
            ws2.cell(row=r_offset, column=1, value=m_label).font = dark_bold if "EBITDA" in m_label or "Gross" in m_label else dark_regular
            ws2.cell(row=r_offset, column=1).border = thin_border
            for col_idx, v in enumerate(vals, start=2):
                c_letter = get_column_letter(col_idx)
                cell_val = v
                if isinstance(v, str) and v.startswith("="):
                    cell_val = v.replace("B", c_letter)
                cell = ws2.cell(row=r_offset, column=col_idx, value=cell_val)
                cell.border = thin_border
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if "EBITDA" in m_label:
                    cell.font = cyan_bold
                    cell.fill = gray_sub_fill

        # Auto-fit columns
        for ws in [ws1, ws2]:
            for col in ws.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = get_column_letter(col[0].column)
                ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

        filename = f"model_retail_{uuid.uuid4().hex[:8]}.xlsx"
        file_path = self.output_dir / filename
        wb.save(str(file_path))

        return {
            "filename": filename,
            "file_path": str(file_path),
            "download_url": f"/api/download/generated/{filename}",
            "file_type": "EXCEL_FINANCIAL_MODEL",
            "title": f"{project_name} 12-Month Financial Model"
        }

excel_model_builder = ExcelModelBuilder()

