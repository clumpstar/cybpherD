import requests
from fastapi import HTTPException
from web3 import Web3
from eth_account.messages import encode_defunct

from utils.database import supabase
from utils.config import SKIP_API_URL, MOCK_ETH_PRICE_USD, SLIPPAGE_TOLERANCE_PERCENT
from services.wallet_service import get_balance, update_balance, create_wallet_if_not_exists
from services.email_notification_service import notify_transfer_complete

w3 = Web3()


def get_usd_to_eth_conversion(usd_amount: float) -> float:
    """Get ETH equivalent for USD amount using Skip API with fallback."""
    try:
        amount_in = str(int(usd_amount * 1_000_000))
        
        payload = {
            "source_asset_denom": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "source_asset_chain_id": "1",
            "dest_asset_denom": "ethereum-native",
            "dest_asset_chain_id": "1",
            "amount_in": amount_in,
            "chain_ids_to_addresses": {"1": "0x0000000000000000000000000000000000000000"},
            "slippage_tolerance_percent": str(SLIPPAGE_TOLERANCE_PERCENT),
            "smart_swap_options": {"evm_swaps": True},
            "allow_unsafe": False
        }
        
        response = requests.post(SKIP_API_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        
        if response.status_code == 200:
            amount_out = int(response.json().get("route", {}).get("amount_out", "0"))
            return float(amount_out) / 1e18
        return usd_amount / MOCK_ETH_PRICE_USD
    except:
        return usd_amount / MOCK_ETH_PRICE_USD


def initiate_transfer(sender_address: str, recipient_address: str, amount: float, transfer_mode: str) -> dict:
    """Prepare transfer and return approval message after balance check."""
    try:
        eth_amount = amount
        usd_amount = None
        
        if transfer_mode == 'USD':
            eth_amount = round(get_usd_to_eth_conversion(amount), 6)
            usd_amount = amount
            approval_message = f"Send {eth_amount} ETH (${usd_amount} USD) to {recipient_address}"
        else:
            eth_amount = round(amount, 6)
            approval_message = f"Send {eth_amount} ETH to {recipient_address}"
        
        sender_balance = get_balance(sender_address)
        if sender_balance < eth_amount:
            raise HTTPException(status_code=400, detail=f"Insufficient balance. You have {sender_balance:.6f} ETH, need {eth_amount:.6f} ETH")
        
        return {"approval_message": approval_message, "eth_amount": eth_amount, "usd_amount": usd_amount}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initiating transfer: {str(e)}")


def verify_signature(message: str, signature: str, expected_address: str) -> bool:
    """Verify cryptographic signature matches expected address."""
    try:
        recovered_address = w3.eth.account.recover_message(encode_defunct(text=message), signature=signature)
        if recovered_address.lower() != expected_address.lower():
            raise HTTPException(status_code=403, detail="Signature verification failed")
        return True
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Signature verification failed: {str(e)}")


def check_slippage(original_usd_amount: float, original_eth_amount: float) -> bool:
    """Check if price changed significantly for USD transfers (slippage protection)."""
    try:
        new_eth_amount = get_usd_to_eth_conversion(original_usd_amount)
        price_diff_percent = abs(new_eth_amount - original_eth_amount) / original_eth_amount * 100
        
        if price_diff_percent > SLIPPAGE_TOLERANCE_PERCENT:
            raise HTTPException(status_code=400, detail=f"Price changed {price_diff_percent:.2f}%. Please try again.")
        return True
    except HTTPException:
        raise
    except:
        return True


def execute_transfer(sender_address: str, recipient_address: str, eth_amount: float, 
                     signed_message: str, approval_message: str, usd_amount: float = None) -> dict:
    """Execute transfer after signature verification and security checks."""
    try:
        verify_signature(approval_message, signed_message, sender_address)
        
        if usd_amount is not None:
            check_slippage(usd_amount, eth_amount)
        
        sender_balance = get_balance(sender_address)
        if sender_balance < eth_amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        
        update_balance(sender_address, sender_balance - eth_amount)
        
        try:
            recipient_balance = get_balance(recipient_address)
            update_balance(recipient_address, recipient_balance + eth_amount)
        except HTTPException as e:
            if e.status_code == 404:
                create_wallet_if_not_exists(recipient_address, eth_amount)
            else:
                raise
        
        transaction_response = supabase.table("transactions").insert({
            "sender_address": sender_address,
            "recipient_address": recipient_address,
            "amount_eth": eth_amount,
            "amount_usd": usd_amount
        }).execute()
        
        notify_transfer_complete(sender_address, recipient_address, eth_amount, usd_amount)
        
        return {
            "success": True,
            "message": "Transfer completed successfully",
            "transaction_id": transaction_response.data[0]["id"] if transaction_response.data else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing transfer: {str(e)}")

