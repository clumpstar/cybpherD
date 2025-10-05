"""
Send transaction tab component.
"""

import streamlit as st
from api.transfer_api import initiate_transfer, execute_transfer
from api.wallet_api import get_balance
from utils.session_manager import (
    set_pending_transfer, 
    clear_pending_transfer, 
    has_pending_transfer, 
    get_pending_transfer,
    update_balance
)
from utils.crypto_utils import sign_message


def render_send_tab():
    """Render the send transaction tab."""
    st.markdown("### Send Transaction")
    
    # Transfer Form
    with st.form("transfer_form"):
        recipient = st.text_input(
            "Recipient Address",
            placeholder="0x..."
        )
        
        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=0.001,
            format="%.6f"
        )
        
        transfer_mode = st.radio(
            "Transfer Mode",
            options=["ETH", "USD"],
            horizontal=True
        )
        
        submit_prepare = st.form_submit_button("Prepare Transfer", use_container_width=True)
    
    if submit_prepare:
        import re
        
        if not recipient or not recipient.strip():
            st.error("Recipient address is required")
        elif not re.match(r'^0x[a-fA-F0-9]{40}$', recipient.strip()):
            st.error("Invalid Ethereum address format")
        elif amount <= 0:
            st.error("Amount must be greater than 0")
        elif amount > 1000000:
            st.error("Amount too large")
        else:
            with st.spinner("Preparing transfer..."):
                success, result = initiate_transfer(
                    st.session_state.address,
                    recipient,
                    amount,
                    transfer_mode
                )
                
                if success:
                    transfer_data = {
                        "recipient": recipient,
                        "eth_amount": result["eth_amount"],
                        "usd_amount": result.get("usd_amount"),
                        "approval_message": result["approval_message"]
                    }
                    set_pending_transfer(transfer_data)
                    st.info(f"📋 **Approval Message:**\n\n{result['approval_message']}")
                    st.rerun()
                else:
                    st.error(result)
    
    # Show confirmation if transfer is pending
    if has_pending_transfer():
        render_pending_transfer()


def render_pending_transfer():
    """Render the pending transfer confirmation section."""
    pending = get_pending_transfer()
    
    st.markdown("---")
    
    # Add blinking red background alert
    st.markdown("""
        <style>
        @keyframes blink {
            0% { background-color: #ff4444; opacity: 0.3; }
            50% { background-color: #ff0000; opacity: 0.6; }
            100% { background-color: #ff4444; opacity: 0.3; }
        }
        .alert-box {
            animation: blink 1.5s infinite;
            padding: 20px;
            border-radius: 10px;
            border: 3px solid #ff0000;
            margin: 20px 0;
        }
        .alert-text {
            color: #ffffff;
            font-weight: bold;
            font-size: 18px;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        </style>
        <div class="alert-box">
            <div class="alert-text">⚠️ ACTION REQUIRED: SIGN TRANSACTION ⚠️</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info(f"📋 **Pending Transfer:**\n\n{pending['approval_message']}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("✅ Confirm & Sign Transaction", use_container_width=True, type="primary"):
            with st.spinner("Signing and executing transfer..."):
                # Sign the message
                signature = sign_message(
                    pending["approval_message"],
                    st.session_state.private_key
                )
                
                # Execute transfer
                success, result = execute_transfer(
                    st.session_state.address,
                    pending["recipient"],
                    pending["eth_amount"],
                    signature,
                    pending["approval_message"],
                    pending.get("usd_amount")
                )
                
                if success:
                    st.success(f"✅ {result['message']}")
                    clear_pending_transfer()
                    
                    # Refresh balance
                    success_balance, new_balance = get_balance(st.session_state.address)
                    if success_balance:
                        update_balance(new_balance)
                    
                    st.rerun()
                else:
                    st.error(result)
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            clear_pending_transfer()
            st.rerun()

