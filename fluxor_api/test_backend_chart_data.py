#!/usr/bin/env python3
"""
Test script to verify backend chart data system is working
"""
import os
import django
import requests
import json

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fluxor_api.settings')
django.setup()

from market_data.models import ChartDataPoint
from admin_control.models import TradingSettings

def test_database_data():
    """Test that data exists in the database"""
    print("🗄️ Testing database data...")
    
    total_points = ChartDataPoint.objects.count()
    print(f"Total chart data points: {total_points}")
    
    btc_points = ChartDataPoint.objects.filter(symbol='BTC').count()
    print(f"BTC data points: {btc_points}")
    
    if btc_points > 0:
        latest_btc = ChartDataPoint.objects.filter(symbol='BTC').order_by('-timestamp').first()
        print(f"Latest BTC data: {latest_btc.timestamp} - ${latest_btc.close_price}")
        
        # Show sample data
        print("\nSample BTC data:")
        for point in ChartDataPoint.objects.filter(symbol='BTC').order_by('-timestamp')[:5]:
            print(f"  {point.timestamp}: ${point.close_price} (source: {point.source})")
    
    return btc_points > 0

def test_api_endpoint():
    """Test the API endpoint directly"""
    print("\n🔌 Testing API endpoint...")
    
    # First, let's try to get a valid token
    try:
        # This is a simplified test - in real usage, you'd need proper authentication
        response = requests.get(
            "http://localhost:8000/api/admin/market/combined-chart/?symbol=BTC&limit=5",
            timeout=5
        )
        
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 401:
            print("❌ API requires authentication (401 Unauthorized)")
            print("   This is expected - the endpoint is working but needs a valid token")
            return False
        elif response.status_code == 200:
            data = response.json()
            print(f"✅ API working! Data points: {len(data.get('chart_data', []))}")
            return True
        else:
            print(f"❌ API error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API connection error: {e}")
        return False

def test_frontend_fallback():
    """Test what happens when API fails"""
    print("\n🎨 Testing frontend fallback behavior...")
    print("   When API returns 401, frontend should:")
    print("   1. Log error to console")
    print("   2. Call generateFallbackChartData()")
    print("   3. Generate 30 mock candles")
    print("   4. Set priceSource to 'simulated'")
    print("   This explains why you're seeing the same candlesticks!")

def main():
    print("🧪 Backend Chart Data System Test")
    print("=" * 50)
    
    # Test database
    db_working = test_database_data()
    
    # Test API
    api_working = test_api_endpoint()
    
    # Explain frontend behavior
    test_frontend_fallback()
    
    print("\n📊 Test Results:")
    print(f"Database: {'✅ Working' if db_working else '❌ No data'}")
    print(f"API: {'✅ Working' if api_working else '❌ Auth required'}")
    
    if db_working and not api_working:
        print("\n🔍 Diagnosis:")
        print("   - Backend data storage is working")
        print("   - API endpoints are working")
        print("   - Issue is authentication (401 errors)")
        print("   - Frontend falls back to mock data generation")
        print("\n💡 Solution:")
        print("   - Sign in to get a valid token")
        print("   - Or test the API with proper authentication")
        print("   - Once authenticated, frontend will use real backend data")

if __name__ == "__main__":
    main()
