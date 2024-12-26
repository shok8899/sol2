from typing import Dict
import logging
from decimal import Decimal

class SlippageCalculator:
    def __init__(self):
        self.price_history: Dict[str, list] = {}  # Token price history
        self.volatility_window = 20  # Number of prices to calculate volatility
        
    async def calculate_auto_slippage(self, token: str, current_price: Decimal) -> float:
        """
        Calculate optimal slippage based on token volatility
        Returns slippage percentage
        """
        try:
            # Update price history
            if token not in self.price_history:
                self.price_history[token] = []
            
            self.price_history[token].append(float(current_price))
            
            # Keep only recent prices
            if len(self.price_history[token]) > self.volatility_window:
                self.price_history[token].pop(0)
            
            # Need minimum number of prices for calculation
            if len(self.price_history[token]) < 5:
                return 1.0  # Default slippage when not enough data
            
            # Calculate price volatility
            prices = self.price_history[token]
            volatility = self._calculate_volatility(prices)
            
            # Adjust slippage based on volatility
            # Higher volatility = higher slippage
            base_slippage = 0.5
            volatility_multiplier = 2.0
            
            slippage = base_slippage + (volatility * volatility_multiplier)
            
            # Cap maximum slippage
            return min(slippage, 5.0)  # Max 5% slippage
            
        except Exception as e:
            logging.error(f"Error calculating slippage: {str(e)}")
            return 1.0  # Default fallback slippage
            
    def _calculate_volatility(self, prices: list) -> float:
        """Calculate price volatility using standard deviation"""
        if not prices:
            return 0
            
        mean = sum(prices) / len(prices)
        variance = sum((p - mean) ** 2 for p in prices) / len(prices)
        return (variance ** 0.5) / mean  # Coefficient of variation