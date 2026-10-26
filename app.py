import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Mohale M. Professional", layout="wide", initial_sidebar_state="expanded")

# --- 2. CUSTOM CSS STYLING (The Look) ---
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #0A1128; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0A1128;
        border-right: 1px solid #D4AF37;
    }
    
    /* Hide standard Streamlit elements for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Buttons */
    .stButton>button {
        background-color: transparent;
        color: #A0A0A0;
        border: none;
        text-align: left;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        color: #D4AF37;
        background-color: #111B3A;
    }
    
    /* Gold Typography */
    h1, h2, h3, .gold-text { color: #D4AF37 !important; }
    .white-text { color: #F8F9FA !important; }
    
    /* Center the greeting */
    .center-hero { text-align: center; padding-top: 50px; }
    
    /* Chat Input box */
    .stChatInput { border: 1px solid #D4AF37; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (Left Menu) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 60px; margin-bottom: 0;'>MP</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #D4AF37; font-size: 12px;'>Mohale M. Professional</p>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    st.button("🏠 Dashboard", use_container_width=True)
    st.button("💬 All Chats", use_container_width=True)
    st.button("📄 Document Analysis", use_container_width=True)
    st.button("📅 Meeting Notes", use_container_width=True)
    st.button("⚙️ Settings", use_container_width=True)
    st.button("❓ Get Help", use_container_width=True)
    
    st.write("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("👤 **M. Mohale**")
    st.button("Logout", use_container_width=True)

# --- 4. MAIN DASHBOARD HERO SECTION ---
st.markdown("""
    <div class='center-hero'>
        <h1 style='font-size: 120px; margin-bottom: 0;'>MP</h1>
        <p class='gold-text' style='font-size: 20px;'>Mohale M. Professional</p>
        <br>
        <h1 style='font-size: 40px; letter-spacing: 2px;'>HI, I'M MOHALE</h1>
        <p class='white-text' style='font-size: 16px;'>How can I assist you today?</p>
    </div>
    <br><br>
""", unsafe_allow_html=True)

# --- 5. CHAT LOGIC ---
load_dotenv()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask anything..."):
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Connect to Gemini
                client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: Make sure your API key is in the .env file. Details: {e}")
