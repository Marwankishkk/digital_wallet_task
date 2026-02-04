from .base import BaseBankParser
from core.database import db_instance
from pymongo.errors import DuplicateKeyError
from datetime import datetime

class PayTechParser(BaseBankParser):
    async def  parse(self, line):
        # Example implementation for PayTech transaction parsing
        parts=line.split('#')
        date=parts[0][:8]
        date = datetime.strptime(date, "%Y%m%d")
        print(date)
        amount=float(parts[0][8:].replace(',','.'))
        reference=parts[1]
        # existing_transaction = await db_instance.db.transactions.find_one({"reference": reference})
        # if existing_transaction is not None:
        #     print(f"Duplicate found: {reference}")
        #     return None
        metadata_parts=parts[2]
        metadata_parts=metadata_parts.split('/')
        meta_data={}
        for i in range(0,len(metadata_parts)-1,2):
            key=metadata_parts[i]
            value=metadata_parts[i+1]
            meta_data[key]=value
        transaction_data = {
            "amount": amount,
            "reference": reference,
            "date": date,
            "bank": "PayTech",
            "metadata": meta_data
        }
   
        try:
            result = await db_instance.db.transactions.insert_one(transaction_data)
            print(result.inserted_id)
            return transaction_data

        except DuplicateKeyError:
            print(f"Duplicate found: {reference}")
            return None
