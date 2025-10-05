from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.database import initialize_database
from routes import wallet_routes, transfer_routes, transaction_routes

app = FastAPI(
    title="Mock Web3 Wallet API",
    description="Backend API for Mock Web3 Wallet application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wallet_routes.router)
app.include_router(transfer_routes.router)
app.include_router(transaction_routes.router)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Mock Web3 Wallet API is running"}


@app.on_event("startup")
async def startup_event():
    print("\n" + "=" * 60)
    print("Mock Web3 Wallet API - Starting...")
    print("=" * 60)
    print("\nChecking database connection...")
    
    db_ready = initialize_database()
    
    if db_ready:
        print("\n✓ All database tables ready")
        print("✓ Application started successfully!")
    else:
        print("\n⚠️  Application started but database setup incomplete")
        print("   API will return errors until tables are created")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
