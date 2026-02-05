from .base import BaseBankParser
from core.database import db_instance
from pymongo.errors import DuplicateKeyError
from datetime import datetime

class AcmeParser(BaseBankParser):
    async def parse(self, line):
        """
        Parse ACME Bank transaction line.
        Format: Amount//Reference//Date
        Example: 156,50//202506159000001//20250615
        """
        # Split by "//" delimiter
        parts = line.split('//')
        
        if len(parts) != 3:
            raise ValueError(f"Invalid ACME format: expected 3 parts separated by '//', got {len(parts)}")
        
        # Extract and parse amount (comma as decimal separator)
        amount_str = parts[0].strip()
        amount = float(amount_str.replace(',', '.'))
        
        # Extract reference
        reference = parts[1].strip()
        
        # Extract and parse date (YYYYMMDD format)
        date_str = parts[2].strip()
        date = datetime.strptime(date_str, "%Y%m%d")
        
        # Build transaction data
        transaction_data = {
            "client_id": "Dummy",
            "amount": amount,
            "reference": reference,
            "date": date,
            "bank": "Acme",
            "metadata": {}
        }
        
        try:
            result = await db_instance.db.transactions.insert_one(transaction_data)
            print(result.inserted_id)
            print(transaction_data)
            return transaction_data
            
        except DuplicateKeyError:
            print(f"Duplicate found: {reference}")
            return None
