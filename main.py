import streamlit as st
import os, json, textwrap, requests
from PIL import Image, ImageDraw, ImageFont
import anthropic

st.set_page_config(page_title="Abdullah Gull | AI Post Generator", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0a0a0a 0%, #1a0800 100%) !important; }
h1, h2, h3 { color: #FF6A00 !important; }
.stButton>button {
    background: linear-gradient(135deg, #FF6A00, #cc4400) !important;
    color: white !important; font-weight: bold !important;
    border: none !important; border-radius: 10px !important;
    padding: 14px 30px !important; font-size: 18px !important; width: 100% !important;
}
.stTextArea textarea { background: #111 !important; color: #fff !important; border: 1px solid #FF6A00 !important; }
.stTextInput input { background: #111 !important; color: #fff !important; border: 1px solid #FF6A00 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🔥 AI LinkedIn Post + Infographic Generator")
st.markdown("**Paste content → AI makes heading & badges → Download ready infographic!**")
st.markdown("---")

# Font paths (system fonts)
F_BOLD     = "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf"
F_REG      = "/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf"
F_CONDBOLD = "/usr/share/fonts/truetype/open-sans/OpenSans-CondBold.ttf"

def install_fonts():
    if not os.path.exists(F_BOLD):
        os.system("apt-get install -y fonts-open-sans -q")
install_fonts()

# ─────────────────────────── UI INPUTS ───────────────────────────
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown("### 📝 Your Raw Content")
    user_content = st.text_area(
        "Paste your Amazon news/tips here:",
        height=200,
        placeholder="Example: Amazon just announced product titles will be capped at 75 characters starting July 27. Sellers have 34 days to update. Titles exceeding limit will be auto-truncated by Amazon..."
    )
    
    st.markdown("### 🎨 Customize")
    c1, c2 = st.columns(2)
    with c1:
        brand_first = st.text_input("First Name (orange):", "Abdullah")
        handle      = st.text_input("Handle:", "@AbdullahGull")
    with c2:
        brand_last  = st.text_input("Last Name (white):", "Gull")

with right_col:
    st.markdown("### 📸 Your Photo")
    st.info("💡 Upload a photo with **transparent OR white background** (PNG preferred) for best results!")
    person_file = st.file_uploader("Upload photo:", type=["png","jpg","jpeg"])
    if person_file:
        st.image(person_file, caption="Your photo ✅", use_container_width=True)

st.markdown("---")
generate_btn = st.button("🚀 Generate AI Post + Infographic", use_container_width=True)

# ─────────────────────────── AI CALL ─────────────────────────────
def call_ai(content, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    prompt = f"""You are an expert Amazon seller content strategist. 

Given this content:
\"\"\"{content}\"\"\"

Return ONLY a JSON object (no markdown, no backticks, no explanation):
{{
  "heading": "SHORT PUNCHY HEADING ALL CAPS MAX 6 WORDS",
  "badge1": "SHORT KEY POINT ALL CAPS MAX 4 WORDS",
  "badge2": "SHORT KEY POINT ALL CAPS MAX 4 WORDS",
  "badge3": "SHORT KEY POINT ALL CAPS MAX 4 WORDS",
  "badge4": "SHORT KEY POINT ALL CAPS MAX 4 WORDS",
  "badge5": "SHORT KEY POINT ALL CAPS MAX 4 WORDS",
  "linkedin_post": "Professional engaging LinkedIn post. Start with bold hook line. 3-4 emoji bullet points with key insights. End with question to drive engagement. Add 5-6 relevant hashtags. Max 180 words total."
}}"""
    
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        messages=[{"role":"user","content":prompt}]
    )
    raw = msg.content[0].text.strip()
    raw = raw.replace("```json","").replace("```","").strip()
    return json.loads(raw)

# ─────────────────────────── IMAGE BUILDER ────────────────────────
def build_image(data, person_img_file, brand_f, brand_l, handle_text):
    W, H     = 1080, 1080
    ORANGE   = (255, 106, 0)
    YELLOW   = (255, 200, 0)
    WHITE    = (255, 255, 255)
    DARK_BOX = (15, 6, 0)
    BLACK    = (0, 0, 0)

    try:
        f_bo = ImageFont.truetype(F_BOLD,     44)
        f_bw = ImageFont.truetype(F_BOLD,     44)
        f_hd = ImageFont.truetype(F_CONDBOLD, 84)
        f_bg = ImageFont.truetype(F_BOLD,     22)
        f_sm = ImageFont.truetype(F_REG,      18)
    except:
        f_bo = f_bw = f_hd = f_bg = f_sm = ImageFont.load_default()

    # Canvas
    canvas = Image.new("RGB",(W,H),(4,4,4))
    draw   = ImageDraw.Draw(canvas)
    for y in range(H):
        t = y/H
        draw.line([(0,y),(W,y)], fill=(int(4+38*t), int(4+6*t), 4))

    # Orange glow
    glow = Image.new("RGBA",(W,H),(0,0,0,0))
    gd   = ImageDraw.Draw(glow)
    for rad in range(500,0,-5):
        a = int(72*(1-rad/500))
        gd.ellipse([(W//2-rad,H-rad),(W//2+rad,H+rad)], fill=(255,75,0,a))
    canvas = Image.alpha_composite(canvas.convert("RGBA"),glow).convert("RGB")
    draw   = ImageDraw.Draw(canvas)

    # Brand
    t1 = brand_f + " "; t2 = brand_l
    w1 = draw.textlength(t1, font=f_bo)
    w2 = draw.textlength(t2, font=f_bw)
    bx = (W-w1-w2)//2
    draw.text((bx,    22), t1, fill=ORANGE, font=f_bo)
    draw.text((bx+w1, 22), t2, fill=WHITE,  font=f_bw)

    # Yellow heading
    hlines = textwrap.wrap(data["heading"], width=20)
    lh=90; py=20; bt=90
    bh = len(hlines)*lh + py*2
    draw.rectangle([(22,bt),(W-22,bt+bh)], fill=YELLOW)
    for i,line in enumerate(hlines):
        lw = draw.textlength(line, font=f_hd)
        draw.text(((W-lw)//2, bt+py+i*lh), line, fill=(8,8,8), font=f_hd)
    he = bt + bh + 10  # heading end

    # Person
    if person_img_file:
        import numpy as np
        p_src = Image.open(person_img_file).convert("RGBA")
        arr   = np.array(p_src)
        r,g,b,a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
        
        # If white background, make transparent
        is_white = (r > 230) & (g > 230) & (b > 230)
        arr[:,:,3] = np.where(is_white, 0, 255).astype(np.uint8)
        p_src = Image.fromarray(arr)
        
        ph = H - he - 45
        pw = int(p_src.width * ph / p_src.height)
        if pw > 600:  # cap width
            pw = 600; ph = int(p_src.height * pw / p_src.width)
        p_r = p_src.resize((pw, ph), Image.LANCZOS)
        ppx = (W-pw)//2
        ppy = H - ph - 10
        canvas.paste(p_r, (ppx, ppy), p_r)
    else:
        # Orange placeholder circle
        draw.ellipse([(W//2-80, he+80),(W//2+80, he+240)], fill=(60,25,0))
        draw.rectangle([(W//2-100, he+230),(W//2+100, H-30)], fill=(60,25,0))

    draw = ImageDraw.Draw(canvas)

    # Badges
    badges = [data[f"badge{i}"] for i in range(1,6)]
    mid_y  = he + (H-he)//2 + 30
    pos    = [
        (W//2,  he+46),
        (163,   mid_y-100),
        (W-163, mid_y-100),
        (163,   mid_y+88),
        (W-163, mid_y+88),
    ]

    def badge(cx,cy,text):
        lines=textwrap.wrap(text, width=14)
        BW=238; BH=60+max(0,len(lines)-1)*25
        x1,y1=cx-BW//2,cy-BH//2; x2,y2=cx+BW//2,cy+BH//2
        draw.rounded_rectangle([(x1+4,y1+4),(x2+4,y2+4)],radius=11,fill=BLACK)
        draw.rounded_rectangle([(x1,y1),(x2,y2)],radius=11,fill=DARK_BOX)
        draw.rounded_rectangle([(x1,y1),(x2,y2)],radius=11,outline=ORANGE,width=3)
        draw.rounded_rectangle([(x1+8,y1+8),(x1+45,y2-8)],radius=7,fill=ORANGE)
        draw.text((x1+16,y1+BH//2-12),"✓",fill=WHITE,font=f_bg)
        for li,ln in enumerate(lines):
            draw.text((x1+52,y1+11+li*25),ln,fill=WHITE,font=f_bg)

    for (cx,cy),bd in zip(pos, badges):
        badge(cx,cy,bd)

    # Handle
    hw = draw.textlength(handle_text, font=f_sm)
    draw.text(((W-hw)//2, H-25), handle_text, fill=ORANGE, font=f_sm)

    return canvas

# ─────────────────────────── GENERATE ────────────────────────────
if generate_btn:
    api_key = os.environ.get("ANTHROPIC_API_KEY","")
    
    if not user_content.strip():
        st.error("❌ Pehle content paste karein!")
        st.stop()
    if not api_key:
        st.error("❌ ANTHROPIC_API_KEY set karein Streamlit secrets mein!")
        st.stop()

    with st.spinner("🤖 AI content analyze kar raha hai..."):
        try:
            ai = call_ai(user_content, api_key)
        except Exception as e:
            st.error(f"AI Error: {e}")
            st.stop()

    with st.spinner("🎨 Infographic design ho raha hai..."):
        img = build_image(ai, person_file, brand_first, brand_last, handle)
        img.save("output_post.png")

    st.markdown("---")
    st.markdown("## ✅ Ready!")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🖼️ Your Infographic")
        st.image("output_post.png", use_container_width=True)
        with open("output_post.png","rb") as f:
            st.download_button(
                "⬇️ Download HD Infographic (1080x1080)",
                f, "linkedin_post.png", "image/png",
                use_container_width=True
            )

    with col_b:
        st.markdown("### 📋 LinkedIn Post (Copy & Paste)")
        st.text_area("", value=ai["linkedin_post"], height=300, key="post_out")
        
        st.markdown("**AI Generated:**")
        st.markdown(f"📌 **Heading:** `{ai['heading']}`")
        for i in range(1,6):
            st.markdown(f"▸ **Badge {i}:** {ai[f'badge{i}']}")
        
        st.info("💡 Copy the post above and paste directly on LinkedIn with the image!")
