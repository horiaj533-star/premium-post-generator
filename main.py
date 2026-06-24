import streamlit as st
import os
import requests
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Premium AI Post Generator v3", layout="centered")
st.title("⚡ Premium E-Com Post Architect")
st.write("Apna content likhein, system automatic clean modern infographic layout ready karega!")

# Font Download karne ka jugaar (Taakay default fonts wala ganda look khatam ho)
@st.cache_data
def download_fonts():
    font_dir = "fonts"
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    
    # Modern clean fonts download karna
    urls = {
        "Oswald-Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/oswald/Oswald%5Bwght%5D.ttf",
        "Roboto-Regular.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf"
    }
    for name, url in urls.items():
        path = os.path.join(font_dir, name)
        if not os.path.exists(path):
            r = requests.get(url)
            with open(path, "wb") as f:
                f.write(r.content)
    return font_dir

font_folder = download_fonts()

# User inputs
user_content = st.text_area("Post Ka Content Yahan Paste Karein:", 
                            placeholder="Example: Amazon just changed its review management system...")

main_heading = st.text_input("Main Heading (Optional):", "AMAZON CRITICAL UPDATE")
box1_text = st.text_input("Box 1 Text (Optional):", "")
box2_text = st.text_input("Box 2 Text (Optional):", "")

hf_token = os.environ.get("HF_TOKEN")

if st.button("Generate Premium HD Post"):
    if not user_content:
        st.error("Pehle content to likhein jaanib!")
    elif not hf_token:
        st.error("HF_TOKEN missing in Secrets!")
    else:
        with st.spinner("Premium Infographic Layout Design ho raha hai..."):
            try:
                client = InferenceClient(provider="wavespeed", api_key=hf_token)
                
                # Fonts load karna
                try:
                    font_title = ImageFont.truetype(os.path.join(font_folder, "Oswald-Bold.ttf"), 44)
                    font_badge = ImageFont.truetype(os.path.join(font_folder, "Oswald-Bold.ttf"), 26)
                    font_body = ImageFont.truetype(os.path.join(font_folder, "Roboto-Regular.ttf"), 22)
                except:
                    font_title = font_badge = font_body = ImageFont.load_default()

                # Dynamic text management
                final_box1 = box1_text if box1_text else "ALERT DETECTED"
                final_box2 = box2_text if box2_text else "ACTION REQUIRED"
                
                if not box1_text or not box2_text:
                    words = user_content.split()
                    if len(words) >= 4:
                        final_box1 = " ".join(words[:2]).upper()
                        final_box2 = " ".join(words[2:5]).upper()

                # AI Background Element Prompt
                ai_prompt = f"Abstract luxury tech background, premium cyber lighting, charcoal black background with bright neon orange highlights, e-commerce data vectors, high-end studio presentation tone, matching context: {user_content[:60]}"
                
                bg_img = client.text_to_image(ai_prompt, model="black-forest-labs/FLUX.1-dev")
                bg_resized = bg_img.resize((520, 720))
                
                # Main 1080x1080 Canvas (Pure Dark Premium Background)
                canvas = Image.new("RGB", (1080, 1080), "#0a0a0a")
                draw = ImageDraw.Draw(canvas)
                
                # Paste AI Background
                canvas.paste(bg_resized, (520, 220))
                
                # --- AAPKI PHOTO INTEGRATION ---
                image_name = "Abdullah_Gull_Amazon_Expert.jpg-removebg-preview.png"
                if os.path.exists(image_name):
                    user_face = Image.open(image_name).convert("RGBA")
                    user_face.thumbnail((480, 680))
                    # Photo overlay
                    canvas.paste(user_face, (540, 260), user_face)
                else:
                    draw.rectangle([(540, 260), (1000, 800)], outline="#ff6a00", width=2)
                    draw.text((600, 500), "Image Missing on GitHub!", fill="#ff0000")
                
                # --- MODERN STYLE DESIGN LAYOUT ---
                # Top Header Box (Rounded Corners like My Amazon Guy style)
                draw.rounded_rectangle([(50, 50), (1030, 160)], radius=15, fill="#ff6a00")
                # Centered Header Text
                draw.text((80, 78), main_heading.upper(), fill="#ffffff", font=font_title)
                
                # Dynamic Badges (Rounded Boxes with smooth borders)
                # Badge 1
                draw.rounded_rectangle([(50, 250), (490, 370)], radius=12, fill="#141414", outline="#ff6a00", width=3)
                draw.text((80, 290), final_box1[:22], fill="#ffffff", font=font_badge)
                
                # Badge 2
                draw.rounded_rectangle([(50, 410), (490, 530)], radius=12, fill="#141414", outline="#ff6a00", width=3)
                draw.text((80, 450), final_box2[:22], fill="#ffffff", font=font_badge)
                
                # Bottom Description Paragraph
                clean_text = user_content[:250] + "..." if len(user_content) > 250 else user_content
                
                # Text wrapping helper for descriptions
                lines = []
                words_desc = clean_text.split()
                current_line = ""
                for w in words_desc:
                    test_line = current_line + " " + w if current_line else w
                    if len(test_line) < 45:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = w
                if current_line:
                    lines.append(current_line)
                
                y_offset = 740
                for line in lines[:4]:
                    draw.text((50, y_offset), line, fill="#d1d1d1", font=font_body)
                    y_offset += 35
                
                # Save & Show
                canvas.save("final_premium_post.png")
                st.image("final_premium_post.png", caption="🔥 Aapka Custom Premium Infographic Style Ready Hai!")
                
                with open("final_premium_post.png", "rb") as file:
                    st.download_button(label="Download HD Infographic", data=file, file_name="premium_ecom_infographic.png", mime="image/png")
                    
            except Exception as e:
                st.error(f"Koi masla aya hai: {e}")
