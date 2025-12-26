from pydantic import BaseModel
from typing import List

class TransactionRequest(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str

class TransactionResponse(TransactionRequest):
    status: str
    created_at: str
    processed_at: str


# sample payload
# {
# "transaction_id": "txn_abc123def456",
# "source_account": "acc_user_789",
# "destination_account": "acc_merchant_456",
# "amount": 1500,
# "currency": "INR"
# }