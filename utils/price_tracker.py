```python
from decimal import Decimal
from typing import Dict, Optional
import logging

class PriceTracker:
    def __init__(self):
        self.token_prices: Dict[str, Decimal] = {}
        self.entry_prices: Dict[str, Decimal] = {}
        
    def update_price(self, token: str, price: Decimal):
        self.token_prices[token] = price
        
    def set_entry_price(self, token: str, price: Decimal):
        self.entry_prices[token] = price
        
    def get_price_change_percentage(self, token: str) -> Optional[float]:
        if token not in self.token_prices or token not in self.entry_prices:
            return None
            
        entry_price = self.entry_prices[token]
        current_price = self.token_prices[token]
        return float((current_price - entry_price) / entry_price * 100)
```