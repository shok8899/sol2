```python
from typing import Optional
from dataclasses import dataclass

@dataclass
class BotConfig:
    # RPC and network settings
    rpc_url: str = "https://api.mainnet-beta.solana.com"
    commitment: str = "confirmed"
    
    # Wallet settings
    private_key: str = ""  # Supports base58, hex, or JSON format
    target_wallets: str = ""  # Comma-separated wallet addresses
    
    # Trading parameters
    trade_size_sol: float = 0.1
    slippage_tolerance: Optional[float] = None  # None for auto-calculation
    
    # Risk management
    stop_loss_percentage: float = 5.0
    take_profit_percentage: Optional[float] = None
    
    # Gas settings
    base_priority_fee: int = 10000
    base_compute_units: int = 200000
    gas_multiplier: float = 1.0
    
    def __post_init__(self):
        # Process comma-separated wallet addresses
        if self.target_wallets:
            self.target_wallets = [
                addr.strip() for addr in self.target_wallets.split(',')
            ]
        else:
            self.target_wallets = []
    
    def validate(self):
        """Validate configuration parameters"""
        assert self.private_key, "Private key is required"
        assert self.target_wallets, "At least one target wallet is required"
        assert self.trade_size_sol > 0, "Trade size must be positive"
        assert self.stop_loss_percentage > 0, "Stop loss must be positive"
        assert self.gas_multiplier >= 0.1, "Gas multiplier must be at least 0.1x"
        if self.slippage_tolerance is not None:
            assert 0 < self.slippage_tolerance <= 100, "Invalid slippage tolerance"
```