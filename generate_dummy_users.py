"""
Dummy user data generator for SQLite database
Creates 500+ sample users with financial profiles
"""
import sqlite3
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import os
import hashlib

DB_PATH = 'financial_app.db'

def generate_dummy_users(num_users=500):
    """Generate dummy user data"""
    
    first_names = ['Rahul', 'Priya', 'Amit', 'Neha', 'Vikram', 'Ananya', 'Arjun', 'Divya', 'Rohan', 
                   'Pooja', 'Nikhil', 'Shreya', 'Karan', 'Aisha', 'Dev', 'Isha', 'Ravi', 'Sana',
                   'Akshay', 'Anjali', 'Varun', 'Zara', 'Siddharth', 'Diya', 'Abhishek', 'Meera',
                   'Aryan', 'Koyal', 'Harsh', 'Divyam', 'Samrat', 'Richa', 'Pranav', 'Swati']
    
    last_names = ['Sharma', 'Patel', 'Singh', 'Gupta', 'Khan', 'Kumar', 'Verma', 'Malik', 'Reddy',
                  'Rao', 'Iyer', 'Nair', 'Chopra', 'Bhat', 'Menon', 'Das', 'Dutta', 'Sinha']
    
    professions = ['Software Engineer', 'Doctor', 'Lawyer', 'Accountant', 'Business Owner', 'Teacher',
                  'Banker', 'Consultant', 'Entrepreneur', 'Manager', 'Engineer', 'Analyst',
                  'Architect', 'Designer', 'Sales Executive', 'HR Manager', 'Freelancer', 'Startup Founder']
    
    employment_types = ['Salaried', 'Self-Employed', 'Business Owner', 'Freelancer', 'Student', 'Retired']
    
    risk_appetites = ['Conservative', 'Moderate', 'Aggressive']
    
    users = []
    
    for i in range(1, num_users + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        
        email = f"{first_name.lower()}.{last_name.lower()}{i}@email.com"
        password = "password123"  # Default password for demo
        # Simple hashing for demo purposes - use proper hashing in production
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        age = random.randint(22, 65)
        profession = random.choice(professions)
        
        # Income distribution (INR)
        base_salaries = [300000, 500000, 700000, 1000000, 1500000, 2000000, 3000000, 5000000]
        annual_income = random.choice(base_salaries) + random.randint(-100000, 500000)
        
        monthly_expenses = annual_income / 12 * random.uniform(0.4, 0.8)
        current_savings = random.choice([0, 50000, 100000, 500000, 1000000, 2000000, 5000000])
        existing_loans = random.choice([0, 500000, 1000000, 2000000, 5000000]) if random.random() > 0.6 else 0
        credit_score = random.randint(600, 900)
        employment_type = random.choice(employment_types)
        risk_appetite = random.choice(risk_appetites)
        
        created_at = datetime.now() - timedelta(days=random.randint(1, 365))
        
        users.append((
            name,
            email,
            hashed_password,
            age,
            profession,
            annual_income,
            monthly_expenses,
            current_savings,
            existing_loans,
            credit_score,
            employment_type,
            risk_appetite,
            created_at,
            datetime.now()
        ))
    
    return users

def generate_dummy_goals(num_goals=500):
    """Generate dummy goal data"""
    goal_types = ['car', 'home', 'education', 'retirement', 'foreign_education', 'vacation', 'business']
    goal_amounts = [300000, 600000, 1000000, 3000000, 5000000, 10000000, 20000000, 50000000]
    statuses = ['active', 'completed', 'on_track', 'behind_schedule']
    
    goals = []
    for i in range(1, num_goals + 1):
        user_id = random.randint(1, 500)
        goal_type = random.choice(goal_types)
        goal_amount = random.choice(goal_amounts)
        current_savings = random.randint(0, int(goal_amount * 0.5))
        years_to_achieve = random.randint(1, 20)
        status = random.choice(statuses)
        created_at = datetime.now() - timedelta(days=random.randint(1, 365))
        
        goals.append((
            user_id,
            goal_type,
            goal_amount,
            current_savings,
            years_to_achieve,
            status,
            created_at
        ))
    
    return goals

def generate_dummy_expenses(num_expenses=1000):
    """Generate dummy expense data"""
    categories = ['Groceries', 'Utilities', 'Rent', 'Transportation', 'Entertainment', 
                 'Healthcare', 'Food', 'Shopping', 'Insurance', 'Education', 'Gym', 'Mobile Phone']
    
    expenses = []
    for i in range(1, num_expenses + 1):
        user_id = random.randint(1, 500)
        category = random.choice(categories)
        amount = random.randint(500, 50000)
        description = f"{category} expense"
        date = datetime.now() - timedelta(days=random.randint(0, 90))
        
        expenses.append((
            user_id,
            category,
            amount,
            description,
            date
        ))
    
    return expenses

def generate_dummy_income(num_income=500):
    """Generate dummy income data"""
    sources = ['Salary', 'Bonus', 'Freelance', 'Investment Returns', 'Rental Income', 'Business']
    frequencies = ['Monthly', 'Quarterly', 'Annual', 'One-time']
    
    incomes = []
    for i in range(1, num_income + 1):
        user_id = random.randint(1, 500)
        source = random.choice(sources)
        amount = random.randint(10000, 200000)
        frequency = random.choice(frequencies)
        date = datetime.now() - timedelta(days=random.randint(0, 90))
        
        incomes.append((
            user_id,
            source,
            amount,
            frequency,
            date
        ))
    
    return incomes

def populate_database():
    """Populate database with dummy data"""
    
    # Remove existing database
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
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
    
    # Insert users
    print("📝 Generating 500 dummy users...")
    users = generate_dummy_users(500)
    cursor.executemany('''
        INSERT INTO users (name, email, password, age, profession, annual_income, 
                          monthly_expenses, current_savings, existing_loans, credit_score,
                          employment_type, risk_appetite, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', users)
    
    # Insert goals
    print("🎯 Generating 500 dummy goals...")
    goals = generate_dummy_goals(500)
    cursor.executemany('''
        INSERT INTO goals (user_id, goal_type, goal_amount, current_savings, years_to_achieve, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', goals)
    
    # Insert expenses
    print("💸 Generating 1000 dummy expenses...")
    expenses = generate_dummy_expenses(1000)
    cursor.executemany('''
        INSERT INTO expenses (user_id, category, amount, description, date)
        VALUES (?, ?, ?, ?, ?)
    ''', expenses)
    
    # Insert income
    print("💰 Generating 500 dummy income records...")
    incomes = generate_dummy_income(500)
    cursor.executemany('''
        INSERT INTO income (user_id, source, amount, frequency, date)
        VALUES (?, ?, ?, ?, ?)
    ''', incomes)
    
    conn.commit()
    
    # Print summary
    counts = cursor.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    print(f"\n✅ Database populated successfully!")
    print(f"📊 Database Summary:")
    print(f"   - Users: {counts}")
    print(f"   - Goals: {cursor.execute('SELECT COUNT(*) FROM goals').fetchone()[0]}")
    print(f"   - Expenses: {cursor.execute('SELECT COUNT(*) FROM expenses').fetchone()[0]}")
    print(f"   - Income: {cursor.execute('SELECT COUNT(*) FROM income').fetchone()[0]}")
    print(f"   - Database file: {DB_PATH}")
    
    conn.close()

if __name__ == '__main__':
    populate_database()
