import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Mohale M. Professional", layout="wide", initial_sidebar_state="expanded")

# --- 2. INJECT THE FIXED WEB BACKGROUND ---
# This creates an absolute layer behind everything that cannot be covered by Streamlit's default colors
st.markdown("""
<style>
    /* Force all Streamlit containers to be transparent */
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* The fixed background web layer */
    .web-bg {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 150vw; /* Huge to cover wide screens */
        height: 150vw;
        z-index: -1; /* Puts it behind everything */
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1000 1000'%3E%3Cg stroke='%23cda34f' stroke-width='1.5' fill='none' opacity='0.2'%3E%3Ccircle cx='500' cy='500' r='100'/%3E%3Ccircle cx='500' cy='500' r='200'/%3E%3Ccircle cx='500' cy='500' r='300'/%3E%3Ccircle cx='500' cy='500' r='400'/%3E%3Ccircle cx='500' cy='500' r='500'/%3E%3Ccircle cx='500' cy='500' r='600'/%3E%3Ccircle cx='500' cy='500' r='700'/%3E%3Cline x1='500' y1='-100' x2='500' y2='1100'/%3E%3Cline x1='-100' y1='500' x2='1100' y2='500'/%3E%3Cline x1='75' y1='75' x2='925' y2='925'/%3E%3Cline x1='925' y1='75' x2='75' y2='925'/%3E%3Cline x1='200' y1='0' x2='800' y2='1000'/%3E%3Cline x1='800' y1='0' x2='200' y2='1000'/%3E%3Cline x1='0' y1='200' x2='1000' y2='800'/%3E%3Cline x1='0' y1='800' x2='1000' y2='200'/%3E%3C/g%3E%3C/svg%3E");
        background-size: cover;
        background-position: center;
        pointer-events: none;
    }
</style>
<div class="web-bg"></div>
""", unsafe_allow_html=True)

# --- 3. MAIN APP STYLING (Locked Frame, Sidebar, etc.) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
    /* Dark blue base */
    .stApp { background-color: #0a1128; font-family: 'Inter', sans-serif; }
    
    /* Hide Streamlit's default top bar */
    [data-testid="stHeader"] { display: none !important; }

    /* --- THE LOCKED GOLD FRAME --- */
    .main {
        border: 1px solid #cda34f;
        border-radius: 8px;
        height: calc(100vh - 2rem); 
        margin: 1rem;
        overflow: hidden; 
        position: relative;
    }
    
    /* Inner scrolling area */
    .main .block-container {
        height: 100%;
        overflow-y: auto; 
        padding: 3rem 3rem 8rem 3rem !important;
        max-width: 100% !important;
    }
    
    /* Sidebar Background and Border */
    [data-testid="stSidebar"] {
        background-color: #0a1128 !important;
        border-right: 1px solid #cda34f;
        padding-top: 2rem;
    }
    
    /* --- SIDEBAR BUTTONS --- */
    [data-testid="stSidebar"] button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        color: #a0a0a0 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        width: 100%;
    }
    
    [data-testid="stSidebar"] button:hover {
        color: #cda34f !important;
        background-color: rgba(205, 163, 79, 0.1) !important;
    }
    
    [data-testid="stSidebar"] button p {
        text-align: left !important;
        justify-content: flex-start !important;
    }

    /* Active Dashboard Button */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:first-child button {
        border-left: 3px solid #cda34f !important;
        background-color: rgba(205, 163, 79, 0.05) !important;
        color: #cda34f !important;
    }

    /* Typography */
    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
    }
    
    /* --- CROP THE TEXT OUT OF THE LOGO IMAGE --- */
    .main [data-testid="stImage"] img {
        clip-path: inset(0 0 32% 0) !important; 
        margin-bottom: -30% !important; 
    }
    
    /* --- THE PERFECT PILL CHAT BAR --- */
    [data-testid="stChatInput"] {
        position: sticky;
        bottom: 2rem;
        border: 1px solid #cda34f !important;
        border-radius: 50px !important; 
        background-color: rgba(10, 17, 40, 0.95) !important;
        max-width: 85% !important;
        margin: 0 auto !important;
        padding: 5px 15px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.6);
        z-index: 100;
    }
    
    [data-testid="stChatInput"] > div {
        border: none !important;
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Check if the logo image exists
logo_exists = os.path.exists("logo.png")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='font-family: Cinzel; color: #cda34f; text-align: center; font-size: 60px; margin-bottom: 0;'>MP</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0a0a0; font-size: 13px; margin-top: -10px; font-family: Cinzel;'>Mohale M. Professional</p>", unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    
    st.button("🏠  Dashboard", use_container_width=True)
    st.button("💬  All Chats", use_container_width=True)
    st.button("📄  Document Analysis", use_container_width=True)
    st.button("📅  Meeting Notes", use_container_width=True)
    st.button("⚙️  Settings", use_container_width=True)
    st.button("❓  Get Help", use_container_width=True)
    
    st.write("<br><br><br>", unsafe_allow_html=True) 
    
    st.markdown("---")
    st.markdown("👤 **M. Mohale**")
    st.button("🚪  Logout", use_container_width=True)

# --- 5. MAIN CONTENT ---
st.markdown("<div class='hero-section'>", unsafe_allow_html=True)

# MIDDLE LOGO
if logo_exists:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_column_width=True)
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

# --- 6. CHAT LOGIC ---
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
