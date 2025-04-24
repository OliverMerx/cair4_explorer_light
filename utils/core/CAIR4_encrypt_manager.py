
from pylibs.streamlit_lib import streamlit as st
from cryptography.fernet import Fernet
from models.core.CAIR4_dynaminc_api_keys import get_api_key


ENCRYPTION_KEY = Fernet.generate_key() 

# Alternativ:
#get_api_key("CAIR4") via .env'
#os.environ.get("ENCRYPTION_KEY")

fernet = Fernet(ENCRYPTION_KEY)  # ✅

def encrypt_data(data: str) -> str | None:
    if fernet and data:
        return fernet.encrypt(data.encode()).decode()
    return None

def decrypt_data(cipher_text: str) -> str | None:
    if fernet and cipher_text:
        try:
            return fernet.decrypt(cipher_text.encode()).decode()
        except Exception as e:
            print(f"❌ Fehler beim Entschlüsseln: {e}")
    return None

def encrypt(data: str, method: str = "fernet") -> str | None:
    return encrypt_data(data)

def decrypt(cipher_text: str, method: str = "fernet") -> str | None:
    return decrypt_data(cipher_text)

if not fernet:
    st.warning("⚠️ Keine ENCRYPTION_KEY-Variable gefunden – Verschlüsselung deaktiviert.")