
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="Custom Post Generator", layout="centered")
st.title("⚡ Premium Post Generator")
st.write("Apna content likhein aur baghair watermark ke HD image banayein.")

# Inputs
user_content = st.text_area("Post Ka Content Yahan Paste Karein:", placeholder="Yahan apna text likhein...", height=150)

if st.button("Generate HD Post", type="primary"):
    if user_content:
        # Create a premium dark canvas (1080x1080)
        canvas_width, canvas_height = 1080, 1080
        background_color = "#0B0C10"  # Luxury Dark Theme
        image = Image.new("RGB", (canvas_width, canvas_height), background_color)
        draw = ImageDraw.Draw(image)
        
        # Simple default font handling
        try:
            font = ImageFont.truetype("arial.ttf", 45)
        except:
            font = ImageFont.load_default()
            
        # Text settings
        text_color = "#FFFFFF" # Clean White
        text_position = (100, 300)
        
        # Draw text on image
        draw.text(text_position, user_content, font=font, fill=text_color, spacing=20)
        
        # Display image
        st.image(image, caption="Aapki Post Ready Hai!", use_column_width=True)
        
        # Save and Download button
        image.save("output_post.png", quality=100)
        with open("output_post.png", "rb") as file:
            st.download_button(label="📥 Download HD Image", data=file, file_name="premium_post.png", mime="image/png")
    else:
        st.warning("Meharbani karke pehle kuch content likhein!")
