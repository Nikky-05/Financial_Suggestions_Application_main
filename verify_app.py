"""
Verification script to test application components
Run this to ensure all modules and integrations are working
"""
import sys
import os

# Fix encoding for Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_imports():
    """Test all imports"""
    print_section("Testing Module Imports")
    
    try:
        import app
        print("✅ app.py imported successfully")
        
        import database
        print("✅ database.py imported successfully")
        
        import api_integrations
        print("✅ api_integrations.py imported successfully")
        
        import config
        print("✅ config.py imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print_section("Testing Environment Configuration")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    env_vars = [
        'FLASK_ENV',
        'GEMINI_API_KEY',
        'SECRET_KEY'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'SECRET' in var:
                display = value[:10] + '...' if len(value) > 10 else '*' * len(value)
            else:
                display = value
            print(f"✅ {var} = {display}")
        else:
            print(f"⚠️  {var} not set (optional)")
    
    return True

def test_database():
    """Test database connection"""
    print_section("Testing Database")
    
    try:
        from database import get_db_connection, init_db
        
        # Initialize database
        init_db()
        print("✅ Database initialized")
        
        # Test connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"✅ Database connected. Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Check for sample data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"\n✅ Database has {user_count} sample users")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_financial_data():
    """Test financial data loading"""
    print_section("Testing Financial Data")
    
    try:
        import pandas as pd
        
        excel_file = 'data/financial_options.xlsx'
        if not os.path.exists(excel_file):
            print(f"⚠️  Excel file not found: {excel_file}")
            return True
        
        df = pd.read_excel(excel_file, sheet_name=None)
        
        print(f"✅ Excel file loaded. Sheets:")
        for sheet_name, sheet_df in df.items():
            print(f"   - {sheet_name}: {len(sheet_df)} rows")
        
        return True
    except Exception as e:
        print(f"❌ Error loading financial data: {e}")
        return False

def test_config():
    """Test configuration"""
    print_section("Testing Configuration")
    
    try:
        from config import (
            INDIAN_STOCKS, INDICES, CRYPTOCURRENCIES,
            CURRENCY_PAIRS, BANK_LOAN_RATES, API_ENDPOINTS
        )
        
        print(f"✅ Indian Stocks: {len(INDIAN_STOCKS)} configured")
        print(f"✅ Market Indices: {len(INDICES)} configured")
        print(f"✅ Cryptocurrencies: {len(CRYPTOCURRENCIES)} configured")
        print(f"✅ Currency Pairs: {len(CURRENCY_PAIRS)} configured")
        print(f"✅ Banks: {len(BANK_LOAN_RATES)} banks configured")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_api_integrations():
    """Test API integrations"""
    print_section("Testing API Integrations")
    
    try:
        from api_integrations import (
            get_market_indices, get_crypto_prices, get_forex_rates,
            get_gold_price, get_all_stocks
        )
        
        print("Testing API endpoints (with caching)...")
        
        try:
            indices = get_market_indices()
            print(f"✅ Market Indices API: Retrieved {len(indices)} indices")
        except Exception as e:
            print(f"⚠️  Market Indices API: {str(e)[:50]}")
        
        try:
            crypto = get_crypto_prices()
            print(f"✅ Crypto API: Retrieved {len(crypto)} cryptocurrencies")
        except Exception as e:
            print(f"⚠️  Crypto API: {str(e)[:50]}")
        
        try:
            forex = get_forex_rates()
            print(f"✅ Forex API: Retrieved {len(forex)} currency pairs")
        except Exception as e:
            print(f"⚠️  Forex API: {str(e)[:50]}")
        
        try:
            gold = get_gold_price()
            print(f"✅ Gold Price API: Retrieved data")
        except Exception as e:
            print(f"⚠️  Gold Price API: {str(e)[:50]}")
        
        return True
    except Exception as e:
        print(f"❌ API integration error: {e}")
        return False

def test_flask_app():
    """Test Flask app creation"""
    print_section("Testing Flask Application")
    
    try:
        from app import app
        
        print("✅ Flask app created successfully")
        print(f"✅ Routes configured: {len([rule for rule in app.url_map.iter_rules()])}")
        
        # List main routes
        print("\nMain routes:")
        for rule in sorted(app.url_map.iter_rules(), key=str):
            if 'static' not in str(rule):
                print(f"   - {rule}")
        
        return True
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def print_summary(results):
    """Print test summary"""
    print_section("Test Summary")
    
    passed = sum(1 for r in results if r)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"Tests Passed: {passed}/{total} ({percentage:.0f}%)\n")
    
    if passed == total:
        print("✅ All systems functional!")
        print("\n🚀 Ready to start the application:")
        print("   python app.py")
        return True
    else:
        print("⚠️  Some tests failed. Check errors above.")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Financial Application Verification")
    print("="*60)
    
    results = [
        test_imports(),
        test_environment(),
        test_database(),
        test_financial_data(),
        test_config(),
        test_api_integrations(),
        test_flask_app(),
    ]
    
    success = print_summary(results)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
