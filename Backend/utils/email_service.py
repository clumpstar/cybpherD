import resend
from typing import Optional
from utils.config import RESEND_API_KEY

resend.api_key = RESEND_API_KEY


def send_transfer_email(to_email: str, amount: float, currency: str, recipient_address: str, 
                       sender_address: str, usd_amount: Optional[float] = None) -> bool:
    """Send email notification for successful transfer."""
    if not resend.api_key:
        print(f"⚠️  RESEND_API_KEY not configured. Email not sent.")
        return False
    
    if not to_email:
        print(f"⚠️  No email address provided. Email not sent.")
        return False
    
    try:
        print(f"📧 Sending transfer email to {to_email}...")
        if currency == "USD" and usd_amount:
            amount_text = f"${usd_amount:.2f} USD ({amount:.6f} ETH)"
        else:
            amount_text = f"{amount:.6f} ETH"
        
        params = {
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": "✅ Transfer Successful",
            "html": f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px 10px 0 0;">
                        <h1 style="color: white; margin: 0;">✅ Transfer Successful</h1>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px;">
                        <p style="font-size: 16px; color: #374151;">Your transfer has been completed successfully!</p>
                        
                        <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #10b981;">
                            <p style="margin: 10px 0;"><strong>Amount:</strong> {amount_text}</p>
                            <p style="margin: 10px 0;"><strong>To:</strong> <code style="background: #e5e7eb; padding: 4px 8px; border-radius: 4px;">{recipient_address[:10]}...{recipient_address[-8:]}</code></p>
                            <p style="margin: 10px 0;"><strong>From:</strong> <code style="background: #e5e7eb; padding: 4px 8px; border-radius: 4px;">{sender_address[:10]}...{sender_address[-8:]}</code></p>
                        </div>
                        
                        <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
                            This is an automated message from Mock Web3 Wallet. Please do not reply to this email.
                        </p>
                    </div>
                </body>
            </html>
            """
        }
        
        r = resend.Emails.send(params)
        print(f"✅ Transfer email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Email send error: {str(e)}")
        return False


def send_welcome_email(to_email: str, address: str) -> bool:
    """Send welcome email when wallet is created."""
    if not resend.api_key:
        print(f"⚠️  RESEND_API_KEY not configured. Email not sent.")
        return False
    
    if not to_email:
        print(f"⚠️  No email address provided. Email not sent.")
        return False
    
    try:
        print(f"📧 Sending welcome email to {to_email}...")
        params = {
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": "🎉 Welcome to Mock Web3 Wallet",
            "html": f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px 10px 0 0;">
                        <h1 style="color: white; margin: 0;">🎉 Welcome to Mock Web3 Wallet</h1>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px;">
                        <p style="font-size: 16px; color: #374151;">Your wallet has been created successfully!</p>
                        
                        <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3b82f6;">
                            <p style="margin: 10px 0;"><strong>Your Wallet Address:</strong></p>
                            <code style="background: #e5e7eb; padding: 8px 12px; border-radius: 4px; display: block; word-break: break-all;">{address}</code>
                        </div>
                        
                        <p style="color: #374151; margin: 20px 0;">
                            ⚠️ <strong>Important Security Reminder:</strong>
                        </p>
                        <ul style="color: #6b7280;">
                            <li>Never share your mnemonic phrase with anyone</li>
                            <li>Keep your private key secure</li>
                            <li>Enable two-factor authentication if available</li>
                        </ul>
                        
                        <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
                            This is an automated message from Mock Web3 Wallet. Please do not reply to this email.
                        </p>
                    </div>
                </body>
            </html>
            """
        }
        
        r = resend.Emails.send(params)
        print(f"✅ Welcome email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Email send error: {str(e)}")
        return False

