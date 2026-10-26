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
    
    header { background: transparent !important; }
    
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

    /* The Active Dashboard Button (Gold Line) */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:first-child button {
        border-left: 3px solid #cda34f !important;
        background-color: rgba(205, 163, 79, 0.05) !important;
        color: #cda34f !important;
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
    
    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 30px;
    }
    
    /* --- THE TRICK TO CROP THE TEXT OUT OF THE IMAGE & FIX SPACING --- */
    .main [data-testid="stImage"] img {
        clip-path: inset(0 0 25% 0); /* Crops the bottom text baked into the image */
        margin-bottom: -20%; /* Pulls the title closer to fix the gap */
    }
    
    /* Chat Input Styling */
    .stChatInput {
        border: 1px solid #cda34f !important;
        border-radius: 30px !important;
        background-color: rgba(20, 30, 60, 0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

# Check if the logo image exists for the middle
logo_exists = os.path.exists("logo.png")

# --- 3. SIDEBAR ---
with st.sidebar:
    # Sidebar Logo Text
    st.markdown("<h1 style='font-family: Cinzel; color: #cda34f; text-align: center; font-size: 60px; margin-bottom: 0; padding-top: 20px;'>MP</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0a0a0; font-size: 13px; margin-top: -10px; font-family: Cinzel;'>Mohale M. Professional</p>", unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    
    # Menu Items
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

# MIDDLE LOGO
if logo_exists:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_column_width=True)
else:
    # Fallback if image is missing
    st.markdown("<h1 style='font-family: Cinzel; color: #cda34f; font-size: 120px; margin-bottom: 0;'>MP</h1>", unsafe_allow_html=True)

# MAIN TITLE (The extra "Mohale M. Professional" is now completely removed here)
st.markdown("""
        <h1 style='font-family: Cinzel; color: #cda34f; font-size: 45px; letter-spacing: 2px; text-align: center; margin-top: 20px;'>HI, I'M MOHALE</h1>
        <p style='color: #a0a0a0; font-size: 16px; text-align: center; margin-bottom: 50px;'>How can I assist you today?</p>
    </div>
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
