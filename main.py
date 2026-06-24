import streamlit as st
import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

st.set_page_config(page_title="Black & Orange Amazon Post Generator", layout="centered")
st.title("🔥 Black & Orange Amazon Post Generator")
st.write("My Amazon Guy style — Black/Orange theme with your photo!")

# ─── FONT DOWNLOAD ───────────────────────────────────────
@st.cache_data
def download_fonts():
    font_dir = "fonts"
    os.makedirs(font_dir, exist_ok=True)
    urls = {
        "Oswald-Bold.ttf":    "https://github.com/google/fonts/raw/main/ofl/oswald/Oswald%5Bwght%5D.ttf",
        "Roboto-Regular.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf",
        "Roboto-Bold.ttf":    "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf",
    }
    for name, url in urls.items():
        path = os.path.join(font_dir, name)
        if not os.path.exists(path):
            r = requests.get(url, timeout=30)
            with open(path, "wb") as f:
                f.write(r.content)
    return font_dir

font_folder = download_fonts()

# ─── INPUTS ──────────────────────────────────────────────
st.sidebar.header("⚙️ Customize Your Post")

main_heading = st.sidebar.text_input("Main Heading:", "AMAZON CRITICAL UPDATE")
brand_name   = st.sidebar.text_input("Brand Name:", "Abdullah Gull  |  Amazon Expert")
website      = st.sidebar.text_input("Website / Handle:", "amazon-expert.com  •  @AbdullahGull")

st.sidebar.markdown("---")
st.sidebar.markdown("**5 Info Badges**")
badge_inputs = []
defaults = [
    ("34 Days Left",    "Deadline: July 27"),
    ("Title Limit",     "75 chars max"),
    ("Auto Force-Edit", "Amazon will change"),
    ("Check NOW",       "Seller Central"),
    ("Update Titles",   "Before deadline"),
]
for i, (dt, ds) in enumerate(defaults, 1):
    t = st.sidebar.text_input(f"Badge {i} Title:", dt,   key=f"bt{i}")
    s = st.sidebar.text_input(f"Badge {i} Sub:",   ds,   key=f"bs{i}")
    badge_inputs.append((t, s))

st.sidebar.markdown("---")
person_file = st.sidebar.file_uploader(
    "Upload Your Photo (PNG with transparent or white bg recommended):",
    type=["png","jpg","jpeg"]
)

