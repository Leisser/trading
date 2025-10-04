import os
import json
import requests
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from cryptography.fernet import Fernet
from web3 import Web3
from eth_account import Account
import secrets

# Global variables for lazy initialization
_w3 = None
_fernet = None

def get_w3():
    """Get Web3 instance with lazy initialization"""
    global _w3
    if _w3 is None:
        try:
            from django.conf import settings
            if hasattr(settings, 'ETHEREUM_RPC_URL'):
                _w3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_RPC_URL))
            else:
                _w3 = None
        except Exception:
            _w3 = None
    return _w3

def get_fernet():
    """Get Fernet instance with lazy initialization"""
    global _fernet
    if _fernet is None:
        try:
            from django.conf import settings
            if hasattr(settings, 'CRYPTO_ENCRYPTION_KEY') and settings.CRYPTO_ENCRYPTION_KEY != 'your-32-byte-encryption-key-here-change-in-production':
                _fernet = Fernet(settings.CRYPTO_ENCRYPTION_KEY.encode())
            else:
                # Generate a temporary key for development
                _fernet = Fernet(Fernet.generate_key())
        except Exception:
            _fernet = None
    return _fernet


class CryptoWalletService:
    """Service for managing crypto wallets"""
    
    @staticmethod
    def generate_ethereum_wallet() -> Tuple[str, str]:
        """Generate a new Ethereum wallet"""
        w3 = get_w3()
        if not w3:
            raise Exception("Ethereum RPC URL not configured")
        
        account = Account.create()
        address = account.address
        private_key = account.key.hex()
        
        return address, private_key
    
    @staticmethod
    def encrypt_private_key(private_key: str) -> str:
        """Encrypt private key for storage"""
        fernet = get_fernet()
        if not fernet:
            raise Exception("Crypto encryption key not configured")
        
        return fernet.encrypt(private_key.encode()).decode()
    
    @staticmethod
    def decrypt_private_key(encrypted_key: str) -> str:
        """Decrypt private key for use"""
        fernet = get_fernet()
        if not fernet:
            raise Exception("Crypto encryption key not configured")
        
        return fernet.decrypt(encrypted_key.encode()).decode()
    
    @staticmethod
    def get_ethereum_balance(address: str) -> Decimal:
        """Get Ethereum balance for an address"""
        w3 = get_w3()
        if not w3:
            return Decimal('0')
        
        try:
            balance_wei = w3.eth.get_balance(address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            return Decimal(str(balance_eth))
        except Exception:
            return Decimal('0')
    
    @staticmethod
    def generate_bitcoin_address() -> Tuple[str, str]:
        """Generate a new Bitcoin address (simplified)"""
        # In production, use proper Bitcoin library
        private_key = secrets.token_hex(32)
        address = f"bc1q{secrets.token_hex(20)}"  # Simplified for demo
        return address, private_key


class CryptoPriceService:
    """Service for fetching crypto prices"""
    
    @staticmethod
    def get_coingecko_prices(symbols: List[str]) -> Dict[str, float]:
        """Get prices from CoinGecko API"""
        try:
            # Convert symbols to CoinGecko IDs
            symbol_to_id = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'SOL': 'solana',
                'ADA': 'cardano',
                'DOT': 'polkadot',
                'LINK': 'chainlink',
            }
            
            ids = [symbol_to_id.get(symbol.upper(), symbol.lower()) for symbol in symbols]
            ids_str = ','.join(ids)
            
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            prices = {}
            
            for symbol in symbols:
                coin_id = symbol_to_id.get(symbol.upper(), symbol.lower())
                if coin_id in data:
                    prices[symbol.upper()] = data[coin_id]['usd']
            
            return prices
        except Exception as e:
            print(f"Error fetching prices from CoinGecko: {e}")
            return {}
    
    @staticmethod
    def get_binance_prices(symbols: List[str]) -> Dict[str, float]:
        """Get prices from Binance API"""
        try:
            prices = {}
            for symbol in symbols:
                url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                prices[symbol] = float(data['price'])
            return prices
        except Exception as e:
            print(f"Error fetching prices from Binance: {e}")
            return {}


