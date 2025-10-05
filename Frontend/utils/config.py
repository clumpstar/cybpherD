"""
Frontend configuration settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page Configuration
PAGE_TITLE = "Mock Web3 Wallet"
PAGE_ICON = "💰"
LAYOUT = "wide"

