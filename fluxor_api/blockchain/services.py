import requests
import json
from decimal import Decimal
from django.utils import timezone
from django.conf import settings
from .models import Transaction, Block, MempoolTransaction, NetworkStats, BlockchainMonitor

class BlockchainService:
    """
    Service for interacting with Bitcoin blockchain APIs
    """
    
    def __init__(self):
        self.base_url = getattr(settings, 'BLOCKCHAIN_API_URL', 'https://blockchain.info')
        self.api_key = getattr(settings, 'BLOCKCHAIN_API_KEY', None)
    
    def get_transaction_info(self, tx_hash):
        """
        Get transaction information from blockchain
        """
        try:
            url = f"{self.base_url}/rawtx/{tx_hash}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract transaction details
            tx_info = {
                'tx_hash': tx_hash,
                'block_height': data.get('block_height'),
                'confirmations': data.get('confirmations', 0),
                'fee': data.get('fee', 0) / 100000000,  # Convert satoshis to BTC
                'size': data.get('size', 0),
                'weight': data.get('weight', 0),
                'timestamp': data.get('time', 0),
                'inputs': data.get('inputs', []),
                'outputs': data.get('out', []),
            }
            
            return tx_info
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch transaction info: {str(e)}")
    
    def get_block_info(self, block_height):
        """
        Get block information from blockchain
        """
        try:
            url = f"{self.base_url}/rawblock/{block_height}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract block details
            block_info = {
                'block_height': block_height,
                'block_hash': data.get('hash'),
                'previous_block_hash': data.get('prev_block'),
                'merkle_root': data.get('mrkl_root'),
                'timestamp': data.get('time', 0),
                'difficulty': data.get('bits'),
                'nonce': data.get('nonce'),
                'size': data.get('size', 0),
                'weight': data.get('weight', 0),
                'transaction_count': len(data.get('tx', [])),
            }
            
            return block_info
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch block info: {str(e)}")
    
    def get_mempool_info(self):
        """
        Get mempool information
        """
        try:
            url = f"{self.base_url}/mempool"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            mempool_info = {
                'mempool_size': data.get('count', 0),
                'mempool_bytes': data.get('vsize', 0),
                'mempool_fee_rate': data.get('fees', {}).get('median', 0),
                'pending_transactions': data.get('count', 0),
            }
            
            return mempool_info
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch mempool info: {str(e)}")
    
    def get_network_stats(self):
        """
        Get network statistics
        """
        try:
            # Get difficulty
            difficulty_url = f"{self.base_url}/q/getdifficulty"
            difficulty_response = requests.get(difficulty_url, timeout=10)
            difficulty = float(difficulty_response.text)
            
            # Get hash rate
            hash_rate_url = f"{self.base_url}/q/hashrate"
            hash_rate_response = requests.get(hash_rate_url, timeout=10)
            hash_rate = float(hash_rate_response.text) / 1000000000000000000  # Convert to EH/s
            
            # Get latest block
            latest_block_url = f"{self.base_url}/latestblock"
            latest_block_response = requests.get(latest_block_url, timeout=10)
            latest_block = latest_block_response.json()
            
            # Get price (using a different API)
            try:
                price_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true"
                price_response = requests.get(price_url, timeout=10)
                price_data = price_response.json()
                btc_price = price_data.get('bitcoin', {}).get('usd', 0)
                market_cap = price_data.get('bitcoin', {}).get('usd_market_cap', 0)
                volume_24h = price_data.get('bitcoin', {}).get('usd_24h_vol', 0)
            except:
                btc_price = 45000.00  # Fallback price
                market_cap = 900000000000  # Fallback market cap
                volume_24h = 25000000000  # Fallback volume
            
            stats = {
                'current_difficulty': difficulty,
                'hash_rate': hash_rate,
                'block_time': 600,  # Average block time
                'btc_price_usd': btc_price,
                'market_cap': market_cap,
                'volume_24h': volume_24h,
            }
            
            return stats
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch network stats: {str(e)}")
    
    def create_or_update_transaction(self, tx_hash, transaction_type='transfer'):
        """
        Create or update a transaction record
        """
        try:
            # Get transaction info from blockchain
            tx_info = self.get_transaction_info(tx_hash)
            
            # Check if transaction already exists
            transaction, created = Transaction.objects.get_or_create(
                tx_hash=tx_hash,
                defaults={
                    'transaction_type': transaction_type,
                    'amount': 0,  # Will be calculated from outputs
                    'fee': tx_info['fee'],
                    'block_height': tx_info['block_height'],
                    'confirmations': tx_info['confirmations'],
                    'raw_data': tx_info,
                }
            )
            
            if not created:
                # Update existing transaction
                transaction.confirmations = tx_info['confirmations']
                transaction.block_height = tx_info['block_height']
                transaction.raw_data = tx_info
                transaction.save()
            
            # Update status based on confirmations
            transaction.update_confirmations(tx_info['confirmations'])
            
            return transaction
        except Exception as e:
            raise Exception(f"Failed to create/update transaction: {str(e)}")
    
    def create_or_update_block(self, block_height):
        """
        Create or update a block record
        """
        try:
            # Get block info from blockchain
            block_info = self.get_block_info(block_height)
            
            # Check if block already exists
            block, created = Block.objects.get_or_create(
                block_height=block_height,
                defaults={
                    'block_hash': block_info['block_hash'],
                    'previous_block_hash': block_info['previous_block_hash'],
                    'merkle_root': block_info['merkle_root'],
                    'timestamp': timezone.datetime.fromtimestamp(block_info['timestamp']),
                    'difficulty': block_info['difficulty'],
                    'nonce': block_info['nonce'],
                    'size': block_info['size'],
                    'weight': block_info['weight'],
                    'transaction_count': block_info['transaction_count'],
                }
            )
            
            return block
        except Exception as e:
            raise Exception(f"Failed to create/update block: {str(e)}")
    
    def update_network_stats(self):
        """
        Update network statistics
        """
        try:
            stats = self.get_network_stats()
            mempool = self.get_mempool_info()
            
            # Combine stats
            combined_stats = {**stats, **mempool}
            
            # Create new network stats record
            NetworkStats.objects.create(
                current_difficulty=combined_stats['current_difficulty'],
                hash_rate=combined_stats['hash_rate'],
                block_time=combined_stats['block_time'],
                mempool_size=combined_stats['mempool_size'],
                mempool_bytes=combined_stats['mempool_bytes'],
                mempool_fee_rate=combined_stats['mempool_fee_rate'],
                btc_price_usd=combined_stats['btc_price_usd'],
                market_cap=combined_stats['market_cap'],
                volume_24h=combined_stats['volume_24h'],
            )
            
            return True
        except Exception as e:
            raise Exception(f"Failed to update network stats: {str(e)}")
    
    def monitor_blockchain_health(self):
        """
        Monitor blockchain health and update status
        """
        try:
            # Get latest block
            latest_block_url = f"{self.base_url}/latestblock"
            response = requests.get(latest_block_url, timeout=10)
            response.raise_for_status()
            
            latest_block = response.json()
            block_time = latest_block.get('time', 0)
            current_time = timezone.now().timestamp()
            
            # Check if blockchain is healthy
            if current_time - block_time < 3600:  # Less than 1 hour old
                status = 'healthy'
                message = 'Blockchain is operating normally'
            elif current_time - block_time < 7200:  # Less than 2 hours old
                status = 'warning'
                message = 'Blockchain may be experiencing delays'
            else:
                status = 'error'
                message = 'Blockchain appears to be down or experiencing issues'
            
            # Create health record
            BlockchainMonitor.objects.create(
                status=status,
                message=message
            )
            
            return status
        except Exception as e:
            # Create error record
            BlockchainMonitor.objects.create(
                status='error',
                message=f'Failed to monitor blockchain health: {str(e)}'
            )
            raise Exception(f"Failed to monitor blockchain health: {str(e)}")
    
    def get_fee_estimates(self):
        """
        Get fee estimates for different confirmation times
        """
        try:
            url = f"{self.base_url}/fees-recommendation"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            fee_estimates = {
                'fastest': data.get('fastestFee', 0) / 100000000,  # Convert satoshis to BTC
                'half_hour': data.get('halfHourFee', 0) / 100000000,
                'hour': data.get('hourFee', 0) / 100000000,
                'economy': data.get('economyFee', 0) / 100000000,
                'minimum': data.get('minimumFee', 0) / 100000000,
            }
            
            return fee_estimates
        except requests.RequestException as e:
            # Return fallback estimates
            return {
                'fastest': 0.0005,
                'half_hour': 0.0003,
                'hour': 0.0002,
                'economy': 0.0001,
                'minimum': 0.00001,
            } 