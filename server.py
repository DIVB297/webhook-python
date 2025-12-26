from contextlib import asynccontextmanager
from datetime import datetime
from anyio import sleep
from fastapi import FastAPI, BackgroundTasks
from mongodb import Mongodb
import uvicorn
import os
from dotenv import load_dotenv
from transactions import TransactionRequest, TransactionResponse

# Load environment variables from .env file
load_dotenv()


MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "webhook_db")
MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "transactions")
db = None

async def process_transaction_after_delay(transaction_id: str):
    """Background task to update transaction status after 30 seconds delay"""
    await sleep(30)
    update_data = {
        "status": "PROCESSED",
        "processed_at": datetime.now().isoformat() + "Z"
    }
    await db.update_transaction(transaction_id, update_data)
    print(f"Transaction {transaction_id} updated to PROCESSED status")

@asynccontextmanager
async def startup_event(app: FastAPI):
    # Code to run on startup
    global db
    mongodb = Mongodb(MONGODB_CONNECTION_STRING, MONGODB_DB_NAME, MONGODB_COLLECTION_NAME)
    db = mongodb
    yield
    # Code to run on shutdown (if needed)

app = FastAPI(
    lifespan=startup_event
)

@app.get("/")
def read_root():
    current_time = datetime.now().isoformat() + "Z"
    return {"status": "healthy", "current_time": current_time}

@app.post("/v1/webhooks/transactions")
async def handle_webhook(payload: TransactionRequest, background_tasks: BackgroundTasks):
    # Process the incoming webhook payload
    try:
        data = {
            **payload.model_dump(),
            "status": "PROCESSING",
            "processed_at": None
        }
        already_exist = await db.get_transaction(payload.transaction_id)
        print("already_exist:", already_exist)
        if already_exist is not None:
            return {"status": already_exist["status"], "message": f"Transaction already {already_exist['status']}"}
        await db.insert_transaction(data)
        
        # Add background task to update status after 30 seconds
        background_tasks.add_task(process_transaction_after_delay, payload.transaction_id)
        
        # Return immediate response
        return {"status": "PROCESSING", "message": "Transaction processing..."}
    except Exception as e:
        return {"status":"failed", "message": "Something went wrong", "error": str(e)}

@app.get("/v1/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    try:
        transaction = await db.get_transaction(transaction_id)
        if not transaction:
            return {"status": "error", "message": "Transaction not found"}
        return {"status": "success", "data": transaction}
    except Exception as e:
        return {"status":"failed", "message": "Something went wrong", "error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)