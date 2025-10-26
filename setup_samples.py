"""
Setup script to create required PDF and DOCX files for testing
"""
import os
from pathlib import Path
from sample_resumes.create_sample_files import create_docx, create_pdf


def setup_sample_files():
    """Create sample resume files in various formats"""
    
    sample_dir = Path(__file__).parent / 'sample_resumes'
    sample_dir.mkdir(exist_ok=True)
    
    print("Creating sample resume files...")
    
    # Create a DOCX file
    docx_path = sample_dir / 'resume_john_smith.docx'
    try:
        create_docx(str(docx_path))
        print(f"✓ Created: {docx_path}")
    except Exception as e:
        print(f"⚠ Could not create DOCX: {e}")
    
    # Create a PDF file
    pdf_path = sample_dir / 'resume_sarah_johnson.pdf'
    try:
        create_pdf(str(pdf_path))
        print(f"✓ Created: {pdf_path}")
    except Exception as e:
        print(f"⚠ Could not create PDF: {e}")


if __name__ == "__main__":
    setup_sample_files()
