
import streamlit as st
from supabase import create_client, Client

# Supabase Connection
url: str = "https://mymvzzflaghrnwfgfrmr.supabase.co"
key: str = "sb_publishable_rQC7U6k12fPKo19KoT8jMw_GikOcEm7"
supabase: Client = create_client(url, key)

st.title("🧕 Ladies Business Bot - Registration Panel")
st.write("Welcome! Yahan se bajiyan apna account register kar sakti hain.")

st.header("🔒 Naya Account Banayein")
phone = st.text_input("WhatsApp Number (e.g., 923001234567):", key="reg_phone")
name = st.text_input("Aap Ka Naam:", key="reg_name")

if st.button("Register Account"):
    if phone and name:
        try:
            data, count = supabase.table("subscribers").insert({
                "phone_number": phone,
                "lady_name": name,
                "status": "active"
            }).execute()
            st.success(f"🎉 Mubarak! {name} ka account register ho gaya.")
        except Exception as e:
            st.error(f"Garbar hui: {e}")
    else:
        st.warning("Meharbani kar ke phone number aur naam dono likhein.")
