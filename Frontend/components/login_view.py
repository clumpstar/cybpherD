import streamlit as st
import re
from api.wallet_api import create_wallet, import_wallet
from utils.session_manager import set_wallet_data


def validate_email(email: str) -> tuple[bool, str]:
    email = email.strip()
    if not email:
        return False, "Email is required"
    if len(email) > 254:
        return False, "Email is too long"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, email


def validate_mnemonic(mnemonic: str) -> tuple[bool, str]:
    mnemonic = mnemonic.strip()
    if not mnemonic:
        return False, "Mnemonic is required"
    words = mnemonic.split()
    if len(words) != 12:
        return False, "Mnemonic must be exactly 12 words"
    if not all(word.isalpha() and word.islower() for word in words):
        return False, "Mnemonic must contain only lowercase letters"
    return True, mnemonic


def render_login_view():
    st.markdown("### Welcome to Mock Web3 Wallet")
    st.markdown("Get started by creating a new wallet or importing an existing one.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🆕 Create New Wallet")
        with st.form("create_form"):
            email_input = st.text_input("Email (for notifications):", placeholder="your@email.com")
            submit_create = st.form_submit_button("Create Wallet", use_container_width=True)
            
            if submit_create:
                valid, result = validate_email(email_input)
                if not valid:
                    st.error(result)
                else:
                    with st.spinner("Creating wallet..."):
                        success, response = create_wallet(result)
                        if success:
                            set_wallet_data(response["address"], response["private_key"], response["mnemonic"], response["balance"])
                            st.success("Wallet created successfully!")
                            st.rerun()
                        else:
                            st.error(response)
    
    with col2:
        st.markdown("#### 📥 Import Existing Wallet")
        with st.form("import_form"):
            mnemonic_input = st.text_area("Enter your 12-word mnemonic phrase:", height=80, placeholder="word1 word2 word3 ...")
            email_input_import = st.text_input("Email (optional, for notifications):", placeholder="your@email.com")
            submit_import = st.form_submit_button("Import Wallet", use_container_width=True)
            
            if submit_import:
                valid_mnemonic, mnemonic_result = validate_mnemonic(mnemonic_input)
                if not valid_mnemonic:
                    st.error(mnemonic_result)
                else:
                    email = None
                    if email_input_import.strip():
                        valid_email, email_result = validate_email(email_input_import)
                        if not valid_email:
                            st.error(email_result)
                            return
                        email = email_result
                    
                    with st.spinner("Importing wallet..."):
                        success, response = import_wallet(mnemonic_result, email)
                        if success:
                            set_wallet_data(response["address"], response["private_key"], mnemonic_result, response["balance"])
                            st.success("Wallet imported successfully!")
                            st.rerun()
                        else:
                            st.error(response)

