from .base import BaseBankParser
from datetime import datetime
from models.transaction import Transaction


class AcmeParser(BaseBankParser):
    async def parse(self, line) -> Transaction:
        """
        Parse ACME Bank transaction line.
        Format: Amount//Reference//Date
        Example: 156,50//202506159000001//20250615
        
        Returns:
            Transaction object (not saved to database)
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
        
        # Build and return Transaction object (no database operations here)
        return Transaction(
            client_id="Dummy",  # TODO: Extract from webhook if available
            amount=amount,
            reference=reference,
            date=date,
            bank="Acme",
            metadata={}
        )
