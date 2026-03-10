#!/usr/bin/env python
"""
Setup script for Financial Suggestions Application
Initializes database, generates dummy data, and verifies all components
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def check_requirements():
    """Check if all required files exist"""
    print_header("Checking Requirements")
    
    required_files = [
        'requirements.txt',
        'app.py',
        'config.py',
        'database.py',
        'api_integrations.py'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print_success(f"Found {file}")
        else:
            print_error(f"Missing {file}")
            return False
    
    return True

def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python 3.8+ required. Found: {version.major}.{version.minor}")
        return False

def check_venv():
    """Check if virtual environment exists"""
    print_header("Checking Virtual Environment")
    
    venv_path = Path('venv')
    if venv_path.exists():
        print_success("Virtual environment found")
        return True
    else:
        print_info("Virtual environment not found. Creating...")
        try:
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
            print_success("Virtual environment created")
            return True
        except subprocess.CalledProcessError:
            print_error("Failed to create virtual environment")
            return False

def install_requirements():
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    pip_cmd = [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']
    
    try:
        subprocess.run(pip_cmd, check=True)
        print_success("Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    print_header("Setting Up Environment Variables")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print_success(".env file already exists")
        return True
    
    if env_example.exists():
        with open(env_example) as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print_success(".env file created from .env.example")
        print_info("⚠️  Please update .env with your API keys!")
        return True
    else:
        print_error(".env.example not found")
        return False

def generate_data():
    """Generate dummy data"""
    print_header("Generating Dummy Data")
    
    # Generate financial data
    if os.path.exists('generate_financial_data.py'):
        print_info("Generating financial options Excel file...")
        try:
            subprocess.run([sys.executable, 'generate_financial_data.py'], check=True)
            print_success("Financial data generated")
        except subprocess.CalledProcessError:
            print_error("Failed to generate financial data")
    
    # Generate dummy users
    if os.path.exists('generate_dummy_users.py'):
        print_info("Generating dummy users in database...")
        try:
            subprocess.run([sys.executable, 'generate_dummy_users.py'], check=True)
            print_success("Dummy users generated")
        except subprocess.CalledProcessError:
            print_error("Failed to generate dummy users")

def verify_installation():
    """Verify installation by importing modules"""
    print_header("Verifying Installation")
    
    try:
        import flask
        print_success(f"Flask {flask.__version__} installed")
        
        import pandas
        print_success(f"Pandas {pandas.__version__} installed")
        
        import google.generativeai
        print_success("Google Generative AI installed")
        
        import yfinance
        print_success("yfinance installed")
        
        # Try importing app modules
        import app
        print_success("App module loads successfully")
        
        return True
    except ImportError as e:
        print_error(f"Import error: {e}")
        return False

def print_next_steps():
    """Print next steps for user"""
    print_header("✅ Setup Complete!")
    print("""
Next steps:
1. Update .env file with your API keys:
   - GEMINI_API_KEY: Get from https://makersuite.google.com/app/apikey
   
2. Run the application:
   
   🐍 Development mode:
      python app.py
   
   🚀 Production mode (with Gunicorn):
      gunicorn -w 4 -b 0.0.0.0:5000 app:app
   
   🐳 Docker mode:
      docker-compose up
   
3. Access the application:
   http://localhost:5000
   
4. Test with sample credentials:
   Email: rahul.sharma1@email.com
   Password: password123

📚 For more information, see README.md
    """)

def main():
    """Main setup workflow"""
    print("\n" + "="*60)
    print("  Financial Suggestions Application Setup")
    print("="*60)
    
    # Run checks
    checks = [
        ("Python version", check_python_version),
        ("Project files", check_requirements),
        ("Virtual environment", check_venv),
        ("Dependencies", install_requirements),
        ("Environment configuration", create_env_file),
        ("Installation", verify_installation),
    ]
    
    for check_name, check_func in checks:
        if not check_func():
            print_error(f"Setup failed at: {check_name}")
            sys.exit(1)
    
    # Generate data
    generate_data()
    
    # Print next steps
    print_next_steps()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_error("Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
