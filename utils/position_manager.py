```python
from decimal import Decimal
from typing import Dict, Optional
import logging

class PositionManager:
    def __init__(self, stop_loss_pct: float, take_profit_pct: Optional[float] = None):
        self.positions: Dict[str, Dict] = {}
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        
    def open_position(self, token: str, entry_price: Decimal, amount: float):
        self.positions[token] = {
            'entry_price': entry_price,
            'amount': amount,
            'pnl_percentage': 0
        }
        logging.info(f"Opened position for {token} at {entry_price} SOL")
        
    def update_position(self, token: str, current_price: Decimal) -> Optional[str]:
        if token not in self.positions:
            return None
            
        position = self.positions[token]
        entry_price = position['entry_price']
        pnl_percentage = float((current_price - entry_price) / entry_price * 100)
        position['pnl_percentage'] = pnl_percentage
        
        # Check stop loss
        if pnl_percentage <= -self.stop_loss_pct:
            return 'stop_loss'
            
        # Check take profit
        if self.take_profit_pct and pnl_percentage >= self.take_profit_pct:
            return 'take_profit'
            
        return None
        
    def close_position(self, token: str, exit_price: Decimal):
        if token in self.positions:
            position = self.positions[token]
            pnl = float((exit_price - position['entry_price']) / position['entry_price'] * 100)
            logging.info(f"Closed position for {token} at {exit_price} SOL. PnL: {pnl:.2f}%")
            del self.positions[token]
```