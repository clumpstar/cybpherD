# Mock Web3 Wallet

A full-stack web3 wallet application built with FastAPI, Streamlit, and Supabase. Features secure wallet management, ETH/USD transfers with Skip API integration, cryptographic signing, and email notifications.

## 🎯 Features

- **Wallet Management**: Create new wallets or import existing ones using 12-word mnemonic phrases
- **Secure Storage**: SHA-256 hashed mnemonics stored in Supabase for verification
- **Dual Transfer Modes**: Send ETH directly or USD (converted to ETH via Skip API)
- **Real-time Balance**: Live balance updates and transaction history
- **Cryptographic Signing**: All transactions require signature verification
- **Slippage Protection**: 1% tolerance for USD transfers to protect against price fluctuations
- **Session Management**: JWT-based browser session with 10-minute auto-expiry
- **Email Notifications**: Automated emails for wallet creation and successful transfers
- **Input Validation**: Comprehensive sanitization and validation at frontend and backend

## 🏗️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Web3.py**: Ethereum wallet and signing
- **Supabase**: PostgreSQL database
- **Pydantic**: Data validation
- **Resend**: Email service

### Frontend
- **Streamlit**: Rapid UI development
- **JWT + Cryptography**: Secure session management
- **Web3.py**: Transaction signing

## 📁 Project Structure

```
cypherd_hackathon/
├── Backend/
│   ├── main.py                 # FastAPI entry point
│   ├── requirements.txt        # Backend dependencies
│   ├── CREATE_TABLES.sql       # Database schema
│   ├── routes/                 # API endpoints
│   │   ├── wallet_routes.py    # Wallet operations
│   │   ├── transfer_routes.py  # Transfer operations
│   │   └── transaction_routes.py # Transaction history
│   ├── services/               # Business logic
│   │   ├── wallet_service.py   # Wallet creation/import
│   │   ├── transfer_service.py # Transfer execution
│   │   ├── transaction_service.py # History queries
│   │   └── email_notification_service.py # Email logic
│   └── utils/                  # Utilities
│       ├── config.py           # Configuration
│       ├── database.py         # Supabase client
│       ├── models.py           # Pydantic models
│       └── email_service.py    # Resend integration
├── Frontend/
│   ├── app.py                  # Streamlit entry point
│   ├── requirements.txt        # Frontend dependencies
│   ├── components/             # UI components
│   │   ├── login_view.py       # Login/create/import UI
│   │   ├── wallet_header.py    # Wallet info display
│   │   ├── send_tab.py         # Transfer UI
│   │   └── history_tab.py      # Transaction history UI
│   ├── api/                    # Backend API clients
│   │   ├── wallet_api.py       # Wallet API calls
│   │   └── transfer_api.py     # Transfer API calls
│   └── utils/                  # Frontend utilities
│       ├── config.py           # Frontend config
│       ├── session_manager.py  # State management
│       ├── jwt_manager.py      # JWT encoding/decoding
│       └── crypto_utils.py     # Message signing
└── .env                        # Environment variables
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Supabase account
- Resend account (for emails)

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd cypherd_hackathon
```

### 2. Environment Variables
Create a `.env` file in the root directory:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key

# Email Configuration
RESEND_API_KEY=your_resend_api_key
```

**How to get credentials:**
- **Supabase**: Sign up at [supabase.com](https://supabase.com) → Create project → Settings → API
- **Resend**: Sign up at [resend.com](https://resend.com) → API Keys

### 3. Database Setup

**Go to your Supabase Dashboard:**
1. Click **SQL Editor** in the left sidebar
2. Click **New Query**
3. Open `Backend/CREATE_TABLES.sql` and copy all contents
4. Paste into the SQL Editor
5. Click **Run** (or press Ctrl+Enter)
6. Verify tables in **Table Editor** (wallets, mnemonic_hashes, transactions)

### 4. Backend Setup
```bash
cd Backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend will run at `http://localhost:8000`

### 5. Frontend Setup
Open a new terminal:
```bash
cd Frontend
pip install -r requirements.txt
streamlit run app.py
```

Frontend will open in your browser at `http://localhost:8501`

## 🎮 Usage Guide

