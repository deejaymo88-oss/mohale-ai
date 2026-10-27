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

# --- 4. APP STYLING (Custom HTML Sidebar, Chat) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
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
    }
    
    /* Hide the default Streamlit sidebar toggle and padding */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
        height: 100vh;
        position: relative;
    }

    /* --- CUSTOM HTML MENU STYLING --- */
    .sidebar-menu {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    
    .menu-item {
        display: flex;
        align-items: center;
        padding: 12px 20px;
        cursor: pointer;
        color: #d1d5db;
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        transition: 0.3s;
    }
    
    .menu-item:hover {
        color: #cda34f;
        background-color: rgba(205, 163, 79, 0.05);
    }
    
    /* Active State */
    .menu-item.active {
        background-color: #2a2a2a;
        border-left: 3px solid #cda34f;
        color: #ffffff;
    }
    
    .menu-item.active svg {
        stroke: #cda34f;
    }

    /* Icons */
    .menu-icon {
        width: 20px;
        height: 20px;
        margin-right: 15px;
        stroke: #a0a0a0;
        stroke-width: 2;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    /* --- CHAT BAR SURROUNDING AREA --- */
    [data-testid="stBottom"], 
    [data-testid="stBottomBlockContainer"],
    .stChatFloatingInputContainer {
        background-color: #0a1128 !important; 
        background: #0a1128 !important;
        border-top: none !important;
    }

    /* --- CHAT BAR PILL (Dark Grey Inside) --- */
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

# --- 5. CUSTOM SIDEBAR (HTML) ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style='font-family: Cinzel; color: #cda34f; font-size: 60px; margin-bottom: 0;'>MP</h1>
        <p style='color: #a0a0a0; font-size: 13px; margin-top: -10px; font-family: Cinzel;'>Mohale M. Professional</p>
    </div>

    <div class="sidebar-menu">
        <!-- Dashboard (Active) -->
        <div class="menu-item active">
            <svg class="menu-icon" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            Dashboard
        </div>
        
        <!-- All Chats -->
        <div class="menu-item">
            <svg class="menu-icon" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
            All Chats
        </div>
        
        <!-- Document Analysis -->
        <div class="menu-item">
            <svg class="menu-icon" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            Document Analysis
        </div>
        
        <!-- Meeting Notes -->
        <div class="menu-item">
            <svg class="menu-icon" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            Meeting Notes
        </div>
        
        <!-- Settings -->
        <div class="menu-item">
            <svg class="menu-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
            Settings
        </div>
        
        <!-- Get Help -->
        <div class="menu-item">
            <svg class="menu-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            Get Help
        </div>
    </div>

    <!-- Bottom Profile Section -->
    <div style="position: absolute; bottom: 20px; width: 100%; left: 0;">
        <hr style="border-color: #333; margin: 0 20px 15px 20px;">
        <div style="display: flex; align-items: center; padding: 10px 20px; margin-bottom: 5px;">
            <img src="https://i.pravatar.cc/150?img=11" style="border-radius: 50%; width: 35px; height: 35px; margin-right: 15px; border: 1px solid #cda34f;">
            <span style="color: #e0d0b0; font-size: 15px; font-family: 'Inter', sans-serif;">M. Mohale</span>
        </div>
        <div class="menu-item">
            <svg class="menu-icon" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
            Logout
        </div>
    </div>
    """, unsafe_allow_html=True)

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
