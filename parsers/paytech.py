from .base import BaseBankParser
from datetime import datetime
from models.transaction import Transaction


class PayTechParser(BaseBankParser):
    async def parse(self, line) -> Transaction:
        """
        Parse PayTech Bank transaction line.
        Format: DateAmount#Reference#Key/Value/Key/Value...
        Example: 20250615156,50#202506159000001#note/debt payment march/internal_reference/A462JE81
        
        Returns:
            Transaction object (not saved to database)
        """
        parts = line.split('#')
        
        if len(parts) != 3:
            raise ValueError(f"Invalid PayTech format: expected 3 parts separated by '#', got {len(parts)}")
        
        # Extract date (first 8 characters: YYYYMMDD)
        date_str = parts[0][:8]
        if len(date_str) < 8:
            raise ValueError(f"Invalid PayTech format: date string too short, got '{date_str}'")
        
        date = datetime.strptime(date_str, "%Y%m%d")
        
        # Extract amount (remaining characters after date)
        amount_str = parts[0][8:].replace(',', '.')
        amount = float(amount_str)
        
        # Extract reference
        reference = parts[1].strip()
        
        # Parse metadata (key/value pairs separated by '/')
        metadata_parts = parts[2].split('/')
        meta_data = {}
        for i in range(0, len(metadata_parts) - 1, 2):
            key = metadata_parts[i]
            value = metadata_parts[i + 1]
            meta_data[key] = value
        
        # Build and return Transaction object (no database operations here)
        return Transaction(
            client_id="Dummy",  # TODO: Extract from webhook if available
            amount=amount,
            reference=reference,
            date=date,
            bank="PayTech",
            metadata=meta_data
        )
