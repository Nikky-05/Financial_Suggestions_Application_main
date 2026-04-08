"""
Financial Suggestions Application - Production Ready Version
Uses environment variables, proper error handling, and production configurations
"""
from flask import Flask, render_template, request, make_response, jsonify, session, redirect, url_for
from functools import wraps
import pandas as pd
from datetime import datetime, timedelta
import google.generativeai as genai
import io, json, os, logging
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import application modules
from database import init_db, get_db_connection
from api_integrations import (
    get_dashboard_data, get_investment_options_with_realtime_data,
    get_loan_rates, get_market_indices, get_crypto_prices,
    get_gold_price, get_silver_price, get_forex_rates, get_all_stocks
)
from config import BANK_LOAN_RATES
from expense_analyzer import ExpenseCategorizer, get_expense_insights, EXPENSE_CATEGORIES

# ReportLab for PDF generation
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# Initialize Flask app
app = Flask(__name__)

# ==================== CONFIGURATION ====================
app.secret_key = os.getenv('SECRET_KEY', 'change-me-in-production')
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Initialize database
try:
    init_db()
    logger.info("✅ Database initialized successfully")
except Exception as e:
    logger.error(f"❌ Database initialization failed: {e}")

# Configure Google Gemini API
try:
    gemini_key = os.getenv('GEMINI_API_KEY')
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    logger.info("✅ Google Gemini API configured successfully")
except Exception as e:
    logger.error(f"❌ Gemini API configuration failed: {e}")
    model = None

# ==================== UTILITY FUNCTIONS ====================

def format_currency(amount):
    """Format currency in Indian Rupees"""
    try:
        amount = float(amount)
    except Exception:
        return str(amount)
    if amount >= 10000000:
        return f"₹{amount/10000000:.2f} crore"
    elif amount >= 100000:
        return f"₹{amount/100000:.2f} lakh"
    else:
        return f"₹{amount:,.2f}"

def hash_password(password):
    """Hash password for storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash, provided_password):
    """Verify password against stored hash"""
    return stored_hash == hashlib.sha256(provided_password.encode()).hexdigest()

def calculate_monthly_savings(annual_income, goal_price, years_to_achieve, expected_return=7.0):
    """Calculate monthly savings needed to achieve financial goal"""
    monthly_income = annual_income / 12 if annual_income else 0
    monthly_rate = expected_return / 100 / 12
    months = max(1, years_to_achieve * 12)

    if monthly_rate <= 0:
        required_savings = goal_price / months
    else:
        required_savings = goal_price * (monthly_rate / ((1 + monthly_rate)**months - 1 + 1e-12))

    savings_percentage = (required_savings / monthly_income) * 100 if monthly_income > 0 else 0

    return {
        "monthly_savings": round(required_savings, 2),
        "savings_percentage": round(savings_percentage, 2),
        "expected_return": expected_return
    }

def load_financial_data():
    """Load financial options from Excel file"""
    try:
        excel_file = 'data/financial_options.xlsx'
        if not os.path.exists(excel_file):
            logger.warning(f"Excel file not found: {excel_file}. Using fallback data.")
            raise FileNotFoundError
            
        df = pd.read_excel(excel_file, sheet_name=None)
        
        data = {
            'car': df.get('cars', pd.DataFrame()).to_dict('records'),
            'home': df.get('homes', pd.DataFrame()).to_dict('records'),
            'education': df.get('education', pd.DataFrame()).to_dict('records'),
            'retirement': df.get('retirement', pd.DataFrame()).to_dict('records'),
            'investment': df.get('investments', pd.DataFrame()).to_dict('records')
        }
        logger.info(f"✅ Loaded financial data from Excel file")
        return data
    except Exception as e:
        logger.warning(f"Error loading Excel data: {e}. Using fallback sample data.")
        # Fallback sample data
        return {
            'car': [
                {"name": "Maruti Suzuki Swift", "price": 600000},
                {"name": "Hyundai i20", "price": 900000},
                {"name": "Honda City", "price": 1200000},
            ],
            'home': [
                {"name": "1BHK Apartment", "price": 3000000},
                {"name": "2BHK Apartment", "price": 5000000},
                {"name": "3BHK Apartment", "price": 8000000},
            ],
            'education': [
                {"name": "Bachelor's Degree", "price": 500000},
                {"name": "Master's Degree", "price": 1000000},
            ],
            'retirement': [
                {"name": "Modest Fund", "price": 10000000},
                {"name": "Comfortable Fund", "price": 20000000},
            ],
            'investment': [
                {"name": "Fixed Deposit", "return_rate": 6.5, "risk": "Low"},
                {"name": "Mutual Fund", "return_rate": 12.0, "risk": "Medium"},
            ]
        }

def recommend_option(goal_type, annual_income):
    """Recommend financial options based on goal and income"""
    options_map = {
        'car': financial_data.get('car', []),
        'home': financial_data.get('home', []),
        'education': financial_data.get('education', []),
        'retirement': financial_data.get('retirement', []),
        'foreign_education': financial_data.get('education', [])
    }

    if goal_type == 'savings':
        return []

    options = options_map.get(goal_type, [])
    affordable_options = []

    affordability_multipliers = {
        'car': 1.5,
        'home': 5.0,
        'education': 2.0,
        'retirement': 15.0,
        'foreign_education': 3.0
    }

    multiplier = affordability_multipliers.get(goal_type, 1.5)

    for option in options:
        price = option.get("price", 0)
        if price and price <= annual_income * multiplier:
            affordable_options.append(option)

    if not affordable_options and options:
        try:
            return [min(options, key=lambda x: x.get('price', float('inf')))]
        except Exception:
            return options[:1]

    return affordable_options

def generate_gemini_advice(user_data, savings_percentage, goal_type, recommendations):
    """Generate financial advice using Google Gemini"""
    try:
        if not model:
            logger.warning("Gemini model not configured")
            return ["Gemini API not available. Please configure GEMINI_API_KEY."]
            
        goal_price = recommendations[0]['price'] if recommendations else 0

        prompt = f"""
