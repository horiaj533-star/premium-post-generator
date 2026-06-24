import streamlit as st
import os
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Premium AI Post Generator", layout="centered")
st.title("⚡ Autonomous Premium Post Generator v2")
st.write("Apna content dalein, system automatic text points aur dynamic reaction set karega!")

# 1. Inputs
user_content = st.text_area("Post Ka Content Yahan Paste Karein:", 
                            placeholder="Example: Amazon just changed its review management system...")

main_heading = st.text_input("Main Heading (Optional):", "AMAZON CRITICAL UPDATE")
box1_text = st.text_input("Box 1 Text (Optional - Auto generated if empty):", "")
box2_text = st.text_input("Box 2 Text (Optional - Auto generated if empty):", "")

# Hugging Face Token setup
hf_token = os.environ.get("HF_TOKEN")

if st.button("Generate Premium HD Post"):
    if not user_content:
        st.error("Pehle content to likhein jaanib!")
    elif not hf_token:
        st.error("HF_TOKEN missing in Secrets!")
    else:
        with st.spinner("AI Analysis aur Image Generation jari hai..."):
            try:
                client = InferenceClient(provider="wavespeed", api_key=hf_token)
                
                # Dynamic text handling (Agar user ne khud nahi likha to content se uthaye)
                final_box1 = box1_text if box1_text else "ALERT DETECTED"
                final_box2 = box2_text if box2_text else "ACTION REQUIRED"
                
                if not box1_text or not box2_text:
                    # Content ke shuruati lafz utha kar dabba text dynamic banana
                    words = user_content.split()
                    if len(words) >= 4:
                        final_box1 = " ".join(words[:2]).upper()
                        final_box2 = " ".join(words[2:5]).upper()

                # Tight Prompting for exact thematic look
                ai_prompt = f"An e-commerce digital strategist professional man, dynamic facial expression matching this context: {user_content[:60]}, high-end commercial tech portrait, cinematic studio lighting, dark charcoal background with sharp neon orange accents, ultra-detailed 8k, photorealistic."
                
                # FLUX Image generation
                reaction_img = client.text_to_image(ai_prompt, model="black-forest-labs/FLUX.1-dev")
                
                # Canvas Creation
                canvas = Image.new("RGB", (1080, 1080), "#0d0d0d")
                draw = ImageDraw.Draw(canvas)
                
                # Paste Generated Image
                reaction_resized = reaction_img.resize((520, 720))
                canvas.paste(reaction_resized, (520, 230))
                
                # Header
                draw.rectangle([(50, 50), (1030, 160)], fill="#ff6a00")
                draw.text((80, 80), main_heading.upper(), fill="#ffffff", font_size=40)
                
                # Dynamic Badges
                draw.rectangle([(50, 250), (480, 380)], outline="#ff6a00", width=4)
                draw.text((70, 290), final_box1[:20], fill="#ffffff", font_size=24)
                
                draw.rectangle([(50, 420), (480, 550)], outline="#ff6a00", width=4)
                draw.text((70, 460), final_box2[:20], fill="#ffffff", font_size=24)
                
                # Bottom Description
                clean_text = user_content[:250] + "..." if len(user_content) > 250 else user_content
                draw.text((50, 780), clean_text, fill="#bbbbbb", font_size=22)
                
                # Save & Display
                canvas.save("final_premium_post.png")
                st.image("final_premium_post.png", caption="Aapki Customized AI Post!")
                
                with open("final_premium_post.png", "rb") as file:
                    st.download_button(label="Download Premium Post", data=file, file_name="premium_ai_post.png", mime="image/png")
                    
            except Exception as e:
                st.error(f"Error: {e}")
