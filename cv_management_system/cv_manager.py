"""
Main orchestrator for the CV Management System
Coordinates all components: WhatsApp simulator, file processing, data extraction, and Google Sheets
"""
from typing import Optional, Dict, List
from datetime import datetime
import os
import json

from whatsapp_simulator import WhatsAppSimulator, WhatsAppMessage
from file_processor import FileProcessor
from data_extractor import ResumeDataExtractor
from google_sheets_handler import GoogleSheetsHandler
from config import SHEET_HEADERS


class CVManagementSystem:
    """Main orchestrator for CV Management System"""
    
    def __init__(self, use_real_google_sheets: bool = False):
        """
        Initialize the CV Management System
        
        Args:
            use_real_google_sheets: If True, attempts to use real Google Sheets API
        """
        self.whatsapp_sim = WhatsAppSimulator()
        self.file_processor = FileProcessor()
        self.data_extractor = ResumeDataExtractor()
        self.sheets_handler = GoogleSheetsHandler(
            credentials_json='credentials.json' if use_real_google_sheets else None
        )
        
        self.processing_log = []
        self.extracted_candidates = []
    
    def process_incoming_message(self, message: WhatsAppMessage) -> Dict:
        """
        Process an incoming WhatsApp message
        
        Args:
            message: WhatsAppMessage object
            
        Returns:
            Dictionary with processing result
        """
        result = {
            'status': 'processing',
            'sender': message.sender_name,
            'timestamp': datetime.now().isoformat(),
            'message_content': None,
            'extracted_data': None,
            'sheet_upload': False,
            'errors': []
        }
        
        try:
            # Step 1: Extract text content
            if message.file_path and os.path.exists(message.file_path):
                success, content = self.file_processor.process_file(message.file_path)
                if success:
                    result['message_content'] = content
                else:
                    result['errors'].append(f"File processing failed: {content}")
            else:
                result['message_content'] = message.message_text
            
            # Step 2: Extract resume data
            if result['message_content']:
                extracted = self.data_extractor.parse_resume(result['message_content'])
                result['extracted_data'] = extracted
                self.extracted_candidates.append(extracted)
                
                # Step 3: Upload to Google Sheets
                row_data = self.data_extractor.format_for_sheet(extracted)
                if self.sheets_handler.append_row(row_data):
                    result['sheet_upload'] = True
                    result['status'] = 'success'
                else:
                    result['errors'].append("Failed to upload to Google Sheets")
                    result['status'] = 'partial_success'
            else:
                result['errors'].append("No content found to process")
                result['status'] = 'failed'
        
        except Exception as e:
            result['status'] = 'failed'
            result['errors'].append(str(e))
        
        self.processing_log.append(result)
        return result
    
    def receive_message(self, message: WhatsAppMessage) -> None:
        """Receive a message in the WhatsApp simulator"""
        self.whatsapp_sim.simulate_message_receipt(message)
    
    def process_all_pending(self) -> List[Dict]:
        """Process all pending messages in the queue"""
        results = []
        while True:
            message = self.whatsapp_sim.get_next_message()
            if not message:
                break
            result = self.process_incoming_message(message)
            results.append(result)
        return results
    
    def initialize_sheet(self, spreadsheet_id: str) -> bool:
        """Initialize Google Sheets with headers"""
        return self.sheets_handler.initialize_sheet(spreadsheet_id, SHEET_HEADERS)
    
    def get_all_candidates(self) -> List[Dict]:
        """Get all extracted candidates"""
        return self.extracted_candidates
    
    def get_processing_summary(self) -> Dict:
        """Get summary of processing activities"""
        return {
            'total_processed': len(self.processing_log),
            'successful': sum(1 for log in self.processing_log if log['status'] == 'success'),
            'partial_success': sum(1 for log in self.processing_log if log['status'] == 'partial_success'),
            'failed': sum(1 for log in self.processing_log if log['status'] == 'failed'),
            'candidates_extracted': len(self.extracted_candidates),
            'whatsapp_stats': self.whatsapp_sim.get_statistics()
        }
    
    def export_results(self, output_file: str) -> bool:
        """Export all results to JSON file"""
        try:
            data = {
                'summary': self.get_processing_summary(),
                'candidates': self.extracted_candidates,
                'processing_log': self.processing_log
            }
            
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting results: {e}")
            return False
    
    def print_summary(self) -> None:
        """Print a summary of the system status"""
        summary = self.get_processing_summary()
        
        print("\n" + "="*60)
        print("CV MANAGEMENT SYSTEM - PROCESSING SUMMARY")
        print("="*60)
        print(f"Total Messages Processed: {summary['total_processed']}")
        print(f"  ✓ Successful: {summary['successful']}")
        print(f"  ⚠ Partial Success: {summary['partial_success']}")
        print(f"  ✗ Failed: {summary['failed']}")
        print(f"\nCandidates Extracted: {summary['candidates_extracted']}")
        print(f"\nWhatsApp Queue Status:")
        print(f"  Pending: {summary['whatsapp_stats']['pending_messages']}")
        print(f"  Processed: {summary['whatsapp_stats']['processed_messages']}")
        print("="*60 + "\n")
