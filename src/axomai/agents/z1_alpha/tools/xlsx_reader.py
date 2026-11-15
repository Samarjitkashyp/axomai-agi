import pandas as pd
import openpyxl
from pathlib import Path
from typing import Dict, Any, Optional, List
from axomai.agents.z1_alpha.tools.base import BaseFileTool
from axomai.core.udm import (
    UnifiedDocumentModel,
    DocumentPage,
    ExtractedTable
)

class XLSXReaderTool(BaseFileTool):
    name = "xlsx_reader"
    description = "Extracts multi-sheet tables, column schemas, and numerical stats from Excel spreadsheets"
    supported_extensions = {".xlsx", ".xls", ".xlsm"}

    def parse(self, file_path: str | Path, options: Optional[Dict[str, Any]] = None) -> UnifiedDocumentModel:
        file_info = self.get_file_info(file_path, "XLSX")
        excel_file = pd.ExcelFile(file_info.file_path)
        sheet_names = excel_file.sheet_names

        pages: List[DocumentPage] = []
        all_tables: List[ExtractedTable] = []
        total_rows = 0

        for idx, sheet_name in enumerate(sheet_names):
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            # Clean dataframe
            df = df.dropna(how="all")
            headers = [str(c) for c in df.columns]
            rows_data = df.fillna("").values.tolist()
            
            table_obj = ExtractedTable(
                table_id=f"sheet_{idx+1}",
                sheet_name=sheet_name,
                title=f"Sheet: {sheet_name}",
                headers=headers,
                rows=rows_data,
                row_count=len(rows_data),
                column_count=len(headers),
                metadata={
                    "numeric_columns": list(df.select_dtypes(include=['number']).columns),
                    "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
                }
            )
            all_tables.append(table_obj)
            total_rows += len(rows_data)

            # Generate sheet summary text
            summary_lines = [
                f"### Sheet: {sheet_name}",
                f"- Columns ({len(headers)}): {', '.join(headers)}",
                f"- Total Rows: {len(rows_data)}"
            ]
            
            # Include statistical summary for numeric columns
            numeric_desc = df.describe().round(2).to_dict() if not df.empty else {}
            if numeric_desc:
                summary_lines.append("- Quick Stats:")
                for col_name, stats in numeric_desc.items():
                    summary_lines.append(f"  * {col_name} -> Mean: {stats.get('mean')}, Min: {stats.get('min')}, Max: {stats.get('max')}")

            # Append markdown table preview
            summary_lines.append("\n" + table_obj.to_markdown())

            page_text = "\n".join(summary_lines)

            pages.append(DocumentPage(
                page_number=idx + 1,
                text=page_text,
                tables=[table_obj],
                images=[],
                metadata={"sheet_name": sheet_name, "rows": len(rows_data), "cols": len(headers)}
            ))

        return UnifiedDocumentModel(
            file=file_info,
            metadata={"sheets": sheet_names, "total_sheets": len(sheet_names)},
            page_count=len(sheet_names),
            pages=pages,
            tables=all_tables,
            images=[],
            stats={
                "total_sheets": len(sheet_names),
                "total_rows": total_rows,
                "total_tables": len(all_tables)
            }
        )

