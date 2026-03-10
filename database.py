"""
SQLite Database Setup and Models
"""
import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Database file path
DB_PATH = 'financial_app.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with all tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age INTEGER,
            profession TEXT,
            annual_income REAL,
            monthly_expenses REAL,
            current_savings REAL,
            existing_loans REAL,
            credit_score INTEGER,
            employment_type TEXT,
            risk_appetite TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Income table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            source TEXT NOT NULL,
            amount REAL NOT NULL,
            frequency TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Budget table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            limit_amount REAL NOT NULL,
            month TEXT,
            year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Goals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal_type TEXT NOT NULL,
            goal_amount REAL NOT NULL,
            current_savings REAL DEFAULT 0,
            years_to_achieve INTEGER,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Loans table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            loan_type TEXT NOT NULL,
            amount REAL NOT NULL,
            interest_rate REAL,
            tenure_months INTEGER,
            emi REAL,
            bank_name TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Investing/Savings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            investment_type TEXT NOT NULL,
            amount REAL NOT NULL,
            return_rate REAL,
            risk_level TEXT,
            date_invested TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

class User:
    """User model"""
    
    @staticmethod
    def create(name, email, password, age=None, profession=None, annual_income=0):
        """Create new user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_password = generate_password_hash(password)
        
        try:
            cursor.execute('''
                INSERT INTO users (name, email, password, age, profession, annual_income)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, email, hashed_password, age, profession, annual_income))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def verify_password(email, password):
        """Verify user password"""
        user = User.get_by_email(email)
        if user and check_password_hash(user['password'], password):
            return user
        return None
    
    @staticmethod
    def update(user_id, **kwargs):
        """Update user info"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        update_fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['annual_income', 'monthly_expenses', 'current_savings', 'existing_loans', 'credit_score', 'risk_appetite']:
                update_fields.append(f'{key} = ?')
                values.append(value)
        
        if not update_fields:
            conn.close()
            return False
        
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return True

class Income:
    """Income model"""
    
    @staticmethod
    def add(user_id, source, amount, frequency='monthly'):
        """Add income"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO income (user_id, source, amount, frequency)
            VALUES (?, ?, ?, ?)
        ''', (user_id, source, amount, frequency))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_by_user(user_id):
        """Get all income for user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM income WHERE user_id = ? ORDER BY date DESC', (user_id,))
        income = cursor.fetchall()
        conn.close()
        return income

class Expense:
    """Expense model"""
    
    @staticmethod
    def add(user_id, category, amount, description=''):
        """Add expense"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (user_id, category, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (user_id, category, amount, description))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_by_user(user_id):
        """Get all expenses for user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (user_id,))
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    @staticmethod
    def get_monthly_total(user_id):
        """Get monthly expense total"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(amount) as total FROM expenses 
            WHERE user_id = ? AND DATE(date) >= date('now', 'start of month')
        ''', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result['total'] if result['total'] else 0

class Goal:
    """Goal model"""
    
    @staticmethod
    def add(user_id, goal_type, goal_amount, years_to_achieve):
        """Add goal"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO goals (user_id, goal_type, goal_amount, years_to_achieve)
            VALUES (?, ?, ?, ?)
        ''', (user_id, goal_type, goal_amount, years_to_achieve))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_by_user(user_id):
        """Get all goals for user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM goals WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        goals = cursor.fetchall()
        conn.close()
        return goals
