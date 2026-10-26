import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Mohale M. Professional", layout="wide", initial_sidebar_state="expanded")

# --- 2. CUSTOM CSS STYLING ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
    /* Main App Background */
    .stApp { 
        background: radial-gradient(circle at center, #111b3a 0%, #050a1f 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Background and Border */
    [data-testid="stSidebar"] {
        background-color: #0a1128 !important;
        border-right: 1px solid #cda34f;
    }
    
    /* Make top header transparent */
    header { background: transparent !important; }
    
    /* --- SIDEBAR BUTTONS FIX --- */
    /* Removes the grey box, shadow, and centers them left */
    [data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;
        color: #a0a0a0 !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        text-align: left !important;
        justify-content: flex-start !important; /* Aligns text to the left */
        padding: 10px 20px !important;
        font-size: 16px !important;
        transition: 0.3s;
        width: 100%;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        color: #cda34f !important;
        background-color: rgba(205, 163, 79, 0.1) !important;
    }
    
    /* The Active Dashboard Button (Gold Left Line) */
    [data-testid="stSidebar"] .stButton:first-child > button {
        border-left: 3px solid #cda34f !important;
        background-color: rgba(205, 163, 79, 0.05) !important;
    }

    /* Main Content Box Border */
    .main-box {
        border: 1px solid #cda34f;
        border-radius: 5px;
        padding: 20px;
        margin: 20px 40px;
        min-height: 80vh;
        position: relative;
    }

    /* Typography */
    .subtitle {
        font-family: 'Cinzel', serif;
        color: #e0d0b0;
        text-align: center;
        font-size: 18px;
        margin-top: -10px;
    }
    
    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 30px;
    }
    
    /* --- THE FINAL LOGO FIX --- */
    /* Inverts white bg to black, makes black transparent, restores gold color */
    [data-testid="stImage"] img {
        mix-blend-mode: screen; 
        filter: invert(1) hue-rotate(180deg) brightness(1.3) contrast(1.2);
    }
    
    /* Chat Input Styling */
    .stChatInput {
        border: 1px solid #cda34f !important;
        border-radius: 30px !important;
        background-color: rgba(20, 30, 60, 0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

# Check if the logo image exists
logo_exists = os.path.exists("logo.png")

# --- 3. SIDEBAR ---
with st.sidebar:
    if logo_exists:
        st.image("logo.png", width=100)
    else:
        st.markdown("<h1 style='font-family: Cinzel; color: #cda34f; text-align: center; font-size: 60px; margin-bottom: 0;'>MP</h1>", unsafe_allow_html=True)
        
    st.markdown("<p style='text-align: center; color: #a0a0a0; font-size: 12px; margin-top: -10px;'>Mohale M. Professional</p>", unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    
    st.button("🏠  Dashboard", use_container_width=True)
    st.button("💬  All Chats", use_container_width=True)
    st.button("📄  Document Analysis", use_container_width=True)
    st.button("📅  Meeting Notes", use_container_width=True)
    st.button("⚙️  Settings", use_container_width=True)
    st.button("❓  Get Help", use_container_width=True)
    
    st.write("<br><br><br><br><br><br>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("👤 **M. Mohale**")
    st.button("🚪  Logout", use_container_width=True)

# --- 4. MAIN CONTENT ---
st.markdown("<div class='main-box'>", unsafe_allow_html=True)
st.markdown("<div class='hero-section'>", unsafe_allow_html=True)

# Center Logo
if logo_exists:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_column_width=True)
else:
    st.markdown("<h1 style='font-family: Cinzel; color: #cda34f; font-size: 120px; margin-bottom: 0;'>MP</h1>", unsafe_allow_html=True)

st.markdown("""
        <p class='subtitle'>Mohale M. Professional</p>
        <br><br>
        <h1 style='font-family: Cinzel; color: #cda34f; font-size: 45px; letter-spacing: 2px; text-align: center;'>HI, I'M MOHALE</h1>
        <p style='color: #a0a0a0; font-size: 16px; text-align: center;'>How can I assist you today?</p>
    </div>
    <br><br><br>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- 5. CHAT LOGIC ---
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
