import streamlit as st
import os
import base64
import pypdf
import io
import datetime
import sqlite3
import glob
from openai import OpenAI
from tavily import TavilyClient

# --- SET UP AI & SEARCH ---
client = OpenAI()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# FORCE SIDEBAR OPEN
st.set_page_config(page_title="Mohale AI", layout="wide", initial_sidebar_state="expanded")

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('my_platform.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

def create_new_session():
    conn = sqlite3.connect('my_platform.db')
    c = conn.cursor()
    title = "New Chat"
    c.execute("INSERT INTO sessions (title, created_at) VALUES (?, ?)", (title, str(datetime.datetime.now())))
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id

def get_sessions():
    conn = sqlite3.connect('my_platform.db')
    c = conn.cursor()
    c.execute("SELECT id, title FROM sessions ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_messages(session_id):
    conn = sqlite3.connect('my_platform.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

def save_message(session_id, role, content):
    conn = sqlite3.connect('my_platform.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)", (session_id, role, content))
    conn.commit()
    conn.close()

def update_session_title(session_id, new_title):
    conn = sqlite3.connect('my_platform.db')
    c = conn.cursor()
    c.execute("UPDATE sessions SET title = ? WHERE id = ?", (new_title, session_id))
    conn.commit()
    conn.close()

# --- SESSION STATE ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "current_session" not in st.session_state:
    st.session_state.current_session = 1
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if len(get_sessions()) == 0:
    st.session_state.current_session = create_new_session()
else:
    if st.session_state.current_session == 1:
        st.session_state.current_session = get_sessions()[0][0]

# --- CSS STYLING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');

        /* 1. Remove the ugly top line but KEEP the sidebar toggle */
        header, [data-testid="stHeader"] { 
            background: transparent !important; 
            border: none !important; 
            box-shadow: none !important;
        }
        /* Hide the deploy button and menu */
        [data-testid="stToolbar"] { display: none !important; }

        /* 2. Background */
        .stApp { 
            background: radial-gradient(circle at 50% 40%, #1E2E4A 0%, #0C1421 60%, #05080F 100%) !important; 
            color: #FFFFFF; 
            font-family: 'Inter', sans-serif; 
        }

        /* 3. Sidebar */
        [data-testid="stSidebar"] { 
            background-color: #05080F !important; 
            border-right: 1px solid rgba(197, 160, 89, 0.15) !important;
            width: 260px !important; 
            min-width: 260px !important;
        }
        [data-testid="stSidebar"] > div:first-child { padding-top: 10px; }
        
        /* Sidebar Buttons */
        [data-testid="stSidebar"] .stButton button {
            background: transparent !important; 
            border: none !important; 
            color: #8892B0 !important;
            text-align: left !important; 
            font-size: 15px !important; 
            font-weight: 500 !important;
            padding: 10px 15px !important; 
            border-radius: 6px !important; 
            transition: all 0.2s ease !important;
            justify-content: flex-start !important; 
            width: 100% !important; 
            display: flex !important; 
            align-items: center !important;
        }
        [data-testid="stSidebar"] .stButton button:hover { 
            color: #C5A059 !important; 
            background-color: rgba(197, 160, 89, 0.08) !important; 
        }
        [data-testid="stSidebar"] .stButton button:disabled { 
            color: #C5A059 !important; 
            background-color: rgba(197, 160, 89, 0.1) !important; 
            border-left: 3px solid #C5A059 !important; 
            opacity: 1 !important; 
        }

        .boss-logo-container { width: 100px; margin-left: 15px; margin-bottom: 20px; margin-top: 10px; }
        .boss-logo { width: 100px; height: auto; mix-blend-mode: screen; filter: brightness(1.1) contrast(1.1) sepia(0.2); }

        /* 4. Hero Screen */
        .hero-container { 
            display: flex; flex-direction: column; justify-content: center; align-items: center; 
            height: 65vh; text-align: center; 
        }
        .hero-logo { 
            width: 400px; mix-blend-mode: screen; filter: brightness(1.1) contrast(1.1); 
            margin-bottom: -80px; 
        }
        .hero-title { 
            font-family: 'Cinzel', serif; font-size: 60px; font-weight: 600; color: #F8FAFC; 
            margin-top: 0px; margin-bottom: 15px; letter-spacing: 1px; text-shadow: 0px 4px 20px rgba(0,0,0,0.8); 
        }
        .hero-subtitle { font-size: 20px; color: #94A3B8; font-weight: 300; letter-spacing: 0.5px; }

        /* 5. Chat Input */
        [data-testid="stChatInput"] {
            background-color: rgba(10, 17, 31, 0.8) !important; 
            backdrop-filter: blur(15px) !important;
            border: 2px solid rgba(197, 160, 89, 0.6) !important; 
            border-radius: 30px !important;
            padding: 5px 15px !important; 
            box-shadow: 0 0 20px rgba(197, 160, 89, 0.15) !important;
        }
        [data-testid="stChatInput"]:focus-within { 
            border: 2px solid #C5A059 !important; 
            box-shadow: 0 0 25px rgba(197, 160, 89, 0.3) !important; 
        }
        [data-testid="stChatInput"] textarea { color: #FFFFFF !important; }

        /* 6. Chat Bubbles (Proper Alignment, No Gaps) */
        [data-testid="stChatMessageAvatarUser"], 
        [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
        
        [data-testid="stChatMessage"] { 
            background-color: transparent !important; 
            padding: 0 !important; 
            margin-bottom: 10px !important; 
            border: none !important; 
            box-shadow: none !important; 
        }
        
        [data-testid="stChatMessageContent"] { 
            padding: 12px 18px !important; 
            border-radius: 15px !important; 
            width: fit-content !important; 
            max-width: 80% !important; 
            text-align: left !important; 
        }
        
        /* User Message (Right) */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > [data-testid="stChatMessageContent"] {
            background-color: #1A1D27 !important; 
            border: 1px solid rgba(197, 160, 89, 0.4) !important; 
            border-bottom-right-radius: 2px !important; 
            margin-left: auto !important; 
            margin-right: 0 !important;
        }
        
        /* Assistant Message (Left) */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) > [data-testid="stChatMessageContent"] {
            background-color: rgba(255, 255, 255, 0.05) !important; 
            border: 1px solid rgba(255, 255, 255, 0.1) !important; 
            border-bottom-left-radius: 2px !important; 
            margin-right: auto !important; 
            margin-left: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- LOAD LOGOS ---
encoded_logo_main = ""
encoded_logo_side = ""

for path in glob.glob("logo_side*"):
    if path.lower().endswith((".png", ".jpg", ".jpeg")):
        with open(path, "rb") as f:
            encoded_logo_side = base64.b64encode(f.read()).decode()
        break

for path in glob.glob("logo*"):
    if "side" not in path.lower() and path.lower().endswith((".png", ".jpg", ".jpeg")):
        with open(path, "rb") as f:
            encoded_logo_main = base64.b64encode(f.read()).decode()
        break

if not encoded_logo_side:
    encoded_logo_side = encoded_logo_main 

# --- SIDEBAR CONTENT ---
with st.sidebar:
    if encoded_logo_side:
        st.markdown(f'<div class="boss-logo-container"><img src="data:image/png;base64,{encoded_logo_side}" class="boss-logo"></div>', unsafe_allow_html=True)

    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.current_page = "Dashboard"
        st.rerun()
    if st.button("📈 Strategy Memos", use_container_width=True):
        st.session_state.current_page = "Strategy Memos"
        st.rerun()
    if st.button("📄 Reports", use_container_width=True):
        st.session_state.current_page = "Reports"
        st.rerun()
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.current_page = "Settings"
        st.rerun()

    st.write("")
    
    if st.button("➕ Start New Chat", use_container_width=True):
        st.session_state.current_session = create_new_session()
        st.session_state.current_page = "Dashboard"
        st.rerun()

    st.write("### 💬 History")
    for sess in get_sessions()[:4]:
        sess_id, title = sess
        if st.session_state.current_session == sess_id:
            st.button(f"👉 {title[:18]}", key=f"active_{sess_id}", disabled=True, use_container_width=True)
        else:
            if st.button(title[:20], key=f"sess_{sess_id}", use_container_width=True):
                st.session_state.current_session = sess_id
                st.session_state.current_page = "Dashboard"
                st.rerun()

    st.write("")
    
    if st.button("👤 Log In / Register", use_container_width=True):
        pass 

# --- MAIN AREA ---
if st.session_state.current_page == "Dashboard":
    messages = get_messages(st.session_state.current_session)
    
    # Hero Screen (Only shows when chat is empty)
    if len(messages) == 0:
        if encoded_logo_main:
            st.markdown(f"""
                <div class="hero-container">
                    <img src="data:image/png;base64,{encoded_logo_main}" class="hero-logo">
                    <div class="hero-title">Hi, I'm Mohale</div>
                    <div class="hero-subtitle">How can I assist you today?</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="hero-container"><div class="hero-title">Hi, I\'m Mohale</div><div class="hero-subtitle">How can I assist you today?</div></div>', unsafe_allow_html=True)

    # Chat History
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    prompt = st.chat_input("Ask anything...", accept_file=True, file_type=["png", "jpg", "jpeg", "pdf", "txt"])

    # Processing logic
    if prompt:
        user_text = prompt.text
        user_files = prompt.files if prompt.files else []
        
        if len(messages) == 0 and user_text:
            new_title = user_text[:20] + "..." if len(user_text) > 20 else user_text
            update_session_title(st.session_state.current_session, new_title)
        
        display_text = user_text if user_text else "Attached file(s)"
        if user_files:
            display_text += f"\n\n📎 *Attached {len(user_files)} file(s)*"
            
        save_message(st.session_state.current_session, "user", display_text)
        with st.chat_message("user"):
            st.markdown(display_text)
            
        image_data = None
        extracted_text = ""
        
        for file in user_files:
            if file.type.startswith("image"):
                image_data = base64.b64encode(file.read()).decode()
            elif file.name.endswith(".pdf"):
                pdf_reader = pypdf.PdfReader(file)
                extracted_text += "\n".join([page.extract_text() for page in pdf_reader.pages])
            elif file.name.endswith(".txt"):
                extracted_text += file.read().decode("utf-8")

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("🧠 Thinking..."):
                try:
                    today = datetime.date.today().strftime("%B %d, %Y")
                    final_prompt = user_text if user_text else "Analyze this."
                    
                    if extracted_text:
                        final_prompt = f"User uploaded a document. Content:\n{extracted_text[:3000]}\n\nUser Question: {user_text}"

                    system_prompt = f"You are Mohale AI, an elite, professional AI assistant. Today is {today}. Respond politely and professionally."
                    api_messages = [{"role": "system", "content": system_prompt}]
                    
                    current_history = get_messages(st.session_state.current_session)
                    if current_history and current_history[-1]["content"] == display_text:
                        current_history = current_history[:-1]
                        
                    api_messages.extend(current_history)
                    
                    if image_data:
                        api_messages.append({"role": "user", "content": [{"type": "text", "text": final_prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}]})
                    else:
                        if not extracted_text:
                            search_results = tavily_client.search(query=f"{final_prompt} {today}", search_depth="advanced", max_results=5)
                            context = "\n\n".join([result["content"] for result in search_results["results"]])
                            final_prompt = f"Web Search Results:\n{context}\n\nUser Question: {final_prompt}"
                            
                        api_messages.append({"role": "user", "content": final_prompt})
                    
                    response = client.chat.completions.create(model="gpt-4o-mini", messages=api_messages, stream=True)
                    
                    full_response = ""
                    for chunk in response:
                        if chunk.choices[0].delta.content:
                            full_response += chunk.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    save_message(st.session_state.current_session, "assistant", full_response)
                    st.rerun()
                except Exception as e:
                    st.error(f"🚨 Error: {e}")

elif st.session_state.current_page in ["Strategy Memos", "Reports", "Settings"]:
    st.title(f"📈 {st.session_state.current_page}")
    st.write("This page is coming soon.")
