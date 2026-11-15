import pandas as pd
import fitz # PyMuPDF
from pathlib import Path

samples_dir = Path("samples")
samples_dir.mkdir(exist_ok=True)

# 1. Create sample Excel file
excel_path = samples_dir / "q1_performance.xlsx"
df1 = pd.DataFrame({
    "Employee": ["Arup", "Priyanka", "Bikash", "Mousumi"],
    "Department": ["AI Research", "Engineering", "Operations", "Marketing"],
    "Rating": [4.8, 4.9, 4.5, 4.7],
    "BonusINR": [150000, 180000, 100000, 120000]
})
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df1.to_excel(writer, sheet_name="Performance", index=False)
print(f"Created {excel_path}")

# 2. Create sample PDF with PyMuPDF
pdf_path = samples_dir / "research_report.pdf"
doc = fitz.open()

# Page 1
page1 = doc.new_page()
page1.insert_text((50, 72), "AXOM AI RESEARCH - WHITE PAPER", fontsize=18, color=(0, 0, 0.8))
page1.insert_text((50, 110), "Z1 Alpha File Intelligence Agent Architecture", fontsize=14)
page1.insert_text((50, 140), "Introduction:\nThis paper defines the Autonomous File Intelligence Agent named Z1 Alpha.\nIt coordinates specialized parsing engines and converts all incoming media into a Unified Document Model (UDM).\nKey components include Task Router, Document Cache, and Evidence Verification Layer.", fontsize=11)

# Page 2
page2 = doc.new_page()
page2.insert_text((50, 72), "Page 2: Experimental Results & Benchmarks", fontsize=16)
page2.insert_text((50, 110), "We benchmarked parsing latency across 10,000 documents:\n- Text Extraction: 12ms average\n- Table Parsing: 34ms average\n- Verification Accuracy: 99.4%", fontsize=11)

doc.save(pdf_path)
doc.close()
print(f"Created {pdf_path}")

