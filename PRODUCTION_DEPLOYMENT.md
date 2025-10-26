# Production Deployment Guide
## AI-Integrated CV Management System

---

## 1. Google Sheets API Setup

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project: "CV Management System"
3. Enable APIs:
   - Google Sheets API
   - Google Drive API

### Step 2: Create Service Account
1. Go to **Service Accounts** page
2. Create new service account
3. Name: `cv-management-system`
4. Grant roles:
   - Editor (for Sheets API)
5. Create JSON key (credentials.json)

### Step 3: Share Google Sheet
1. Create Google Sheet for candidates
2. Share it with service account email
3. Set "Editor" permissions
4. Copy spreadsheet ID from URL

### Step 4: Configure Environment
```bash
# Create .env file
GOOGLE_SHEETS_API_KEY=<service_account_email>
SPREADSHEET_ID=<your_spreadsheet_id>
OPENAI_API_KEY=<optional>
```

### Step 5: Update Code
```python
cv_system = CVManagementSystem(use_real_google_sheets=True)
```

---

## 2. WhatsApp Integration

### Option A: Twilio WhatsApp API

#### Setup
```bash
pip install twilio
```

#### Configuration
```python
from twilio.rest import Client

class WhatsAppIntegration:
    def __init__(self, account_sid, auth_token):
        self.client = Client(account_sid, auth_token)
    
    def receive_messages(self):
        """Receive WhatsApp messages"""
        messages = self.client.messages.stream()
        return messages
    
    def process_message(self, message):
        """Process incoming message"""
        media_url = message.media_url
        text = message.body
        sender = message.from_
        # Download and process
```

### Option B: Official WhatsApp Business API

1. Apply for WhatsApp Business API access
2. Get Verified Business Account
3. Set up webhook endpoint
4. Configure message webhooks

#### Example Webhook
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    if data['entry'][0]['changes'][0]['value'].get('messages'):
        messages = data['entry'][0]['changes'][0]['value']['messages']
        for message in messages:
            process_whatsapp_message(message)
    
    return '200', 200
