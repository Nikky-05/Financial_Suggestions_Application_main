"""
API Integration Module for Real-Time Financial Data
Handles fetching data from various financial APIs with caching and error handling
"""
import requests
import yfinance as yf
from datetime import datetime, timedelta
from cachetools import TTLCache
import logging
from config import *

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize caches
stock_cache = TTLCache(maxsize=100, ttl=CACHE_EXPIRY['STOCK_PRICES'])
crypto_cache = TTLCache(maxsize=50, ttl=CACHE_EXPIRY['CRYPTO_PRICES'])
forex_cache = TTLCache(maxsize=10, ttl=CACHE_EXPIRY['FOREX_RATES'])
gold_cache = TTLCache(maxsize=5, ttl=CACHE_EXPIRY['GOLD_PRICES'])
indices_cache = TTLCache(maxsize=10, ttl=CACHE_EXPIRY['INDICES'])

# ==================== STOCK MARKET DATA ====================

def get_stock_price(symbol):
    """
    Fetch real-time stock price using yfinance
    Args:
        symbol: Stock symbol (e.g., 'RELIANCE.NS')
    Returns:
        dict with price, change, change_percent, volume
    """
    if symbol in stock_cache:
        logger.info(f"Cache hit for {symbol}")
        return stock_cache[symbol]
    
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d', interval='1m')
        
        if data.empty:
            logger.warning(f"No data for {symbol}")
            return None
        
        current_price = data['Close'].iloc[-1]
        previous_close = ticker.info.get('previousClose', current_price)
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100 if previous_close else 0
        
        result = {
            'symbol': symbol,
            'name': INDIAN_STOCKS.get(symbol, symbol),
            'price': round(current_price, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'volume': int(data['Volume'].iloc[-1]) if 'Volume' in data else 0,
            'timestamp': datetime.now().isoformat()
        }
        
        stock_cache[symbol] = result
        return result
        
    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {e}")
        return None

def get_all_stocks():
    """Fetch prices for all configured Indian stocks"""
    stocks_data = []
    for symbol in INDIAN_STOCKS.keys():
        data = get_stock_price(symbol)
        if data:
            stocks_data.append(data)
    return stocks_data

def get_market_indices():
    """Fetch major Indian market indices"""
    if 'indices_all' in indices_cache:
        return indices_cache['indices_all']
    
    indices_data = []
    for symbol, name in INDICES.items():
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m')
            
            if not data.empty:
                current_price = data['Close'].iloc[-1]
                previous_close = ticker.info.get('previousClose', current_price)
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100 if previous_close else 0
                
                indices_data.append({
                    'symbol': symbol,
                    'name': name,
                    'value': round(current_price, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2),
                    'timestamp': datetime.now().isoformat()
                })
        except Exception as e:
            logger.error(f"Error fetching index {symbol}: {e}")
    
    indices_cache['indices_all'] = indices_data
    return indices_data

# ==================== CRYPTOCURRENCY DATA ====================

def get_crypto_prices():
    """
    Fetch cryptocurrency prices from CoinGecko
    Returns list of crypto data with prices in INR
    """
    if 'crypto_all' in crypto_cache:
        return crypto_cache['crypto_all']
    
    try:
        crypto_ids = ','.join(CRYPTOCURRENCIES.keys())
        url = f"{API_ENDPOINTS['COINGECKO_BASE']}/simple/price"
        params = {
            'ids': crypto_ids,
            'vs_currencies': 'inr,usd',
            'include_24hr_change': 'true',
            'include_24hr_vol': 'true'
        }
        
        response = requests.get(url, params=params, timeout=APP_SETTINGS['TIMEOUT'])
        response.raise_for_status()
        data = response.json()
        
        crypto_data = []
        for crypto_id, name in CRYPTOCURRENCIES.items():
            if crypto_id in data:
                crypto_info = data[crypto_id]
                crypto_data.append({
                    'id': crypto_id,
                    'name': name,
                    'price_inr': crypto_info.get('inr', 0),
                    'price_usd': crypto_info.get('usd', 0),
                    'change_24h': round(crypto_info.get('inr_24h_change', 0), 2),
                    'volume_24h': crypto_info.get('inr_24h_vol', 0),
                    'timestamp': datetime.now().isoformat()
                })
        
        crypto_cache['crypto_all'] = crypto_data
        return crypto_data
        
    except Exception as e:
        logger.error(f"Error fetching crypto prices: {e}")
        return []

def get_single_crypto_price(crypto_id):
    """Get price for a single cryptocurrency"""
    all_cryptos = get_crypto_prices()
    for crypto in all_cryptos:
        if crypto['id'] == crypto_id:
            return crypto
    return None

# ==================== FOREX / CURRENCY EXCHANGE ====================

def get_forex_rates():
    """
    Fetch currency exchange rates to INR
    Returns dict of currency rates
    """
    if 'forex_all' in forex_cache:
        return forex_cache['forex_all']
    
    try:
        forex_data = {}
        for currency in CURRENCY_PAIRS.keys():
            symbol = f"{currency}INR=X"
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m')
            
            if not data.empty:
                current_rate = data['Close'].iloc[-1]
                previous_close = ticker.info.get('previousClose', current_rate)
                change = current_rate - previous_close
                change_percent = (change / previous_close) * 100 if previous_close else 0
                
                forex_data[currency] = {
                    'currency': currency,
                    'name': CURRENCY_PAIRS[currency],
                    'rate': round(current_rate, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2),
                    'timestamp': datetime.now().isoformat()
                }
        
        forex_cache['forex_all'] = forex_data
        return forex_data
        
    except Exception as e:
        logger.error(f"Error fetching forex rates: {e}")
        # Fallback to approximate rates
        return {
            'USD': {'currency': 'USD', 'name': 'US Dollar', 'rate': 83.12, 'change': 0, 'change_percent': 0},
            'EUR': {'currency': 'EUR', 'name': 'Euro', 'rate': 90.45, 'change': 0, 'change_percent': 0},
            'GBP': {'currency': 'GBP', 'name': 'British Pound', 'rate': 105.23, 'change': 0, 'change_percent': 0},
        }

# ==================== GOLD & COMMODITIES ====================

def get_gold_price():
    """
    Fetch current gold price in INR per 10 grams
    Uses web scraping or fallback data
    """
    if 'gold' in gold_cache:
        return gold_cache['gold']
    
    try:
        # Using GC=F (Gold Futures) as proxy
        ticker = yf.Ticker("GC=F")
        data = ticker.history(period='1d', interval='1m')
        
        if not data.empty:
            # Gold futures price in USD per troy ounce
            price_usd_oz = data['Close'].iloc[-1]
            
            # Convert to INR per 10 grams
            # 1 troy ounce = 31.1035 grams
            # Get USD to INR rate
            forex = get_forex_rates()
            usd_to_inr = forex.get('USD', {}).get('rate', 83.0)
            
            price_inr_10g = (price_usd_oz / 31.1035) * 10 * usd_to_inr
            
            previous_close = ticker.info.get('previousClose', price_usd_oz)
            change_percent = ((price_usd_oz - previous_close) / previous_close) * 100 if previous_close else 0
            
            result = {
                'commodity': 'gold',
                'name': 'Gold (10g)',
                'price_inr': round(price_inr_10g, 2),
                'price_usd_oz': round(price_usd_oz, 2),
                'change_percent': round(change_percent, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            gold_cache['gold'] = result
            return result
            
    except Exception as e:
        logger.error(f"Error fetching gold price: {e}")
    
    # Fallback price
    return {
        'commodity': 'gold',
        'name': 'Gold (10g)',
        'price_inr': 62500,
        'price_usd_oz': 2050,
        'change_percent': 0,
        'timestamp': datetime.now().isoformat()
    }

def get_silver_price():
    """Fetch current silver price in INR per kg"""
    if 'silver' in gold_cache:
        return gold_cache['silver']
    
    try:
        ticker = yf.Ticker("SI=F")  # Silver Futures
        data = ticker.history(period='1d', interval='1m')
        
        if not data.empty:
            price_usd_oz = data['Close'].iloc[-1]
            
            # Convert to INR per kg (1 troy oz = 31.1035g, 1kg = 1000g)
            forex = get_forex_rates()
            usd_to_inr = forex.get('USD', {}).get('rate', 83.0)
            price_inr_kg = (price_usd_oz / 31.1035) * 1000 * usd_to_inr
            
            previous_close = ticker.info.get('previousClose', price_usd_oz)
            change_percent = ((price_usd_oz - previous_close) / previous_close) * 100 if previous_close else 0
            
            result = {
                'commodity': 'silver',
                'name': 'Silver (1kg)',
                'price_inr': round(price_inr_kg, 2),
                'price_usd_oz': round(price_usd_oz, 2),
                'change_percent': round(change_percent, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            gold_cache['silver'] = result
            return result
            
    except Exception as e:
        logger.error(f"Error fetching silver price: {e}")
    
    return {
        'commodity': 'silver',
        'name': 'Silver (1kg)',
        'price_inr': 75000,
        'price_usd_oz': 24.5,
        'change_percent': 0,
        'timestamp': datetime.now().isoformat()
    }

# ==================== INVESTMENT RECOMMENDATIONS ====================

def get_investment_options_with_realtime_data(risk_appetite='moderate'):
    """
    Get investment options with real-time prices based on risk appetite
    """
    options = []
    
    # Add stocks based on risk
    stocks = get_all_stocks()
    if risk_appetite in ['moderate', 'high']:
        # Add top 5 stocks
        for stock in stocks[:5]:
            options.append({
                'type': 'stock',
                'name': stock['name'],
                'current_price': stock['price'],
                'change_percent': stock['change_percent'],
                'risk': 'Medium-High' if risk_appetite == 'high' else 'Medium',
                'expected_return': 15.0 if risk_appetite == 'high' else 12.0,
                'investment_type': 'Equity'
            })
    
    # Add cryptocurrencies for high risk
    if risk_appetite == 'high':
        cryptos = get_crypto_prices()
        for crypto in cryptos[:3]:
            options.append({
                'type': 'cryptocurrency',
                'name': crypto['name'],
                'current_price': crypto['price_inr'],
                'change_percent': crypto['change_24h'],
                'risk': 'Very High',
                'expected_return': 25.0,
                'investment_type': 'Crypto'
            })
    
    # Add gold for low-medium risk
    if risk_appetite in ['low', 'moderate']:
        gold = get_gold_price()
        options.append({
            'type': 'commodity',
            'name': 'Gold',
            'current_price': gold['price_inr'],
            'change_percent': gold['change_percent'],
            'risk': 'Low',
            'expected_return': 8.0,
            'investment_type': 'Commodity'
        })
    
    # Add mutual funds
    for category, details in list(MUTUAL_FUND_CATEGORIES.items())[:3]:
        if (risk_appetite == 'low' and details['risk'] in ['Low', 'Very Low']) or \
           (risk_appetite == 'moderate' and details['risk'] in ['Low', 'Medium', 'Medium-High']) or \
           (risk_appetite == 'high'):
            options.append({
                'type': 'mutual_fund',
                'name': f'{category} Mutual Fund',
                'current_price': 'NAV Based',
                'change_percent': 0,
                'risk': details['risk'],
                'expected_return': details['expected_return'],
                'investment_type': 'Mutual Fund'
            })
    
    return options

# ==================== LOAN RATES ====================

def get_loan_rates(loan_type='home_loan'):
    """
    Get current loan rates from major banks
    Args:
        loan_type: 'home_loan', 'car_loan', 'personal_loan', 'education_loan'
    Returns:
        list of bank loan rates
    """
    loan_rates = []
    
    for bank, rates in BANK_LOAN_RATES.items():
        if loan_type in rates:
            rate_info = rates[loan_type]
            loan_rates.append({
                'bank': bank,
                'loan_type': loan_type.replace('_', ' ').title(),
                'min_rate': rate_info['min'],
                'max_rate': rate_info['max'],
                'avg_rate': round((rate_info['min'] + rate_info['max']) / 2, 2),
                'timestamp': datetime.now().isoformat()
            })
    
    return sorted(loan_rates, key=lambda x: x['avg_rate'])

# ==================== DASHBOARD DATA ====================

def get_dashboard_data():
    """
    Get comprehensive dashboard data with all real-time information
    """
    return {
        'indices': get_market_indices(),
        'top_stocks': get_all_stocks()[:10],
        'cryptocurrencies': get_crypto_prices()[:5],
        'forex': get_forex_rates(),
        'gold': get_gold_price(),
        'silver': get_silver_price(),
        'loan_rates': {
            'home_loan': get_loan_rates('home_loan')[:3],
            'car_loan': get_loan_rates('car_loan')[:3],
            'personal_loan': get_loan_rates('personal_loan')[:3],
        },
        'last_updated': datetime.now().isoformat()
    }
