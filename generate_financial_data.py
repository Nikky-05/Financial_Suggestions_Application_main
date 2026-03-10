"""
Generate dummy financial data for the application
Creates Excel file with 1000+ rows of financial options
"""
import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# ================ CAR OPTIONS ================
cars_data = []
car_models = [
    'Maruti Suzuki Swift', 'Maruti Suzuki Baleno', 'Hyundai i20', 'Hyundai i10',
    'Honda City', 'Honda Jazz', 'Toyota Fortuner', 'Toyota Innova', 'Toyota Glanza',
    'Tata Nexon', 'Tata Nexon EV', 'Tata Harrier', 'Mahindra XUV500', 'Mahindra XUV300',
    'Mahindra Bolero', 'Kia Seltos', 'Kia Seltos EV', 'Renault Kwid', 'Renault Duster',
    'Ford EcoSport', 'Ford Mustang', 'BMW 3 Series', 'Audi A4', 'Mercedes C-Class',
    'Skoda Superb', 'Volkswagen Jetta', 'MG Hector', 'Citroen C5 Aircross', 'BYD Atto 2'
]

for i, car in enumerate(car_models * 34):  # ~1020 rows
    base_price = random.randint(300000, 5000000)
    cars_data.append({
        'Car_ID': i + 1,
        'Name': f"{car} - Model {i % 10 + 2024}",
        'Price': base_price,
        'Price_Range': 'Budget' if base_price < 700000 else 'Mid-Range' if base_price < 2000000 else 'Premium',
        'Fuel_Type': random.choice(['Petrol', 'Diesel', 'CNG', 'Electric']),
        'Transmission': random.choice(['Manual', 'Automatic']),
        'Mileage': round(random.uniform(15, 25), 1),
        'Seating': random.choice([5, 7, 8, 9]),
        'Year': 2024 + (i % 3),
        'Insurance_Cost': round(base_price * 0.03),
        'Resale_Value_5yr': round(base_price * 0.5 + random.randint(-50000, 100000)),
    })

cars_df = pd.DataFrame(cars_data)

# ================ HOME OPTIONS ================
homes_data = []
home_types = ['1BHK', '2BHK', '3BHK', '4BHK', '5BHK', 'Villa', 'Penthouse', 'Studio', 'Duplex']
cities = ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai', 'Kolkata', 'Ahmedabad', 'Surat', 'Jaipur']
localities = ['Downtown', 'Suburban', 'Outskirts', 'Premium Area', 'Developing Area', 'Business District']

for i in range(1, 1021):
    home_type = random.choice(home_types)
    city = random.choice(cities)
    locality = random.choice(localities)
    
    base_price_per_sqft = random.randint(3000, 80000)
    sqft = random.randint(400, 5000)
    price = base_price_per_sqft * sqft
    
    homes_data.append({
        'Property_ID': i,
        'Type': home_type,
        'City': city,
        'Locality': locality,
        'Price': price,
        'Price_Range': 'Budget' if price < 3000000 else 'Mid-Range' if price < 8000000 else 'Luxury',
        'Area_SqFt': sqft,
        'Price_Per_SqFt': base_price_per_sqft,
        'Bedrooms': int(home_type[0]) if home_type[0].isdigit() else random.randint(1, 5),
        'Bathrooms': random.randint(1, 4),
        'Parking': random.randint(0, 3),
        'Furnishing': random.choice(['Unfurnished', 'Semi-Furnished', 'Furnished']),
        'Age_Years': random.randint(0, 30),
        'Maintenance_Annual': round(price * 0.005),
        'Expected_Appreciation_5yr': round(price * 0.25 + random.randint(-200000, 500000)),
    })

homes_df = pd.DataFrame(homes_data)

# ================ EDUCATION OPTIONS ================
education_data = []
degree_types = ['Bachelor\'s Degree', 'Master\'s Degree', 'Ph.D.', 'Diploma', 'Certification', 'Professional Course']
fields = ['Engineering', 'Medical', 'Business', 'Arts', 'Science', 'Law', 'Architecture', 'Agriculture', 'Commerce', 'Design']
institutions = ['Public University', 'Private University', 'Online Platform', 'Institute', 'College', 'Academy']
countries = ['India', 'USA', 'UK', 'Canada', 'Australia', 'Germany', 'Singapore', 'New Zealand']

for i in range(1, 1001):
    degree = random.choice(degree_types)
    field = random.choice(fields)
    institution_type = random.choice(institutions)
    country = random.choice(countries)
    
    base_cost = random.randint(100000, 5000000) if country == 'India' else random.randint(1000000, 10000000)
    
    education_data.append({
        'Course_ID': i,
        'Degree_Type': degree,
        'Field': field,
        'Institution_Type': institution_type,
        'Country': country,
        'Cost_INR': base_cost,
        'Duration_Years': random.randint(1, 5),
        'Course_Rating': round(random.uniform(3.0, 5.0), 1),
        'Placement_Rate': random.randint(60, 100),
        'Average_Starting_Salary': base_cost * random.uniform(1, 5),
        'Scholarships_Available': random.choice([True, False]),
        'Scholarship_Amount': round(base_cost * random.uniform(0, 0.5)) if random.choice([True, False]) else 0,
        'Study_Mode': random.choice(['Full-Time', 'Part-Time', 'Online', 'Hybrid']),
    })

education_df = pd.DataFrame(education_data)

