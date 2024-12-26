```python
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solana.publickey import PublicKey
from decimal import Decimal
import logging
from typing import Dict, Optional

from utils.position_manager import PositionManager
from utils.price_tracker import PriceTracker
from utils.trade_logger import TradeLogger

class DexTrader:
    def __init__(self, client: AsyncClient, config: 'BotConfig', 
                 logger: TradeLogger):
        self.client = client
        self.config = config
        self.logger = logger
        self.position_manager = PositionManager(
            config.stop_loss_percentage,
            config.take_profit_percentage
        )
        self.price_tracker = PriceTracker()
        
    async def handle_transaction(self, wallet: str, tx_data: Dict):
        """Handle incoming transaction from monitored wallet"""
        try:
            # Extract token and trade details
            token = self._extract_token_address(tx_data)
            is_buy = self._is_buy_transaction(tx_data)
            amount = self._extract_amount(tx_data)
            percentage = self._calculate_trade_percentage(tx_data)
            
            # Execute mirrored trade
            await self.execute_trade(token, is_buy, amount, percentage)
            
        except Exception as e:
            self.logger.logger.error(f"Error handling transaction: {str(e)}")
            
    async def execute_trade(self, token: PublicKey, is_buy: bool, 
                          base_amount: float, percentage: float = 100.0):
        """Execute trade with position tracking and risk management"""
        try:
            # Calculate adjusted amount based on percentage
            amount = self.config.trade_size_sol * (percentage / 100.0)
            
            # Get current price and execute trade
            price = await self._get_token_price(token)
            
            # Update price tracker
            self.price_tracker.update_price(str(token), Decimal(str(price)))
            
            # Execute the trade
            result = await self._execute_dex_trade(token, is_buy, amount)
            
            if result:
                if is_buy:
                    # Open new position
                    self.position_manager.open_position(
                        str(token),
                        Decimal(str(price)),
                        amount
                    )
                else:
                    # Close position
                    self.position_manager.close_position(
                        str(token),
                        Decimal(str(price))
                    )
                
                # Log trade
                self.logger.log_trade(
                    str(token),
                    "buy" if is_buy else "sell",
                    amount,
                    Decimal(str(price)),
                    self.config.slippage_tolerance or 0.5,
                    self.config.gas_multiplier
                )
                
        except Exception as e:
            self.logger.logger.error(f"Trade execution error: {str(e)}")
```