```python
import asyncio
from solana.rpc.async_api import AsyncClient
from config import BotConfig
from trading.dex_trader import DexTrader
from trading.transaction_monitor import TransactionMonitor
from utils.trade_logger import TradeLogger

async def main():
    # Initialize configuration
    config = BotConfig(
        rpc_url="https://cold-hanni-fast-mainnet.helius-rpc.com/",
        target_wallets="wallet1,wallet2,wallet3",  # Comma-separated addresses
        private_key="YOUR_PRIVATE_KEY",
        trade_size_sol=0.1,
        stop_loss_percentage=20,
        gas_multiplier=1.5
    )
    
    # Validate configuration
    config.validate()
    
    # Initialize components
    client = AsyncClient(config.rpc_url)
    logger = TradeLogger()
    trader = DexTrader(client, config, logger)
    monitor = TransactionMonitor(client, config.target_wallets, trader)
    
    # Start monitoring
    logger.logger.info(f"Starting bot with {len(config.target_wallets)} target wallets")
    logger.logger.info(f"Gas multiplier: {config.gas_multiplier}x")
    
    try:
        await monitor.start_monitoring()
    except KeyboardInterrupt:
        logger.logger.info("Shutting down bot...")
    except Exception as e:
        logger.logger.error(f"Error: {str(e)}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```