### Creating a Wallet
1. Enter your email address
2. Click **Create Wallet**
3. **Save your 12-word mnemonic phrase** (you'll need it to import later)
4. Check your email for welcome notification

### Importing a Wallet
1. Enter your 12-word mnemonic phrase
2. (Optional) Enter email for notifications
3. Click **Import Wallet**

### Sending Transfers
1. Enter recipient address (0x...)
2. Enter amount
3. Choose **ETH** or **USD** mode
4. Click **Prepare Transfer**
5. Review the transaction details
6. Click **Confirm & Sign Transaction**
7. Check your email for transfer confirmation

### Viewing History
1. Click the **History** tab
2. See all sent and received transactions
3. Click any transaction to view details

## 🔒 Security Features

1. **Mnemonic Hashing**: SHA-256 hashed storage, never stores plaintext
2. **Signature Verification**: All transactions verified cryptographically
3. **Input Validation**: Multi-layer validation (frontend + backend)
4. **Email Validation**: RFC 5322 compliant email checking
5. **Address Validation**: Ethereum address format verification
6. **Slippage Protection**: 1% tolerance for USD transfers
7. **Balance Checks**: Pre-transfer and execution-time verification
8. **JWT Encryption**: Sensitive data encrypted in browser cookies
9. **Session Expiry**: 10-minute auto-logout
10. **CORS Protection**: Configured allowed origins
11. **Case-insensitive Lookups**: Prevents address casing issues
12. **SQL Injection Protection**: Parameterized queries via Supabase
13. **Error Handling**: Comprehensive try-catch blocks

## 🧪 Testing

### Manual Testing
1. **Create Wallet**: Verify mnemonic generation and balance assignment
2. **Import Wallet**: Test with the generated mnemonic
3. **ETH Transfer**: Send ETH to another address
4. **USD Transfer**: Send USD (tests Skip API integration)
5. **History**: Verify transaction records
6. **Session Expiry**: Wait 10 minutes, verify auto-logout
7. **Email**: Check for welcome and transfer emails

### API Endpoints
- `POST /wallet/create` - Create new wallet
- `POST /wallet/import` - Import existing wallet
- `GET /wallet/balance/{address}` - Get balance
- `POST /transfer/initiate` - Prepare transfer
- `POST /transfer/execute` - Execute transfer
- `GET /transaction/history/{address}` - Get history

## 📧 Email Notifications

Emails are sent for:
- **Wallet Creation**: Welcome email with wallet address
- **Transfer Success**: Confirmation with amount and recipient

**Test Email Setup:**
- Uses Resend's test domain: `onboarding@resend.dev`
- For production: Verify your domain in Resend dashboard

## 🐛 Troubleshooting

### "Wallet not found" error
- Database lookup issue has been fixed with case-insensitive queries
- If persists, verify wallet exists in Supabase Table Editor

### Email not sending
- Check `RESEND_API_KEY` in `.env`
- Verify API key is active in Resend dashboard
- Check backend terminal for debug logs

### Session expires immediately
- Check system time (JWT uses UTC)
- Clear browser cookies and restart frontend

### Skip API errors
- Fallback to mock ETH price ($3000) automatically
- Network issues are handled gracefully

## 📝 Notes

- **Mock Application**: This is a demo wallet, not for production use
- **Private Keys**: Stored in browser session only (10 min)
- **Mnemonics**: Never transmitted after wallet creation/import
- **Decimal Precision**: ETH (18 decimals), USDC (6 decimals)

## 🛠️ Development

### Adding Features
- Backend logic: `Backend/services/`
- API routes: `Backend/routes/`
- UI components: `Frontend/components/`
- Validation: `Backend/utils/models.py`

### Environment
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:8501`
- API Docs: `http://localhost:8000/docs`

## Demo

- **Home Screen: Wallet creation** :

![Wallet creation](readmeNeeds/Home.gif)

- **Home Screen Wallet Import** :

![Wallet Import](readmeNeeds/Home_mneo.gif)

- **Live Mail Notifications** :

![Mail Notifications](readmeNeeds/mail_show.gif)

- **Transaction** : [Sample Transaction Video](https://youtu.be/mYl_BzssQA0)

