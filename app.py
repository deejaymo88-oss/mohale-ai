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
    /* 1. Base Background */
    .stApp { 
        background-color: #0a1128;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit's top bar completely */
    [data-testid="stHeader"] { display: none !important; }

    /* 2. THE LOCKED GOLD FRAME */
    /* This fixes the border to the screen so it NEVER moves */
    .main {
        border: 1px solid #cda34f;
        border-radius: 8px;
        
        /* Lock the height and margins */
        height: calc(100vh - 2rem); 
        margin-top: 1rem;
        margin-bottom: 1rem;
        margin-right: 1rem;
        margin-left: 1rem;
        overflow: hidden; /* Stops the whole page from scrolling */
        
        /* The subtle background glow inside the frame */
        background: radial-gradient(circle at 50% 30%, #152244 0%, #0a1128 70%);
    }
    
    /* 3. THE INNER SCROLLING AREA */
    /* Only the content inside the frame scrolls */
    .main .block-container {
        height: 100%;
        overflow-y: auto; 
        padding: 2rem 3rem 8rem 3rem !important;
        max-width: 100% !important;
    }
    
    /* 4. SIDEBAR (Matches the dark blue background) */
    [data-testid="stSidebar"] {
        background-color: #0a1128 !important;
        border-right: 1px solid #cda34f;
        padding-top: 2rem;
    }
    
    /* Sidebar Buttons */
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
    
    /* 5. CROP THE TEXT OUT OF THE LOGO IMAGE */
    .main [data-testid="stImage"] img {
        clip-path: inset(0 0 28% 0); /* Chops off the bottom text */
        margin-bottom: -24%; /* Pulls the new text up perfectly */
    }
    
    /* 6. THE STICKY PILL CHAT BAR */
    [data-testid="stChatInput"] {
        position: sticky;
        bottom: 2rem; /* Sticks to the bottom of the frame */
        border: 1px solid #cda34f !important;
        border-radius: 50px !important; /* Perfect Pill Shape */
        background-color: rgba(10, 17, 40, 0.95) !important;
        max-width: 85% !important;
        margin: 0 auto !important;
        padding: 5px 15px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.6);
        z-index: 100;
    }
    
    /* Removes Streamlit's inner box borders so the pill looks smooth */
    [data-testid="stChatInput"] > div {
        border: none !important;
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Check if the logo image exists
logo_exists = os.path.exists("logo.png")

# --- 3. SIDEBAR ---
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

# --- 4. MAIN CONTENT ---
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
        <p style='font-family: "Cinzel", serif; color: #e0d0b0; text-align: center; font-size: 20px; margin-top: 5px;'>Mohale M. Professional</p>
        <br><br>
        <h1 style='font-family: Cinzel; color: #cda34f; font-size: 45px; letter-spacing: 2px; text-align: center; margin-top: 10px;'>HI, I'M MOHALE</h1>
        <p style='color: #a0a0a0; font-size: 16px; text-align: center; margin-bottom: 50px;'>How can I assist you today?</p>
    </div>
""", unsafe_allow_html=True)

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
