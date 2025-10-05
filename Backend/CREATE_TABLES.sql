-- ============================================================
-- Mock Web3 Wallet - Database Setup
-- ============================================================
-- 
-- INSTRUCTIONS:
-- 1. Go to your Supabase Dashboard
-- 2. Click "SQL Editor" in the left sidebar
-- 3. Click "New Query"
-- 4. Copy and paste this entire file
-- 5. Click "Run" or press Ctrl+Enter
-- 6. Verify tables in "Table Editor"
--
-- ============================================================

-- Create wallets table
-- Stores wallet addresses and their ETH balances
CREATE TABLE IF NOT EXISTS wallets (
    address TEXT PRIMARY KEY,
    balance NUMERIC NOT NULL DEFAULT 0,
    email TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create mnemonic_hashes table
-- Stores hashed mnemonics for verification
CREATE TABLE IF NOT EXISTS mnemonic_hashes (
    id BIGSERIAL PRIMARY KEY,
    wallet_address TEXT NOT NULL REFERENCES wallets(address) ON DELETE CASCADE,
    mnemonic_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(wallet_address)
);

-- Create transactions table
-- Stores all transfer history
CREATE TABLE IF NOT EXISTS transactions (
    id BIGSERIAL PRIMARY KEY,
    sender_address TEXT NOT NULL,
    recipient_address TEXT NOT NULL,
    amount_eth NUMERIC NOT NULL,
    amount_usd NUMERIC,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_transactions_sender 
    ON transactions(sender_address);

CREATE INDEX IF NOT EXISTS idx_transactions_recipient 
    ON transactions(recipient_address);

CREATE INDEX IF NOT EXISTS idx_transactions_timestamp 
    ON transactions(timestamp DESC);

-- ============================================================
-- Verification Queries (Optional - run these to test)
-- ============================================================

-- Check if tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('wallets', 'transactions');

-- Count rows in each table
SELECT 
    (SELECT COUNT(*) FROM wallets) as wallet_count,
    (SELECT COUNT(*) FROM transactions) as transaction_count;

-- ============================================================
-- Done! Now you can start the backend server:
--   cd Backend
--   uvicorn main:app --reload
-- ============================================================

