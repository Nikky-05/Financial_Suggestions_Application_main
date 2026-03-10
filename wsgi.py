"""
WSGI configuration for production deployment with Gunicorn
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Flask app
from app import app

if __name__ == "__main__":
    app.run()
