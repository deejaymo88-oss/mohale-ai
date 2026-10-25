import streamlit as st
import os
from openai import OpenAI
from tavily import TavilyClient
import sqlite3
import datetime
import base64
import pypdf
import io
import glob

# --- SET UP YOUR AI'S BRAIN (OPENAI) & SEARCH (TAVILY) ---
client = OpenAI()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

st.set_page_config(page_title="Mohale AI", page_icon="⚽", layout="wide", initial_sidebar_state="expanded")

# --- PREMIUM NAVY & GOLD UI ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
        
        /* Hide default Streamlit elements */
        header, #MainMenu, footer, [data-testid="stStatusWidget"], .stDeployButton { 
            display: none !important; 
            visibility: hidden !important;
        }

        /* --- ABSOLUTE NUCLEAR OPTION: DESTROY ALL GHOST LINES AND SCROLLBARS --- */
        
        /* 1. Hide all scrollbars globally */
        ::-webkit-scrollbar {
            display: none !important;
            width: 0px !important;
            height: 0px !important;
        }
        * {
            scrollbar-width: none !important; 
        }

        /* 2. Target every single wrapper, including the sticky bottom container */
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > section,
        [data-testid="stAppViewContainer"] > div,
        [data-testid="stMain"],
        [data-testid="stMain"] > div,
        [data-testid="stVerticalBlock"],
        [data-testid="stVerticalBlock"] > div,
        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stHorizontalBlock"],
        [data-testid="stBottom"],
        [data-testid="stBottom"] > div,
        .block-container,
        .block-container > div {
            border: none !important;
            border-top: none !important;
            border-bottom: none !important;
            outline: none !important;
            box-shadow: none !important;
            background-color: transparent !important;
            background: transparent !important;
        }

        /* 3. Layout padding */
        .block-container { 
            padding-top: 0rem !important; 
            padding-bottom: 0rem !important;
            max-width: 100% !important;
            padding-left: 12% !important; 
            padding-right: 12% !important;
        }

        /* Background */
        .stApp { 
            background: radial-gradient(circle at 50% 30%, #16233B 0%, #0A111E 70%, #05080F 100%) !important; 
            color: #FFFFFF;
            font-family: 'Inter', sans-serif;
            min-height: 100vh !important;
        }

        /* SIDEBAR */
        [data-testid="collapsedControl"] { display: block !important; }
        section[data-testid="stSidebar"] { 
            display: block !important;
            background-color: #05080F !important;
            border-right: 1px solid rgba(197, 160, 89, 0.15) !important;
            width: 260px !important;
            min-width: 260px !important;
            transform: translateX(0px) !important;
            margin-left: 0px !important;
        }
        
        [data-testid="stSidebar"] > div:first-child { padding-top: 10px; }

        /* SIDEBAR BUTTONS */
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
        
        [data-testid="stSidebar"] .stButton button > div {
            display: flex !important;
            justify-content: flex-start !important;
            align-items: center !important;
            text-align: left !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
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

        .boss-logo-container {
            width: 100px;
            margin-left: 15px;
            margin-bottom: 20px;
            margin-top: 10px;
        }
        .boss-logo {
            width: 100px;
            height: auto;
            mix-blend-mode: screen;
            filter: brightness(1.1) contrast(1.1) sepia(0.2);
        }

        div[data-testid="stPopover"] > button {
            background-color: #1A1D27 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
            color: white !important;
            padding: 10px 15px !important;
            width: 100% !important;
            justify-content: flex-start !important;
            font-weight: 500 !important;
        }
        div[data-testid="stPopover"] > button:hover {
            background-color: #252A37 !important;
        }

        /* Main Hero Screen */
        .main-hero {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 75vh;
            text-align: center;
            margin-top: -40px; 
        }
        
        .main-center-logo {
            width: 500px;
            height: auto;
            mix-blend-mode: screen;
            filter: brightness(1.1) contrast(1.1) sepia(0.2);
            margin-bottom: -120px; 
        }

        .hero-title {
            font-family: 'Cinzel', serif;
            font-size: 65px;
            font-weight: 600;
            color: #F8FAFC;
            margin-top: 0px;
            margin-bottom: 15px;
            letter-spacing: 1px;
            text-shadow: 0px 4px 20px rgba(0,0,0,0.8);
        }
        .hero-subtitle {
            font-size: 20px;
            color: #94A3B8;
            font-weight: 300;
            letter-spacing: 0.5px;
        }

        /* --- CHAT INPUT --- */
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

        [data-testid="stChatInput"] textarea { 
            color: #FFFFFF !important; 
        }

        /* Chat Bubbles */
        [data-testid="stChatMessageAvatarUser"],
        [data-testid="stChatMessageAvatarAssistant"] {
            display: none !important;
        }

        [data-testid="stChatMessage"] {
            background-color: transparent !important;
            padding: 0 !important;
            margin-bottom: 15px !important;
            display: flex !important;
            width: 100% !important;
            align-items: flex-start !important;
        }

        [data-testid="stChatMessageContent"] {
            padding: 12px 18px !important;
            border-radius: 15px !important;
            width: fit-content !important;
            max-width: 85% !important; 
            flex-grow: 0 !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
            text-align: left !important;
        }

        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
            justify-content: flex-end !important;
        }
        
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > [data-testid="stChatMessageContent"] {
            background-color: #1A1D27 !important;
            border: 1px solid rgba(197, 160, 89, 0.4) !important; 
            border-bottom-right-radius: 2px !important;
            margin-left: auto !important;
            margin-right: 0 !important;
        }

        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
            justify-content: flex-start !important;
        }
        
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) > [data-testid="stChatMessageContent"] {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important; 
            border-bottom-left-radius: 2px !important;
            margin-right: auto !important;
            margin-left: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "current_session" not in st.session_state:
    st.session_state.current_session = 1
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def init_db():
    conn = sqlite3.connect('my_platform.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER, role TEXT, content TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS memos (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, updated_at TEXT)''')
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

def clear_all_history():
    conn = sqlite3.connect('my_platform.db')
    c = conn.cursor()
    c.execute("DELETE FROM sessions")
    c.execute("DELETE FROM messages")
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('my_platform.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sessions")
    chats = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM messages")
    msgs = c.fetchone()[0]
    conn.close()
    return chats, msgs

def save_memo(content):
    conn = sqlite3.connect('my_platform.db')
    c = conn.cursor()
    c.execute("DELETE FROM memos")
    c.execute("INSERT INTO memos (content, updated_at) VALUES (?, ?)", (content, str(datetime.datetime.now())))
    conn.commit()
    conn.close()

def get_memo():
    conn = sqlite3.connect('my_platform.db')
    c = conn.cursor()
    c.execute("SELECT content FROM memos LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row[0] if row else ""

if len(get_sessions()) == 0:
    st.session_state.current_session = create_new_session()
else:
    if st.session_state.current_session == 1:
        st.session_state.current_session = get_sessions()[0][0]

encoded_logo_main = ""
encoded_logo_side = ""

side_logo_path = None
for path in glob.glob("logo_side*"):
    if path.lower().endswith((".png", ".jpg", ".jpeg")):
        side_logo_path = path
        break

if side_logo_path:
    try:
        with open(side_logo_path, "rb") as f:
            encoded_logo_side = base64.b64encode(f.read()).decode()
    except:
        pass

center_logo_path = None
for path in glob.glob("logo*"):
    if "side" not in path.lower() and path.lower().endswith((".png", ".jpg", ".jpeg")):
        center_logo_path = path
        break

if center_logo_path:
    try:
        with open(center_logo_path, "rb") as f:
            encoded_logo_main = base64.b64encode(f.read()).decode()
    except Exception as e:
        pass

if not encoded_logo_side:
    encoded_logo_side = encoded_logo_main 

# --- SIDEBAR ---
with st.sidebar:
    if encoded_logo_side:
        st.markdown(f'<div class="boss-logo-container"><img src="data:image/png;base64,{encoded_logo_side}" class="boss-logo"></div>', unsafe_allow_html=True)

    pages = [
        ("🏠", "Dashboard"),
        ("📈", "Strategy Memos"),
        ("📄", "Reports"),
        ("⚙️", "Settings")
    ]
    
    for icon, p in pages:
        label = f"{icon} {p}"
        
        if st.session_state.current_page == p:
            st.button(label, key=f"nav_{p}", disabled=True, use_container_width=True)
        else:
            if st.button(label, key=f"nav_{p}", use_container_width=True):
                st.session_state.current_page = p
                if p == "Dashboard":
                    st.session_state.current_session = create_new_session()
                st.rerun()

    st.write("---")
    
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

    st.write("---")

    if st.session_state.logged_in:
        with st.popover("👤 Mohale M.", use_container_width=True):
            if st.button("⚙️ Settings", use_container_width=True):
                st.session_state.current_page = "Settings"
                st.rerun()
            st.write("❓ Help & Feedback")
            if st.button("🚪 Log out", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()
    else:
        if st.button("👤 Log In / Register", use_container_width=True):
            st.session_state.current_page = "Login"
            st.rerun()

# --- MAIN AREA ---
if st.session_state.current_page == "Dashboard":
    messages = get_messages(st.session_state.current_session)
    
    if len(messages) == 0:
        center_logo_html = f'<img src="data:image/png;base64,{encoded_logo_main}" class="main-center-logo">' if encoded_logo_main else ""
        
        st.markdown(
            f'<div class="main-hero">'
            f'{center_logo_html}'
            f'<div class="hero-title">Hi, I\'m Mohale</div>'
            f'<div class="hero-subtitle">How can I assist you today?</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask anything about strategy, research, or insights...", accept_file=True, file_type=["png", "jpg", "jpeg", "pdf", "txt"])

    if prompt:
        user_text = prompt.text
        user_files = prompt.files if prompt.files else []
        
        if len(messages) == 0 and user_text:
            new_title = user_text[:20] + "..." if len(user_text) > 20 else user_text
            update_session_title(st.session_state.current_session, new_title)
        
        if user_text:
            save_message(st.session_state.current_session, "user", user_text)
        
        with st.chat_message("user"):
            if user_text: st.markdown(user_text)
            if user_files: st.write(f"📎 Attached {len(user_files)} file(s)")
            
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
                    if current_history and current_history[-1]["content"] == final_prompt:
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

elif st.session_state.current_page == "Strategy Memos":
    st.title("📈 Strategy Memos")
    st.write("Write down your business strategies, AI ideas, and plans here. This saves to your database.")
    
    current_memo = get_memo()
    memo_text = st.text_area("Your Notes:", value=current_memo, height=400, placeholder="Type your strategy here...")
    
    if st.button("Save Memo"):
        save_memo(memo_text)
        st.success("Strategy Memo Saved Successfully!")

elif st.session_state.current_page == "Reports":
    st.title("📄 Reports")
    st.write("View your platform usage and analytics here.")
    
    total_chats, total_msgs = get_stats()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Chats Created", total_chats)
    with col2:
        st.metric("Total Messages Sent", total_msgs)
        
    st.info("Your platform is running perfectly on OpenAI GPT-4o-mini.")

elif st.session_state.current_page == "Settings":
    st.title("⚙️ Settings")
    st.write("Manage your AI platform settings.")
    
    st.checkbox("Enable Live Web Search (Feature coming soon)", value=True)
    st.checkbox("Enable Dark Mode (Default)", value=True, disabled=True)
    
    st.divider()
    st.write("### Danger Zone")
    if st.button("🚨 Clear All Chat History"):
        clear_all_history()
        st.session_state.current_session = create_new_session()
        st.success("All chat history has been permanently deleted.")
        st.rerun()

elif st.session_state.current_page == "Login":
    st.title("👤 Log In / Register")
    st.write("Access your Mohale AI dashboard.")
    
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email Address", placeholder="name@example.com")
    with col2:
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
    st.write("")
    if st.button("Log In", use_container_width=True):
        st.session_state.logged_in = True
        st.session_state.current_page = "Dashboard"
        st.rerun()
