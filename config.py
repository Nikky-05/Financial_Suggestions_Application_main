"""
Configuration file for API keys, endpoints, and application settings
"""
import os
from datetime import timedelta

# API Keys (use environment variables in production)
API_KEYS = {
    'ALPHA_VANTAGE': os.getenv('ALPHA_VANTAGE_KEY', 'demo'),  # Get free key from alphavantage.co
    'COINGECKO': None,  # CoinGecko free tier doesn't require API key
}

# API Endpoints
API_ENDPOINTS = {
    'ALPHA_VANTAGE_BASE': 'https://www.alphavantage.co/query',
    'COINGECKO_BASE': 'https://api.coingecko.com/api/v3',
    'YAHOO_FINANCE': 'https://query1.finance.yahoo.com/v8/finance/chart',
    'RBI_REFERENCE_RATE': 'https://www.rbi.org.in/Scripts/ReferenceRateArchive.aspx',
    'GOLD_API': 'https://www.goldapi.io/api',  # Alternative: use web scraping
}

# Cache Configuration (in seconds)
CACHE_EXPIRY = {
    'STOCK_PRICES': 300,  # 5 minutes
    'CRYPTO_PRICES': 60,  # 1 minute
    'GOLD_PRICES': 3600,  # 1 hour
    'FOREX_RATES': 1800,  # 30 minutes
    'MUTUAL_FUNDS': 86400,  # 24 hours (NAV updated once daily)
    'LOAN_RATES': 604800,  # 7 days
    'INDICES': 300,  # 5 minutes
}

# Rate Limiting (requests per minute)
RATE_LIMITS = {
    'ALPHA_VANTAGE': 5,  # Free tier: 5 requests per minute
    'COINGECKO': 50,  # Free tier: 50 requests per minute
    'YAHOO_FINANCE': 2000,  # No official limit, but be reasonable
}

# Indian Stock Market Symbols
INDIAN_STOCKS = {
    'RELIANCE.NS': 'Reliance Industries',
    'TCS.NS': 'Tata Consultancy Services',
    'HDFCBANK.NS': 'HDFC Bank',
    'INFY.NS': 'Infosys',
    'ICICIBANK.NS': 'ICICI Bank',
    'HINDUNILVR.NS': 'Hindustan Unilever',
    'ITC.NS': 'ITC Limited',
    'SBIN.NS': 'State Bank of India',
    'BHARTIARTL.NS': 'Bharti Airtel',
    'KOTAKBANK.NS': 'Kotak Mahindra Bank',
    'LT.NS': 'Larsen & Toubro',
    'AXISBANK.NS': 'Axis Bank',
    'ASIANPAINT.NS': 'Asian Paints',
    'MARUTI.NS': 'Maruti Suzuki',
    'TITAN.NS': 'Titan Company',
}

# Market Indices
INDICES = {
    '^NSEI': 'NIFTY 50',
    '^BSESN': 'SENSEX',
    '^NSEBANK': 'NIFTY Bank',
}

# Cryptocurrencies
CRYPTOCURRENCIES = {
    'bitcoin': 'Bitcoin',
    'ethereum': 'Ethereum',
    'binancecoin': 'Binance Coin',
    'cardano': 'Cardano',
    'ripple': 'XRP',
    'solana': 'Solana',
    'polkadot': 'Polkadot',
    'dogecoin': 'Dogecoin',
    'matic-network': 'Polygon',
    'shiba-inu': 'Shiba Inu',
}

# Currency Pairs
CURRENCY_PAIRS = {
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'GBP': 'British Pound',
    'JPY': 'Japanese Yen',
    'AUD': 'Australian Dollar',
}

# Bank Loan Interest Rates (Static fallback - will be updated with real-time data)
BANK_LOAN_RATES = {
    'SBI': {
        'home_loan': {'min': 8.50, 'max': 9.65},
        'car_loan': {'min': 8.70, 'max': 9.20},
        'personal_loan': {'min': 10.30, 'max': 15.00},
        'education_loan': {'min': 8.50, 'max': 10.50},
    },
    'HDFC': {
        'home_loan': {'min': 8.60, 'max': 9.50},
        'car_loan': {'min': 8.75, 'max': 9.50},
        'personal_loan': {'min': 10.50, 'max': 21.00},
        'education_loan': {'min': 9.00, 'max': 11.00},
    },
    'ICICI': {
        'home_loan': {'min': 8.75, 'max': 9.65},
        'car_loan': {'min': 8.75, 'max': 10.50},
        'personal_loan': {'min': 10.75, 'max': 19.00},
        'education_loan': {'min': 9.50, 'max': 11.50},
    },
    'Axis': {
        'home_loan': {'min': 8.75, 'max': 9.65},
        'car_loan': {'min': 8.80, 'max': 9.80},
        'personal_loan': {'min': 10.49, 'max': 22.00},
        'education_loan': {'min': 9.00, 'max': 11.25},
    },
    'Kotak': {
        'home_loan': {'min': 8.70, 'max': 9.40},
        'car_loan': {'min': 8.70, 'max': 9.50},
        'personal_loan': {'min': 10.99, 'max': 18.00},
        'education_loan': {'min': 9.00, 'max': 11.00},
    },
}

# Mutual Fund Categories (Sample data - will be enhanced with real-time NAV)
MUTUAL_FUND_CATEGORIES = {
    'Large Cap': {'risk': 'Medium', 'expected_return': 12.0},
    'Mid Cap': {'risk': 'Medium-High', 'expected_return': 14.0},
    'Small Cap': {'risk': 'High', 'expected_return': 16.0},
    'Debt Funds': {'risk': 'Low', 'expected_return': 7.0},
    'Hybrid Funds': {'risk': 'Medium', 'expected_return': 10.0},
    'Index Funds': {'risk': 'Medium', 'expected_return': 11.0},
    'ELSS': {'risk': 'Medium-High', 'expected_return': 13.0},
    'Liquid Funds': {'risk': 'Very Low', 'expected_return': 5.5},
    'Gilt Funds': {'risk': 'Low', 'expected_return': 6.5},
    'International Funds': {'risk': 'High', 'expected_return': 15.0},
}

# Commodities
COMMODITIES = {
    'gold': 'Gold (per 10g)',
    'silver': 'Silver (per kg)',
    'crude_oil': 'Crude Oil (per barrel)',
}

# Application Settings
APP_SETTINGS = {
    'DEFAULT_CURRENCY': 'INR',
    'ENABLE_CACHING': True,
    'CACHE_TYPE': 'simple',  # 'simple' or 'redis'
    'MAX_CACHE_SIZE': 1000,
    'TIMEOUT': 10,  # API request timeout in seconds
    'RETRY_ATTEMPTS': 3,
    'RETRY_DELAY': 2,  # seconds
}

# Real Estate Price Index (Sample data for major Indian cities - ₹ per sq ft)
REAL_ESTATE_PRICES = {
    'Mumbai': {'min': 15000, 'max': 50000, 'avg': 25000},
    'Delhi': {'min': 8000, 'max': 30000, 'avg': 15000},
    'Bangalore': {'min': 5000, 'max': 15000, 'avg': 8000},
    'Hyderabad': {'min': 4000, 'max': 10000, 'avg': 6000},
    'Chennai': {'min': 4500, 'max': 12000, 'avg': 7000},
    'Pune': {'min': 5000, 'max': 12000, 'avg': 7500},
    'Kolkata': {'min': 3500, 'max': 8000, 'avg': 5500},
    'Ahmedabad': {'min': 3000, 'max': 7000, 'avg': 4500},
}
