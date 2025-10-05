from supabase import create_client, Client
from utils.config import SUPABASE_URL, SUPABASE_ANON_KEY


# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def check_table_exists(table_name: str) -> bool:
    """Check if a table exists in the database."""
    try:
        supabase.table(table_name).select("*").limit(1).execute()
        return True
    except:
        return False


def initialize_database() -> bool:
    """
    Check if required tables exist and provide setup instructions if not.
    Returns True if all tables exist, False otherwise.
    """
    tables_exist = {
        "wallets": check_table_exists("wallets"),
        "transactions": check_table_exists("transactions")
    }
    
    # Print status
    for table, exists in tables_exist.items():
        status = "✓" if exists else "✗"
        print(f"{status} {table} table {'exists' if exists else 'not found'}")
    
    # If any table is missing, show setup instructions
    if not all(tables_exist.values()):
        print("\n" + "=" * 60)
        print("⚠️  DATABASE SETUP REQUIRED")
        print("=" * 60)
        print("\nSome tables are missing. Please run the setup script:")
        print("   python Backend/setup_database.py")
        print("\nOr manually create tables in Supabase SQL Editor:")
        print("\nCREATE TABLE IF NOT EXISTS wallets (")
        print("    address TEXT PRIMARY KEY,")
        print("    balance NUMERIC NOT NULL DEFAULT 0,")
        print("    created_at TIMESTAMPTZ DEFAULT NOW()")
        print(");")
        print("\nCREATE TABLE IF NOT EXISTS transactions (")
        print("    id BIGSERIAL PRIMARY KEY,")
        print("    sender_address TEXT NOT NULL,")
        print("    recipient_address TEXT NOT NULL,")
        print("    amount_eth NUMERIC NOT NULL,")
        print("    amount_usd NUMERIC,")
        print("    timestamp TIMESTAMPTZ DEFAULT NOW()")
        print(");")
        print("\n" + "=" * 60)
        return False
    
    return True

