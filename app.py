import streamlit as st
import os
import base64
import re
import time
import sqlite3
import json
import pypdf
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Mohale M. Professional", layout="wide", initial_sidebar_state="expanded")
load_dotenv()

# --- 2. DATABASE SETUP (SQLite) ---
def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats
                 (id TEXT PRIMARY KEY, title TEXT, messages TEXT)''')
    conn.commit()
    conn.close()

def save_chat_to_db(chat_id, title, messages):
    clean_messages = []
    for msg in messages:
        clean_msg = {"role": msg["role"], "content": msg["content"]}
        clean_messages.append(clean_msg)
        
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    messages_json = json.dumps(clean_messages)
    c.execute("INSERT OR REPLACE INTO chats (id, title, messages) VALUES (?, ?, ?)", 
              (chat_id, title, messages_json))
    conn.commit()
    conn.close()

def load_chat_from_db(chat_id):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT messages FROM chats WHERE id = ?", (chat_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return []

def get_all_chats_from_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT id, title FROM chats ORDER BY rowid DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_chat_title_from_db(chat_id):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT title FROM chats WHERE id = ?", (chat_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else "Saved Chat"

init_db()

# --- 3. STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "book_text" not in st.session_state:
    st.session_state.book_text = ""

# --- 4. ROUTING LOGIC ---
page = st.query_params.get("page", "dashboard")
chat_id_param = st.query_params.get("chat_id")

if chat_id_param:
    st.session_state.current_chat_id = chat_id_param
    st.session_state.messages = load_chat_from_db(chat_id_param)
    page = "chat"

if st.query_params.get("new_chat") == "true":
    st.session_state.messages = []
    st.session_state.current_chat_id = None
    del st.query_params["new_chat"]
    st.rerun()

# --- 5. CONVERT WALLPAPER TO BASE64 ---
@st.cache_data
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

# --- 6. REAL WALLPAPER BACKGROUND & GREY FRAME ---
st.markdown(f"""
<style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stBottom"], [data-testid="stBottomBlockContainer"], .stChatFloatingInputContainer {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
    }}
    
    html, body {{ background-color: #0a1128 !important; }}
    
    .web-bg {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -2;
        {bg_css} background-size: cover; background-position: center; background-repeat: no-repeat; pointer-events: none;
    }}
    
    /* THE GREY FRAME */
    .grey-frame {{
        position: fixed; 
        top: 1rem; 
        bottom: 1rem; 
        left: 1rem; 
        right: 1rem;
        border: 1px solid #666666; 
        border-radius: 8px; 
        pointer-events: none; 
        z-index: 999999999 !important; 
    }}
</style>
<div class="web-bg"></div>
<div class="grey-frame"></div>
""", unsafe_allow_html=True)

# --- 7. APP STYLING ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
    [data-testid="stHeader"] { background: transparent !important; z-index: 10000 !important; }
    .stDeployButton { display: none !important; }
    .main .block-container { padding: 4rem 3rem 8rem 3rem !important; max-width: 100% !important; background: transparent !important; }
    
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; border-right: 1px solid #666666; }
    [data-testid="stSidebar"] > div:first-child { height: 100vh; padding-top: 2rem; display: flex; flex-direction: column; overflow: visible !important; }
    
    [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] {
        display: block !important; visibility: visible !important; z-index: 100000 !important;
        background-color: #1a1a1a !important; border: 1px solid #666666 !important; border-radius: 8px !important; color: #666666 !important; padding: 5px !important;
    }
    [data-testid="stSidebarCollapseButton"] { position: absolute !important; right: -15px !important; top: 15px !important; border-radius: 50% !important; }
    [data-testid="collapsedControl"] { left: 10px !important; top: 10px !important; }
    [data-testid="stSidebarCollapseButton"] svg, [data-testid="collapsedControl"] svg { stroke: #666666 !important; color: #666666 !important; }

    .sidebar-container { display: flex; flex-direction: column; height: 100%; min-height: 85vh; width: 100%; overflow-x: hidden; }
    .sidebar-menu { display: flex; flex-direction: column; flex-grow: 1; width: 100%; overflow-x: hidden; }
    .sidebar-footer { margin-top: auto; padding-bottom: 20px; }
    
    .menu-item { display: flex; align-items: center; padding: 12px 20px; margin-bottom: 5px; cursor: pointer; color: #d1d5db; font-family: 'Inter', sans-serif; font-size: 16px; text-decoration: none !important; transition: 0.3s; white-space: nowrap; width: 100%; box-sizing: border-box; }
    .menu-item:hover { color: #cda34f; background-color: rgba(205, 163, 79, 0.05); }
    .menu-item.active { background-color: #2a2a2a; border-left: 3px solid #666666; color: #ffffff; }
    .menu-item.active svg { stroke: #cda34f; }
    .menu-icon { width: 20px; height: 20px; margin-right: 15px; stroke: #a0a0a0; stroke-width: 2; fill: none; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0; }

    details.menu-item { display: block !important; padding: 0; width: 100%; box-sizing: border-box; overflow: hidden; outline: none !important; border: none !important; }
    details.menu-item summary { padding: 12px 20px; display: flex; align-items: center; list-style: none; cursor: pointer; width: 100%; box-sizing: border-box; outline: none !important; border: none !important; }
    details.menu-item summary:focus { outline: none !important; border: none !important; }
    details.menu-item summary::-webkit-details-marker { display: none; }
    details.menu-item[open] summary { color: #cda34f; }
    
    .history-list { display: flex; flex-direction: column; padding-left: 45px; padding-right: 15px; max-height: 250px; overflow-y: auto; overflow-x: hidden; margin-bottom: 10px; width: 100%; box-sizing: border-box; }
    .history-link { display: block; width: 100%; color: #a0a0a0; font-size: 14px; padding: 6px 0; text-decoration: none !important; font-family: 'Inter', sans-serif; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; box-sizing: border-box; }
    .history-link:hover { color: #cda34f; }
    .history-link.active { color: #ffffff; font-weight: bold; }

    /* --- FORCE CHAT BAR TO FLOAT ABOVE THE BOTTOM LINE --- */
    [data-testid="stBottom"], 
    [data-testid="stBottomBlockContainer"], 
    .stChatFloatingInputContainer { 
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        padding: 0 !important;
        z-index: 99999 !important;
    }

    [data-testid="stChatInput"] { 
        border: 1px solid #666666 !important; /* Grey border for chat bar */
        border-radius: 50px !important; 
        background-color: #1a1a1a !important; 
        width: 85% !important; 
        max-width: 900px !important;
        margin: 0 auto 2.5rem auto !important; 
        padding: 5px 15px !important; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.6); 
        z-index: 100000 !important; 
    }
    
    [data-testid="stChatInput"] > div { display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: space-between !important; width: 100% !important; background-color: transparent !important; border: none !important; }
    [data-testid="stChatInput"] textarea { flex-grow: 1 !important; text-align: left !important; border: none !important; background-color: transparent !important; color: #ffffff !important; padding-left: 10px !important; }
    [data-testid="stChatInput"] button { color: #cda34f !important; background-color: transparent !important; }
    
    .hero-section { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 8. BUILD THE DYNAMIC HISTORY HTML ---
history_items = ""
db_chats = get_all_chats_from_db()
for cid, title in db_chats:
    is_active = "active" if st.session_state.current_chat_id == cid else ""
    display_title = title[:18] + "..." if len(title) > 18 else title
    history_items += f'<a href="?chat_id={cid}" target="_self" class="history-link {is_active}">{display_title}</a>'

is_history_open = "open" if st.session_state.current_chat_id else ""

# --- 9. CUSTOM SIDEBAR (HTML) ---
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
        <a href="?new_chat=true" target="_self" class="menu-item">
            <svg class="menu-icon" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
            New Chat
        </a>
        
        <details class="menu-item" {is_history_open}>
            <summary>
                <svg class="menu-icon" viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><polyline points="3 3 3 8 8 8"></polyline><line x1="12" y1="7" x2="12" y2="12"></line><line x1="12" y1="12" x2="16" y2="16"></line></svg>
                Chat History
            </summary>
            <div class="history-list">
                {history_items if history_items else '<span style="color:#666; font-size:12px;">No history yet</span>'}
            </div>
        </details>

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
            <img src="https://i.pravatar.cc/150?img=11" style="border-radius: 50%; width: 35px; height: 35px; margin-right: 15px; border: 1px solid #666666;">
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

# --- 10. MAIN CONTENT ROUTING ---
if page == "dashboard":
    st.markdown("<div class='hero-section'>", unsafe_allow_html=True)
    logo_exists = os.path.exists("logo.png")
    if logo_exists:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            @st.cache_data
            def load_logo():
                img = Image.open("logo.png")
                width, height = img.size
                crop_height = int(height * 0.70) 
                return img.crop((0, 0, width, crop_height))
            st.image(load_logo(), use_column_width=True)
    else:
        st.markdown("<h1 style='font-family: Cinzel; color: #cda34f; font-size: 120px; margin-bottom: 0;'>MP</h1>", unsafe_allow_html=True)

    st.markdown("""
            <div style='text-align: center; margin-top: -10px;'>
                <p style='font-family: "Cinzel", serif; color: #e0d0b0; font-size: 20px; letter-spacing: 1px;'>MOHALE M. PROFESSIONAL</p>
                <h1 style='font-family: Cinzel; color: #cda34f; font-size: 45px; letter-spacing: 2px; margin-top: 10px;'>HI, I'M MOHALE</h1>
                <p style='color: #a0a0a0; font-size: 16px; margin-bottom: 50px;'>How can I assist you today?</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif page == "settings":
    st.markdown("<h1 style='color: white; font-family: Cinzel; text-align: center; margin-top: 50px;'>Settings</h1>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #cda34f; font-family: Cinzel; text-align: center;'>Train AI with a Book</h3>", unsafe_allow_html=True)
    uploaded_book = st.file_uploader("Upload a .txt or .pdf book to read", type=["txt", "pdf"])
    
    if uploaded_book is not None:
        with st.spinner("Reading the book..."):
            if uploaded_book.type == "application/pdf":
                pdf_reader = pypdf.PdfReader(uploaded_book)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            else:
                text = uploaded_book.read().decode("utf-8")
            
            st.session_state.book_text = text[:25000]
            st.success("Book read successfully! The AI will now remember this during your chat.")

elif page == "meeting":
    st.markdown("<h1 style='color: white; font-family: Cinzel; text-align: center; margin-top: 50px;'>Meeting Notes</h1>", unsafe_allow_html=True)
elif page == "help":
    st.markdown("<h1 style='color: white; font-family: Cinzel; text-align: center; margin-top: 50px;'>Get Help</h1>", unsafe_allow_html=True)
elif page == "logout":
    st.markdown("<h1 style='color: white; font-family: Cinzel; text-align: center; margin-top: 50px;'>Logged Out</h1>", unsafe_allow_html=True)

# --- 11. CHAT LOGIC ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything...", accept_file=True):
    
    text_input = prompt.text if prompt.text else ""
    uploaded_files = prompt.files
    
    image_data_list = []
    if uploaded_files:
        for file in uploaded_files:
            file_bytes = file.read()
            base64_image = base64.b64encode(file_bytes).decode('utf-8')
            image_data_list.append((file.type, base64_image))
    
    user_message = {"role": "user", "content": text_input}
    if image_data_list:
        user_message["image_data"] = image_data_list
        
    st.session_state.messages.append(user_message)
    
    with st.chat_message("user"):
        st.markdown(text_input)
        if uploaded_files:
            for file in uploaded_files:
                st.info(f"📎 Attached File: {file.name}")

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
                client = OpenAI(api_key=api_key)
                
                system_prompt = "You are Mohale M. Professional, an elite AI assistant. Keep your answers concise and elegant."
                system_prompt += "\n\nIf the user provides an image, you must analyze it carefully, even if it contains small text, charts, or tables. Read the text directly from the image to answer the user."
                
                if st.session_state.book_text:
                    system_prompt += f"\n\nCRITICAL INSTRUCTION: You have been provided with a text excerpt from a book. You cannot open external files because the text has already been pasted into your memory. If the user asks you to 'open' the book or asks about something not in the text, explain that you are currently reading a text excerpt and answer based ONLY on what is provided in the excerpt below:\n\n{st.session_state.book_text}"

                messages_payload = [{"role": "system", "content": system_prompt}]
                
                for msg in st.session_state.messages:
                    if "image_data" in msg and msg["image_data"]:
                        content_list = [{"type": "text", "text": msg["content"] if msg["content"] else "Describe this image."}]
                        for img_type, img_b64 in msg["image_data"]:
                            content_list.append({
                                "type": "image_url",
                                "image_url": {"url": f"data:{img_type};base64,{img_b64}"}
                            })
                        messages_payload.append({"role": msg["role"], "content": content_list})
                    else:
                        messages_payload.append({"role": msg["role"], "content": msg["content"]})

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages_payload
                )
                
                response_text = response.choices[0].message.content
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

                if st.session_state.current_chat_id is None:
                    new_id = str(int(time.time()))
                    
                    first_text = "New Chat"
                    for msg in st.session_state.messages:
                        if msg["role"] == "user" and msg["content"] and msg["content"].strip():
                            first_text = msg["content"].strip()
                            break
                            
                    title = first_text[:25] + "..." if len(first_text) > 25 else first_text
                    st.session_state.current_chat_id = new_id
                    save_chat_to_db(new_id, title, st.session_state.messages)
                else:
                    original_title = get_chat_title_from_db(st.session_state.current_chat_id)
                    save_chat_to_db(st.session_state.current_chat_id, original_title, st.session_state.messages)
                
                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")
