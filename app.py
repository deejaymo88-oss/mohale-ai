# --- 8. CHAT LOGIC ---
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
                    
                    # NEW: Using the Interactions API for gemini-3.8-flash
                    interaction = client.interactions.create(
                        model="gemini-3.8-flash",
                        input=text_input
                    )
                    response_text = interaction.output_text
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error: {e}")
