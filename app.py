# app.py mein yeh change karein (taki user ko code dikhe)
import streamlit as st
from supabase import create_client

# ✅ AAP KI ASLI SUPABASE CREDENTIALS DIRECT ADD KAR DI HAIN
SUPABASE_URL = "https://mymvzzflaghrnwfgfrmr.supabase.co"
SUPABASE_KEY = "sb_publishable_rQC7U6k12fPKo19KoT8jMw_GikOcEm7"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("WhatsApp Bot Registration")

name = st.text_input("Apna Naam Likhein")
phone = st.text_input("Phone Number (with country code)")

if st.button("Register Account"):
    # Database mein save karein
    supabase.table("subscribers").insert({
        "name": name,
        "phone_number": phone,
        "status": "pending"
    }).execute()
    
    st.success("✅ Number registered! Waiting for pairing code...")
    
    # 🔄 Code check karein (har 5 seconds baad)
    import time
    for i in range(20):  # 100 seconds tak wait karein
        time.sleep(5)
        res = supabase.table("subscribers").select("pairing_code, status").eq("phone_number", phone).execute()
        
        if res.data and res.data[0].get("status") == "pairing":
            code = res.data[0].get("pairing_code")
            st.success(f"🎉 Aapka Pairing Code: **{code}**")
            st.info("📱 WhatsApp mein ja kar Settings → Link Device → Code enter karein")
            break
        elif i == 19:
            st.error("❌ Code generate nahi ho saka. Dobara try karein.")
