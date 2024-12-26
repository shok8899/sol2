from typing import Dict
import logging

class GasManager:
    def __init__(self, base_gas: Dict[str, int]):
        """
        Initialize GasManager with base gas settings
        
        :param base_gas: Dict with 'priority_fee' and 'compute_units'
        """
        self.base_gas = base_gas
        
    def calculate_gas(self, multiplier: float = 1.0) -> Dict[str, int]:
        """
        Calculate gas parameters using multiplier
        
        :param multiplier: Gas multiplier (e.g., 1.5 = 150% of base gas)
        :return: Dict with adjusted priority_fee and compute_units
        """
        try:
            # Ensure multiplier is at least 0.1x
            multiplier = max(0.1, multiplier)
            
            # Calculate adjusted gas values
            gas = {
                "priority_fee": int(self.base_gas["priority_fee"] * multiplier),
                "compute_units": int(self.base_gas["compute_units"] * multiplier)
            }
            
            # Log gas settings
            logging.info(f"Gas Settings:")
            logging.info(f"  Multiplier: {multiplier}x")
            logging.info(f"  Priority Fee: {gas['priority_fee']} lamports")
            logging.info(f"  Compute Units: {gas['compute_units']}")
            
            return gas
            
        except Exception as e:
            logging.error(f"Gas calculation error: {str(e)}")
            return self.base_gas.copy()  # Return base gas as fallback