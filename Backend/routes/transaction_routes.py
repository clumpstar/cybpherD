from fastapi import APIRouter

from utils.models import Transaction, TransactionHistoryResponse
from services.transaction_service import get_transaction_history


router = APIRouter(prefix="/transaction", tags=["Transaction"])


@router.get("/history/{address}", response_model=TransactionHistoryResponse)
async def get_transaction_history_endpoint(address: str):
    """Get transaction history for a wallet address."""
    transactions_data = get_transaction_history(address)
    
    transactions = [Transaction(**tx) for tx in transactions_data]
    return TransactionHistoryResponse(transactions=transactions)

