import streamlit as st
import os

st.set_page_config(page_title="Mohale M. Professional", layout="wide", initial_sidebar_state="expanded")

# --- ONLY THE BACKGROUND CSS ---
st.markdown("""
<style>
    /* Make the app transparent */
    .stApp, [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }

    /* THE PERFECT WATER-DROP RIPPLE BACKGROUND */
    .web-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw; 
        height: 100vh;
        z-index: -2;
        /* 
           Layer 1: A complex SVG of overlapping, offset circles to create the water drop/Guilloché effect.
           Layer 2: The rich dark blue gradient so it doesn't look flat.
        */
        background-image: 
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1000 1000'%3E%3Cg stroke='%23cda34f' stroke-width='1' fill='none' opacity='0.1'%3E%3Ccircle cx='500' cy='500' r='100'/%3E%3Ccircle cx='500' cy='500' r='150'/%3E%3Ccircle cx='500' cy='500' r='200'/%3E%3Ccircle cx='500' cy='500' r='250'/%3E%3Ccircle cx='500' cy='500' r='300'/%3E%3Ccircle cx='500' cy='500' r='350'/%3E%3Ccircle cx='500' cy='500' r='400'/%3E%3Ccircle cx='500' cy='500' r='450'/%3E%3Ccircle cx='500' cy='500' r='500'/%3E%3Ccircle cx='500' cy='500' r='550'/%3E%3Ccircle cx='500' cy='500' r='600'/%3E%3Ccircle cx='450' cy='450' r='200'/%3E%3Ccircle cx='450' cy='450' r='250'/%3E%3Ccircle cx='450' cy='450' r='300'/%3E%3Ccircle cx='450' cy='450' r='350'/%3E%3Ccircle cx='550' cy='550' r='200'/%3E%3Ccircle cx='550' cy='550' r='250'/%3E%3Ccircle cx='550' cy='550' r='300'/%3E%3Ccircle cx='550' cy='550' r='350'/%3E%3C/g%3E%3C/svg%3E"),
            radial-gradient(circle at 50% 40%, #152244 0%, #0a1128 60%, #050a1f 100%);
        background-size: cover, cover;
        background-position: center, center;
        pointer-events: none;
    }
</style>
<div class="web-bg"></div>
""", unsafe_allow_html=True)
