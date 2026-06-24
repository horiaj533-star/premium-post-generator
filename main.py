import streamlit as st
import os
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw

st.set_page_config(page_title="Premium AI Post Generator", layout="centered")
st.title("⚡ 100% Free Autonomous Post Generator")
st.write("Apna content likhein, AI background generate karega aur aapki photo khud set karega!")

# 1. User inputs
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
        with st.spinner("AI Background aur Text points generate ho rahe hain..."):
            try:
                client = InferenceClient(provider="wavespeed", api_key=hf_token)
                
                # Dynamic text management (Agar khaali ho to content ke shuruati lafz uthaye)
                final_box1 = box1_text if box1_text else "ALERT DETECTED"
                final_box2 = box2_text if box2_text else "ACTION REQUIRED"
                
                if not box1_text or not box2_text:
                    words = user_content.split()
                    if len(words) >= 4:
                        final_box1 = " ".join(words[:2]).upper()
                        final_box2 = " ".join(words[2:5]).upper()

                # AI ko bol rahe hain ke content ke mutabik background element banaye
                ai_prompt = f"Abstract premium tech background, cyberpunk style, dark charcoal background with sharp neon orange lighting, futuristic data analytics charts or broken Amazon boxes blending in dark mist, ultra-detailed 8k, product design stage tone, matching context: {user_content[:60]}"
                
                # FLUX se dynamic background image lena
                bg_img = client.text_to_image(ai_prompt, model="black-forest-labs/FLUX.1-dev")
                bg_resized = bg_img.resize((520, 720))
                
                # Main 1080x1080 Canvas (Black Theme)
                canvas = Image.new("RGB", (1080, 1080), "#0d0d0d")
                draw = ImageDraw.Draw(canvas)
                
                # AI ka banaya hua background right side par lagana
                canvas.paste(bg_resized, (520, 230))
                
                # --- AAPKI PHOTO INTEGRATION (Aapki Image Ka Exact Naam) ---
                image_name = "Abdullah_Gull_Amazon_Expert.jpg-removebg-preview.png"
                
                if os.path.exists(image_name):
                    user_face = Image.open(image_name).convert("RGBA")
                    # Aapki photo ko scale karna taakay background par fit baithe
                    user_face.thumbnail((450, 650))
                    # Photo ko AI background ke upar blend karna
                    canvas.paste(user_face, (550, 300), user_face)
                else:
                    # Agar photo nahi mili to error show karega
                    draw.rectangle([(550, 300), (950, 800)], outline="#ff6a00", width=2)
                    draw.text((560, 500), "Image Not Found In GitHub!", fill="#ff0000", font_size=24)
                
                # --- DESIGN LAYOUT (Orange & Black) ---
                # Top Header
                draw.rectangle([(50, 50), (1030, 160)], fill="#ff6a00")
                draw.text((80, 80), main_heading.upper(), fill="#ffffff", font_size=40)
                
                # Dynamic Side Badges (Content ke mutabik)
                draw.rectangle([(50, 250), (480, 380)], outline="#ff6a00", width=4)
                draw.text((70, 290), final_box1[:20], fill="#ffffff", font_size=24)
                
                draw.rectangle([(50, 420), (480, 550)], outline="#ff6a00", width=4)
                draw.text((70, 460), final_box2[:20], fill="#ffffff", font_size=24)
                
                # Bottom Content Description
                clean_text = user_content[:250] + "..." if len(user_content) > 250 else user_content
                draw.text((50, 780), clean_text, fill="#bbbbbb", font_size=22)
                
                # Save & Show
                canvas.save("final_free_post.png")
                st.image("final_free_post.png", caption="Aapki Customized 100% Free AI Post Ready Hai!")
                
                with open("final_free_post.png", "rb") as file:
                    st.download_button(label="Download HD Post", data=file, file_name="premium_free_post.png", mime="image/png")
                    
            except Exception as e:
                st.error(f"Koi rola aya hai: {e}")
