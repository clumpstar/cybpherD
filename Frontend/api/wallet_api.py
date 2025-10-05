import requests
from utils.config import BACKEND_URL


def create_wallet(email: str):
    try:
        response = requests.post(f"{BACKEND_URL}/wallet/create", json={"email": email})
        if response.status_code == 200:
            return True, response.json()
        return False, f"Error: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return False, f"Error creating wallet: {str(e)}"


def import_wallet(mnemonic: str, email: str = None):
    try:
        payload = {"mnemonic": mnemonic}
        if email:
            payload["email"] = email
            
        response = requests.post(f"{BACKEND_URL}/wallet/import", json=payload)
        if response.status_code == 200:
            return True, response.json()
        return False, f"Error: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return False, f"Error importing wallet: {str(e)}"


def get_balance(address: str):
    try:
        response = requests.get(f"{BACKEND_URL}/wallet/balance/{address}")
        if response.status_code == 200:
            return True, response.json()["balance"]
        return False, f"Error: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return False, f"Error refreshing balance: {str(e)}"

