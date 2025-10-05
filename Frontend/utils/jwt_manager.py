import jwt
import streamlit as st
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import base64

JWT_SECRET = "mock_wallet_secret_key_change_in_production"
JWT_ALGORITHM = "HS256"
SESSION_DURATION_MINUTES = 10
ENCRYPTION_KEY = b'mock_wallet_encryption_key_32bt'


def _get_encryption_key():
    """Get consistent encryption key."""
    key = base64.urlsafe_b64encode(ENCRYPTION_KEY.ljust(32)[:32])
    return key


def _encrypt_data(data: str) -> str:
    """Encrypt sensitive data."""
    fernet = Fernet(_get_encryption_key())
    return fernet.encrypt(data.encode()).decode()


def _decrypt_data(encrypted_data: str) -> str:
    """Decrypt sensitive data."""
    fernet = Fernet(_get_encryption_key())
    return fernet.decrypt(encrypted_data.encode()).decode()


def create_jwt_token(wallet_data: dict) -> str:
    """Create JWT token with encrypted wallet data."""
    encrypted_mnemonic = _encrypt_data(wallet_data["mnemonic"])
    encrypted_private_key = _encrypt_data(wallet_data["private_key"])
    
    payload = {
        "address": wallet_data["address"],
        "mnemonic": encrypted_mnemonic,
        "private_key": encrypted_private_key,
        "balance": wallet_data["balance"],
        "exp": datetime.utcnow() + timedelta(minutes=SESSION_DURATION_MINUTES),
        "iat": datetime.utcnow()
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_jwt_token(token: str) -> dict:
    """Decode JWT token and decrypt wallet data."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        decrypted_mnemonic = _decrypt_data(payload["mnemonic"])
        decrypted_private_key = _decrypt_data(payload["private_key"])
        
        return {
            "address": payload["address"],
            "mnemonic": decrypted_mnemonic,
            "private_key": decrypted_private_key,
            "balance": payload["balance"],
            "exp": payload.get("exp"),
            "valid": True
        }
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "Session expired"}
    except Exception as e:
        return {"valid": False, "error": str(e)}

