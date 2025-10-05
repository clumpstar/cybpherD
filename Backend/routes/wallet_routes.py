from fastapi import APIRouter

from utils.models import (
    WalletCreateRequest,
    WalletCreateResponse,
    WalletImportRequest,
    WalletImportResponse,
    BalanceResponse
)
from services.wallet_service import create_wallet, import_wallet, get_balance


router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.post("/create", response_model=WalletCreateResponse)
async def create_wallet_endpoint(request: WalletCreateRequest):
    """Generate a new wallet with mnemonic phrase."""
    result = create_wallet(request.email)
    return WalletCreateResponse(**result)


@router.post("/import", response_model=WalletImportResponse)
async def import_wallet_endpoint(request: WalletImportRequest):
    """Import an existing wallet using mnemonic phrase."""
    result = import_wallet(request.mnemonic, request.email)
    return WalletImportResponse(**result)


@router.get("/balance/{address}", response_model=BalanceResponse)
async def get_balance_endpoint(address: str):
    """Get the current balance for a wallet address."""
    balance = get_balance(address)
    return BalanceResponse(address=address, balance=balance)

