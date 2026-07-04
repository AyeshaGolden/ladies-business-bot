import streamlit as st
import time
import requests

# Page configuration
st.set_page_config(page_title="Ladies Business Bot", page_icon="🧕", layout="centered")

# --- AAPKI SUPABASE DETAILS ---
SUPABASE_URL = "https://mymvzzflaghrnwfgfrmr.supabase.co"
SUPABASE_KEY = "sb_publishable_rQC7U6k12fPKo19KoT8jMw_GikOcEm7" 
headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json"}

st.title("🧕 Ladies Business Bot")
st.write("Welcome! Apna account register karein aur 1 minute mein apna bot connect karein.")
st.write("---")

# 1. Browser Memory (Session State) initialize karna
if 'registered' not in st.session_state:
    st.session_state.registered = False
if 'phone' not in st.session_state:
    st.session_state.phone = ""
if 'baji_name' not in st.session_state:
    st.session_state.baji_name = ""

# ==========================================
# SCENE 1: AGAR USER REGISTERED NAHI HAI
# ==========================================
if not st.session_state.registered:
    st.subheader("🔒 Naya Account Banayein")
    whatsapp_num = st.text_input("WhatsApp Number (e.g., 923144257762):", value=st.session_state.phone)
    baji_name = st.text_input("Aap Ka Naam:", value=st.session_state.baji_name)
    
    if st.button("Register Aur Link Code Nikalein", type="primary"):
        if whatsapp_num and baji_name:
            # Clean spaces
            whatsapp_num = whatsapp_num.strip()
            baji_name = baji_name.strip()
            
            # Pehle check karo kya yeh number pehle se database mein hai?
            check_res = requests.get(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration?whatsapp_num=eq.{whatsapp_num}", headers=headers)
            
            if check_res.status_code == 200 and len(check_res.json()) > 0:
                # Agar pehle se hai, toh status ko 'WAITING' kar do taake naya code generate ho ske
                requests.patch(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration?whatsapp_num=eq.{whatsapp_num}", json={"pairing_code": "WAITING", "baji_name": baji_name}, headers=headers)
            else:
                # Agar naya user hai, toh insert karo
                data = {"baji_name": baji_name, "whatsapp_num": whatsapp_num, "pairing_code": "WAITING"}
                requests.post(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration", json=data, headers=headers)
            
            # Memory mein save karo taake page refresh par data na urey
            st.session_state.registered = True
            st.session_state.phone = whatsapp_num
            st.session_state.baji_name = baji_name
            st.rerun()
        else:
            st.error("Dono dabbay fill karein!")

# ==========================================
# SCENE 2: AGAR USER REGISTERED HAI (CODE SHOW PAGE)
# ==========================================
else:
    st.info(f"👋 Khushamdeed **{st.session_state.baji_name}** ({st.session_state.phone})")
    
    # Do option buttons top par
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Dobara Code Mangwayein (Resend)", type="secondary"):
            # Database mein status dubara WAITING kar do taake Colab active ho jaye
            requests.patch(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration?whatsapp_num=eq.{st.session_state.phone}", json={"pairing_code": "WAITING"}, headers=headers)
            st.toast("⏳ Naye code ki request bhej di gayi hai...")
            st.rerun()
            
    with col2:
        if st.button("❌ Number Tabdeel Karein", type="danger"):
            # Memory clear karke registration page par wapas bhejo
            st.session_state.registered = False
            st.session_state.phone = ""
            st.session_state.baji_name = ""
            st.rerun()

    st.write("---")
    
    # Real-time tracking elements
    code_placeholder = st.empty()
    status_placeholder = st.empty()
    
    # 45 Seconds tak check karega live loop
    code_found = False
    for i in range(45):
        status_placeholder.write(f"🔄 **WhatsApp Server se code mangwaya ja raha hai... ({i+1}/45s)**")
        
        res = requests.get(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration?whatsapp_num=eq.{st.session_state.phone}&select=pairing_code", headers=headers)
        
        if res.status_code == 200 and res.json():
            current_code = res.json()[0]['pairing_code']
            
            if current_code not in ["WAITING", "FAILED_TRY_AGAIN"]:
                status_placeholder.empty()
                code_placeholder.markdown(f"""
                <div style="background-color:#e1f5fe; padding:25px; border-radius:12px; text-align:center; border:2px dashed #0288d1; margin: 15px 0;">
                    <span style='font-size:15px; color:#555; display:block; font-weight:bold; margin-bottom:5px;'>AAPKA WHATSAPP LINK CODE:</span>
                    <span style='font-size:36px; font-weight:bold; color:#0288d1; letter-spacing:4px;'>{current_code}</span>
                </div>
                """, unsafe_allow_html=True)
                st.success("💡 Yeh code apne WhatsApp -> Linked Devices -> Link with phone number mein daalein!")
                code_found = True
                break
            
            elif current_code == "FAILED_TRY_AGAIN":
                status_placeholder.empty()
                st.error("❌ WhatsApp Server ne is number par code nahi diya. Shayad bohot zyada tries ki wajah se block hai.")
                st.warning("👉 Upar majood **'Dobara Code Mangwayein (Resend)'** wale button par click kar ke check karein.")
                code_found = True
                break
                
        time.sleep(1)
        
    if not code_found:
        status_placeholder.empty()
        st.warning("⏱️ Code aane mein thoda waqt lag raha hai. Aap upar diye gaye **'Resend'** button ko daba kar dubara request bhej sakti hain.")
