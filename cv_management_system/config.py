"""
Configuration module for CV Management System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Google Sheets Configuration
GOOGLE_SHEETS_API_KEY = os.getenv('GOOGLE_SHEETS_API_KEY')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET_NAME = 'Candidates'

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Application Configuration
DEMO_MODE = True  # Set to True for demo without actual WhatsApp/Google APIs
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Sample sheet headers
SHEET_HEADERS = [
    'Timestamp',
    'Full Name',
    'Email',
    'Phone Number',
    'Education',
    'Skills',
    'Experience',
    'Source'
]
