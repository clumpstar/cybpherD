import streamlit as st
from datetime import datetime, timedelta
from streamlit_js_eval import get_cookie, set_cookie
from utils.jwt_manager import create_jwt_token, decode_jwt_token

SESSION_DURATION_MINUTES = 10


def initialize_session_state():
    """Initialize session state and restore from cookie if available."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.address = None
        st.session_state.private_key = None
        st.session_state.mnemonic = None
        st.session_state.balance = 0.0
        st.session_state.jwt_token = None
        st.session_state.session_start = None
        
        try:
            token = get_cookie("wallet_token")
            if token:
                restore_from_token(token)
        except:
            pass
    
    check_session_expiry()


def set_wallet_data(address: str, private_key: str, mnemonic: str, balance: float):
    """Set wallet data and save to cookie."""
    st.session_state.address = address
    st.session_state.private_key = private_key
    st.session_state.mnemonic = mnemonic
    st.session_state.balance = balance
    st.session_state.session_start = datetime.utcnow()
    
    wallet_data = {
        "address": address,
        "private_key": private_key,
        "mnemonic": mnemonic,
        "balance": balance
    }
    token = create_jwt_token(wallet_data)
    st.session_state.jwt_token = token
    
    try:
        set_cookie("wallet_token", token, max_age=SESSION_DURATION_MINUTES * 60)
    except:
        pass


def restore_from_token(token: str):
    """Restore wallet data from JWT token."""
    result = decode_jwt_token(token)
    if result.get("valid"):
        st.session_state.address = result["address"]
        st.session_state.private_key = result["private_key"]
        st.session_state.mnemonic = result["mnemonic"]
        st.session_state.balance = result["balance"]
        st.session_state.jwt_token = token
        
        exp_timestamp = result.get("exp")
        if exp_timestamp:
            session_duration = SESSION_DURATION_MINUTES * 60
            session_start = datetime.utcfromtimestamp(exp_timestamp) - timedelta(seconds=session_duration)
            st.session_state.session_start = session_start


def clear_wallet_data():
    """Clear wallet data from session and cookie."""
    st.session_state.address = None
    st.session_state.private_key = None
    st.session_state.mnemonic = None
    st.session_state.balance = 0.0
    st.session_state.jwt_token = None
    st.session_state.session_start = None
    
    try:
        set_cookie("wallet_token", "", max_age=0)
    except:
        pass


def check_session_expiry() -> bool:
    """Check if session has expired."""
    if st.session_state.get("session_start"):
        expiry = st.session_state.session_start + timedelta(minutes=SESSION_DURATION_MINUTES)
        if datetime.utcnow() > expiry:
            clear_wallet_data()
            return True
    return False


def update_balance(new_balance: float):
    """Update balance in session state."""
    st.session_state.balance = new_balance


def is_logged_in() -> bool:
    """Check if user is logged in."""
    return st.session_state.address is not None


def set_pending_transfer(transfer_data: dict):
    """Set pending transfer data in session state."""
    st.session_state.pending_transfer = transfer_data


def clear_pending_transfer():
    """Clear pending transfer from session state."""
    if hasattr(st.session_state, "pending_transfer"):
        del st.session_state.pending_transfer


def has_pending_transfer() -> bool:
    """Check if there's a pending transfer."""
    return hasattr(st.session_state, "pending_transfer")


def get_pending_transfer() -> dict:
    """Get pending transfer data."""
    return st.session_state.pending_transfer if has_pending_transfer() else None

