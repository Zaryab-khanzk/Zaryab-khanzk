import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap():
    with open("data/contributions.json", "r") as f:
        data = json.load(f)

    days = data.get("days", [])
    total = data.get("total", 0)

    box_size = 10
    box_gap = 4
    start_x = 20
    start_y = 30

    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="860" height="170" viewBox="0 0 860 170">',
        '  <style>',
        '    .bg { fill: #0d1117; stroke: #30363d; stroke-width: 1px; }',
        '    .lbl { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica; font-size: 12px; fill: #8b949e; }',
        '    .day-box { transform-box: fill-box; transform-origin: center; animation: slideIn 0.3s ease-out forwards; opacity: 0; }',
        '    @keyframes slideIn { from { opacity: 0; transform: translateY(-5px); } to { opacity: 1; transform: translateY(0); } }',
        '  </style>',
        '  <rect width="860" height="170" class="bg" rx="6" />',
        f'  <text x="{start_x}" y="20" class="lbl" style="font-weight:bold; fill:#c9d1d9;">{total:,} contributions in the last year</text>'
    ]

    for idx, day in enumerate(days):
        week = idx // 7
        day_of_week = idx % 7

        x = start_x + week * (box_size + box_gap)
        y = start_y + day_of_week * (box_size + box_gap)

        color = PALETTE[min(day.get("level", 0), len(PALETTE) - 1)]
        delay = (week * 0.01) + (day_of_week * 0.015)

        rect = f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}" class="day-box" style="animation-delay: {delay:.3f}s;"><title>{day["date"]}: level {day["level"]}</title></rect>'
        svg.append(rect)

    legend_x = 700
    legend_y = 145
    svg.append(f'  <text x="{legend_x - 30}" y="{legend_y + 9}" class="lbl" font-size="10">Less</text>')
    for i, p_color in enumerate(PALETTE):
        lx = legend_x + i * (box_size + 3)
        svg.append(f'  <rect x="{lx}" y="{legend_y}" width="{box_size}" height="{box_size}" rx="2" fill="{p_color}" />')
    svg.append(f'  <text x="{legend_x + len(PALETTE)*(box_size+3) + 5}" y="{legend_y + 9}" class="lbl" font-size="10">More</text>')

    svg.append('</svg>')

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print("Generated contrib-heatmap.svg")

if __name__ == "__main__":
    render_heatmap()