# ─── GENERATE ────────────────────────────────────────────
if st.button("🔥 Generate Black & Orange Post"):

    W, H   = 1080, 1080
    ORANGE = "#FF6A00"
    WHITE  = "#FFFFFF"
    DARK   = "#0e0e0e"
    GRAY   = "#aaaaaa"

    # Fonts
    try:
        f_brand = ImageFont.truetype(os.path.join(font_folder,"Roboto-Bold.ttf"),    33)
        f_head  = ImageFont.truetype(os.path.join(font_folder,"Oswald-Bold.ttf"),    82)
        f_bl    = ImageFont.truetype(os.path.join(font_folder,"Roboto-Bold.ttf"),    27)
        f_bs    = ImageFont.truetype(os.path.join(font_folder,"Roboto-Regular.ttf"), 21)
    except:
        f_brand = f_head = f_bl = f_bs = ImageFont.load_default()

    # Canvas
    canvas = Image.new("RGB", (W, H), "#080808")
    draw   = ImageDraw.Draw(canvas)
    for y in range(H):
        t = y / H
        draw.line([(0,y),(W,y)], fill=(int(8+30*t), int(8+5*t), 8))

    # Orange glow
    glow = Image.new("RGBA",(W,H),(0,0,0,0))
    gd   = ImageDraw.Draw(glow)
    for rad in range(300,0,-4):
        a = int(55*(1-rad/300))
        gd.ellipse([(W-rad,H-rad),(W+rad,H+rad)],fill=(255,80,0,a))
    canvas = Image.alpha_composite(canvas.convert("RGBA"),glow).convert("RGB")
    draw   = ImageDraw.Draw(canvas)

    # Orange border
    draw.rectangle([(10,10),(W-10,H-10)], outline=ORANGE, width=5)

    # Brand name
    bw = draw.textlength(brand_name, font=f_brand)
    bx = (W-bw)//2
    for i,c in enumerate(["#FF6A00","#FF2200","#FFB300","#FF5500"]):
        draw.rectangle([(bx-88+i*17,32),(bx-88+i*17+12,62)],fill=c)
    draw.text((bx,30), brand_name, fill=ORANGE, font=f_brand)

    # Header bar
    draw.rectangle([(35,78),(W-35,178)],fill=ORANGE)
    hw = draw.textlength(main_heading, font=f_head)
    # If too long, reduce
    if hw > W - 100:
        heading_lines = textwrap.wrap(main_heading, width=20)
        for li, line in enumerate(heading_lines[:2]):
            lw = draw.textlength(line, font=f_bl)
            draw.text(((W-lw)//2, 92 + li*44), line, fill=WHITE, font=f_bl)
    else:
        draw.text(((W-hw)//2, 110), main_heading, fill=WHITE, font=f_head)

    # ── PERSON IMAGE ──
    PERSON_AREA_LEFT = W // 2 + 30   # person goes in RIGHT half
    PERSON_TOP       = 185
    PERSON_BOT       = H - 70
    PERSON_H         = PERSON_BOT - PERSON_TOP
    PERSON_W         = W - PERSON_AREA_LEFT - 20

    if person_file:
        person_src = Image.open(person_file).convert("RGBA")
        # Scale to fit right-half area
        scale  = min(PERSON_W / person_src.width, PERSON_H / person_src.height)
        pw     = int(person_src.width  * scale)
        ph     = int(person_src.height * scale)
        person = person_src.resize((pw, ph), Image.LANCZOS)
        px     = PERSON_AREA_LEFT + (PERSON_W - pw) // 2
        py     = PERSON_BOT - ph
        canvas.paste(person, (px, py), person)
    else:
        draw.rectangle([(PERSON_AREA_LEFT, PERSON_TOP),(W-20, PERSON_BOT)],
                       outline=ORANGE, width=2)
        draw.text((PERSON_AREA_LEFT+20, PERSON_TOP+PERSON_H//2-20),
                  "Upload your photo →", fill=ORANGE, font=f_bs)

    draw = ImageDraw.Draw(canvas)

    # ── BADGES (LEFT SIDE) ──
    def badge(cx, cy, title, sub=""):
        BW=255; BH=72 if not sub else 100
        x1,y1=cx-BW//2,cy-BH//2; x2,y2=cx+BW//2,cy+BH//2
        draw.rounded_rectangle([(x1+4,y1+4),(x2+4,y2+4)],radius=13,fill="#000000")
        draw.rounded_rectangle([(x1,y1),(x2,y2)],radius=13,fill=DARK)
        draw.rounded_rectangle([(x1,y1),(x2,y2)],radius=13,outline=ORANGE,width=3)
        ck_x=x1+28; ck_y=y1+BH//2-(10 if sub else 0)
        draw.ellipse([(ck_x-15,ck_y-15),(ck_x+15,ck_y+15)],fill=ORANGE)
        draw.text((ck_x-5,ck_y-11),"✓",fill=WHITE,font=f_bl)
        draw.text((x1+52,y1+12),title[:20],fill=WHITE,font=f_bl)
        if sub:
            draw.text((x1+52,y1+48),sub[:24],fill=GRAY,font=f_bs)

    LX   = 190          # left column center
    BY   = 210          # starting y for badges
    BGAP = 158          # gap between badges

    for i, (t, s) in enumerate(badge_inputs):
        badge(LX, BY + i * BGAP, t, s)

    # Bottom bar
    draw.rectangle([(0,H-68),(W,H)],fill="#000000")
    tw2 = draw.textlength(website, font=f_bs)
    draw.text(((W-tw2)//2, H-48), website, fill=ORANGE, font=f_bs)

    # Save & show
    out = "black_orange_post.png"
    canvas.save(out)
    st.image(out, caption="✅ Your Black & Orange Post is Ready!")
    with open(out,"rb") as f:
        st.download_button("⬇️ Download HD Post", f,
                           file_name="amazon_post.png", mime="image/png")

    st.info("💡 Tip: Upload a transparent-background (PNG cutout) photo of yourself for best results!")
