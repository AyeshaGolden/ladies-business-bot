import streamlit as st
from supabase import create_client
import time

# ✅ AAP KI ASLI SUPABASE CREDENTIALS DIRECT ADD KAR DI HAIN
SUPABASE_URL = "https://mymvzzflaghrnwfgfrmr.supabase.co"
SUPABASE_KEY = "sb_publishable_rQC7U6k12fPKo19KoT8jMw_GikOcEm7"

# Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="WhatsApp Bot", page_icon="🤖")
st.title("🤖 WhatsApp Pairing Bot")

st.subheader("👩‍💼 Baji Register Karein")
baji_name = st.text_input("👤 Apna Naam Likhein")
whatsapp_num = st.text_input("📱 WhatsApp Number (with country code)", placeholder="923001234567")

if st.button("🔘 Register Account"):
    if not baji_name or not whatsapp_num:
        st.error("❌ Please fill all fields!")
    else:
        try:
            # 🔥 INSERT into ladies_bot_registration table
            data = {
                "baji_name": baji_name,
                "whatsapp_num": whatsapp_num,
                "pairing_code": "WAITING"  # Default value
            }
            
            response = supabase.table("ladies_bot_registration").insert(data).execute()
            
            if response.data:
                st.success("✅ Registration successful!")
                st.info("⏳ Waiting for pairing code... (Bot will generate it in 1-2 minutes)")
                
                # 🎯 Check for pairing code
                code_found = False
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(24):  # 2 minutes tak check karein
                    progress_bar.progress(int((i + 1) * 4.16))
                    status_text.text(f"⏳ Generating code... {i+1}/24")
                    time.sleep(5)
                    
                    # Database se check karein
                    check_response = supabase.table("ladies_bot_registration") \
                        .select("pairing_code") \
                        .eq("whatsapp_num", whatsapp_num) \
                        .execute()
                    
                    if check_response.data:
                        code = check_response.data[0].get("pairing_code")
                        if code and code != "WAITING":
                            st.balloons()
                            st.success(f"🎉 Aapka Pairing Code: **{code}**")
                            st.info("📱 WhatsApp mein ja kar Settings → Link Device → Code enter karein")
                            code_found = True
                            break
                
                if not code_found:
                    st.warning("⏳ Code generate ho raha hai... Thoda aur intezar karein")
                    st.info("💡 Refresh karein agar 3 minute baad bhi code na aaye")
            else:
                st.error("❌ Database mein save nahi ho saka. Please try again.")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Check: Same number already registered?")

# 📊 Show all registered users
st.subheader("📊 Registered Bajiyan")
try:
    users = supabase.table("ladies_bot_registration") \
        .select("*") \
        .order("created_at", desc=True) \
        .limit(10) \
        .execute()
    
    if users.data:
        # Clean display
        display_data = []
        for user in users.data:
            display_data.append({
                "Name": user["baji_name"],
                "WhatsApp": user["whatsapp_num"],
                "Code": user["pairing_code"],
                "Registered": user["created_at"][:10] if user["created_at"] else "N/A"
            })
        st.table(display_data)
    else:
        st.info("No users registered yet")
except Exception as e:
    st.error(f"Unable to fetch users: {str(e)}")
