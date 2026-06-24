import streamlit as st
import os
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Premium AI Post Generator", layout="centered")
st.title("⚡ Autonomous Premium Post Generator")
st.write("Apna content likhein, AI khud reaction image generate karega aur post banayega!")

# User input content
user_content = st.text_area("Post Ka Content Yahan Paste Karein:", 
                            placeholder="Example: Amazon just changed its review management system...")

# Hugging Face Token setup (Streamlit secrets se uthayega)
hf_token = os.environ.get("HF_TOKEN")

if st.button("Generate Premium HD Post"):
    if not user_content:
        st.error("Pehle content to likhein jaanib!")
    elif not hf_token:
        st.error("HF_TOKEN nahi mila! App Settings -> Secrets mein token lagayein.")
    else:
        with st.spinner("AI aapka content samajh raha hai aur image generate kar raha hai... (Isme 20-30 seconds lag sakte hain)"):
            try:
                # 1. Hugging Face Client Initialize karna
                client = InferenceClient(provider="wavespeed", api_key=hf_token)
                
                # 2. Automatically prompt banana content ke hisab se
                ai_prompt = f"An e-commerce professional person looking shocked or giving a heavy reaction, corporate style, high-end commercial photography, cyberpunk lighting, strictly black and neon orange background tone, ultra realistic, studio lighting, matching context: {user_content[:100]}"
                
                # 3. FLUX Model se image generate karna
                reaction_img = client.text_to_image(
                    ai_prompt,
                    model="black-forest-labs/FLUX.1-dev",
                )
                
                # 4. Final Post Layout Design (1080x1080 Instagram/LinkedIn Size)
                # Canvas banana (Black Background)
                canvas = Image.new("RGB", (1080, 1080), "#0d0d0d")
                draw = ImageDraw.Draw(canvas)
                
                # AI ki banayi hui Image ko resize karke right side par set karna
                reaction_resized = reaction_img.resize((500, 700))
                canvas.paste(reaction_resized, (530, 250))
                
                # Top Header Banner (Orange Gradient Block)
                draw.rectangle([(50, 50), (1030, 150)], fill="#ff6a00")
                
                # Header Text
                draw.text((80, 75), "AMAZON CRITICAL UPDATE", fill="#ffffff", font_size=42)
                
                # Content points background badges (Orange outline boxes)
                draw.rectangle([(50, 250), (500, 380)], outline="#ff6a00", width=4)
                draw.text((70, 280), "SYSTEM CHANGED", fill="#ffffff", font_size=28)
                
                draw.rectangle([(50, 420), (500, 550)], outline="#ff6a00", width=4)
                draw.text((70, 450), "ACTION REQUIRED", fill="#ffffff", font_size=28)
                
                # Niche baaki ka bacha hua text draw karna
                clean_text = user_content[:200] + "..." if len(user_content) > 200 else user_content
                draw.text((50, 750), clean_text, fill="#aaaaaa", font_size=24)
                
                # Output Save karna
                canvas.save("final_premium_post.png")
                
                # Screen par dikhana
                st.image("final_premium_post.png", caption="Aapki AI-Generated Post Ready Hai!")
                
                # Download Button
                with open("final_premium_post.png", "rb") as file:
                    st.download_button(
                        label="Download Premium Post",
                        data=file,
                        file_name="premium_ai_post.png",
                        mime="image/png"
                    )
                    
            except Exception as e:
                st.error(f"Post banane mein koi rola aaya hai: {e}")
