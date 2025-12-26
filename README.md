# Webhook Python API

A FastAPI-based webhook service for handling transaction data with MongoDB Atlas integration.

## Features

- **Transaction Webhook**: Receive and process transaction data
- **Transaction Lookup**: Retrieve transaction details by ID
- **Health Check**: Monitor API status
- **MongoDB Atlas Integration**: Cloud-based data storage
- **Async Processing**: Non-blocking transaction handling(Background tasks)

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
cd /Users/macair/Divansh/Project/webhook-python
```

### 2. Create and Activate Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root with your MongoDB Atlas credentials:
```env
MONGODB_CONNECTION_STRING=mongodb+srv://your_username:your_password@cluster0.xxxxx.mongodb.net/
MONGODB_DB_NAME=webhook_db
MONGODB_COLLECTION_NAME=transactions
```

### 5. Run the Application
```bash
# Using the virtual environment
/Users/macair/Divansh/Project/webhook-python/venv/bin/python server.py

# Or if virtual environment is activated
python server.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### 1. Health Check
**GET** `/`

Check if the API is running and healthy.

You can also run on "https://localhost:8000/docs

```bash
curl -X GET "http://localhost:8000/"
```

**Response:**
```json
{
  "status": "healthy",
  "current_time": "2025-12-26T10:30:45.123456Z"
}
```

### 2. Create Transaction Webhook
**POST** `/v1/webhooks/transactions`

Process incoming transaction webhook data.

```bash
curl -X POST "http://localhost:8000/v1/webhooks/transactions" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_abc123def456",
    "source_account": "acc_user_789",
    "destination_account": "acc_merchant_456",
    "amount": 1500,
    "currency": "INR"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Transaction processing...",
  "transaction_id": "507f1f77bcf86cd799439011"
}
```

### 3. Get Transaction Details
**GET** `/v1/transactions/{transaction_id}`

Retrieve transaction details by MongoDB ObjectId.

```bash
curl -X GET "http://localhost:8000/v1/transactions/507f1f77bcf86cd799439011"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "transaction_id": "txn_abc123def456",
    "source_account": "acc_user_789",
    "destination_account": "acc_merchant_456",
    "amount": 1500,
    "currency": "INR",
    "status": "PROCESSED",
    "processed_at": "2025-12-26T10:31:15.123456Z"
  }
}
```

**Error Response (Transaction not found):**
```json
{
  "status": "error",
  "message": "Transaction not found"
}
```

## Sample Transaction Payload

```json
{
  "transaction_id": "txn_abc123def456",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500,
  "currency": "INR"
}
```

## Testing Workflow

1. **Start the server:**
   ```bash
   source venv/bin/activate
   python server.py
   ```

2. **Test health endpoint:**
   ```bash
   curl -X GET "http://localhost:8000/"
   ```

3. **Create a transaction:**
   ```bash
   curl -X POST "http://localhost:8000/v1/webhooks/transactions" \
     -H "Content-Type: application/json" \
     -d '{
       "transaction_id": "txn_test123",
       "source_account": "acc_user_001",
       "destination_account": "acc_merchant_002",
       "amount": 2500,
       "currency": "INR"
     }'
   ```

4. **Copy the `transaction_id` from the response and retrieve the transaction:**
   ```bash
   curl -X GET "http://localhost:8000/v1/transactions/YOUR_TRANSACTION_ID_HERE"
   ```

## Project Structure

```
webhook-python/
├── server.py              # Main FastAPI application
├── mongodb.py             # MongoDB connection and operations
├── transactions.py        # Pydantic models for request/response
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (MongoDB credentials)
├── venv/                 # Virtual environment
└── README.md             # This file
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **uvicorn**: ASGI server for running FastAPI
- **pydantic**: Data validation and parsing
- **pymongo**: MongoDB driver for Python
- **python-dotenv**: Load environment variables from .env file
- **anyio**: Async I/O operations

## Transaction Processing

1. When a webhook is received, the transaction is initially stored with status `"PROCESSING"`
2. The transaction is immediately updated to status `"PROCESSED"` with a timestamp
3. Both the creation and processing timestamps are stored in ISO format

## Environment Variables

- `MONGODB_CONNECTION_STRING`: MongoDB Atlas connection string
- `MONGODB_DB_NAME`: Database name (default: webhook_db)
- `MONGODB_COLLECTION_NAME`: Collection name (default: transactions)

## Notes

- The application uses MongoDB Atlas for cloud-based data storage
- All timestamps are in UTC ISO format
- Transaction IDs returned by the API are MongoDB ObjectIds
- The original `transaction_id` from the payload is preserved in the stored document
