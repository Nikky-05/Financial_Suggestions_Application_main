# Deployment Guide

Production-ready deployment instructions for the Financial Suggestions Application.

## 📋 Pre-Deployment Checklist

- [ ] `.env` file created with production API keys
- [ ] Database backed up
- [ ] SSL certificates ready (for HTTPS)
- [ ] Load balancer/reverse proxy configured
- [ ] Monitoring and logging setup
- [ ] Error tracking (Sentry/similar) configured
- [ ] Email service configured for notifications
- [ ] Database updated to PostgreSQL (optional but recommended)

---

## 🌐 Deployment Options

### Option 1: Heroku (Easiest for Beginners)

#### Prerequisites
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

heroku login
```

#### Deploy
```bash
# 1. Create Procfile
echo "web: gunicorn wsgi:app" > Procfile

# 2. Create runtime.txt (optional, for specific Python version)
echo "python-3.10.11" > runtime.txt

# 3. Create app on Heroku
heroku create your-app-name

# 4. Setup environment variables
heroku config:set FLASK_ENV=production
heroku config:set GEMINI_API_KEY=your-key
heroku config:set SECRET_KEY=your-secret-key

# 5. Deploy to Heroku
git push heroku main

# 6. View logs
heroku logs --tail
```

---

### Option 2: AWS EC2 (Most Flexible)

#### Prerequisites
- AWS Account
- EC2 instance running Ubuntu 20.04+
- Security groups configured (ports 80, 443)
- Domain name and DNS configured

#### Setup Ubuntu Server
```bash
# 1. SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 2. Update system
sudo apt update && sudo apt upgrade -y

# 3. Install Python and dependencies
sudo apt install python3-pip python3-venv nginx supervisor -y

# 4. Clone repository
git clone <your-repo-url>
cd Financial-Suggestions-Application

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install dependencies
pip install -r requirements.txt

# 7. Create .env file
cp .env.example .env
nano .env  # Edit with production values
```

#### Configure Gunicorn
```bash
# Create gunicorn config
nano gunicorn_config.py
```

Add:
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
max_requests = 1000
timeout = 60
```

#### Configure Supervisor
```bash
# Create supervisor config
sudo nano /etc/supervisor/conf.d/financial_app.conf
```

Add:
```ini
[program:financial_app]
directory=/home/ubuntu/Financial-Suggestions-Application
command=/home/ubuntu/Financial-Suggestions-Application/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/financial_app.log
```

#### Configure Nginx
```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/financial_app
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ubuntu/Financial-Suggestions-Application/static/;
    }
}
```

#### Enable and Start Services
```bash
# Enable Nginx config
sudo ln -s /etc/nginx/sites-available/financial_app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start supervisor program
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start financial_app
```

#### Setup HTTPS with Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured by default
```

---

### Option 3: Docker & Docker Compose

#### Prerequisites
- Docker installed
- Docker Compose installed
- Docker Hub account (for image repository)

#### Build and Push Image
```bash
# 1. Build image
docker build -t your-username/financial-app:1.0.0 .

# 2. Login to Docker Hub
docker login

# 3. Push to repository
docker push your-username/financial-app:1.0.0
```

#### Deploy with Docker Compose
```bash
# Update docker-compose.yml with your image
nano docker-compose.yml

# Start service
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop service
docker-compose down
```

---

### Option 4: DigitalOcean App Platform

#### Deploy via App Spec
1. Create `app.spec.yaml`:
```yaml
name: financial-app
services:
- name: web
  github:
    branch: main
    repo: your-username/Financial-Suggestions-Application
  build_command: pip install -r requirements.txt
  run_command: gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
  envs:
  - key: FLASK_ENV
    value: production
  - key: GEMINI_API_KEY
    value: ${GEMINI_API_KEY}
  - key: SECRET_KEY
    value: ${SECRET_KEY}
  http_port: 8080
