import random
import hashlib
from eth_account import Account
from fastapi import HTTPException

from utils.database import supabase
from utils.config import MIN_STARTING_BALANCE, MAX_STARTING_BALANCE
from utils.email_service import send_welcome_email

Account.enable_unaudited_hdwallet_features()


def hash_mnemonic(mnemonic: str) -> str:
    """Hash mnemonic using SHA-256 for secure storage."""
    return hashlib.sha256(mnemonic.encode()).hexdigest()


def create_wallet(email: str = None) -> dict:
    """Generate new HD wallet with mnemonic phrase."""
    try:
        account, mnemonic = Account.create_with_mnemonic()
        address = account.address.lower()
        starting_balance = round(random.uniform(MIN_STARTING_BALANCE, MAX_STARTING_BALANCE), 4)
        
        supabase.table("wallets").insert({
            "address": address,
            "balance": starting_balance,
            "email": email
        }).execute()
        
        supabase.table("mnemonic_hashes").insert({
            "wallet_address": address,
            "mnemonic_hash": hash_mnemonic(mnemonic)
        }).execute()
        
        if email:
            send_welcome_email(email, address)
        
        return {
            "mnemonic": mnemonic,
            "private_key": account.key.hex(),
            "address": address,
            "balance": starting_balance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating wallet: {str(e)}")


def import_wallet(mnemonic: str, email: str = None) -> dict:
    """Import wallet from mnemonic with hash verification."""
    try:
        account = Account.from_mnemonic(mnemonic)
        address = account.address.lower()
        
        response = supabase.table("wallets").select("*").ilike("address", address).execute()
        
        if response.data:
            hash_response = supabase.table("mnemonic_hashes").select("mnemonic_hash").ilike("wallet_address", address).execute()
            if hash_response.data and hash_response.data[0]["mnemonic_hash"] != hash_mnemonic(mnemonic):
                raise HTTPException(status_code=403, detail="Invalid mnemonic for this wallet")
            balance = float(response.data[0]["balance"])
            
            if email and not response.data[0].get("email"):
                supabase.table("wallets").update({"email": email}).ilike("address", address).execute()
        else:
            balance = round(random.uniform(MIN_STARTING_BALANCE, MAX_STARTING_BALANCE), 4)
            supabase.table("wallets").insert({
                "address": address,
                "balance": balance,
                "email": email
            }).execute()
            supabase.table("mnemonic_hashes").insert({
                "wallet_address": address,
                "mnemonic_hash": hash_mnemonic(mnemonic)
            }).execute()
        
        return {"address": address, "private_key": account.key.hex(), "balance": balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing wallet: {str(e)}")


def get_balance(address: str) -> float:
    """Get current balance for wallet address."""
    try:
        response = supabase.table("wallets").select("balance").ilike("address", address.lower()).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Wallet not found")
        return float(response.data[0]["balance"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching balance: {str(e)}")


def update_balance(address: str, new_balance: float):
    """Update wallet balance."""
    supabase.table("wallets").update({"balance": new_balance}).ilike("address", address.lower()).execute()


def create_wallet_if_not_exists(address: str, initial_balance: float):
    """Create wallet if it doesn't exist."""
    response = supabase.table("wallets").select("address").ilike("address", address.lower()).execute()
    if not response.data:
        supabase.table("wallets").insert({"address": address.lower(), "balance": initial_balance}).execute()

