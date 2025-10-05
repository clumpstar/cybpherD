import streamlit as st
from datetime import datetime, timedelta
from api.wallet_api import get_balance
from utils.session_manager import clear_wallet_data, update_balance, check_session_expiry


def render_wallet_header():
    if check_session_expiry():
        st.error("Session expired. Please login again.")
        st.rerun()
        return
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.markdown(f"**Address:** `{st.session_state.address}`")
        st.markdown(f"**Balance:** {st.session_state.balance:.6f} ETH")
    
    with col2:
        if st.session_state.session_start:
            expiry = st.session_state.session_start + timedelta(minutes=10)
            remaining = expiry - datetime.utcnow()
            if remaining.total_seconds() > 0:
                minutes = int(remaining.total_seconds() // 60)
                seconds = int(remaining.total_seconds() % 60)
                st.markdown(f"**Session:** {minutes}m {seconds}s")
            else:
                st.markdown("**Session:** Expired")
    
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            success, result = get_balance(st.session_state.address)
            if success:
                update_balance(result)
                st.success("Balance refreshed!")
                st.rerun()
            else:
                st.error(result)
    
    with col4:
        if st.button("🚪 Logout", use_container_width=True):
            clear_wallet_data()
            st.rerun()
    
    st.markdown("---")
    
    with st.expander("🔐 View Mnemonic Phrase (Keep this safe!)", expanded=False):
        st.code(st.session_state.mnemonic, language=None)
        st.warning("⚠️ Never share your mnemonic phrase with anyone!")