```

---

## 3. Database Integration

### Option A: PostgreSQL

```bash
pip install psycopg2-binary sqlalchemy
```

```python
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'
    
    id = Column(String, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    education = Column(String)
    skills = Column(String)
    experience = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
engine = create_engine('postgresql://user:password@localhost/cv_db')
Base.metadata.create_all(engine)
```

### Option B: MongoDB

```bash
pip install pymongo
```

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['cv_management']
candidates = db['candidates']

# Insert candidate
candidate = {
    'full_name': 'John Smith',
    'email': 'john@example.com',
    'phone': '+91-9876543210',
    'education': 'B.Tech',
    'skills': ['Python', 'Java'],
    'experience': '5 years',
    'created_at': datetime.utcnow()
}
candidates.insert_one(candidate)
```

---

## 4. API Server Deployment

### Flask REST API

```bash
pip install flask flask-cors python-dotenv
```

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.insert(0, 'cv_management_system')

app = Flask(__name__)
CORS(app)

from cv_manager import CVManagementSystem
cv_system = CVManagementSystem(use_real_google_sheets=True)

@app.route('/api/process-resume', methods=['POST'])
def process_resume():
    """Process resume and extract data"""
    if 'resume_text' not in request.json:
        return {'error': 'Missing resume_text'}, 400
    
    resume_text = request.json['resume_text']
    
    from whatsapp_simulator import WhatsAppMessage
    message = WhatsAppMessage(
        sender_id='api_user',
        sender_name='API User',
        message_text=resume_text
    )
    
    result = cv_system.process_incoming_message(message)
    return jsonify(result)

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    """Get all extracted candidates"""
    candidates = cv_system.get_all_candidates()
    return jsonify({'candidates': candidates})

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get processing statistics"""
    stats = cv_system.get_processing_summary()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

---

## 5. Async Job Processing

### Celery Setup

```bash
pip install celery redis
```

```python
from celery import Celery
import sys
sys.path.insert(0, 'cv_management_system')

from cv_manager import CVManagementSystem

app = Celery('cv_system', broker='redis://localhost:6379/0')

cv_system = CVManagementSystem(use_real_google_sheets=True)

@app.task
def process_resume_async(resume_text, sender_id, sender_name):
    """Async task to process resume"""
    from whatsapp_simulator import WhatsAppMessage
    
    message = WhatsAppMessage(
        sender_id=sender_id,
        sender_name=sender_name,
        message_text=resume_text
    )
    
    result = cv_system.process_incoming_message(message)
    return result
```

---

## 6. Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy project files
COPY requirements.txt .
COPY cv_management_system/ ./cv_management_system/
COPY credentials.json .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Run Flask app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  cv-system:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GOOGLE_SHEETS_API_KEY=${GOOGLE_SHEETS_API_KEY}
      - SPREADSHEET_ID=${SPREADSHEET_ID}
    volumes:
      - ./credentials.json:/app/credentials.json
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:14-alpine
    environment:
      - POSTGRES_DB=cv_db
      - POSTGRES_USER=cvuser
      - POSTGRES_PASSWORD=cvpassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Deploy

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f cv-system
```

---

## 7. Environment Variables

### .env Template

```bash
# Google Sheets
GOOGLE_SHEETS_API_KEY=<service_account_email>
SPREADSHEET_ID=<spreadsheet_id>

# Twilio (if using)
TWILIO_ACCOUNT_SID=<account_sid>
TWILIO_AUTH_TOKEN=<auth_token>
TWILIO_PHONE_NUMBER=<phone_number>

# OpenAI (optional for enhanced extraction)
OPENAI_API_KEY=<api_key>

# Database
DATABASE_URL=postgresql://user:password@localhost/cv_db

# Redis (if using Celery)
REDIS_URL=redis://localhost:6379/0

# App Settings
DEBUG=False
LOG_LEVEL=INFO
```

---

## 8. Monitoring & Logging

### Logging Setup

```python
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# File handler
file_handler = RotatingFileHandler(
    'cv_system.log',
    maxBytes=10485760,  # 10MB
    backupCount=10
)
logging.getLogger().addHandler(file_handler)
```

### Metrics & Alerting

```python
from prometheus_client import Counter, Histogram

resumes_processed = Counter('resumes_processed_total', 'Total resumes processed')
extraction_duration = Histogram('extraction_duration_seconds', 'Time to extract data')

@extraction_duration.time()
def process_resume(text):
    # Processing logic
    resumes_processed.inc()
```

---

## 9. Security Considerations

### API Authentication

```python
from flask_httpauth import HTTPBearerAuth

auth = HTTPBearerAuth()

@app.before_request
@auth.login_required
def verify_token():
    token = auth.get_auth()
    # Verify token against authorized list
    pass
```

### Data Privacy

```python
# Anonymize sensitive data
def anonymize_candidate(candidate):
    candidate['email'] = 'hidden@example.com'
    candidate['phone'] = 'XXX-XXXX'
    return candidate
```

---

## 10. Scaling Considerations

### Horizontal Scaling

```
Load Balancer (NGINX)
        ↓
    [API Server 1]
    [API Server 2]
    [API Server 3]
        ↓
    [Shared Database]
    [Shared Redis]
    [Shared Google Sheets]
```

### Queue-Based Processing

```
Message Queue (Redis/RabbitMQ)
        ↓
[Worker 1]
[Worker 2]
[Worker 3]
        ↓
    [Database]
    [Google Sheets]
```

---

## Testing Production Setup

```bash
# Test API endpoint
curl -X POST http://localhost:5000/api/process-resume \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "resume_text": "John Smith john@example.com +91-9876543210..."
  }'

# Expected response:
{
  "status": "success",
  "extracted_data": {
    "full_name": "John Smith",
    "email": "john@example.com",
    ...
  }
}
```

---

## Troubleshooting Production Issues

### Google Sheets API Errors
```
Error: Failed to upload to Google Sheets
Solution: Check credentials.json and spreadsheet permissions
```

### WhatsApp Webhook Not Receiving
```
Error: Messages not being received
Solution: Verify webhook URL is publicly accessible and HTTPS
```

### High Latency
```
Error: Slow response times
Solution: Implement async processing with Celery
```

---

## Checklist for Production

- [ ] Google Sheets API configured
- [ ] WhatsApp integration tested
- [ ] Database created and connected
- [ ] Environment variables set
- [ ] SSL/TLS certificates configured
- [ ] Logging and monitoring enabled
- [ ] Backup strategy implemented
- [ ] Rate limiting configured
- [ ] Error handling comprehensive
- [ ] Load testing completed
- [ ] Security audit done
- [ ] Documentation updated

---

**Status**: Ready for production deployment
**Version**: 1.0.0 Production Guide
