import streamlit as st
import time

# Page configuration
st.set_page_config(page_title="Ladies Business Bot", page_icon="🧕", layout="centered")

st.title("🧕 Ladies Business Bot - Registration Panel")
st.write("Welcome! Yahan se bajiyan apna account register kar sakti hain aur apna bot active kar sakti hain.")

# Custom styling for professional look
st.markdown("""
<style>
    .main-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Session state to track registration status
if 'registered' not in st.session_state:
    st.session_state.registered = False

if not st.session_state.registered:
    st.subheader("🔒 Naya Account Banayein")
    
    # Form inputs
    whatsapp_num = st.text_input("WhatsApp Number (e.g., 923001234567):", placeholder="Mulk ke code ke sath likhein")
    baji_name = st.text_input("Aap Ka Naam:", placeholder="Apna poora naam likhein")
    
    if st.button("Register Aur QR Code Nikalein", type="primary"):
        if whatsapp_num and baji_name:
            with st.spinner("Supabase mein data save ho raha hai..."):
                # Yahan hum ne data dikhane ke liye loading simulator lagaya hai
                time.sleep(1.5) 
                st.session_state.registered = True
                st.session_state.baji_name = baji_name
                st.rerun()
        else:
            st.error("Baraye meherbani dono dabbay fill karein!")

else:
    st.success(f"Mubarak ho {st.session_state.baji_name}! Aapka data register ho gaya hai.")
    
    st.markdown("### 📲 Apne WhatsApp Se QR Code Scan Karein")
    st.write("Apne mobile par WhatsApp kholein -> Linked Devices par jayein -> aur niche diye gaye QR code ko scan karein taake aapka bot active ho jaye!")
    
    # Placeholder for QR Code image
    # Jab node.js backend chalega, toh yeh image dynamic ho jayegi
    st.info("🔄 QR Code load ho raha hai... (Backend engine se connect ho raha hai)")
    
    # Ek simple button wapas jaane ke liye agar zaroorat ho
    if st.button("Naya Registration Karein"):
        st.session_state.registered = False
        st.rerun()
