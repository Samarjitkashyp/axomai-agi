"""
Z7 Visionary - High-DPI Chart & Assam Catchment Map Renderer (Pillow PIL).
Renders crisp PNG graphics on disk for embedding directly into .pptx slides and .docx DPRs:
1. Break-Even Point (BEP) Crossover Chart (Fixed Cost, Total Cost, Revenue & BEP% marker)
2. Assam Strategic Catchment & Highway Corridor Map (highlighting target district & NH links)
"""

import uuid
from typing import Dict, Any, Tuple
from PIL import Image, ImageDraw, ImageFont

from axomai.config import settings
from axomai.agents.z7_visionary.tools.assam_benchmarks_and_schemes import ASSAM_DISTRICT_PROFILES


class ChartAndMapRenderer:
    """Renders high-DPI PNG financial charts and Assam district maps via Pillow."""

    def __init__(self):
        self.output_dir = settings.STORAGE_DIR / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def render_bep_crossover_chart(
        self,
        bep_capacity_pct: float,
        bep_revenue_lakhs: float,
        yr1_revenue_lakhs: float
    ) -> Dict[str, Any]:
        """Generates a 1000x560 PNG Break-Even Point Crossover Chart."""
        w, h = 1000, 560
        img = Image.new("RGB", (w, h), (15, 23, 42))
        draw = ImageDraw.Draw(img)

        # Plot area bounds
        x0, y0, x1, y1 = 110, 80, 920, 470
        draw.rectangle([x0, y0, x1, y1], outline=(71, 85, 105), width=2)

        # Grid lines
        for i in range(1, 5):
            gy = y0 + int((y1 - y0) * i / 5)
            draw.line([(x0, gy), (x1, gy)], fill=(30, 41, 59), width=1)
            gx = x0 + int((x1 - x0) * i / 5)
            draw.line([(gx, y0), (gx, y1)], fill=(30, 41, 59), width=1)

        # Coordinates for lines (0% -> 100% capacity)
        bep_x = x0 + int((x1 - x0) * (min(max(bep_capacity_pct, 10.0), 90.0) / 100.0))
        bep_y = y1 - int((y1 - y0) * (min(max(bep_capacity_pct, 10.0), 90.0) / 100.0) * 0.85)

        fixed_y = y1 - int((y1 - y0) * 0.25)
        # Fixed Cost line (Horizontal Slate/Amber)
        draw.line([(x0, fixed_y), (x1, fixed_y)], fill=(245, 158, 11), width=3)
        # Total Cost line (Fixed -> above BEP -> end)
        draw.line([(x0, fixed_y), (x1, y0 + 95)], fill=(244, 63, 94), width=4)
        # Total Revenue line (0 -> through BEP -> top right)
        draw.line([(x0, y1), (bep_x, bep_y), (x1, y0 + 25)], fill=(34, 197, 94), width=5)

        # BEP Intersection Dot & Drop Line
        draw.line([(bep_x, bep_y), (bep_x, y1)], fill=(56, 189, 248), width=2)
        draw.ellipse([bep_x - 9, bep_y - 9, bep_x + 9, bep_y + 9], fill=(56, 189, 248), outline=(255, 255, 255), width=2)

        # Labels (Default bitmap font scaled cleanly via concise labels)
        draw.text((x0, 28), f"BREAK-EVEN POINT (BEP) CROSSOVER ANALYSIS — BEP @ {bep_capacity_pct}% Capacity (INR {bep_revenue_lakhs}L)", fill=(56, 189, 248))
        draw.text((bep_x - 65, bep_y - 26), f"BEP: {bep_capacity_pct}%", fill=(255, 255, 255))
        draw.text((x1 - 160, y0 + 10), "Total Revenue Line", fill=(34, 197, 94))
        draw.text((x1 - 160, y0 + 75), "Total Cost Line", fill=(244, 63, 94))
        draw.text((x0 + 12, fixed_y - 20), "Fixed Cost Floor", fill=(245, 158, 11))
        draw.text((x0, y1 + 15), "0% Capacity", fill=(148, 163, 184))
        draw.text((x1 - 95, y1 + 15), "100% Capacity", fill=(148, 163, 184))

        filename = f"chart_bep_{uuid.uuid4().hex[:8]}.png"
        file_path = self.output_dir / filename
        img.save(str(file_path))
        return {"filename": filename, "file_path": str(file_path), "download_url": f"/api/download/generated/{filename}"}

    def render_assam_catchment_map(self, target_district: str) -> Dict[str, Any]:
        """Generates a 1000x540 PNG Assam Corridor & Catchment Network Map."""
        w, h = 1000, 540
        img = Image.new("RGB", (w, h), (10, 20, 35))
        draw = ImageDraw.Draw(img)

        draw.text((40, 24), f"ASSAM STRATEGIC CATCHMENT & NH CORRIDOR MAP — TARGET HUB: {target_district.upper()}", fill=(0, 229, 255))

        # Brahmaputra River stylized curve
        river_pts = [(60, 310), (220, 295), (420, 275), (620, 230), (880, 155)]
        draw.line(river_pts, fill=(14, 116, 144), width=14)

        # Draw highway edges between key hubs
        d_target = target_district.lower().split("(")[0].strip()
        hubs = ["kokrajhar", "guwahati", "nagaon", "tezpur", "jorhat", "dibrugarh", "tinsukia", "silchar"]
        edges = [
            ("kokrajhar", "guwahati"), ("guwahati", "nagaon"), ("nagaon", "tezpur"),
            ("nagaon", "jorhat"), ("jorhat", "dibrugarh"), ("dibrugarh", "tinsukia"),
            ("guwahati", "silchar")
        ]

        def to_px(norm: Tuple[float, float]) -> Tuple[int, int]:
            return int(70 + norm[0] * (w - 140)), int(70 + norm[1] * (h - 120))

        for u, v in edges:
            if u in ASSAM_DISTRICT_PROFILES and v in ASSAM_DISTRICT_PROFILES:
                p1 = to_px(ASSAM_DISTRICT_PROFILES[u]["coords_norm"])
                p2 = to_px(ASSAM_DISTRICT_PROFILES[v]["coords_norm"])
                draw.line([p1, p2], fill=(71, 85, 105), width=3)

        # Draw nodes
        for hub_name, meta in ASSAM_DISTRICT_PROFILES.items():
            px, py = to_px(meta["coords_norm"])
            is_target = (hub_name == d_target)
            if is_target:
                draw.ellipse([px - 22, py - 22, px + 22, py + 22], outline=(245, 158, 11), width=3)
                draw.ellipse([px - 10, py - 10, px + 10, py + 10], fill=(0, 229, 255), outline=(255, 255, 255), width=2)
                draw.text((px + 16, py - 14), f"{hub_name.upper()} (TARGET)", fill=(245, 158, 11))
            elif hub_name in hubs:
                draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(148, 163, 184))
                draw.text((px + 10, py - 6), hub_name.title(), fill=(203, 213, 225))

        filename = f"assam_map_{uuid.uuid4().hex[:8]}.png"
        file_path = self.output_dir / filename
        img.save(str(file_path))
        return {"filename": filename, "file_path": str(file_path), "download_url": f"/api/download/generated/{filename}"}

    def render_pan_india_corridor_map(self, target_hub: str, target_state: str) -> Dict[str, Any]:
        """Generates a 1000x540 PNG Pan-India Industrial & Startup Corridor Map for non-Assam hubs."""
        w, h = 1000, 540
        img = Image.new("RGB", (w, h), (10, 20, 35))
        draw = ImageDraw.Draw(img)

        draw.text((40, 24), f"PAN-INDIA INDUSTRIAL CORRIDOR MAP — TARGET: {target_hub.upper()} ({target_state.upper()})", fill=(0, 229, 255))

        pan_hubs = {
            "delhi": (0.42, 0.24),
            "noida": (0.46, 0.26),
            "jaipur": (0.35, 0.34),
            "ahmedabad": (0.24, 0.48),
            "surat": (0.25, 0.56),
            "mumbai": (0.26, 0.64),
            "pune": (0.31, 0.68),
            "hyderabad": (0.46, 0.68),
            "bengaluru": (0.43, 0.82),
            "chennai": (0.54, 0.82),
            "kolkata": (0.72, 0.50),
            "guwahati": (0.85, 0.34),
        }
        edges = [
            ("delhi", "noida"), ("delhi", "jaipur"), ("jaipur", "ahmedabad"),
            ("ahmedabad", "surat"), ("surat", "mumbai"), ("mumbai", "pune"),
            ("pune", "hyderabad"), ("hyderabad", "bengaluru"), ("bengaluru", "chennai"),
            ("chennai", "kolkata"), ("kolkata", "delhi"), ("kolkata", "guwahati"),
        ]

        def to_px(norm: Tuple[float, float]) -> Tuple[int, int]:
            return int(70 + norm[0] * (w - 140)), int(70 + norm[1] * (h - 120))

        for u, v in edges:
            draw.line([to_px(pan_hubs[u]), to_px(pan_hubs[v])], fill=(71, 85, 105), width=3)

        t_low = (target_hub or "").lower().strip()
        matched = False
        for hub_name, coords in pan_hubs.items():
            px, py = to_px(coords)
            is_target = (hub_name in t_low or t_low in hub_name)
            if is_target:
                matched = True
                draw.ellipse([px - 22, py - 22, px + 22, py + 22], outline=(245, 158, 11), width=3)
                draw.ellipse([px - 10, py - 10, px + 10, py + 10], fill=(0, 229, 255), outline=(255, 255, 255), width=2)
                draw.text((px + 16, py - 14), f"{target_hub.upper()} (TARGET)", fill=(245, 158, 11))
            else:
                draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(148, 163, 184))
                draw.text((px + 10, py - 6), hub_name.title(), fill=(203, 213, 225))

        if not matched:
            px, py = to_px((0.50, 0.50))
            draw.ellipse([px - 22, py - 22, px + 22, py + 22], outline=(245, 158, 11), width=3)
            draw.ellipse([px - 10, py - 10, px + 10, py + 10], fill=(0, 229, 255), outline=(255, 255, 255), width=2)
            draw.text((px + 16, py - 14), f"{target_hub.upper()} (TARGET)", fill=(245, 158, 11))

        filename = f"pan_india_map_{uuid.uuid4().hex[:8]}.png"
        file_path = self.output_dir / filename
        img.save(str(file_path))
        return {"filename": filename, "file_path": str(file_path), "download_url": f"/api/download/generated/{filename}"}


chart_map_renderer = ChartAndMapRenderer()
