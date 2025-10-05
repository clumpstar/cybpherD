import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")

SKIP_API_URL = "https://api.skip.build/v2/fungible/msgs_direct"
MOCK_ETH_PRICE_USD = 3000.0
MIN_STARTING_BALANCE = 1.0
MAX_STARTING_BALANCE = 10.0
SLIPPAGE_TOLERANCE_PERCENT = 1.0

