import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
from axomai.agents.z1_alpha.tools.base import BaseFileTool
from axomai.core.udm import (
    UnifiedDocumentModel,
    DocumentPage,
    ExtractedTable
)

class CSVReaderTool(BaseFileTool):
    name = "csv_reader"
    description = "Extracts tabular data, columns, and data statistics from CSV and TSV files"
    supported_extensions = {".csv", ".tsv"}

    def parse(self, file_path: str | Path, options: Optional[Dict[str, Any]] = None) -> UnifiedDocumentModel:
        file_info = self.get_file_info(file_path, "CSV")
        sep = "\t" if Path(file_path).suffix.lower() == ".tsv" else ","

        df = pd.read_csv(file_info.file_path, sep=sep)
        headers = [str(c) for c in df.columns]
        rows_data = df.fillna("").values.tolist()

        table_obj = ExtractedTable(
            table_id="csv_table_1",
            title=f"Table: {file_info.filename}",
            headers=headers,
            rows=rows_data,
            row_count=len(rows_data),
            column_count=len(headers),
            metadata={
                "numeric_columns": list(df.select_dtypes(include=['number']).columns),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
            }
        )

        summary_lines = [
            f"### CSV File: {file_info.filename}",
            f"- Columns ({len(headers)}): {', '.join(headers)}",
            f"- Total Rows: {len(rows_data)}"
        ]
        
        numeric_desc = df.describe().round(2).to_dict() if not df.empty else {}
        if numeric_desc:
            summary_lines.append("- Quick Stats:")
            for col_name, stats in numeric_desc.items():
                summary_lines.append(f"  * {col_name} -> Mean: {stats.get('mean')}, Min: {stats.get('min')}, Max: {stats.get('max')}")

        summary_lines.append("\n" + table_obj.to_markdown())
        page_text = "\n".join(summary_lines)

        page = DocumentPage(
            page_number=1,
            text=page_text,
            tables=[table_obj],
            images=[],
            metadata={"rows": len(rows_data), "cols": len(headers)}
        )

        return UnifiedDocumentModel(
            file=file_info,
            metadata={"columns": headers, "total_rows": len(rows_data)},
            page_count=1,
            pages=[page],
            tables=[table_obj],
            images=[],
            stats={
                "total_rows": len(rows_data),
                "total_columns": len(headers),
                "total_tables": 1
            }
        )

