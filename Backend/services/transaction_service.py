from fastapi import HTTPException
from typing import List

from utils.database import supabase


def get_transaction_history(address: str) -> List[dict]:
    """Get transaction history for wallet address."""
    try:
        address_lower = address.lower()
        response = supabase.table("transactions").select("*").or_(
            f"sender_address.ilike.{address_lower},recipient_address.ilike.{address_lower}"
        ).order("timestamp", desc=True).execute()
        
        return [{
            "id": tx["id"],
            "sender_address": tx["sender_address"],
            "recipient_address": tx["recipient_address"],
            "amount_eth": float(tx["amount_eth"]),
            "amount_usd": float(tx["amount_usd"]) if tx.get("amount_usd") else None,
            "timestamp": tx["timestamp"]
        } for tx in response.data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching transaction history: {str(e)}")

