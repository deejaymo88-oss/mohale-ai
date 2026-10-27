import streamlit as st
import os
import base64
import re
import time
import requests
from dotenv import load_dotenv
from PIL import Image
# Load environment variables
load_dotenv()

# --- 2. ROUTING LOGIC ---
page = st.query_params.get("page", "dashboard")

# --- 3. CONVERT WALLPAPER TO BASE64 ---
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

# --- 4. REAL WALLPAPER BACKGROUND & GOLD FRAME ---
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

# --- 5. APP STYLING ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
    [data-testid="stHeader"] { display: none !important; }

    .main .block-container {
        padding: 4rem 3rem 8rem 3rem !important;
        max-width: 100% !important;
        background: transparent !important;
    }
    
    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important; 
        border-right: 1px solid #cda34f;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        height: 100vh;
        padding-top: 2rem;
        display: flex;
        flex-direction: column;
    }

    .sidebar-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        min-height: 85vh; 
    }
    
    .sidebar-menu {
        display: flex;
        flex-direction: column;
        flex-grow: 1; 
    }
    
    .sidebar-footer {
        margin-top: auto; 
        padding-bottom: 20px;
    }

    .menu-item {
        display: flex;
        align-items: center;
        padding: 12px 20px;
        margin-bottom: 5px;
        cursor: pointer;
        color: #d1d5db;
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        text-decoration: none !important; 
        transition: 0.3s;
        white-space: nowrap;
    }
    
    .menu-item:hover {
        color: #cda34f;
        background-color: rgba(205, 163, 79, 0.05);
    }
    
    .menu-item.active {
        background-color: #2a2a2a;
        border-left: 3px solid #cda34f;
        color: #ffffff;
    }
    .menu-item.active svg { stroke: #cda34f; }

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

    /* --- CHAT BAR --- */
    [data-testid="stBottom"], 
    [data-testid="stBottomBlockContainer"],
    .stChatFloatingInputContainer {
        background-color: #0a1128 !important; 
        background: #0a1128 !important;
        border-top: none !important;
    }

    [data-testid="stChatInput"] {
        border: 1px solid #cda34f !important;
        border-radius: 50px !important; 
        background-color: #1a1a1a !important; 
        width: 85% !important; 
        margin: 0 auto 3rem auto !important; 
        padding: 5px 15px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.6);
        z-index: 100;
    }

    [data-testid="stChatInput"] > div {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important; 
        width: 100% !important;
        background-color: transparent !important;
        border: none !important;
    }

    [data-testid="stChatInput"] textarea {
        flex-grow: 1 !important; 
        text-align: left !important; 
        border: none !important;
        background-color: transparent !important;
        color: #ffffff !important;
        padding-left: 10px !important;
    }

    [data-testid="stChatInput"] button {
        color: #cda34f !important; 
        background-color: transparent !important;
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

# --- 6. CUSTOM SIDEBAR (HTML) ---
raw_html = f"""
<div class="sidebar-container">
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style='font-family: Cinzel; color: #cda34f; font-size: 60px; margin-bottom: 0;'>MP</h1>
        <p style='color: #a0a0a0; font-size: 13px; margin-top: -10px; font-family: Cinzel;'>Mohale M. Professional</p>
    </div>
    
    <div class="sidebar-menu">
        <a href="?page=dashboard" target="_self" class="menu-item {'active' if page == 'dashboard' else ''}">
            <svg class="menu-icon" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            Dashboard
        </a>
        <a href="?page=chats" target="_self" class="menu-item {'active' if page == 'chats' else ''}">
            <svg class="menu-icon" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
            All Chats
        </a>
        <a href="?page=document" target="_self" class="menu-item {'active' if page == 'document' else ''}">
            <svg class="menu-icon" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            Document Analysis
        </a>
        <a href="?page=meeting" target="_self" class="menu-item {'active' if page == 'meeting' else ''}">
            <svg class="menu-icon" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            Meeting Notes
        </a>
        <a href="?page=settings" target="_self" class="menu-item {'active' if page == 'settings' else ''}">
            <svg class="menu-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
            Settings
        </a>
        <a href="?page=help" target="_self" class="menu-item {'active' if page == 'help' else ''}">
            <svg class="menu-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            Get Help
        </a>
    </div>

    <div class="sidebar-footer">
        <hr style="border-color: #333; margin: 0 20px 15px 20px;">
        <div style="display: flex; align-items: center; padding: 10px 20px; margin-bottom: 5px;">
            <img src="https://i.pravatar.cc/150?img=11" style="border-radius: 50%; width: 35px; height: 35px; margin-right: 15px; border: 1px solid #cda34f;">
            <span style="color: #e0d0b0; font-size: 15px; font-family: 'Inter', sans-serif;">M. Mohale</span>
        </div>
        <a href="?page=logout" target="_self" class="menu-item">
            <svg class="menu-icon" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
            Logout
        </a>
    </div>
</div>
"""

clean_html = re.sub(r'\n\s*', '', raw_html)

with st.sidebar:
    st.markdown(clean_html, unsafe_allow_html=True)

# --- 7. MAIN CONTENT ROUTING ---
if page == "dashboard":
    st.markdown("<div class='hero-section'>", unsafe_allow_html=True)
    
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

    st.markdown("""
            <div style='text-align: center; margin-top: 20px;'>
                <p style='font-family: "Cinzel", serif; color: #e0d0b0; font-size: 20px;'>Mohale M. Professional</p>
                <br>
                <h1 style='font-family: Cinzel; color: #cda34f; font-size: 45px; letter-spacing: 2px;'>HI, I'M MOHALE</h1>
                <p style='color: #a0a0a0; font-size: 16px; margin-bottom: 50px;'>How can I assist you today?</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif page == "chats":
    st.markdown("<h1 style='color: white; font-family: Cinzel; text-align: center; margin-top: 50px;'>All Chats</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; text-align: center;'>Your chat history will appear here.</p>", unsafe_allow_html=True)

elif page == "document":
    st.markdown("<h1 style='color: white; font-family: Cinzel; text-align: center; margin-top: 50px;'>Document Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; text-align: center;'>Upload a document to get started.</p>", unsafe_allow_html=True)

elif page == "meeting":
    st.markdown("<h1 style='color: white; font-family: Cinzel; text-align: center; margin-top: 50px;'>Meeting Notes</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; text-align: center;'>Take and review your meeting notes here.</p>", unsafe_allow_html=True)

elif page == "settings":
    st.markdown("<h1 style='color: white; font-family: Cinzel; text-align: center; margin-top: 50px;'>Settings</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; text-align: center;'>Adjust your application preferences here.</p>", unsafe_allow_html=True)

elif page == "help":
    st.markdown("<h1 style='color: white; font-family: Cinzel; text-align: center; margin-top: 50px;'>Get Help</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; text-align: center;'>How can we help you today?</p>", unsafe_allow_html=True)

elif page == "logout":
    st.markdown("<h1 style='color: white; font-family: Cinzel; text-align: center; margin-top: 50px;'>Logged Out</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; text-align: center;'>You have been logged out.</p>", unsafe_allow_html=True)


# --- 8. DIRECT REST API CHAT LOGIC (NO HANGING) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_ai_response(api_key, user_text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    payload = {
        "contents": [{
            "parts": [{"text": user_text}]
        }]
    }

    # Try up to 3 times if Google's servers are busy
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            response_data = response.json()

            if "candidates" in response_data:
                return response_data["candidates"][0]["content"]["parts"][0]["text"]
            
            # If Google is busy (503), wait 2 seconds and retry
            if response.status_code == 503:
                if attempt < 2:
                    time.sleep(2)
                    continue
                else:
                    return "Google's servers are super busy right now. Please wait a minute and try again."
            
            return f"API Error: {response_data}"
            
        except requests.exceptions.Timeout:
            return "Timeout error: Google's servers took too long to respond."
        except Exception as e:
            return f"Connection Error: {str(e)}"

if prompt := st.chat_input("Ask anything...", accept_file=True):
    
    text_input = prompt.text if prompt.text else ""
    uploaded_files = prompt.files
    
    st.session_state.messages.append({"role": "user", "content": text_input})
    with st.chat_message("user"):
        st.markdown(text_input)
        if uploaded_files:
            for file in uploaded_files:
                st.info(f"📎 Attached File: {file.name}")

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if uploaded_files:
                file_names = ", ".join([f.name for f in uploaded_files])
                response_text = f"I see you uploaded: **{file_names}**! I am currently configured to just read text, but soon you will be able to analyze documents right here."
            else:
                api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
                
                if not api_key:
                    response_text = "Error: No API key found. Please check your Streamlit Secrets."
                else:
                    response_text = get_ai_response(api_key, text_input)
            
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
