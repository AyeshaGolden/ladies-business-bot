import streamlit as st
import time
import requests
from streamlit_autorefresh import st_autorefresh

# Page configurations
st.set_page_config(page_title="Ladies Business Bot", page_icon="🧕", layout="centered")

# --- CONFIGURATION ---
SUPABASE_URL = "https://mymvzzflaghrnwfgfrmr.supabase.co"
SUPABASE_KEY = "sb_publishable_rQC7U6k12fPKo19KoT8jMw_GikOcEm7" 
headers = {
    "apikey": SUPABASE_KEY, 
    "Authorization": f"Bearer {SUPABASE_KEY}", 
    "Content-Type": "application/json"
}

st.title("🧕 Ladies Business Bot")
st.write("Welcome! Apna account open karein aur website se Code le kar WhatsApp bot activate karein.")
st.write("---")

if 'registered' not in st.session_state:
    st.session_state.registered = False
if 'phone' not in st.session_state:
    st.session_state.phone = ""
if 'baji_name' not in st.session_state:
    st.session_state.baji_name = ""

# ==========================================
# SCENE 1: SMART REGISTRATION & RE-ENTRY PAGE
# ==========================================
if not st.session_state.registered:
    st.subheader("🔒 Register Karein Ya Apna Account Open Karein")
    st.caption("ℹ️ Agar aap ka page pehle band ho gaya tha, toh dubara wahi number likhein, website aapko seedha aap ke live code par le jayegi.")
    
    whatsapp_num = st.text_input("WhatsApp Number (e.g., 03144357762):", value=st.session_state.phone)
    baji_name = st.text_input("Aap Ka Naam:", value=st.session_state.baji_name)
    
    if st.button("Aagay Barhein ➔", type="primary", key="submit_registration_btn"):
        if whatsapp_num:
            whatsapp_num = whatsapp_num.strip()
            baji_name = baji_name.strip()
            
            check_res = requests.get(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration?whatsapp_num=eq.{whatsapp_num}", headers=headers)
            
            if check_res.status_code == 200 and len(check_res.json()) > 0:
                user_data = check_res.json()[0]
                st.session_state.baji_name = user_data['baji_name'] 
                st.session_state.phone = whatsapp_num
                st.session_state.registered = True
                st.toast(f"👋 Khushamdeed wapas!")
                time.sleep(0.5)
                st.rerun()
            else:
                if baji_name:
                    data = {"baji_name": baji_name, "whatsapp_num": whatsapp_num, "pairing_code": "WAITING"}
                    requests.post(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration", json=data, headers=headers)
                    
                    st.session_state.registered = True
                    st.session_state.phone = whatsapp_num
                    st.session_state.baji_name = baji_name
                    st.toast("🎉 Account register ho raha hai...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Naye account ke liye 'Aap Ka Naam' likhna zaroori hai!")
        else:
            st.error("Meharbani kar ke WhatsApp number darj karein!")

# ==========================================
# SCENE 2: LIVE CODE TRACKING PAGE (8 Boxes Style)
# ==========================================
else:
    st.info(f"👋 Khushamdeed **{st.session_state.baji_name}** ({st.session_state.phone})")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Naya Code Mangwayein", type="secondary", key="resend_code_action_btn"):
            requests.patch(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration?whatsapp_num=eq.{st.session_state.phone}", json={"pairing_code": "RESEND_REQUESTED"}, headers=headers)
            st.toast("⏳ Naye code ki request bhej di gayi hai...")
            time.sleep(0.5)
            st.rerun()
            
    with col2:
        if st.button("❌ Account Se Exit Karein", type="secondary", key="exit_account_action_btn"):
            st.session_state.registered = False
            st.session_state.phone = ""
            st.session_state.baji_name = ""
            st.rerun()

    st.write("---")
    
    code_placeholder = st.empty()
    status_placeholder = st.empty()
    
    # Live fetch from Supabase
    res = requests.get(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration?whatsapp_num=eq.{st.session_state.phone}&select=pairing_code", headers=headers)
    
    if res.status_code == 200 and res.json():
        current_code = res.json()[0]['pairing_code']
        
        if current_code in ["WAITING", "RESEND_REQUESTED"]:
            status_placeholder.warning("🔄 Supabase server ke zariye code ready ho raha hai... Please wait (10-15 seconds)")
            # Auto refresh page every 4 seconds to fetch newly generated code seamlessly
            st_autorefresh(interval=4000, limit=20, key="frontend_reload_loop")
            
        elif current_code == "FAILED_TRY_AGAIN":
            status_placeholder.empty()
            st.error("❌ WhatsApp Server se connection build nahi ho saka.")
            st.warning("👉 Koshish karein ke number correct format mein ho, aur upar diye gaye **'Naya Code Mangwayein'** button par click karein.")
            
        else:
            status_placeholder.empty()
            clean_code = current_code.replace("-", "").strip()
            
            if len(clean_code) == 8:
                boxes_html = "".join([f"<div style='display:inline-block; width:42px; height:48px; line-height:48px; font-size:24px; font-weight:bold; color:#0288d1; background:#e1f5fe; border:2px solid #0288d1; border-radius:8px; margin:4px; text-align:center;'>{char}</div>" for char in clean_code])
                
                code_placeholder.markdown(f"""
                <div style="text-align:center; padding:20px; border: 2px dashed #90caf9; border-radius:15px; background:#fafafa; margin:15px 0;">
                    <span style='font-size:15px; color:#555; display:block; font-weight:bold; margin-bottom:12px;'>APNE WHATSAPP LINK DEVICES MEIN YEH CODE DARJ KAREIN:</span>
                    <div style='display:flex; justify-content:center; flex-wrap:wrap;'>
                        {boxes_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.success("💡 **Kaam Kaise Karega?** \n1. Apne mobile par WhatsApp open karein.\n2. **Linked Devices** par jayein -> **Link with phone number** par click karein.\n3. Screen par dikhne wala yeh 8-digit code wahan type kar dein!")
            else:
                st.info(f"Aap ka pairing code yeh hai: **{current_code}**")