You are a financial advisor and loan consultant.
Generate personalized financial and loan advice for:

Applicant: {user_data.get('name')} (Age: {user_data.get('age')})
Professional: {user_data.get('profession')}
Annual Income: ₹{user_data.get('annual_income')}
Goal: {goal_type} (Cost: ₹{goal_price})
Years to achieve: {user_data.get('years_to_achieve')}
Risk Appetite: {user_data.get('risk_appetite', 'Moderate')}
Current Savings: ₹{user_data.get('current_savings', 0)}
Monthly Expenses: ₹{user_data.get('monthly_expenses', 0)}
Existing Loans: ₹{user_data.get('existing_loans', 0)}
Credit Score: {user_data.get('credit_score', 700)}
Required Savings: {savings_percentage}%

Provide concise financial advice (3-5 bullet points) and 2-3 loan options.
"""
        response = model.generate_content(prompt)
        text = getattr(response, "text", None) or str(response)
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        return lines or ["Unable to generate advice. Please try again."]
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return [
            "Create an emergency fund covering 3–6 months of expenses.",
            "Automate monthly savings into an SIP or recurring deposit.",
            "Reduce high-interest debt before investing aggressively."
        ]

# Load financial data on startup
financial_data = load_financial_data()

# ==================== AUTHENTICATION DECORATORS ====================

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'GET':
        return render_template('register.html')
    
    try:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        age = request.form.get('age') or None
        profession = request.form.get('profession', '').strip()
        annual_income = request.form.get('annual_income') or 0

        # Validation
        if not name or not email or not password:
            return render_template('register.html', error='Required fields missing')
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        if len(password) < 6:
            return render_template('register.html', error='Password must be at least 6 characters')

        # Create user in database
        try:
            age = int(age) if age else None
            annual_income = float(annual_income) if annual_income else 0
        except ValueError:
            return render_template('register.html', error='Invalid input format')

        conn = get_db_connection()
        cursor = conn.cursor()
        
        hashed_password = hash_password(password)
        cursor.execute('''
            INSERT INTO users (name, email, password, age, profession, annual_income)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, hashed_password, age, profession, annual_income))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        session['user_id'] = user_id
        session['user_name'] = name
        logger.info(f"✅ User registered: {email}")
        return redirect(url_for('dashboard'))

    except Exception as e:
        logger.error(f"Registration error: {e}")
        return render_template('register.html', error='Registration failed. Email may already exist.')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'GET':
        return render_template('login.html')
    
    try:
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            return render_template('login.html', error='Email and password required')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, password FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if not user or not verify_password(user['password'], password):
            return render_template('login.html', error='Invalid credentials')

        session['user_id'] = user['id']
        session['user_name'] = user['name']
        logger.info(f"✅ User logged in: {email}")
        return redirect(url_for('dashboard'))

    except Exception as e:
        logger.error(f"Login error: {e}")
        return render_template('login.html', error='Login failed')

@app.route('/logout')
def logout():
    """User logout"""
    logger.info(f"User logged out: {session.get('user_name', 'Unknown')}")
    session.clear()
    return redirect(url_for('login'))

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    try:
        user_id = session.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get user name for greeting
        cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        market_data = get_dashboard_data()
        return render_template('dashboard_expense.html', data=market_data, user_name=user['name'] if user else 'User')
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return render_template('dashboard_expense.html', data={}, error=str(e))

@app.route('/calculate', methods=['POST'])
@login_required
def calculate():
    """Calculate financial recommendations"""
    try:
        name = request.form.get('name', '').strip()
        age = int(request.form.get('age', 0)) if request.form.get('age') else 0
        profession = request.form.get('profession', '').strip()
        annual_income = float(request.form.get('annual_income', 0)) if request.form.get('annual_income') else 0.0
        goal_type = request.form.get('goal_type', 'savings')
        years_to_achieve = int(request.form.get('years_to_achieve', 5)) if request.form.get('years_to_achieve') else 5
        risk_appetite = request.form.get('risk_appetite', 'Moderate')
        current_savings = float(request.form.get('current_savings', 0)) if request.form.get('current_savings') else 0.0
        monthly_expenses = float(request.form.get('monthly_expenses', 0)) if request.form.get('monthly_expenses') else 0.0
        existing_loans = float(request.form.get('existing_loans', 0)) if request.form.get('existing_loans') else 0.0
        credit_score = int(request.form.get('credit_score', 700)) if request.form.get('credit_score') else 700

        user_data = {
            'name': name, 'age': age, 'profession': profession, 'annual_income': annual_income,
            'goal_type': goal_type, 'years_to_achieve': years_to_achieve, 'risk_appetite': risk_appetite,
            'current_savings': current_savings, 'monthly_expenses': monthly_expenses,
            'existing_loans': existing_loans, 'credit_score': credit_score
        }

        recommendations = recommend_option(user_data['goal_type'], user_data['annual_income'])

        if user_data['goal_type'] not in ['savings', 'foreign_education']:
            expected_return = 8.0 if user_data['goal_type'] == 'retirement' else 7.0
            goal_price = recommendations[0].get('price', 0) if recommendations else 0
            savings_calculation = calculate_monthly_savings(
                user_data['annual_income'], goal_price, user_data['years_to_achieve'], expected_return
            )
        else:
            savings_calculation = {}

        savings_percent = savings_calculation.get('savings_percentage', 20) if savings_calculation else 20
        advice = generate_gemini_advice(user_data, savings_percent, user_data['goal_type'], recommendations)
        
        realtime_investments = get_investment_options_with_realtime_data(user_data['risk_appetite'].lower())
        loan_type_map = {'car': 'car_loan', 'home': 'home_loan', 'education': 'education_loan', 'foreign_education': 'education_loan'}
        loan_type = loan_type_map.get(user_data['goal_type'], 'personal_loan')
        current_loan_rates = get_loan_rates(loan_type)
        
        market_indices = get_market_indices()
        gold_price = get_gold_price()

        result_data = {
            'user_data': user_data,
            'recommendations': recommendations,
            'savings_calculation': savings_calculation,
            'advice': advice,
            'realtime_investments': realtime_investments,
            'loan_rates': current_loan_rates,
            'market_indices': market_indices,
            'gold_price': gold_price,
            'format_currency': format_currency,
        }

        logger.info(f"✅ Calculation completed for user: {name}")
        return render_template('results.html', **result_data)

    except Exception as e:
        logger.error(f"Calculation error: {e}")
        return render_template('results.html', error=str(e))

@app.route('/download_pdf', methods=['POST'])
@login_required
def download_pdf():
    """Generate and download PDF report"""
    try:
        report_data_raw = request.form.get('report_data') or request.data.decode('utf-8')
        report_data = json.loads(report_data_raw)
    except Exception as e:
        logger.error(f"PDF report parsing error: {e}")
        return "Error generating PDF", 500

    user_data = report_data.get('user_data', {})
    recommendations = report_data.get('recommendations', [])
    savings = report_data.get('savings_calculation', {})
    advice = report_data.get('advice', [])

    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        elements = []
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        subtitle_style = styles["Heading2"]
        normal = styles["Normal"]

        elements.append(Paragraph("Financial Recommendation Report", title_style))
        elements.append(Spacer(1, 8))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal))
        elements.append(Spacer(1, 12))

        # User Information
        elements.append(Paragraph("User Information", subtitle_style))
        user_table = [
            ["Name", user_data.get("name", "")],
            ["Age", str(user_data.get("age", ""))],
            ["Annual Income", format_currency(user_data.get('annual_income', 0))],
            ["Risk Appetite", user_data.get("risk_appetite", "")]
        ]
        t = Table(user_table, hAlign="LEFT", colWidths=[140, 340])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.whitesmoke),
            ("GRID", (0,0), (-1,-1), 0.5, colors.lightgrey)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

        # Financial Advice
        elements.append(Paragraph("Financial Advice", subtitle_style))
        if advice:
            for line in advice:
                elements.append(Paragraph(f"• {line}", normal))
        elements.append(Spacer(1, 12))

        doc.build(elements)
        pdf_value = buffer.getvalue()
        buffer.close()

        response = make_response(pdf_value)
        response.headers["Content-Disposition"] = "attachment; filename=financial_report.pdf"
        response.headers["Content-Type"] = "application/pdf"
        logger.info(f"✅ PDF generated for user: {user_data.get('name', 'Unknown')}")
        return response

    except Exception as e:
        logger.error(f"PDF generation error: {e}")
        return "Error generating PDF", 500

# ==================== API ROUTES ====================

@app.route('/api/market-data')
def api_market_data():
    """API endpoint for market data"""
    try:
        data = get_dashboard_data()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Market data error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stocks')
def api_stocks():
    """Get stock prices"""
    try:
        stocks = get_all_stocks()
        return jsonify(stocks)
    except Exception as e:
        logger.error(f"Stocks error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/crypto')
def api_crypto():
    """Get crypto prices"""
    try:
        crypto = get_crypto_prices()
        return jsonify(crypto)
    except Exception as e:
        logger.error(f"Crypto error: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== EXPENSE TRACKING ROUTES ====================

@app.route('/expenses')
@login_required
def expenses():
    """View expenses page"""
    try:
        user_id = session.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all-time expenses (no date filter)
        cursor.execute('''
            SELECT * FROM expenses 
            WHERE user_id = ?
            ORDER BY date DESC
            LIMIT 100
        ''', (user_id,))
        
        expenses_list = [dict(row) for row in cursor.fetchall()]
        
        # Get all-time income (no date filter)
        cursor.execute('''
            SELECT * FROM income 
            WHERE user_id = ?
            ORDER BY date DESC
        ''', (user_id,))
        income_list = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Calculate totals from ALL records
        total_income = sum([i['amount'] for i in income_list])
        total_expenses = sum([e['amount'] for e in expenses_list])
        balance = total_income - total_expenses
        
        return render_template('expenses.html', 
                             expenses=expenses_list, 
                             income=income_list,
                             total_income=total_income,
                             total_expenses=total_expenses,
                             balance=balance,
                             format_currency=format_currency)
    except Exception as e:
        logger.error(f"Expenses page error: {e}")
        return render_template('expenses.html', error=str(e))

@app.route('/add-expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add new expense"""
    try:
        if request.method == 'GET':
            return render_template('add_expense.html', categories=list(EXPENSE_CATEGORIES.keys()))
        
        # POST request
        user_id = session.get('user_id')
        amount = float(request.form.get('amount', 0))
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        expense_date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        # Auto-categorize if not provided
        if not category:
            category, _ = ExpenseCategorizer.categorize(description)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (user_id, amount, description, category, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, amount, description, category, expense_date))
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Expense added for user {user_id}: ₹{amount} - {category}")
        return redirect(url_for('expenses'))
        
    except Exception as e:
        logger.error(f"Add expense error: {e}")
        return render_template('add_expense.html', error=str(e), categories=list(EXPENSE_CATEGORIES.keys()))

