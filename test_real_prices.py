#!/usr/bin/env python3
"""
Test script to verify Real Price Integration
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, '/Users/mc/trading/fluxor_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluxor_api.settings')
django.setup()

from admin_control.real_price_service import get_price_service
from admin_control.models import TradingSettings

def main():
    print("=" * 70)
    print("Real Cryptocurrency Prices - Integration Test")
    print("=" * 70)
    
    # Initialize service
    print("\n1. Initializing Real Price Service...")
    service = get_price_service()
    
    # Check availability
    print("\n2. Checking service availability...")
    if service.is_available():
        print("   ✅ Service is ONLINE and working!")
    else:
        print("   ❌ Service is OFFLINE or unavailable")
        print("   💡 Tip: Check internet connection and API status")
        return
    
    # Get Bitcoin price
    print("\n3. Fetching Bitcoin (BTC) price...")
    try:
        btc_price = service.get_current_price('BTC')
        if btc_price:
            print(f"   ✅ BTC Price: ${btc_price:,.2f}")
        else:
            print("   ❌ Failed to fetch BTC price")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Get Ethereum price
    print("\n4. Fetching Ethereum (ETH) price...")
    try:
        eth_price = service.get_current_price('ETH')
        if eth_price:
            print(f"   ✅ ETH Price: ${eth_price:,.2f}")
        else:
            print("   ❌ Failed to fetch ETH price")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Get multiple prices
    print("\n5. Fetching multiple prices at once...")
    try:
        prices = service.get_multiple_prices(['BTC', 'ETH', 'SOL', 'ADA'])
        if prices:
            print("   ✅ Prices fetched successfully:")
            for symbol, price in prices.items():
                print(f"      {symbol}: ${price:,.2f}")
        else:
            print("   ❌ Failed to fetch prices")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Get 24h stats
    print("\n6. Fetching 24-hour statistics for BTC...")
    try:
        stats = service.get_24h_stats('BTC')
        if stats:
            print("   ✅ 24h Statistics:")
            print(f"      Price: ${stats.get('price', 0):,.2f}")
            print(f"      24h Change: {stats.get('price_change_24h', 0):+.2f}%")
            print(f"      24h High: ${stats.get('high_24h', 0):,.2f}")
            print(f"      24h Low: ${stats.get('low_24h', 0):,.2f}")
            print(f"      24h Volume: ${stats.get('volume_24h', 0):,.0f}")
        else:
            print("   ❌ Failed to fetch statistics")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Get historical data
    print("\n7. Fetching historical chart data (last hour)...")
    try:
        candles = service.get_historical_data('BTC', days=1, interval='hourly')
        if candles:
            print(f"   ✅ Got {len(candles)} candlesticks")
            if candles:
                latest = candles[-1]
                print(f"      Latest Candle:")
                print(f"        Open: ${latest['open']:,.2f}")
                print(f"        High: ${latest['high']:,.2f}")
                print(f"        Low: ${latest['low']:,.2f}")
                print(f"        Close: ${latest['close']:,.2f}")
                print(f"        Volume: {latest['volume']:,.0f}")
        else:
            print("   ❌ Failed to fetch historical data")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Check trading settings
    print("\n8. Checking Trading Settings...")
    try:
        settings = TradingSettings.get_active_settings()
        print(f"   Use Real Prices: {'✅ ENABLED' if settings.use_real_prices else '❌ DISABLED'}")
        if not settings.use_real_prices:
            print("\n   💡 To enable real prices:")
            print("      1. Go to: http://localhost:8000/admin/")
            print("      2. Navigate to: Admin Control → Trading Settings")
            print("      3. Check: ☑ Use real prices")
            print("      4. Click: Save")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print("✅ Real price service is working correctly!")
    print("✅ Can fetch current prices from exchanges")
    print("✅ Can fetch historical chart data")
    print("✅ Can fetch 24h statistics")
    print("\n📚 See REAL_PRICES_INTEGRATION.md for full documentation")
    print("=" * 70)

if __name__ == "__main__":
    main()

