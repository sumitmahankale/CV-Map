"""
Module for handling Google Sheets API integration
"""
from typing import List, Optional, Dict
import json
import os

class GoogleSheetsHandler:
    """Handle Google Sheets API operations"""
    
    def __init__(self, credentials_json: Optional[str] = None):
        """
        Initialize Google Sheets handler
        In demo mode, this simulates the API without actual authentication
        """
        self.demo_mode = True
        self.spreadsheet_id = None
        self.sheet_name = 'Candidates'
        self.demo_data = []
        
        if credentials_json and os.path.exists(credentials_json):
            try:
                from google.auth.transport.requests import Request
                from google.oauth2.service_account import Credentials
                
                self.credentials = Credentials.from_service_account_file(
                    credentials_json,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
                self.demo_mode = False
            except Exception as e:
                print(f"Warning: Could not initialize real Google Sheets API: {e}")
                print("Using demo mode instead")
    
    def initialize_sheet(self, spreadsheet_id: str, headers: List[str]) -> bool:
        """Initialize a new sheet with headers"""
        self.spreadsheet_id = spreadsheet_id
        
        if self.demo_mode:
            print(f"[DEMO MODE] Would initialize sheet: {spreadsheet_id}")
            self.demo_data = [headers]
            return True
        
        try:
            from googleapiclient.discovery import build
            service = build('sheets', 'v4', credentials=self.credentials)
            
            body = {
                'values': [headers]
            }
            
            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f"{self.sheet_name}!A1",
                valueInputOption="RAW",
                body=body
            ).execute()
            
            return True
        except Exception as e:
            print(f"Error initializing sheet: {e}")
            return False
    
    def append_row(self, row_data: List[str]) -> bool:
        """Append a row of data to the sheet"""
        if self.demo_mode:
            self.demo_data.append(row_data)
            print(f"[DEMO MODE] Appended row: {row_data}")
            return True
        
        try:
            from googleapiclient.discovery import build
            service = build('sheets', 'v4', credentials=self.credentials)
            
            body = {
                'values': [row_data]
            }
            
            result = service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A:H",
                valueInputOption="RAW",
                body=body
            ).execute()
            
            return True
        except Exception as e:
            print(f"Error appending row: {e}")
            return False
    
    def get_all_data(self) -> Optional[List[List[str]]]:
        """Retrieve all data from the sheet"""
        if self.demo_mode:
            return self.demo_data
        
        try:
            from googleapiclient.discovery import build
            service = build('sheets', 'v4', credentials=self.credentials)
            
            result = service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=self.sheet_name
            ).execute()
            
            return result.get('values', [])
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return None
    
    def export_to_json(self, output_file: str) -> bool:
        """Export sheet data to JSON file"""
        try:
            data = self.get_all_data()
            if not data or len(data) < 1:
                return False
            
            headers = data[0]
            records = []
            
            for row in data[1:]:
                record = {}
                for i, header in enumerate(headers):
                    record[header] = row[i] if i < len(row) else ''
                records.append(record)
            
            with open(output_file, 'w') as f:
                json.dump(records, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
