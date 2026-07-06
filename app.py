import streamlit as st
from supabase import create_client, Client
import time

# Supabase Connection
url: str = "https://mymvzzflaghrnwfgfrmr.supabase.co"
key: str = "sb_publishable_rQC7U6k12fPKo19KoT8jMw_GikOcEm7"
supabase: Client = create_client(url, key)

st.title("🧕 Ladies Business Bot - Registration Panel")
st.write("Welcome! Yahan se bajiyan apna WhatsApp AI Bot jor sakti hain.")

st.header("🔒 Naya Account Banayein")
phone = st.text_input("WhatsApp Number (Poore country code ke sath, e.g., 923001234567):", key="reg_phone")
name = st.text_input("Aap Ka Naam:", key="reg_name")

if st.button("Register Account"):
    if phone and name:
        try:
            # 1. Baji ka data 'pending' status ke sath database mein daalna
            supabase.table("subscribers").insert({
                "phone_number": phone,
                "lady_name": name,
                "status": "pending"
            }).execute()
            
            st.info("🔄 Account register ho gaya hai! Background mein pairing code ban raha hai, meharbani kar ke thoda intezar karein...")
            
            # 2. Website yahan ruk kar database se Pairing Code uthaye gi
            code_found = False
            for _ in range(15):
                time.sleep(2) # Har 2 second baad check karegi
                res = supabase.table("subscribers").select("pairing_code").eq("phone_number", phone).maybeSingle().execute()
                
                if res.data and res.data.get("pairing_code"):
                    pairing_code = res.data["pairing_code"]
                    
                    st.success("✨ AA GAYA PAIRING CODE!")
                    st.markdown(f"## 📋 Aap ka Code hai: `{pairing_code}`")
                    st.write("**Ab aap ne kya karna hai?**")
                    st.write("1. Apne mobile par WhatsApp kholein.")
                    st.write("2. Linked Devices -> **Link with phone number** par click karein.")
                    st.write("3. Upar wala 8 pishon ka code wahan likh dein.")
                    code_found = True
                    break
            
            if not code_found:
                st.warning("⚠️ Code banne mein thoda time lag raha hai. Aap page refresh kar ke dobara check karein.")
                
        except Exception as e:
            st.error(f"Garbar hui: {e}")
    else:
        st.warning("Meharbani kar ke phone number aur naam dono likhein.")
