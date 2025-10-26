"""
Module for processing various file formats (PDF, DOCX, TXT)
"""
import os
from typing import Optional, Tuple
from pathlib import Path

class FileProcessor:
    """Process different file formats to extract text"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> Optional[str]:
        """Extract text from PDF file"""
        try:
            import PyPDF2
            text = []
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            return '\n'.join(text)
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return None
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> Optional[str]:
        """Extract text from DOCX file"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return None
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> Optional[str]:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error extracting TXT: {e}")
            return None
    
    @staticmethod
    def process_file(file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Process a file and extract text based on its extension
        Returns (success: bool, text: Optional[str])
        """
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"
        
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            text = FileProcessor.extract_text_from_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            text = FileProcessor.extract_text_from_docx(file_path)
        elif file_ext == '.txt':
            text = FileProcessor.extract_text_from_txt(file_path)
        else:
            return False, f"Unsupported file type: {file_ext}"
        
        if text:
            return True, text
        else:
            return False, "Could not extract text from file"
