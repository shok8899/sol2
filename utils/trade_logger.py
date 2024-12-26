```python
import logging
from datetime import datetime
from decimal import Decimal
from typing import Dict

class TradeLogger:
    def __init__(self, log_file: str = 'trading_bot.log'):
        self.logger = logging.getLogger('trade_logger')
        self.logger.setLevel(logging.INFO)
        
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
    def log_trade(self, token: str, action: str, amount: float, 
                  price: Decimal, slippage: float, gas_multiplier: float):
        self.logger.info(
            f"TRADE: {action.upper()} {amount} {token} @ {price} SOL | "
            f"Slippage: {slippage}% | Gas: {gas_multiplier}x"
        )
        
    def log_pnl(self, token: str, entry_price: Decimal, 
                exit_price: Decimal, amount: float):
        pnl = float((exit_price - entry_price) / entry_price * 100)
        self.logger.info(
            f"PNL: {token} | Entry: {entry_price} | Exit: {exit_price} | "
            f"Amount: {amount} | PnL: {pnl:.2f}%"
        )
```