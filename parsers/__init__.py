from .paytech import PayTechParser
from .acme import AcmeParser

# Parser registry mapping bank names to their parser classes
PARSER_REGISTRY = {
    "paytech": PayTechParser,
    "acme": AcmeParser,
}

def get_parser(bank_name: str):
    """
    Factory function to get the appropriate parser for a bank.
    
    Args:
        bank_name: Name of the bank (case-insensitive)
        
    Returns:
        Parser instance for the specified bank
        
    Raises:
        ValueError: If bank_name is not supported
    """
    bank_name_lower = bank_name.lower()
    parser_class = PARSER_REGISTRY.get(bank_name_lower)
    
    if parser_class is None:
        supported_banks = ", ".join(PARSER_REGISTRY.keys())
        raise ValueError(
            f"Unsupported bank: {bank_name}. "
            f"Supported banks: {supported_banks}"
        )
    
    return parser_class()
