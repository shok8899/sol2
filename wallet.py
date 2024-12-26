from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
from solana.publickey import PublicKey
from base58 import b58decode
import json

class WalletManager:
    @staticmethod
    def load_private_key(private_key: str) -> Keypair:
        """
        Load private key from various formats (base58, hex, JSON)
        """
        try:
            # Try base58 format
            if len(private_key) == 88:
                return Keypair.from_secret_key(b58decode(private_key))
            
            # Try hex format
            elif len(private_key) == 64:
                return Keypair.from_secret_key(bytes.fromhex(private_key))
            
            # Try JSON format
            else:
                key_data = json.loads(private_key)
                return Keypair.from_secret_key(bytes(key_data))
                
        except Exception as e:
            raise ValueError(f"Invalid private key format: {str(e)}")
    
    @staticmethod
    async def get_sol_balance(client: AsyncClient, public_key: PublicKey) -> float:
        """
        Get SOL balance for a wallet
        """
        response = await client.get_balance(public_key)
        return response['result']['value'] / 10**9  # Convert lamports to SOL