@app.route('/add-income', methods=['GET', 'POST'])
@login_required
def add_income():
    """Add income"""
    try:
        if request.method == 'GET':
            return render_template('add_income.html')
        
        # POST request
        user_id = session.get('user_id')
        amount = float(request.form.get('amount', 0))
        source = request.form.get('source', 'Salary').strip()
        income_date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
        frequency = request.form.get('frequency', 'Monthly')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO income (user_id, amount, source, frequency, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, amount, source, frequency, income_date))
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Income added for user {user_id}: ₹{amount} - {source}")
        return redirect(url_for('expenses'))
        
    except Exception as e:
        logger.error(f"Add income error: {e}")
        return render_template('add_income.html', error=str(e))

@app.route('/delete-all-income', methods=['POST'])
@login_required
def delete_all_income():
    """Delete all income records for current user"""
    try:
        user_id = session.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete all income records
        cursor.execute('DELETE FROM income WHERE user_id = ?', (user_id,))
        conn.commit()
        
        deleted_count = cursor.rowcount
        conn.close()
        
        logger.info(f"✅ Deleted {deleted_count} income records for user {user_id}")
        return jsonify({'success': True, 'message': f'Deleted {deleted_count} income records'})
    except Exception as e:
        logger.error(f"Delete all income error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/financial-insights')
@login_required
def financial_insights():
    """Get AI-powered financial insights and analysis"""
    try:
        user_id = session.get('user_id')
        conn = get_db_connection()
        
        insights = get_expense_insights(user_id, conn)
        conn.close()
        
        return render_template('insights.html', 
                             insights=insights,
                             format_currency=format_currency)
    except Exception as e:
        logger.error(f"Financial insights error: {e}")
        return render_template('insights.html', error=str(e))

@app.route('/api/expense-stats')
@login_required
def api_expense_stats():
    """API endpoint for expense statistics (for charts)"""
    try:
        user_id = session.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        
        insights = get_expense_insights(user_id, conn)
        stats = insights['stats']
        
        # Calculate income breakdown by source
        cursor.execute('''
            SELECT source, SUM(amount) as total 
            FROM income 
            WHERE user_id = ? 
            GROUP BY source 
            ORDER BY total DESC
        ''', (user_id,))
        
        income_breakdown = {}
        for row in cursor.fetchall():
            income_breakdown[row['source']] = row['total']
        
        # Format for charts
        chart_data = {
            'total_income': stats['total_income'],
            'total_expenses': stats['total_expenses'],
            'balance': stats['balance'],
            'savings_rate': stats['savings_rate'],
            'category_breakdown': stats['category_breakdown'],
            'income_breakdown': income_breakdown,
            'top_categories': stats['top_categories'],
            'average_expense': stats['average_expense']
        }
        
        conn.close()
        return jsonify(chart_data)
    except Exception as e:
        logger.error(f"Expense stats error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/delete-expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete an expense"""
    try:
        user_id = session.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify ownership
        cursor.execute('SELECT user_id FROM expenses WHERE id = ?', (expense_id,))
        expense = cursor.fetchone()
        
        if not expense or expense['user_id'] != user_id:
            conn.close()
            return jsonify({'error': 'Unauthorized'}), 403
        
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Expense {expense_id} deleted for user {user_id}")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Delete expense error: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {request.path}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    return render_template('500.html'), 500

# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
