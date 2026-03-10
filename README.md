# Financial Suggestions Application

A comprehensive web-based financial planning and advisory platform that provides personalized financial recommendations using AI (Google Gemini) and real-time market data.

## 🎯 Features

### Core Features
- **Personalized Financial Profiling**: Capture user demographics, income, savings, loans, and risk appetite
- **Smart Goal Planning**: Support for major financial milestones (car, home, education, retirement, etc.)
- **AI-Powered Recommendations**: Leverage Google Gemini API for personalized financial advice
- **Real-Time Market Data**: Integration with yfinance, CoinGecko, and other financial APIs
- **PDF Report Generation**: Create detailed financial recommendation reports
- **Rich Dashboard**: Real-time market overview and investment tracking

### Financial Goals Supported
- 🚗 Car Purchase Planning
- 🏠 Real Estate/Home Planning
- 🎓 Education (Domestic & International)
- 🏦 Retirement Planning
- 💰 Investment Dashboard
- 💳 Loan Management

### Real-Time Integrations
- **Stock Market**: Indian stocks (NSE), indices (NIFTY, SENSEX)
- **Cryptocurrencies**: Bitcoin, Ethereum, and 8+ cryptocurrencies
- **Precious Metals**: Gold and Silver prices
- **Forex Rates**: USD, EUR, GBP, JPY, AUD conversion rates
- **Loan Rates**: Real-time rates from major Indian banks
- **Investment Options**: Mutual funds, ETFs, and direct stocks

## 📊 Project Statistics

- **Excel Data**: 5,031 rows of financial options across 6 categories
- **Database**: 500+ dummy users with 2,000+ associated records
- **Lines of Code**: 1,600+ lines of production-ready Python
- **HTML Templates**: 6 responsive web templates

### Data Structure
| Category | Records |
|----------|---------|
| Cars | 986 |
| Homes | 1,020 |
| Education | 1,000 |
| Investments | 1,000 |
| Retirement | 1,000 |
| Retirement Products | 25 |
| Users (SQLite) | 500 |
| User Goals | 500 |
| Expenses | 1,000+ |
| Income Records | 500+ |

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Financial-Suggestions-Application
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\Activate.ps1
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env with your API keys
   nano .env  # Linux/Mac
   # or
   code .env  # VS Code
   ```

5. **Generate dummy data (optional)**
   ```bash
   # Generate Excel financial data
   python generate_financial_data.py
   
   # Populate database with sample users
   python generate_dummy_users.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open browser and navigate to: `http://localhost:5000`

## 🔐 Environment Configuration

Create a `.env` file based on `.env.example`:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key

# Alpha Vantage API (optional, for stock data)
ALPHA_VANTAGE_KEY=your-alpha-vantage-key

# Application Settings
APP_PORT=5000
LOG_LEVEL=INFO
```

### Getting API Keys

1. **Google Gemini API**
   - Get free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. **Alpha Vantage API** (Optional)
   - Free tier at [Alpha Vantage](https://www.alphavantage.co/api_signup/)

## 📁 Project Structure

```
Financial-Suggestions-Application/
├── app.py                          # Main Flask application
├── config.py                       # Configuration constants
├── database.py                     # SQLite database models
├── api_integrations.py             # Real-time data integrations
├── generate_financial_data.py      # Generate dummy financial data
├── generate_dummy_users.py         # Generate dummy users
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (create from .env.example)
├── .gitignore                      # Git ignore patterns
├── data/
│   └── financial_options.xlsx      # 5,000+ rows of financial options
├── templates/
│   ├── base.html                   # Base template
│   ├── index.html                  # Home page
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── dashboard.html              # Dashboard
│   └── results.html                # Results/recommendations
├── static/
│   ├── style.css                   # Main styles
│   ├── css/
│   │   └── realtime.css            # Real-time data styles
│   └── js/
│       └── realtime.js             # Real-time updates JavaScript
└── financial_app.db                # SQLite database (auto-created)
```

## 🗄️ Database Schema

### Tables
- **users**: User profiles and financial information
- **goals**: Financial goals and targets
- **expenses**: Expense tracking and categorization
- **income**: Income sources and records
- **loans**: Loan details and EMI tracking
- **investments**: Investment portfolio and tracking
- **budget**: Budget limits and tracking

## 🔄 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Main Routes
- `GET /` - Home (redirects to login/dashboard)
- `GET /dashboard` - Dashboard with market data
- `POST /calculate` - Calculate recommendations
- `POST /download_pdf` - Generate PDF report

### Data APIs
- `GET /api/market-data` - Market overview
- `GET /api/stocks` - Indian stock prices
- `GET /api/crypto` - Cryptocurrency prices

## 💡 Key Features Explanation

### Financial Recommendations
The app calculates:
- **Monthly Savings Needed**: Based on goal amount, timeline, and expected returns
- **Affordability Analysis**: Recommends options within user's income bracket
- **Risk Assessment**: Matches investments to user's risk appetite

### Real-Time Data
- Stock prices update every 5 minutes (cached)
- Crypto prices update every 1 minute (cached)
- Loan rates update weekly (cached)

### AI Integration
- Google Gemini generates personalized financial advice
- Considers user's income, expenses, existing loans, and goals
- Provides specific loan product recommendations

## 🛠️ Development

### Running Tests
```bash
# Check for syntax errors
python -m py_compile *.py

# List coverage of modules
python -c "import app, database, api_integrations; print('✅ All modules imported successfully')"
```

### Adding New Features
1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test locally
3. Commit with descriptive messages
4. Push to repository

## 📦 Production Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Environment Variables for Production
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-secure-key>
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm financial_app.db

# Recreate with dummy data
python generate_dummy_users.py
```

### Missing Dependencies
```bash
# Reinstall all requirements
pip install --upgrade -r requirements.txt
```

### API Key Issues
- Verify `.env` file is in project root
- Check API key validity
- Ensure `python-dotenv` is installed

## 📝 Sample Credentials

Test the application with these sample users:

| Email | Password | Purpose |
|-------|----------|---------|
| rahul.sharma1@email.com | password123 | Testing |
| priya.patel2@email.com | password123 | Testing |
| amit.singh3@email.com | password123 | Testing |

## 📊 Data Generation

### Financial Data Excel File
- **986 Cars**: Multiple categories and price ranges
- **1,020 Homes**: Various cities and property types
- **1,000 Education**: Degrees, courses, institutions
- **1,000 Investments**: Various investment vehicles
- **1,000 Retirement**: Scenarios and planning options

### Database Users
- 500 unique users with varied profiles
- 500 financial goals
- 1,000+ expense records
- 500+ income records

## 🔒 Security Features

- ✅ Password hashing with SHA-256
- ✅ Session management with secure cookies
- ✅ Environment variable protection
- ✅ SQL injection prevention via parameterized queries
- ✅ CSRF token support (via Flask-Session)
- ✅ Secure headers configuration

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review error logs in console
3. Check `.env` configuration

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Google Generative AI (Gemini) for AI recommendations
- yfinance for stock market data
- CoinGecko for cryptocurrency data
- Flask community for excellent web framework

## 📈 Future Enhancements

- [ ] Mobile app version
- [ ] Advanced portfolio analytics
- [ ] Automated investment suggestions
- [ ] Tax optimization recommendations
- [ ] Healthcare &insurance planning
- [ ] Export to multiple formats (CSV, JSON)
- [ ] Real-time notifications
- [ ] Multi-language support
- [ ] Advanced charting and visualization
- [ ] Integration with brokers and banks

---

**Version**: 1.0.0  
**Last Updated**: March 2026  
**Status**: Production Ready ✅
