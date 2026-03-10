# Quick Start Guide

Get the Financial Suggestions Application running in 5 minutes.

## ⚡ 5-Minute Setup

### Step 1: Clone & Navigate
```bash
git clone <repository-url>
cd Financial-Suggestions-Application
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\Activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment
```bash
# Copy template
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Or create manually with:
# FLASK_ENV=development
# GEMINI_API_KEY=AIzaSyAdXfCtaViMyBoLW0jI0s48MToxS1qqxf4
# SECRET_KEY=financial-app-secret-key-2024
```

### Step 5: Run Application
```bash
python app.py
```

**🎉 Done!** Open http://localhost:5000

---

## 📝 First Time Setup

### Verify Installation
```bash
python verify_app.py
```

### Generate Fresh Data (Optional)
```bash
# Generate financial data
python generate_financial_data.py

# Generate test users
python generate_dummy_users.py
```

---

## 🔐 Test Login

Use any of these accounts:

```
Email: rahul.sharma1@email.com
Password: password123

Email: priya.patel2@email.com
Password: password123

Email: amit.singh3@email.com
Password: password123
```

---

## 📂 Project Layout

```
├── app.py                    ← Main app (start here!)
├── config.py               ← Configuration
├── database.py             ← Database setup
├── api_integrations.py     ← API calls
├── templates/              ← HTML pages
│   ├── index.html          ← Landing
│   ├── dashboard.html      ← Main page
│   ├── login.html          ← Login
│   └── results.html        ← Recommendations
├── static/                 ← CSS & JS
├── data/                   ← Financial data
└── financial_app.db        ← Database (auto-created)
```

---

## 🚀 Common Tasks

### Register New User
1. Click "Register" at http://localhost:5000/register
2. Fill in the form
3. Click "Register"

### Get Recommendations
1. Login
2. Go to Dashboard
3. Click "Get Recommendations"
4. Fill in your financial profile
5. Click "Calculate"

### Download PDF Report
1. After getting recommendations
2. Click "Download PDF Report"

### Check Market Data
- Visit `http://localhost:5000/dashboard`
- Or API: `http://localhost:5000/api/market-data`

---

## 🐛 Troubleshooting

### "No module named 'X'"
```bash
pip install -r requirements.txt
```

### Port 5000 Already in Use
```bash
# Windows
netstat -ano | findstr :5000

# macOS/Linux
lsof -i :5000

# Kill process and try again
```

### Database Issues
```bash
# Delete and recreate
rm financial_app.db
python generate_dummy_users.py
python app.py
```

### API Errors
- Check `.env` file exists
- Verify `GEMINI_API_KEY` is set
- Check internet connection

---

## 📚 Documentation  

- **README.md** - Full documentation
- **SETUP_COMPLETE.md** - Project summary
- **DEPLOYMENT.md** - Production deployment

---

## 💡 Next Steps

1. Update `.env` with your own API keys
2. Customize financial data in `data/financial_options.xlsx`
3. Modify templates in `templates/` folder
4. Deploy to production (see DEPLOYMENT.md)

---

## 🆘 Need Help?

1. Check README.md
2. Run `python verify_app.py`
3. Check `financial_app.db` exists
4. Ensure all packages installed: `pip list`

---

**Happy Coding!** 🎉
