"""
Transaction Service
Handles all database operations for transactions.
This is where database persistence logic should live.
"""
from core.database import db_instance
from pymongo.errors import DuplicateKeyError
from models.transaction import Transaction
from typing import Optional, Dict, Any


class TransactionService:
    """Service for managing transaction persistence"""
    
    @staticmethod
    async def save_transaction(transaction: Transaction) -> Optional[Dict[str, Any]]:
        """
        Save a transaction to the database.
        Handles duplicate detection via unique index.
        
        Args:
            transaction: Transaction object to save
            
        Returns:
            Dict with transaction data including _id if successful, None if duplicate
        """
        # Convert Pydantic model to dict for MongoDB
        transaction_data = transaction.dict()
        
        try:
            result = await db_instance.db.transactions.insert_one(transaction_data)
            transaction_data['_id'] = result.inserted_id
            return transaction_data
            
        except DuplicateKeyError:
            # Transaction already exists (handled by unique index)
            return None
    
    @staticmethod
    async def create_indexes():
        """
        Create necessary indexes for the transactions collection.
        Should be called on application startup.
        """
        try:
            await db_instance.db.transactions.create_index(
                [("reference", 1), ("bank", 1)],
                unique=True,
                name="unique_reference_bank"
            )
            print("Created unique index on (reference, bank)")
        except Exception as e:
            # Index might already exist, that's okay
            print(f"Index creation note: {e}")
