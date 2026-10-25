st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
        
        /* Hide the top header */
        header { visibility: hidden !important; display: none !important; }
        
        /* --- THE SURGICAL FIX FOR THE LINE --- */
        /* We target the bottom container and remove ONLY the shadow and borders */
        [data-testid="stBottom"],
        [data-testid="stBottom"] > div,
        [data-testid="stBottomBlockContainer"] {
            box-shadow: none !important;
            border: none !important;
            border-top: none !important;
            background: transparent !important;
        }

        /* Background (No forced heights, so scrolling works normally) */
        .stApp { 
            background: radial-gradient(circle at 50% 30%, #16233B 0%, #0A111E 70%, #05080F 100%) !important; 
            color: #FFFFFF;
            font-family: 'Inter', sans-serif;
        }

        /* Layout padding */
        .block-container { 
            padding-top: 2rem !important; 
            padding-left: 12% !important; 
            padding-right: 12% !important;
        }

        /* SIDEBAR */
        [data-testid="collapsedControl"] { display: block !important; }
        section[data-testid="stSidebar"] { 
            display: block !important;
            background-color: #05080F !important;
            border-right: 1px solid rgba(197, 160, 89, 0.15) !important;
            width: 260px !important;
            min-width: 260px !important;
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

        /* Main Hero Screen */
        .main-hero {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 65vh;
            text-align: center;
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
