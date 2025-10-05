"""
Cryptographic utilities for signing transactions.
"""

from web3 import Web3
from eth_account.messages import encode_defunct

# Initialize Web3
w3 = Web3()


def sign_message(message: str, private_key: str) -> str:
    """
    Sign a message with a private key.
    Returns: signature as hex string with 0x prefix
    """
    encoded_message = encode_defunct(text=message)
    signed_message = w3.eth.account.sign_message(encoded_message, private_key=private_key)
    signature = signed_message.signature.hex()
    if not signature.startswith('0x'):
        signature = '0x' + signature
    return signature

