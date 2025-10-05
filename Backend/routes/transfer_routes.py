from fastapi import APIRouter

from utils.models import (
    InitiateTransferRequest,
    InitiateTransferResponse,
    ExecuteTransferRequest,
    ExecuteTransferResponse
)
from services.transfer_service import initiate_transfer, execute_transfer


router = APIRouter(prefix="/transfer", tags=["Transfer"])


@router.post("/initiate", response_model=InitiateTransferResponse)
async def initiate_transfer_endpoint(request: InitiateTransferRequest):
    """Prepare a transfer and return approval message."""
    result = initiate_transfer(
        request.sender_address,
        request.recipient_address,
        request.amount,
        request.transfer_mode
    )
    return InitiateTransferResponse(**result)


@router.post("/execute", response_model=ExecuteTransferResponse)
async def execute_transfer_endpoint(request: ExecuteTransferRequest):
    """Execute a transfer after signature verification."""
    result = execute_transfer(
        request.sender_address,
        request.recipient_address,
        request.eth_amount,
        request.signed_message,
        request.approval_message,
        request.usd_amount
    )
    return ExecuteTransferResponse(**result)

