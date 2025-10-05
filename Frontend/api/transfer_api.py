import requests
from utils.config import BACKEND_URL


def initiate_transfer(sender_address: str, recipient_address: str, amount: float, transfer_mode: str):
    """Initiate transfer via API. Returns: (success: bool, data_or_message: dict/str)"""
    try:
        response = requests.post(f"{BACKEND_URL}/transfer/initiate", json={
            "sender_address": sender_address,
            "recipient_address": recipient_address,
            "amount": amount,
            "transfer_mode": transfer_mode
        })
        
        if response.status_code == 200:
            return True, response.json()
        return False, f"Error: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return False, f"Error preparing transfer: {str(e)}"


def execute_transfer(sender_address: str, recipient_address: str, eth_amount: float, 
                     signed_message: str, approval_message: str, usd_amount: float = None):
    """Execute transfer via API. Returns: (success: bool, data_or_message: dict/str)"""
    try:
        response = requests.post(f"{BACKEND_URL}/transfer/execute", json={
            "sender_address": sender_address,
            "recipient_address": recipient_address,
            "eth_amount": eth_amount,
            "signed_message": signed_message,
            "approval_message": approval_message,
            "usd_amount": usd_amount
        })
        
        if response.status_code == 200:
            return True, response.json()
        return False, f"Error: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return False, f"Error executing transfer: {str(e)}"


def get_transaction_history(address: str):
    """Get transaction history via API. Returns: (success: bool, transactions_or_message: list/str)"""
    try:
        response = requests.get(f"{BACKEND_URL}/transaction/history/{address}")
        
        if response.status_code == 200:
            return True, response.json()["transactions"]
        return False, f"Error: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return False, f"Error fetching transaction history: {str(e)}"

