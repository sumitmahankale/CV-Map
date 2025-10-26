"""
Main demo script - Shows the CV Management System in action
This script demonstrates the complete workflow:
1. Simulating WhatsApp message receipt with resumes
2. Extracting data from resume text
3. Storing extracted data in Google Sheets
"""
import os
import sys
from pathlib import Path

# Add the cv_management_system module to path
current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_dir, 'cv_management_system'))

from cv_manager import CVManagementSystem
from whatsapp_simulator import WhatsAppMessageBuilder
from sample_data import SAMPLE_RESUME_1, SAMPLE_RESUME_2, SAMPLE_RESUME_3, SAMPLE_TEXT_RESUME
from config import SHEET_HEADERS


def create_sample_files():
    """Create sample resume files for demonstration"""
    sample_dir = Path(__file__).parent / 'sample_resumes'
    sample_dir.mkdir(exist_ok=True)
    
    # Create text file
    txt_file = sample_dir / 'resume_rajesh.txt'
    with open(txt_file, 'w') as f:
        f.write(SAMPLE_TEXT_RESUME)
    print(f"✓ Created: {txt_file}")
    
    return str(txt_file)


def main():
    """Main demo function"""
    
    print("\n" + "="*70)
    print("   AI-INTEGRATED CV MANAGEMENT SYSTEM - DEMO")
    print("="*70)
    print("\nThis demo shows how the system:")
    print("  1. Receives resumes via WhatsApp (simulated)")
    print("  2. Extracts key information (name, email, skills, etc.)")
    print("  3. Stores data in Google Sheets (demo mode)\n")
    
    # Initialize the CV Management System
    print("Initializing CV Management System...")
    cv_system = CVManagementSystem(use_real_google_sheets=False)
    
    # Initialize Google Sheet (demo mode)
    print("Initializing Google Sheet with headers...")
    cv_system.initialize_sheet('demo_spreadsheet_id')
    print("[OK] Sheet initialized with headers:", SHEET_HEADERS[:4], "...")
    
    # Create sample files
    print("\nCreating sample resume files...")
    txt_file = create_sample_files()
    
    print("\n" + "-"*70)
    print("STEP 1: SIMULATING WHATSAPP MESSAGE RECEPTION")
    print("-"*70)
    
    # Simulate receiving resume 1 (text message)
    print("\n[1/3] Receiving resume as text message from John Smith...")
    msg1 = (WhatsAppMessageBuilder()
            .with_sender("1234567890", "John Smith")
            .with_message(SAMPLE_RESUME_1)
            .build())
    cv_system.receive_message(msg1)
    
    # Simulate receiving resume 2 (text message)
    print("[2/3] Receiving resume as text message from Sarah Johnson...")
    msg2 = (WhatsAppMessageBuilder()
            .with_sender("9876543210", "Sarah Johnson")
            .with_message(SAMPLE_RESUME_2)
            .build())
    cv_system.receive_message(msg2)
    
    # Simulate receiving resume 3 (file upload)
    print("[3/3] Receiving resume as file attachment from Priya Sharma...")
    msg3 = (WhatsAppMessageBuilder()
            .with_sender("5555555555", "Priya Sharma")
            .with_message("Hi, here's my resume")
            .with_file(txt_file, "txt")
            .build())
    cv_system.receive_message(msg3)
    
    print("\n[OK] All 3 resumes received in message queue")
    
    print("\n" + "-"*70)
    print("STEP 2: PROCESSING MESSAGES AND EXTRACTING DATA")
    print("-"*70)
    
    results = cv_system.process_all_pending()
    
    print("\n" + "-"*70)
    print("STEP 3: EXTRACTED CANDIDATE DATA")
    print("-"*70)
    
    candidates = cv_system.get_all_candidates()
    for i, candidate in enumerate(candidates, 1):
        print(f"\nCandidate {i}:")
        print(f"  Name: {candidate['full_name']}")
        print(f"  Email: {candidate['email']}")
        print(f"  Phone: {candidate['phone']}")
        print(f"  Education: {candidate['education'][:60]}...")
        print(f"  Skills: {candidate['skills'][:60]}...")
        print(f"  Experience: {candidate['experience'][:60]}...")
    
    # Print summary
    print("\n" + "-"*70)
    cv_system.print_summary()
    
    # Export results
    output_file = Path(__file__).parent / 'demo_results.json'
    print(f"Exporting results to {output_file}...")
    if cv_system.export_results(str(output_file)):
        print(f"[OK] Results exported successfully")
    
    # Print detailed processing log
    print("\n" + "="*70)
    print("PROCESSING DETAILS")
    print("="*70)
    
    for i, result in enumerate(results, 1):
        print(f"\nMessage {i}: {result['sender']}")
        print(f"  Status: {result['status'].upper()}")
        print(f"  Data Extracted: {result['extracted_data'] is not None}")
        print(f"  Uploaded to Sheet: {result['sheet_upload']}")
        if result['errors']:
            print(f"  Errors: {', '.join(result['errors'])}")
    
    print("\n" + "="*70)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\nKey Achievements:")
    print("  [OK] Simulated WhatsApp message reception")
    print("  [OK] Processed multiple resume formats (text, file)")
    print("  [OK] Extracted key candidate information using NLP")
    print("  [OK] Stored data in structured format (Google Sheets)")
    print("  [OK] Generated processing report and statistics")
    print("\nFor production use:")
    print("  - Set up real Google Sheets API credentials")
    print("  - Integrate with WhatsApp Business API or Twilio")
    print("  - Add PDF/DOCX support for more resume formats")
    print("  - Implement advanced NLP models for better extraction")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
