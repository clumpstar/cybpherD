from utils.database import supabase
from utils.email_service import send_transfer_email


def get_wallet_email(address: str) -> str:
    """Get email associated with wallet address."""
    try:
        response = supabase.table("wallets").select("email").ilike("address", address.lower()).execute()
        if response.data and response.data[0].get("email"):
            email = response.data[0]["email"]
            print(f"📧 Found email for {address[:10]}...{address[-8:]}: {email}")
            return email
        print(f"⚠️  No email found for {address[:10]}...{address[-8:]}")
        return None
    except Exception as e:
        print(f"❌ Error fetching email: {str(e)}")
        return None


def notify_transfer_complete(sender_address: str, recipient_address: str, 
                            eth_amount: float, usd_amount: float = None):
    """Send email notification to sender about completed transfer."""
    try:
        print(f"\n🔔 Attempting to send transfer notification...")
        sender_email = get_wallet_email(sender_address)
        if sender_email:
            currency = "USD" if usd_amount else "ETH"
            send_transfer_email(
                to_email=sender_email,
                amount=eth_amount,
                currency=currency,
                recipient_address=recipient_address,
                sender_address=sender_address,
                usd_amount=usd_amount
            )
        else:
            print(f"⚠️  No email configured for sender. Skipping notification.")
    except Exception as e:
        print(f"❌ Email notification error: {str(e)}")

