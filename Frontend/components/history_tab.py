import streamlit as st
from api.transfer_api import get_transaction_history


def render_history_tab():
    st.markdown("### Transaction History")
    
    if st.button("🔄 Refresh History"):
        st.rerun()
    
    success, result = get_transaction_history(st.session_state.address)
    
    if success:
        if len(result) == 0:
            st.info("No transactions yet")
        else:
            for tx in result:
                render_transaction(tx)
    else:
        st.error(result)


def render_transaction(tx: dict):
    is_outgoing = tx["sender_address"].lower() == st.session_state.address.lower()
    usd_part = f" (${tx['amount_usd']:.2f} USD)" if tx['amount_usd'] else ""
    title = f"{'📤 Sent' if is_outgoing else '📥 Received'} {tx['amount_eth']:.6f} ETH{usd_part} - {tx['timestamp'][:19].replace('T', ' ')}"
    
    with st.expander(title):
        st.markdown(f"**Transaction ID:** {tx['id']}")
        st.markdown(f"**From:** `{tx['sender_address']}`")
        st.markdown(f"**To:** `{tx['recipient_address']}`")
        st.markdown(f"**Amount:** {tx['amount_eth']:.6f} ETH")
        if tx['amount_usd']:
            st.markdown(f"**USD Value:** ${tx['amount_usd']:.2f}")
        st.markdown(f"**Timestamp:** {tx['timestamp']}")

