import streamlit as st
import os

st.set_page_config(page_title="Premium Post Architect", layout="centered")

st.title("⚡ Premium HTML/CSS Post Architect")
st.write("Apna content likhein, system instantly ek modern high-end web graphic card ready karega!")

# Inputs
user_content = st.text_area("Post Ka Content Yahan Paste Karein:", 
                            placeholder="Example: Amazon just changed its review management system...")

main_heading = st.text_input("Main Heading:", "AMAZON CRITICAL UPDATE")
box1_text = st.text_input("Box 1 Text (Chota Text):", "ALERT DETECTED")
box2_text = st.text_input("Box 2 Text (Chota Text):", "ACTION REQUIRED")

# Image check from GitHub
image_name = "Abdullah_Gull_Amazon_Expert.jpg-removebg-preview.png"
image_url = ""

# Streamlit mein local image ko HTML mein use karne ka jugaar
if os.path.exists(image_name):
    # Image available hai
    st.sidebar.success("Aapki photo repository mein active hai!")
else:
    st.sidebar.warning("Photo missing hai, check repository.")

if st.button("Generate Premium Post Card"):
    if not user_content:
        st.error("Pehle content to likhein jaanib!")
    else:
        # Dynamic text handling for boxes if empty
        b1 = box1_text if box1_text else "SYSTEM UPDATE"
        b2 = box2_text if box2_text else "CRITICAL CHANGE"
        
        # HTML/CSS Code for the Premium Card
        html_code = f"""
        <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@600&family=Plus+Jakarta+Sans:wght@400;600&display=swap" rel="stylesheet">
        
        <style>
            .post-card {{
                width: 100%;
                max-width: 600px;
                background: #0d0d0d;
                border: 2px solid #1a1a1a;
                border-radius: 24px;
                padding: 35px;
                font-family: 'Plus Jakarta Sans', sans-serif;
                color: #ffffff;
                box-shadow: 0px 20px 40px rgba(0,0,0,0.5);
                margin: 0 auto;
                position: relative;
                overflow: hidden;
            }}
            .header-banner {{
                background: linear-gradient(135deg, #ff6a00, #e65c00);
                padding: 18px 25px;
                border-radius: 16px;
                font-family: 'Oswald', sans-serif;
                font-size: 28px;
                letter-spacing: 1px;
                text-transform: uppercase;
                margin-bottom: 30px;
                box-shadow: 0 4px 15px rgba(255, 106, 0, 0.3);
            }}
            .main-body {{
                display: flex;
                gap: 20px;
                align-items: flex-start;
            }}
            .left-column {{
                flex: 1.1;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }}
            .badge-box {{
                background: #141414;
                border: 2px solid #ff6a00;
                border-radius: 14px;
                padding: 15px;
                font-family: 'Oswald', sans-serif;
                font-size: 16px;
                color: #ffffff;
                letter-spacing: 0.5px;
                text-transform: uppercase;
                box-shadow: inset 0 0 10px rgba(255,106,0,0.1);
            }}
            .right-column {{
                flex: 0.9;
                text-align: right;
                position: relative;
            }}
            .avatar-bg {{
                background: radial-gradient(circle, rgba(255,106,0,0.15) 0%, rgba(0,0,0,0) 70%);
                border-radius: 50%;
                position: absolute;
                width: 250px;
                height: 250px;
                right: -20px;
                top: -20px;
                z-index: 1;
            }}
            .user-avatar {{
                width: 100%;
                max-width: 220px;
                height: auto;
                position: relative;
                z-index: 2;
                filter: drop-shadow(0px 10px 20px rgba(255,106,0,0.2));
            }}
            .description {{
                margin-top: 30px;
                font-size: 15px;
                line-height: 1.6;
                color: #b3b3b3;
                border-top: 1px solid #222;
                padding-top: 20px;
            }}
        </style>
        
        <div class="post-card">
            <div class="header-banner">{main_heading}</div>
            
            <div class="main-body">
                <div class="left-column">
                    <div class="badge-box">⚠️ {b1}</div>
                    <div class="badge-box">🔥 {b2}</div>
                </div>
                
                <div class="right-column">
                    <div class="avatar-bg"></div>
                    <!-- Streamlit local image render logic -->
                    <img class="user-avatar" src="app/static/{image_name}" onerror="this.src='https://via.placeholder.com/220x280/141414/ff6a00?text=Abdullah+Gull'">
                </div>
            </div>
            
            <div class="description">
                {user_content}
            </div>
        </div>
        """
        
        # Displaying HTML in Streamlit cleanly
        st.components.v1.html(html_code, height=600, scrolling=False)