# ================ INVESTMENT OPTIONS ================
investments_data = []
investment_types = [
    'Fixed Deposit', 'Savings Account', 'PPF (Public Provident Fund)',
    'NSC (National Savings Certificate)', 'Equity Mutual Fund', 'Debt Mutual Fund',
    'Hybrid Mutual Fund', 'Direct Stocks', 'Gold', 'Silver', 'Real Estate',
    'Cryptocurrency', 'Bonds', 'Treasury Bills', 'ULIPs', 'SIP',
    'Peer-to-Peer Lending', 'Corporate Deposits', 'Senior Citizen Savings'
]
banks = ['HDFC', 'ICICI', 'SBI', 'Axis', 'IDBI', 'PNB', 'Kotak', 'Canara', 'BOI', 'Federal']

for i in range(1, 1001):
    investment_type = random.choice(investment_types)
    bank = random.choice(banks) if 'Fund' not in investment_type and 'Direct' not in investment_type else None
    
    min_investment = random.randint(1000, 100000)
    return_rate = random.uniform(3.5, 18)
    risk_level = 'Low' if return_rate < 6 else 'Medium' if return_rate < 12 else 'High'
    
    investments_data.append({
        'Investment_ID': i,
        'Type': investment_type,
        'Bank_Provider': bank or 'Market',
        'Min_Investment': min_investment,
        'Return_Rate_Annual': round(return_rate, 2),
        'Risk_Level': risk_level,
        'Liquidity': random.choice(['High', 'Medium', 'Low']),
        'Tenure_Years': random.choice([1, 2, 3, 5, 7, 10, 15, 20, 25]),
        'Tax_Treatment': random.choice(['Fully Taxable', 'Partially Tax-Free', 'Tax-Free']),
        'Max_Investment': random.choice([None, 50000, 150000, 500000, 1000000]),
        'Maturity_Bonus': random.choice([True, False]),
        'Withdrawal_Charges': random.choice([0, 100, 500, 1000]),
        'Rating': round(random.uniform(3.0, 5.0), 1),
    })

investments_df = pd.DataFrame(investments_data)

# ================ RETIREMENT OPTIONS ================
retirement_data = []
retirement_scenarios = []

for i in range(1, 1001):
    current_age = random.randint(25, 50)
    retirement_age = random.randint(55, 65)
    life_expectancy = random.randint(80, 100)
    years_in_retirement = life_expectancy - retirement_age
    annual_expense = random.randint(300000, 2000000)
    target_corpus = annual_expense * years_in_retirement
    
    retirement_scenario = {
        'Scenario_ID': i,
        'Current_Age': current_age,
        'Retirement_Age': retirement_age,
        'Life_Expectancy': life_expectancy,
        'Years_In_Retirement': years_in_retirement,
        'Annual_Expense_Current': annual_expense,
        'Inflation_Rate': round(random.uniform(5, 7), 2),
        'Projected_Annual_Expense': round(annual_expense * ((1 + random.uniform(0.05, 0.07)) ** (retirement_age - current_age))),
        'Target_Corpus_Required': target_corpus,
        'Investment_Return_Assumed': round(random.uniform(7, 12), 2),
        'Monthly_Savings_Needed': round(target_corpus / ((retirement_age - current_age) * 12)),
        'Risk_Profile': random.choice(['Conservative', 'Moderate', 'Aggressive']),
        'Life_Insurance_Needed': random.choice([True, False]),
    }
    retirement_scenario['Life_Insurance_Amount'] = target_corpus if retirement_scenario['Life_Insurance_Needed'] else 0
    retirement_data.append(retirement_scenario)

retirement_df = pd.DataFrame(retirement_data)

# ================ RETIREMENT PRODUCTS ================
retirement_products_data = []
product_types = ['Pension Plan', 'Annuity Plan', 'NPS (National Pension Scheme)', 'APY (Atal Pension Yojana)', 'EPF']

for i in range(1, 26):
    retirement_products_data.append({
        'Product_ID': i,
        'Product_Name': f"{random.choice(product_types)} - {i}",
        'Provider': random.choice(['LIC', 'HDFC Life', 'ICICI Prudential', 'SBI Life', 'Max Life', 'IRDA']),
        'Min_Investment': random.choice([500, 1000, 2000, 5000, 10000]),
        'Expected_Return': round(random.uniform(7, 9), 2),
        'Pension_Start_Age': random.choice([55, 58, 60, 65]),
        'Annual_Pension_Per_Lakh': random.randint(4000, 8000),
        'Lock_in_Period': random.choice([3, 5, 7, 10, 15]),
        'Flexibility': random.choice(['Low', 'Medium', 'High']),
    })

retirement_products_df = pd.DataFrame(retirement_products_data)

# Create Excel writer and write all sheets
excel_file = 'data/financial_options.xlsx'
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    cars_df.to_excel(writer, sheet_name='cars', index=False)
    homes_df.to_excel(writer, sheet_name='homes', index=False)
    education_df.to_excel(writer, sheet_name='education', index=False)
    investments_df.to_excel(writer, sheet_name='investments', index=False)
    retirement_df.to_excel(writer, sheet_name='retirement', index=False)
    retirement_products_df.to_excel(writer, sheet_name='retirement_products', index=False)

print(f"✅ Dummy data created successfully!")
print(f"📊 File: {excel_file}")
print(f"📈 Data Summary:")
print(f"   - Cars: {len(cars_df)} rows")
print(f"   - Homes: {len(homes_df)} rows")
print(f"   - Education: {len(education_df)} rows")
print(f"   - Investments: {len(investments_df)} rows")
print(f"   - Retirement: {len(retirement_df)} rows")
print(f"   - Retirement Products: {len(retirement_products_df)} rows")
print(f"   - Total: {len(cars_df) + len(homes_df) + len(education_df) + len(investments_df) + len(retirement_df) + len(retirement_products_df)} rows")
