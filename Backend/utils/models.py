"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, List
import re


class WalletCreateRequest(BaseModel):
    email: EmailStr


class WalletCreateResponse(BaseModel):
    mnemonic: str
    private_key: str
    address: str
    balance: float


class WalletImportRequest(BaseModel):
    mnemonic: str
    email: Optional[EmailStr] = None
    
    @field_validator('mnemonic')
    @classmethod
    def validate_mnemonic(cls, v: str) -> str:
        words = v.strip().split()
        if len(words) != 12:
            raise ValueError('Mnemonic must be exactly 12 words')
        if not all(word.isalpha() and word.islower() for word in words):
            raise ValueError('Mnemonic must contain only lowercase letters')
        return v.strip()


class WalletImportResponse(BaseModel):
    address: str
    private_key: str
    balance: float


class BalanceResponse(BaseModel):
    address: str
    balance: float


# Transfer Models
class InitiateTransferRequest(BaseModel):
    sender_address: str = Field(min_length=42, max_length=42)
    recipient_address: str = Field(min_length=42, max_length=42)
    amount: float = Field(gt=0)
    transfer_mode: str = Field(pattern='^(ETH|USD)$')
    
    @field_validator('sender_address', 'recipient_address')
    @classmethod
    def validate_ethereum_address(cls, v: str) -> str:
        if not re.match(r'^0x[a-fA-F0-9]{40}$', v):
            raise ValueError('Invalid Ethereum address format')
        return v.lower()


class InitiateTransferResponse(BaseModel):
    approval_message: str
    eth_amount: float
    usd_amount: Optional[float] = None


class ExecuteTransferRequest(BaseModel):
    sender_address: str = Field(min_length=42, max_length=42)
    recipient_address: str = Field(min_length=42, max_length=42)
    eth_amount: float = Field(gt=0)
    signed_message: str
    approval_message: str = Field(min_length=10, max_length=500)
    usd_amount: Optional[float] = Field(default=None, gt=0)
    
    @field_validator('sender_address', 'recipient_address')
    @classmethod
    def validate_ethereum_address(cls, v: str) -> str:
        if not re.match(r'^0x[a-fA-F0-9]{40}$', v):
            raise ValueError('Invalid Ethereum address format')
        return v.lower()
    
    @field_validator('signed_message')
    @classmethod
    def validate_signature(cls, v: str) -> str:
        if not v.startswith('0x'):
            v = '0x' + v
        if not re.match(r'^0x[a-fA-F0-9]{130}$', v):
            raise ValueError('Invalid signature format')
        return v


class ExecuteTransferResponse(BaseModel):
    success: bool
    message: str
    transaction_id: Optional[int] = None


# Transaction Models
class Transaction(BaseModel):
    id: int
    sender_address: str
    recipient_address: str
    amount_eth: float
    amount_usd: Optional[float]
    timestamp: str


class TransactionHistoryResponse(BaseModel):
    transactions: List[Transaction]

