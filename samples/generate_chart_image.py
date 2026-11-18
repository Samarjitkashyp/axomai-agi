from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

samples_dir = Path("samples")
samples_dir.mkdir(exist_ok=True)

img_path = samples_dir / "cloud_sales_chart.png"

# Create a clean 800x500 infographic/chart
img = Image.new("RGB", (800, 500), color=(17, 24, 39)) # dark slate background
draw = ImageDraw.Draw(img)

# Title
draw.text((50, 40), "AxomAI Quarterly Cloud Revenue 2025 (in Lakhs INR)", fill=(56, 189, 248))

# Subtitle
draw.text((50, 70), "Infrastructure Growth across Northeast India", fill=(156, 163, 175))

# Draw Bar Chart
# Axes
draw.line([(80, 420), (720, 420)], fill=(75, 85, 99), width=2) # X axis
draw.line([(80, 120), (80, 420)], fill=(75, 85, 99), width=2)  # Y axis

# Bars: (Label, Value in Lakhs, Color)
data = [
    ("Q1 Jan-Mar", 120, (6, 182, 212)),
    ("Q2 Apr-Jun", 195, (99, 102, 241)),
    ("Q3 Jul-Sep", 310, (168, 85, 247)),
    ("Q4 Oct-Dec", 480, (236, 72, 153))
]

x_start = 120
bar_width = 100
spacing = 50
max_val = 500
chart_height = 280

for label, val, color in data:
    bar_height = int((val / max_val) * chart_height)
    y_top = 420 - bar_height
    y_bottom = 420
    x_left = x_start
    x_right = x_start + bar_width

    # Draw Bar
    draw.rectangle([(x_left, y_top), (x_right, y_bottom)], fill=color, outline=(255, 255, 255))
    
    # Value text on top
    draw.text((x_left + 25, y_top - 25), f"{val} L", fill=(255, 255, 255))
    
    # Label at bottom
    draw.text((x_left + 10, y_bottom + 10), label, fill=(209, 213, 219))
    
    x_start += bar_width + spacing

# Legend / Notes
draw.text((50, 465), "Note: Q4 shows highest 54% growth driven by Axom Cloud Enterprise.", fill=(52, 211, 153))

img.save(img_path)
print(f"Generated test image: {img_path}")

