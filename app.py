import streamlit as st
import os
import base64
from dotenv import load_dotenv
from google import genai
from PIL import Image

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Mohale M. Professional", layout="wide", initial_sidebar_state="expanded")

# --- 2. CONVERT WALLPAPER TO BASE64 ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

wallpaper_file = "wallpaper.jpg"
if os.path.exists("wallpaper.png"):
    wallpaper_file = "wallpaper.png"

if os.path.exists(wallpaper_file):
    img_base64 = get_base64_of_bin_file(wallpaper_file)
    bg_css = f"background-image: url('data:image/jpeg;base64,{img_base64}');"
else:
    bg_css = "background-color: #0a1128;"

# --- 3. REAL WALLPAPER BACKGROUND & GOLD FRAME ---
st.markdown(f"""
<style>
    .stApp, [data-testid="stAppViewContainer"] {{
        background: transparent !important;
    }}
    html, body {{
        background-color: #0a1128 !important;
    }}
    .web-bg {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw; 
        height: 100vh;
        z-index: -2;
        {bg_css}
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        pointer-events: none;
    }}
    .gold-frame {{
        position: fixed;
        top: 1rem;
        bottom: 1rem;
        left: 1rem;
        right: 1rem;
        border: 1px solid #cda34f;
        border-radius: 8px;
        pointer-events: none; 
        z-index: 9999;
    }}
</style>
<div class="web-bg"></div>
<div class="gold-frame"></div>
""", unsafe_allow_html=True)

# --- 4. APP STYLING (Sidebar, Chat) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    [data-testid="stHeader"] { display: none !important; }

    .main .block-container {
        padding: 4rem 3rem 8rem 3rem !important;
        max-width: 100% !important;
        background: transparent !important;
    }
    
    /* --- SIDEBAR: DARK GREY --- */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important; 
        border-right: 1px solid #cda34f;
        padding-top: 2rem;
        z-index: 10;
    }
    
    /* General Sidebar Button Styling */
    [data-testid="stSidebar"] button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        padding: 12px 20px !important;
        width: 100% !important;
        display: flex !important;
        justify-content: flex-start !important; /* Forces button content left */
        text-align: left !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background-color: rgba(205, 163, 79, 0.05) !important;
    }

    /* Force text container inside button to align left */
    [data-testid="stSidebar"] button div[data-testid="stMarkdownContainer"] {
        display: flex !important;
        justify-content: flex-start !important;
        width: 100%;
    }

    [data-testid="stSidebar"] button p {
        text-align: left !important;
        justify-content: flex-start !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        font-size: 16px !important;
        margin: 0 !important;
        padding: 0 !important;
        color: #d1d5db !important;
    }

    /* Base icon styling */
    [data-testid="stSidebar"] button p::before {
        font-family: "Font Awesome 6 Free" !important;
        font-weight: 900 !important;
        margin-right: 15px !important;
        font-size: 18px !important;
        color: #a0a0a0;
        width: 20px !important; 
        text-align: center !important;
        display: inline-block !important;
    }

    /* Target specific buttons using nth-child on the main vertical block */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(4) button p::before { content: "\f015"; } /* Dashboard */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(5) button p::before { content: "\f086"; } /* All Chats */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(6) button p::before { content: "\f15c"; } /* Document Analysis */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(7) button p::before { content: "\f133"; } /* Meeting Notes */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(8) button p::before { content: "\f013"; } /* Settings */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(9) button p::before { content: "\f059"; } /* Get Help */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(13) button p::before { content: "\f2f5"; } /* Logout */

    /* --- ACTIVE BUTTON HIGHLIGHT (Dashboard) --- */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(4) button {
        background-color: #2a2a2a !important; 
        border-left: 3px solid #cda34f !important;
    }
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(4) button p {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(4) button p::before {
        color: #cda34f !important;
    }

    /* --- CHAT BAR SURROUNDING AREA --- */
    [data-testid="stBottom"], 
    [data-testid="stBottomBlockContainer"],
    .stChatFloatingInputContainer {
        background-color: #0a1128 !important; 
        background: #0a1128 !important;
        border-top: none !important;
    }

    /* --- CHAT BAR PILL --- */
    [data-testid="stChatInput"] {
        border: 1px solid #cda34f !important;
        border-radius: 50px !important; 
        background-color: #1a1a1a !important; 
        max-width: 85% !important;
        margin: 0 auto 3rem auto !important; 
        padding: 5px 15px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.6);
        z-index: 100;
        display: flex;
        align-items: center;
    }
    
    [data-testid="stChatInput"] > div, 
    [data-testid="stChatInput"] textarea {
        border: none !important;
        background-color: transparent !important;
        color: #ffffff !important;
        margin-top: 5px !important; 
    }

    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='font-family: Cinzel; color: #cda34f; text-align: center; font-size: 60px; margin-bottom: 0;'>MP</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0a0a0; font-size: 13px; margin-top: -10px; font-family: Cinzel; margin-bottom: 30px;'>Mohale M. Professional</p>", unsafe_allow_html=True)
    
    st.button("Dashboard", use_container_width=True)
    st.button("All Chats", use_container_width=True)
    st.button("Document Analysis", use_container_width=True)
    st.button("Meeting Notes", use_container_width=True)
    st.button("Settings", use_container_width=True)
    st.button("Get Help", use_container_width=True)
    
    st.write("<br><br><br>", unsafe_allow_html=True) 
    
    st.markdown("---")
    
    # Custom Profile Section
    st.markdown("""
        <div style="display: flex; align-items: center; padding: 10px 0;">
            <img src="https://i.pravatar.cc/150?img=11" style="border-radius: 50%; width: 35px; height: 35px; margin-right: 15px; border: 1px solid #cda34f;">
            <span style="color: #e0d0b0; font-size: 15px; font-family: 'Inter', sans-serif;">M. Mohale</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.button("Logout", use_container_width=True)

# --- 6. MAIN CONTENT ---
st.markdown("<div class='hero-section'>", unsafe_allow_html=True)

# MIDDLE LOGO
logo_exists = os.path.exists("logo.png")
if logo_exists:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        img = Image.open("logo.png")
        width, height = img.size
        crop_height = int(height * 0.70) 
        cropped_img = img.crop((0, 0, width, crop_height))
        st.image(cropped_img, use_column_width=True)
else:
    st.markdown("<h1 style='font-family: Cinzel; color: #cda34f; font-size: 120px; margin-bottom: 0;'>MP</h1>", unsafe_allow_html=True)

# TEXT BELOW LOGO 
st.markdown("""
        <p style='font-family: "Cinzel", serif; color: #e0d0b0; text-align: center; font-size: 20px; margin-top: 10px;'>Mohale M. Professional</p>
        <br><br>
        <h1 style='font-family: Cinzel; color: #cda34f; font-size: 45px; letter-spacing: 2px; text-align: center; margin-top: 10px;'>HI, I'M MOHALE</h1>
        <p style='color: #a0a0a0; font-size: 16px; text-align: center; margin-bottom: 50px;'>How can I assist you today?</p>
    </div>
""", unsafe_allow_html=True)

# --- 7. CHAT LOGIC ---
load_dotenv()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: Check your API key. Details: {e}")