class CryptoSwapService:
    """Service for crypto-to-crypto swaps"""
    
    @staticmethod
    def get_swap_quote(from_token: str, to_token: str, amount: Decimal) -> Dict:
        """Get swap quote from 1inch API"""
        try:
            # Simplified swap quote - in production, use 1inch API
            exchange_rates = {
                'BTC-ETH': 15.5,
                'BTC-SOL': 1200,
                'BTC-ADA': 45000,
                'BTC-DOT': 1800,
                'BTC-LINK': 1200,
                'ETH-BTC': 0.064,
                'ETH-SOL': 77,
                'ETH-ADA': 2900,
                'ETH-DOT': 116,
                'ETH-LINK': 77,
                'SOL-BTC': 0.00083,
                'SOL-ETH': 0.013,
                'SOL-ADA': 37.5,
                'SOL-DOT': 1.5,
                'SOL-LINK': 1,
                'ADA-BTC': 0.000022,
                'ADA-ETH': 0.00034,
                'ADA-SOL': 0.027,
                'ADA-DOT': 0.04,
                'ADA-LINK': 0.027,
                'DOT-BTC': 0.00056,
                'DOT-ETH': 0.0086,
                'DOT-SOL': 0.67,
                'DOT-ADA': 25,
                'DOT-LINK': 0.67,
                'LINK-BTC': 0.00083,
                'LINK-ETH': 0.013,
                'LINK-SOL': 1,
                'LINK-ADA': 37.5,
                'LINK-DOT': 1.5,
            }
            
            pair = f"{from_token}-{to_token}"
            rate = exchange_rates.get(pair, 1)
            
            to_amount = amount * Decimal(str(rate))
            network_fee = Decimal('0.001')  # Mock network fee
            
            return {
                'from_token': from_token,
                'to_token': to_token,
                'from_amount': amount,
                'to_amount': to_amount,
                'exchange_rate': Decimal(str(rate)),
                'network_fee': network_fee,
                'provider': '1inch',
                'estimated_time': '30 seconds'
            }
        except Exception as e:
            print(f"Error getting swap quote: {e}")
            return {}
    
    @staticmethod
    def execute_swap(swap_data: Dict) -> Dict:
        """Execute a crypto swap"""
        try:
            # In production, this would interact with DEX APIs
            # For now, we'll simulate the swap
            return {
                'success': True,
                'transaction_hash': f"0x{secrets.token_hex(32)}",
                'status': 'completed',
                'executed_at': timezone.now(),
                'swap_data': swap_data
            }
        except Exception as e:
            print(f"Error executing swap: {e}")
            return {
                'success': False,
                'error': str(e)
            }


class CryptoPaymentService:
    """Service for crypto payment processing"""
    
    @staticmethod
    def create_coinbase_payment(amount_usd: Decimal, cryptocurrency: str) -> Dict:
        """Create a payment using Coinbase Commerce"""
        try:
            # In production, use Coinbase Commerce API
            # For demo, we'll create a mock payment
            payment_id = secrets.token_hex(16)
            wallet_address = f"bc1q{secrets.token_hex(20)}"  # Mock address
            
            # Calculate crypto amount based on current price
            prices = CryptoPriceService.get_coingecko_prices([cryptocurrency])
            price_usd = prices.get(cryptocurrency, 45000)  # Default fallback
            amount_crypto = amount_usd / Decimal(str(price_usd))
            
            return {
                'payment_id': payment_id,
                'amount_usd': amount_usd,
                'amount_crypto': amount_crypto,
                'cryptocurrency': cryptocurrency,
                'wallet_address': wallet_address,
                'payment_url': f"https://commerce.coinbase.com/checkout/{payment_id}",
                'expires_at': timezone.now() + timedelta(hours=1),
                'status': 'pending'
            }
        except Exception as e:
            print(f"Error creating Coinbase payment: {e}")
            return {}
    
    @staticmethod
    def verify_payment(payment_id: str, transaction_hash: str) -> bool:
        """Verify a crypto payment"""
        try:
            # In production, verify the transaction on the blockchain
            # For demo, we'll simulate verification
            return True
        except Exception as e:
            print(f"Error verifying payment: {e}")
            return False


class CryptoTransactionService:
    """Service for blockchain transaction management"""
    
    @staticmethod
    def send_ethereum_transaction(from_address: str, to_address: str, amount: Decimal, private_key: str) -> Dict:
        """Send Ethereum transaction"""
        w3 = get_w3()
        if not w3:
            return {'success': False, 'error': 'Ethereum RPC not configured'}
        
        try:
            # Convert amount to Wei
            amount_wei = w3.to_wei(amount, 'ether')
            
            # Get nonce
            nonce = w3.eth.get_transaction_count(from_address)
            
            # Build transaction
            transaction = {
                'nonce': nonce,
                'to': to_address,
                'value': amount_wei,
                'gas': 21000,
                'gasPrice': w3.eth.gas_price,
                'chainId': w3.eth.chain_id
            }
            
            # Sign transaction
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
            
            # Send transaction
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return {
                'success': True,
                'transaction_hash': tx_hash.hex(),
                'from_address': from_address,
                'to_address': to_address,
                'amount': amount
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_transaction_status(transaction_hash: str) -> Dict:
        """Get transaction status"""
        w3 = get_w3()
        if not w3:
            return {'status': 'unknown', 'error': 'Ethereum RPC not configured'}
        
        try:
            receipt = w3.eth.get_transaction_receipt(transaction_hash)
            if receipt:
                return {
                    'status': 'confirmed' if receipt['status'] == 1 else 'failed',
                    'block_number': receipt['blockNumber'],
                    'gas_used': receipt['gasUsed']
                }
            else:
                return {'status': 'pending'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}





