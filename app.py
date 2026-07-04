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
st.write("Welcome! Apna account register/connect karein aur 1 minute mein apna bot live karein.")
st.write("---")

# Session State Initialize karna
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
    st.caption("ℹ️ Agar aap ka page band ho gaya tha, toh dubara wahi number likhein, website aap ko seedha aap ke code par le jayegi.")
    
    whatsapp_num = st.text_input("WhatsApp Number (e.g., 923144257762):", value=st.session_state.phone)
    baji_name = st.text_input("Aap Ka Naam (Naye Users Ke Liye):", value=st.session_state.baji_name)
    
    if st.button("Aagay Barhein ➔", type="primary"):
        if whatsapp_num:
            whatsapp_num = whatsapp_num.strip()
            baji_name = baji_name.strip()
            
            # DATABASE CHECK: Kya yeh number pehle se maujood hai?
            check_res = requests.get(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration?whatsapp_num=eq.{whatsapp_num}", headers=headers)
            
            if check_res.status_code == 200 and len(check_res.json()) > 0:
                # 🔥 CASE A: Number pehle se hai (Page band ho gaya tha)
                user_data = check_res.json()[0]
                st.session_state.baji_name = user_data['baji_name'] # Purana naam database se utha lo
                st.session_state.phone = whatsapp_num
                st.session_state.registered = True
                st.toast(f"👋 Khushamdeed wapas! Aap ka account pehle se register hai.")
                time.sleep(1)
                st.rerun()
            else:
                # 🆕 CASE B: Bilkul naya user hai
                if baji_name:
                    data = {"baji_name": baji_name, "whatsapp_num": whatsapp_num, "pairing_code": "WAITING"}
                    requests.post(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration", json=data, headers=headers)
                    
                    st.session_state.registered = True
                    st.session_state.phone = whatsapp_num
                    st.session_state.baji_name = baji_name
                    st.toast("🎉 Account register ho raha hai...")
                    time.sleep(1)
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
    
    # Action Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Dobara Code Mangwayein (Resend)", type="secondary", key="resend_btn"):
            requests.patch(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration?whatsapp_num=eq.{st.session_state.phone}", json={"pairing_code": "RESEND_REQUESTED"}, headers=headers)
            st.toast("⏳ Naye code ki request bhej di gayi hai...")
            time.sleep(1)
            st.rerun()
            
    with col2:
        if st.button("❌ Account Se Exit / Number Tabdeel", type="danger", key="change_num_btn"):
            st.session_state.registered = False
            st.session_state.phone = ""
            st.session_state.baji_name = ""
            st.rerun()

    st.write("---")
    
    code_placeholder = st.empty()
    status_placeholder = st.empty()
    
    # Supabase se code live track karna
    res = requests.get(f"{SUPABASE_URL}/rest/v1/ladies_bot_registration?whatsapp_num=eq.{st.session_state.phone}&select=pairing_code", headers=headers)
    
    if res.status_code == 200 and res.json():
        current_code = res.json()[0]['pairing_code']
        
        # 1. Agar code abhi generate ho raha hai
        if current_code in ["WAITING", "RESEND_REQUESTED"]:
            status_placeholder.warning("🔄 WhatsApp Server se pairing code mangwaya ja raha hai... (Max 15s)...")
            time.sleep(2)
            st.rerun()
            
        # 2. Agar code mil gaya (8-Boxes View)
        elif current_code not in ["FAILED_TRY_AGAIN"]:
            status_placeholder.empty()
            clean_code = current_code.replace("-", "").strip()
            
            if len(clean_code) == 8:
                boxes_html = "".join([f"<div style='display:inline-block; width:45px; height:50px; line-height:50px; font-size:26px; font-weight:bold; color:#0288d1; background:#e1f5fe; border:2px solid #0288d1; border-radius:8px; margin:5px; text-align:center;'>{char}</div>" for char in clean_code])
                
                code_placeholder.markdown(f"""
                <div style="text-align:center; padding:20px; border: 2px dashed #90caf9; border-radius:15px; background:#fafafa; margin:15px 0;">
                    <span style='font-size:16px; color:#555; display:block; font-weight:bold; margin-bottom:15px;'>AAPKA WHATSAPP LINK CODE:</span>
                    <div style='display:flex; justify-content:center; flex-wrap:wrap;'>
                        {boxes_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.success("💡 Yeh code apne WhatsApp -> Linked Devices -> Link with phone number mein daalein!")
            else:
                st.info(f"Aap ka code yeh hai: **{current_code}**")
                
        # 3. Agar fail ho jaye
        elif current_code == "FAILED_TRY_AGAIN":
            status_placeholder.empty()
            st.error("❌ WhatsApp Server is waqt code nahi de pa raha.")
            st.warning("👉 Pareshan na hon! Upar diye gaye **'Dobara Code Mangwayein (Resend)'** button par click karein.")
