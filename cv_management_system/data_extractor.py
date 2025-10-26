"""
Module for extracting resume data using NLP and AI
"""
import re
from typing import Dict, List, Optional
import json

class ResumeDataExtractor:
    """Extract structured data from resume text using regex patterns and NLP"""
    
    def __init__(self):
        """Initialize the extractor with regex patterns"""
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        # Simplified phone pattern to avoid regex issues
        self.phone_pattern = r'[\+]?[0-9\-\.\s]{10,}'
        self.name_pattern = r'([A-Z][a-z]+ [A-Z][a-z]+|[A-Z][a-z]+)'
        
    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text"""
        match = re.search(self.email_pattern, text)
        return match.group(0) if match else None
    
    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        match = re.search(self.phone_pattern, text)
        return match.group(0) if match else None
    
    def extract_name(self, text: str) -> Optional[str]:
        """Extract person's name from text"""
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            # Look for capitalized names at the beginning
            words = line.strip().split()
            if len(words) >= 2:
                if all(word[0].isupper() for word in words[:2] if word):
                    return ' '.join(words[:2])
        return None
    
    def extract_education(self, text: str) -> str:
        """Extract education details from text"""
        education = []
        edu_keywords = ['B.E', 'B.Tech', 'B.S', 'B.A', 'M.Tech', 'M.S', 'MBA', 'M.A', 'PhD', 'Bachelor', 'Master']
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if any(keyword in line for keyword in edu_keywords):
                # Get this line and next line for context
                context = line
                if i + 1 < len(lines):
                    context += ' ' + lines[i + 1]
                education.append(context.strip())
        
        return '; '.join(education[:3]) if education else 'Not specified'
    
    def extract_skills(self, text: str) -> str:
        """Extract technical skills from text"""
        skills = []
        skill_keywords = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'SQL', 'HTML', 'CSS',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'AWS', 'Azure',
            'Machine Learning', 'Data Analysis', 'Git', 'Docker', 'Kubernetes',
            'REST API', 'GraphQL', 'MongoDB', 'PostgreSQL', 'MySQL'
        ]
        
        for skill in skill_keywords:
            # Simple string search instead of regex to avoid special character issues
            if skill.lower() in text.lower():
                skills.append(skill)
        
        return ', '.join(skills) if skills else 'Not specified'
    
    def extract_experience(self, text: str) -> str:
        """Extract work experience from text"""
        experience = []
        exp_keywords = ['experience', 'worked', 'years', 'software engineer', 'developer', 'manager', 'analyst']
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in exp_keywords):
                # Get this line and next line for context
                context = line
                if i + 1 < len(lines):
                    context += ' ' + lines[i + 1]
                experience.append(context.strip())
        
        return '; '.join(experience[:2]) if experience else 'Not specified'
    
    def parse_resume(self, text: str) -> Dict[str, str]:
        """
        Parse resume text and extract key information
        Returns a dictionary with extracted data
        """
        if not text or not isinstance(text, str):
            return self._create_empty_result()
        
        text = text.strip()
        
        result = {
            'full_name': self.extract_name(text) or 'Not specified',
            'email': self.extract_email(text) or 'Not specified',
            'phone': self.extract_phone(text) or 'Not specified',
            'education': self.extract_education(text),
            'skills': self.extract_skills(text),
            'experience': self.extract_experience(text),
        }
        
        return result
    
    def _create_empty_result(self) -> Dict[str, str]:
        """Create an empty result dictionary"""
        return {
            'full_name': 'Not specified',
            'email': 'Not specified',
            'phone': 'Not specified',
            'education': 'Not specified',
            'skills': 'Not specified',
            'experience': 'Not specified',
        }
    
    def format_for_sheet(self, parsed_data: Dict[str, str]) -> List[str]:
        """Format parsed data for Google Sheets insertion"""
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return [
            timestamp,
            parsed_data.get('full_name', 'Not specified'),
            parsed_data.get('email', 'Not specified'),
            parsed_data.get('phone', 'Not specified'),
            parsed_data.get('education', 'Not specified'),
            parsed_data.get('skills', 'Not specified'),
            parsed_data.get('experience', 'Not specified'),
            'WhatsApp/File Upload'
        ]
