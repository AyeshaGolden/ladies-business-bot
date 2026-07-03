import streamlit as st
import time
import requests

# Page config
st.set_page_config(page_title="Ladies Business Bot", page_icon="🧕", layout="centered")

# --- AAPKI SUPABASE DETAILS ---
SUPABASE_URL = "https://mymvzzflaghrnwfgfrmr.supabase.co"
SUPABASE_KEY = "sb_publishable_rQC7U6k12fPKo19KoT8jMw_GikOcEm7" 

st.title("🧕 Ladies Business Bot")
st.write("Welcome! Apna account register karein aur 1 minute mein apna bot connect karein.")

if 'registered' not in st.session_state:
    st.session_state.registered = False

if not st.session_state.registered:
    st.subheader("🔒 Naya Account Banayein")
    whatsapp_num = st.text_input("WhatsApp Number (e.g., 923001234567):")
    baji_name = st.text_input("Aap Ka Naam:")
    
    if st.button("Register Aur Link Code Nikalein", type="primary"):
        if whatsapp_num and baji_name:
            headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json"}
            data = {"baji_name": baji_name, "whatsapp_num": whatsapp_num, "pairing_code": "WAITING"}
            
            # Supabase mein data bhej rahe hain
            res = requests.post(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration", json=data, headers=headers)
            
            if res.status_code in [200, 201]:
                st.session_state.registered = True
                st.session_state.phone = whatsapp_num
                st.rerun()
            else:
                st.error("Registration mein masla aaya! User pehle se majood ho sakta hai ya key galat hai.")
        else:
            st.error("Dono dabbay fill karein!")
else:
    st.success("Data register ho gaya hai!")
    st.write("🔄 **WhatsApp se Pairing Code mangwaya ja raha hai...**")
    
    # Live check karna ke Colab ne code bheja ya nahi
    code_placeholder = st.empty()
    
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    
    for _ in range(30): # 30 seconds tak check karega
        res = requests.get(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration?whatsapp_num=eq.{st.session_state.phone}&select=pairing_code", headers=headers)
        if res.status_code == 200 and res.json():
            current_code = res.json()[0]['pairing_code']
            if current_code != "WAITING":
                code_placeholder.markdown(f"""
                <div style="background-color:#e1f5fe; padding:20px; border-radius:10px; text-align:center; border:2px dashed #0288d1;">
                    <span style='font-size:14px; color:#555; display:block; font-weight:bold;'>AAPKA WHATSAPP LINK CODE:</span>
                    <span style='font-size:32px; font-weight:bold; color:#0288d1; letter-spacing:4px;'>{current_code}</span>
                </div>
                """, unsafe_allow_html=True)
                st.info("💡 Yeh code apne WhatsApp -> Linked Devices -> Link with phone number mein daalein!")
                break
        time.sleep(2)