```

2. Deploy:
```bash
doctl apps create --spec app.spec.yaml
```

---

### Option 5: Render (Simplest Free Option)

#### Deploy Steps
1. Push code to GitHub
2. Go to https://render.com
3. Create new Web Service
4. Select your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app`
6. Add Environment Variables:
   - `FLASK_ENV=production`
   - `GEMINI_API_KEY=your-key`
   - `SECRET_KEY=your-key`
7. Deploy!

---

## 🔧 Post-Deployment Setup

### Database

#### Option A: PostgreSQL (Recommended)
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Create database
sudo -u postgres createdb financial_app_db
sudo -u postgres createuser financial_user
sudo -u postgres psql -c "ALTER USER financial_user WITH PASSWORD 'password';"

# Update .env
DATABASE_URL=postgresql://financial_user:password@localhost/financial_app_db
```

#### Option B: Keep SQLite (Easy)
Already configured, ensure backups are setup.

### Monitoring

#### Setup Error Tracking (Sentry)
```python
# In app.py after Flask initialization
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1
)
```

#### Setup Application Monitoring
```bash
# Install tools
pip install python-json-logger prometheus-client

# Configure in your wsgi.py or monitoring module
```

### Backup Strategy

#### Automated Backups (AWS S3 Example)
```bash
# Install boto3
pip install boto3

# Create backup script
nano backup_db.py
```

Add:
```python
import boto3
import subprocess
from datetime import datetime

def backup_database():
    # Backup SQLite
    backup_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    subprocess.run(f"cp financial_app.db backup_financial_app_{backup_time}.db", shell=True)
    
    # Upload to S3
    s3 = boto3.client('s3')
    s3.upload_file(f'backup_financial_app_{backup_time}.db', 'your-bucket', f'backups/{backup_time}.db')

if __name__ == '__main__':
    backup_database()
```

#### Cron Job for Automated Backups
```bash
# Run daily at 2 AM
crontab -e

# Add:
0 2 * * * cd /path/to/app && python backup_db.py
```

---

## 📊 Performance Optimization

### Caching Configuration
```python
# Enable Redis caching (optional)
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
```

### Database Optimization
```sql
-- Create indexes for faster queries
CREATE INDEX idx_users_id ON users(id);
CREATE INDEX idx_goals_user_id ON goals(user_id);
CREATE INDEX idx_expenses_user_id ON expenses(user_id);
```

### API Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## 🔒 Security Checklist

- [ ] HTTPS enabled (SSL certificates)
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Database password strong and rotated
- [ ] API keys rotated regularly
- [ ] Rate limiting enabled
- [ ] Input validation on all forms
- [ ] CSRF tokens implemented
- [ ] SQL injection protection verified
- [ ] Secrets not in version control
- [ ] Regular security audits scheduled

---

## 📈 Monitoring & Maintenance

### Daily Checks
```bash
# Check application health
curl https://your-domain.com/api/market-data

# Check disk space
df -h

# Check logs for errors
tail -f /var/log/financial_app.log
```

### Weekly Tasks
- Review error logs
- Check database size
- Verify backups completed
- Monitor system resources

### Monthly Tasks
- Security updates
- Dependency updates
- Performance optimization review
- User feedback analysis

---

## 🚨 Troubleshooting

### Application Won't Start
```bash
# Check Python packages
pip list | grep -E "Flask|pandas|google-generativeai"

# Check logs
docker-compose logs web

# Verify environment variables
echo $GEMINI_API_KEY
```

### Database Connection Issues
```bash
# Test connection
python -c "from database import get_db_connection; print(get_db_connection().cursor())"

# Check file permissions
ls -la financial_app.db
```

### High Memory Usage
- Reduce Gunicorn workers
- Enable caching
- Optimize database queries
- Check for memory leaks

---

## 📞 Support

For deployment issues:
1. Check application logs
2. Review error tracking (Sentry)
3. Check status page of provider
4. Contact support of hosting platform

---

**Deployment Version**: 1.0.0  
**Last Updated**: March 2026
