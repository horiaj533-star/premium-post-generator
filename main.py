import streamlit as st
import os
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap

st.set_page_config(page_title="Premium AI Post Generator - MAG Style", layout="centered")
st.title("⚡ Premium E-Com Post Architect")
st.write("My Amazon Guy style clean infographic generator!")

# Font Download
@st.cache_data
def download_fonts():
    font_dir = "fonts"
    os.makedirs(font_dir, exist_ok=True)
    urls = {
        "Oswald-Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/oswald/Oswald%5Bwght%5D.ttf",
        "Roboto-Regular.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf",
        "Roboto-Bold.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf",
    }
    for name, url in urls.items():
        path = os.path.join(font_dir, name)
        if not os.path.exists(path):
            r = requests.get(url)
            with open(path, "wb") as f:
                f.write(r.content)
    return font_dir

font_folder = download_fonts()

# ─── INPUTS ───────────────────────────────────────────────
main_heading   = st.text_input("Main Heading:", "FBM Sellers Just Got More Protection")
brand_name     = st.text_input("Brand / Channel Name:", "My Amazon Guy")

st.markdown("**4 Benefit Badges (green chips around the person)**")
col1, col2 = st.columns(2)
with col1:
    badge1 = st.text_input("Badge 1:", "Fewer no-return refunds")
    badge3 = st.text_input("Badge 3:", "Lower CSBA barrier")
with col2:
    badge2 = st.text_input("Badge 2:", "Centralized messages")
    badge4 = st.text_input("Badge 4:", "Better customer issue data")

person_image_path = st.text_input(
    "Person PNG path (transparent bg preferred):",
    "Abdullah_Gull_Amazon_Expert.jpg-removebg-preview.png"
)

# ─── GENERATE ─────────────────────────────────────────────
if st.button("Generate MAG-Style Infographic"):

    # ── Load fonts ──
    try:
        f_heading  = ImageFont.truetype(os.path.join(font_folder, "Oswald-Bold.ttf"),   88)
        f_brand    = ImageFont.truetype(os.path.join(font_folder, "Roboto-Bold.ttf"),   34)
        f_badge    = ImageFont.truetype(os.path.join(font_folder, "Roboto-Bold.ttf"),   32)
    except Exception:
        f_heading = f_brand = f_badge = ImageFont.load_default()

    W, H = 1080, 1080

    # ── Canvas – mint-to-white gradient background ──
    canvas = Image.new("RGB", (W, H), "#ffffff")
    draw   = ImageDraw.Draw(canvas)

    # Mint gradient top half
    for y in range(H):
        ratio = y / H
        r = int(200 + (255 - 200) * ratio)
        g = int(240 + (255 - 240) * ratio)
        b = int(230 + (255 - 230) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # ── Black bottom bar ──
    draw.rectangle([(0, 980), (W, H)], fill="#111111")

    # ── Brand name (top center) ──
    brand_w = draw.textlength(brand_name, font=f_brand)
    # Small colored bars (like MAG logo) before name
    bar_x = (W - brand_w) // 2 - 40
    for i, color in enumerate(["#4285F4", "#EA4335", "#FBBC05", "#34A853"]):
        draw.rectangle([(bar_x + i*10, 42), (bar_x + i*10 + 7, 70)], fill=color)
    draw.text(((W - brand_w) // 2, 38), brand_name, fill="#111111", font=f_brand)

    # ── Yellow heading background + text ──
    heading_lines = textwrap.wrap(main_heading, width=18)
    line_h        = 96
    total_h       = len(heading_lines) * line_h + 30
    pad           = 24

    # Draw yellow rectangles (slight offset, stacked like MAG)
    rect_y = 100
    for i, line in enumerate(heading_lines):
        tw = draw.textlength(line, font=f_heading)
        rx1 = (W - tw) // 2 - pad
        rx2 = (W + tw) // 2 + pad
        ry1 = rect_y + i * line_h - 10
        ry2 = ry1 + line_h + 4
        draw.rectangle([(rx1, ry1), (rx2, ry2)], fill="#FFD600")
        draw.text(((W - tw) // 2, rect_y + i * line_h), line, fill="#111111", font=f_heading)

    # ── Person image ──
    person_y_top = rect_y + total_h + 10
    if os.path.exists(person_image_path):
        person = Image.open(person_image_path).convert("RGBA")
        # Scale to fill lower portion
        ph = H - person_y_top - 80
        pw = int(person.width * ph / person.height)
        person = person.resize((pw, ph), Image.LANCZOS)
        px = (W - pw) // 2
        canvas.paste(person, (px, person_y_top), person)
    else:
        draw.text((W//2 - 150, H//2), "[ Person image missing ]", fill="#ff0000", font=f_badge)

    # ── Helper: draw a rounded green badge ──
    def draw_badge(cx, cy, text, anchor="center"):
        """cx, cy = center of badge"""
        lines = textwrap.wrap(text, width=14)
        lh    = 38
        bw    = 260
        bh    = len(lines) * lh + 28
        bx1   = cx - bw // 2
        by1   = cy - bh // 2
        bx2   = cx + bw // 2
        by2   = cy + bh // 2

        # Shadow
        draw.rounded_rectangle([(bx1+4, by1+4), (bx2+4, by2+4)], radius=14, fill=(0,0,0,60))
        # Green box
        draw.rounded_rectangle([(bx1, by1), (bx2, by2)], radius=14, fill="#2DB67D")
        # Checkmark circle
        ck_x, ck_y = bx1 + 26, (by1 + by2) // 2
        draw.ellipse([(ck_x-14, ck_y-14), (ck_x+14, ck_y+14)], fill="#1a8a57")
        draw.text((ck_x-7, ck_y-10), "✓", fill="#ffffff", font=f_badge)
        # Text
        txt_x = bx1 + 54
        for i, ln in enumerate(lines):
            draw.text((txt_x, by1 + 14 + i * lh), ln, fill="#ffffff", font=f_badge)

    # Badge positions (around person, like MAG style)
    mid_y = person_y_top + (H - person_y_top) // 2
    draw_badge(160,  mid_y - 100, badge1)   # top-left
    draw_badge(920,  mid_y - 100, badge2)   # top-right
    draw_badge(W//2, person_y_top + 30,  badge1[:0] or badge1, )  # top-center — skip, MAG uses top-center for 1 badge
    draw_badge(160,  mid_y + 80,  badge3)   # bottom-left
    draw_badge(920,  mid_y + 80,  badge4)   # bottom-right
    # Top-center badge (5th if needed, else first badge goes here)
    draw_badge(W//2, person_y_top + 50, badge1)

    # ── Save & Display ──
    out_path = "mag_style_post.png"
    canvas.save(out_path)
    st.image(out_path, caption="✅ MAG-Style Infographic Ready!")
    with open(out_path, "rb") as f:
        st.download_button("⬇️ Download HD Post", f, file_name="mag_infographic.png", mime="image/png")
