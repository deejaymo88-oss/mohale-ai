# --- 8. CHAT LOGIC ---
import time

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
            try:
                if uploaded_files:
                    file_names = ", ".join([f.name for f in uploaded_files])
                    response_text = f"I see you uploaded: **{file_names}**! I am currently configured to just read text, but soon you will be able to analyze documents right here."
                else:
                    api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
                    client = genai.Client(api_key=api_key)
                    
                    # RETRY LOOP: Tries 3 times if Google's servers are busy
                    max_retries = 3
                    for attempt in range(max_retries):
                        try:
                            response = client.models.generate_content(
                                model="gemini-2.0-flash", # Switched to this highly stable model
                                contents=text_input
                            )
                            response_text = response.text
                            break # If it works, break out of the loop!
                        except Exception as e:
                            if "503" in str(e) or "429" in str(e): # 503 is High Demand
                                if attempt < max_retries - 1:
                                    time.sleep(2) # Wait 2 seconds and try again
                                    continue
                                else:
                                    raise Exception("Google's servers are super busy right now. Please wait a minute and try again!")
                            else:
                                raise e # If it's a different error, show it
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error: {e}")
