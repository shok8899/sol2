from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
import asyncio
from typing import List, Dict, Callable
import json
import logging

class TransactionMonitor:
    def __init__(self, client: AsyncClient, target_wallets: List[str]):
        self.client = client
        self.target_wallets = [PublicKey(addr) for addr in target_wallets]
        self.callbacks: List[Callable] = []
        
    def add_callback(self, callback: Callable):
        """Add callback function to be called when new transactions are detected"""
        self.callbacks.append(callback)
        
    async def start_monitoring(self):
        """Start monitoring transactions for target wallets"""
        while True:
            try:
                # Subscribe to transaction websocket for each wallet
                ws_url = self.client._provider.endpoint.replace('http', 'ws')
                subscription_ids = []
                
                for wallet in self.target_wallets:
                    sub_id = await self._subscribe_to_wallet(wallet)
                    subscription_ids.append(sub_id)
                    
                await asyncio.sleep(0.001)  # Millisecond-level monitoring
                    
            except Exception as e:
                logging.error(f"Monitoring error: {str(e)}")
                await asyncio.sleep(1)
                
    async def _subscribe_to_wallet(self, wallet: PublicKey):
        """Subscribe to a wallet's transactions"""
        ws = await self.client.create_subscription()
        
        async def on_transaction(tx):
            for callback in self.callbacks:
                await callback(wallet, tx)
                
        return await ws.account_subscribe(
            wallet,
            encoding="jsonParsed",
            commitment="confirmed",
            callback=on_transaction
        )