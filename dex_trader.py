from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solana.publickey import PublicKey
import logging
from decimal import Decimal
from typing import Dict, Optional
from slippage_calculator import SlippageCalculator
from gas_manager import GasManager

class DexTrader:
    def __init__(self, client: AsyncClient, config: 'BotConfig'):
        self.client = client
        self.config = config
        self.positions: Dict[str, Dict] = {}
        self.slippage_calculator = SlippageCalculator()
        self.gas_manager = GasManager(
            base_priority_fee=config.base_priority_fee,
            base_compute_units=config.base_compute_units
        )
        
    async def execute_trade(self, token: PublicKey, is_buy: bool, amount: float, 
                          percentage: float = 100.0):
        """
        Execute a trade on DEX with specified parameters
        """
        try:
            # Calculate trade amount based on percentage
            adjusted_amount = amount * (percentage / 100.0)
            
            # Get current token price and calculate optimal slippage
            current_price = await self._get_token_price(token)
            slippage = await self.slippage_calculator.calculate_auto_slippage(
                str(token),
                Decimal(str(current_price))
            )
            
            # Calculate gas parameters
            gas_params = self.gas_manager.calculate_gas_params(self.config.gas_multiplier)
            
            # Build DEX swap instruction
            swap_ix = await self._build_swap_instruction(
                token,
                is_buy,
                adjusted_amount,
                slippage
            )
            
            # Set compute units and priority fee
            tx = Transaction().add(swap_ix)
            tx.recent_blockhash = await self._get_recent_blockhash()
            
            # Sign and send transaction with calculated gas
            result = await self.client.send_transaction(
                tx,
                opts={
                    "skip_preflight": True,
                    "compute_budget": {
                        "units": gas_params["compute_units"],
                        "priority_fee": gas_params["priority_fee"]
                    }
                }
            )
            
            # Log trade details
            self._log_trade(token, is_buy, adjusted_amount, result, slippage)
            
            # Update position tracking
            await self._update_position(token, is_buy, adjusted_amount)
            
            return result
            
        except Exception as e:
            logging.error(f"Trade execution error: {str(e)}")
            return None