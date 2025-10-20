# Virtual Startup - Deployment Guide

**Version**: 1.0.0
**Last Updated**: October 18, 2025
**Target Environments**: Production, Staging, Development

This guide covers deploying the Virtual Startup multi-agent AI system to production environments.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Database Configuration](#database-configuration)
6. [Web Server Configuration](#web-server-configuration)
7. [SSL/HTTPS Setup](#sslhttps-setup)
8. [Monitoring & Logging](#monitoring--logging)
9. [Scaling Considerations](#scaling-considerations)
10. [CI/CD Pipeline](#cicd-pipeline)
11. [Rollback Procedures](#rollback-procedures)
12. [Security Checklist](#security-checklist)

---

## Prerequisites

### System Requirements

**Minimum Server Specifications:**
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB SSD
- **OS**: Ubuntu 22.04 LTS or similar Linux distribution

**Recommended for Production:**
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Storage**: 50GB+ SSD
- **OS**: Ubuntu 22.04 LTS

### Required Software

- **Python**: 3.12+
- **Node.js**: 18+ with npm
- **uv**: Python package installer
- **NGINX**: Web server (or Apache)
- **Supervisor**: Process manager (or systemd)
- **Git**: Version control
- **PostgreSQL**: 14+ (for production) or SQLite (for staging)

### API Keys and Services

- **OpenAI API Key**: For LLM functionality
- **Domain Name**: With DNS configured (for production)
- **SSL Certificate**: Let's Encrypt or commercial (for HTTPS)

---

## Environment Setup

### 1. Clone Repository

```bash
# Create deployment directory
sudo mkdir -p /var/www/virtual-startup
sudo chown $USER:$USER /var/www/virtual-startup

# Clone repository
cd /var/www/virtual-startup
git clone https://github.com/your-org/virtual-startup.git .
```

### 2. Create System User

```bash
# Create dedicated user for the application
sudo useradd -r -s /bin/bash -d /var/www/virtual-startup virtualstartup
sudo chown -R virtualstartup:virtualstartup /var/www/virtual-startup
```

### 3. Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.12
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install NGINX
sudo apt install -y nginx

# Install Supervisor
sudo apt install -y supervisor

# Install PostgreSQL (optional, for production)
sudo apt install -y postgresql postgresql-contrib
```

---

## Backend Deployment

### 1. Install Backend Dependencies

```bash
cd /var/www/virtual-startup/backend

# Install Python dependencies with uv
uv add flask flask-sqlalchemy flask-migrate flask-cors \
  flask-socketio python-socketio python-dotenv \
  autogen-agentchat chromadb openai requests

# Install production dependencies
uv add gunicorn gevent gevent-websocket
```

### 2. Configure Environment Variables

Create production environment file:

```bash
nano /var/www/virtual-startup/backend/.env.production
```

**Environment Variables:**

```env
# Flask Configuration
FLASK_APP=app
FLASK_ENV=production
SECRET_KEY=<GENERATE_STRONG_SECRET_KEY>

# Database Configuration
# For PostgreSQL
DATABASE_URL=postgresql://virtualstartup:PASSWORD@localhost/virtualstartup_db

# For SQLite (staging only)
# DATABASE_URL=sqlite:///app.db

# CORS Configuration
CORS_ORIGINS=https://yourdomain.com

# OpenAI Configuration
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>

# Agent Configuration
DEFAULT_LLM_MODEL=gpt-4
DEFAULT_TEMPERATURE=0.7
MAX_DYNAMIC_AGENTS=10

# RAG Configuration
CHROMA_PERSIST_DIR=/var/www/virtual-startup/backend/chroma_db
CHROMA_COLLECTION_NAME=virtual_startup_knowledge

# WebSocket Configuration
SOCKETIO_CORS_ALLOWED_ORIGINS=https://yourdomain.com
SOCKETIO_ASYNC_MODE=gevent

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

**Generate Secret Key:**

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Set Up Database

**For PostgreSQL:**

```bash
# Create database and user
sudo -u postgres psql

CREATE DATABASE virtualstartup_db;
CREATE USER virtualstartup WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE virtualstartup_db TO virtualstartup;
\q
```

**Run Migrations:**

```bash
cd /var/www/virtual-startup/backend

# Set environment
export FLASK_ENV=production
export DATABASE_URL="postgresql://virtualstartup:PASSWORD@localhost/virtualstartup_db"

# Run migrations
uv run flask db upgrade
```

### 4. Test Backend Locally

```bash
# Test with production config
cd /var/www/virtual-startup/backend
export FLASK_ENV=production
uv run python run.py

# In another terminal, test API
curl http://localhost:5000/api/health
```

### 5. Create Supervisor Configuration

Create supervisor config for backend:

```bash
sudo nano /etc/supervisor/conf.d/virtualstartup-backend.conf
```

**Supervisor Config:**

```ini
[program:virtualstartup-backend]
command=/home/virtualstartup/.local/bin/uv run gunicorn --worker-class gevent --workers 4 --bind 127.0.0.1:5000 --timeout 120 'app:create_app()'
directory=/var/www/virtual-startup/backend
user=virtualstartup
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
environment=FLASK_ENV="production",PATH="/home/virtualstartup/.local/bin:%(ENV_PATH)s"
stdout_logfile=/var/log/virtualstartup/backend.log
stderr_logfile=/var/log/virtualstartup/backend_error.log
```

**Create log directory:**

```bash
sudo mkdir -p /var/log/virtualstartup
sudo chown virtualstartup:virtualstartup /var/log/virtualstartup
```

**Start backend service:**

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start virtualstartup-backend
sudo supervisorctl status virtualstartup-backend
```

---

## Frontend Deployment

### 1. Install Frontend Dependencies

```bash
cd /var/www/virtual-startup/frontend
npm install
```

### 2. Configure Environment Variables

Create production environment file:

```bash
nano /var/www/virtual-startup/frontend/.env.production
```

**Environment Variables:**

```env
VITE_API_URL=https://yourdomain.com/api
VITE_WS_URL=wss://yourdomain.com
```

### 3. Build Frontend

```bash
cd /var/www/virtual-startup/frontend

# Build production bundle
npm run build

# Output will be in dist/ directory
ls -la dist/
```

### 4. Deploy Static Files

```bash
# Create web root
sudo mkdir -p /var/www/virtual-startup/public
sudo cp -r /var/www/virtual-startup/frontend/dist/* /var/www/virtual-startup/public/
sudo chown -R www-data:www-data /var/www/virtual-startup/public
```

---

## Web Server Configuration

### NGINX Configuration

Create NGINX config:

```bash
sudo nano /etc/nginx/sites-available/virtualstartup
```

**NGINX Config:**

```nginx
# Upstream for backend
upstream backend {
    server 127.0.0.1:5000;
}

# HTTP Server (redirect to HTTPS)
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Root directory for frontend
    root /var/www/virtual-startup/public;
    index index.html;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json;

    # Frontend - serve static files
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API requests - proxy to backend
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    # WebSocket - proxy to backend
    location /socket.io/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Disable access to hidden files
    location ~ /\. {
        deny all;
    }
}
```

**Enable site:**

```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/virtualstartup /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart NGINX
sudo systemctl restart nginx
```

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### Certificate Auto-Renewal

Certbot automatically sets up a cron job. Verify:

```bash
sudo systemctl status certbot.timer
```

---

## Database Configuration

### PostgreSQL Production Setup

**Performance Tuning:**

```bash
sudo nano /etc/postgresql/14/main/postgresql.conf
```

**Key Settings:**

```ini
# Memory
shared_buffers = 256MB          # 25% of RAM
effective_cache_size = 1GB      # 50-75% of RAM

# Connections
max_connections = 100

# Logging
log_min_duration_statement = 1000  # Log slow queries (>1s)

# Checkpoint
checkpoint_completion_target = 0.9
```

**Restart PostgreSQL:**

```bash
sudo systemctl restart postgresql
```

### Backup Configuration

**Automated Daily Backups:**

```bash
# Create backup script
sudo nano /usr/local/bin/backup-virtualstartup.sh
```

**Backup Script:**

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/virtualstartup"
DB_NAME="virtualstartup_db"
DB_USER="virtualstartup"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Backup ChromaDB
tar -czf $BACKUP_DIR/chroma_backup_$DATE.tar.gz /var/www/virtual-startup/backend/chroma_db

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

**Make executable and schedule:**

```bash
sudo chmod +x /usr/local/bin/backup-virtualstartup.sh

# Add to crontab
sudo crontab -e

# Add line (backup daily at 2 AM)
0 2 * * * /usr/local/bin/backup-virtualstartup.sh >> /var/log/virtualstartup/backup.log 2>&1
```

---

## Monitoring & Logging

### Application Logging

**Backend Logs:**

```bash
# Supervisor logs
tail -f /var/log/virtualstartup/backend.log
tail -f /var/log/virtualstartup/backend_error.log

# NGINX logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### System Monitoring

**Install Monitoring Tools:**

```bash
# Install htop for process monitoring
sudo apt install -y htop

# Install netdata for system monitoring (optional)
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

### Health Check Endpoint

**Monitor Backend Health:**

```bash
# Create health check script
nano /usr/local/bin/health-check.sh
```

**Health Check Script:**

```bash
#!/bin/bash
HEALTH_URL="https://yourdomain.com/api/health"

response=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $response -eq 200 ]; then
    echo "OK: Backend is healthy"
    exit 0
else
    echo "ERROR: Backend health check failed (HTTP $response)"
    exit 1
fi
```

**Schedule Health Checks:**

```bash
sudo chmod +x /usr/local/bin/health-check.sh

# Add to crontab (check every 5 minutes)
*/5 * * * * /usr/local/bin/health-check.sh >> /var/log/virtualstartup/health.log 2>&1
```

---

## Scaling Considerations

### Horizontal Scaling

**Load Balancer Setup (NGINX):**

```nginx
upstream backend_cluster {
    least_conn;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    # ... SSL config ...

    location /api/ {
        proxy_pass http://backend_cluster;
        # ... other proxy settings ...
    }
}
```

### Vertical Scaling

**Increase Gunicorn Workers:**

```ini
# In supervisor config
command=uv run gunicorn --worker-class gevent --workers 8 --bind 127.0.0.1:5000 ...
```

**Rule of thumb**: `workers = (2 * CPU_CORES) + 1`

### Database Scaling

**Connection Pooling:**

```python
# In backend config
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 20
SQLALCHEMY_POOL_TIMEOUT = 30
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Backend Tests
        run: |
          cd backend
          uv run pytest --cov=app

      - name: Run Frontend Tests
        run: |
          cd frontend
          npm install
          npx playwright install --with-deps
          npm run test:e2e

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/virtual-startup
            git pull origin main
            cd backend && uv sync
            cd ../frontend && npm install && npm run build
            sudo supervisorctl restart virtualstartup-backend
            sudo systemctl reload nginx
```

---

## Rollback Procedures

### Quick Rollback

```bash
# Stop services
sudo supervisorctl stop virtualstartup-backend

# Checkout previous version
cd /var/www/virtual-startup
git log --oneline  # Find commit hash
git checkout <previous-commit-hash>

# Rebuild frontend
cd frontend
npm run build
sudo cp -r dist/* /var/www/virtual-startup/public/

# Rollback database (if needed)
cd backend
uv run flask db downgrade

# Restart services
sudo supervisorctl start virtualstartup-backend
sudo systemctl reload nginx
```

---

## Security Checklist

### Pre-Deployment Security

- [ ] Change default `SECRET_KEY`
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set secure session cookies
- [ ] Disable debug mode (`FLASK_ENV=production`)
- [ ] Use environment variables for secrets (never commit `.env`)
- [ ] Configure firewall (UFW)
- [ ] Enable automatic security updates
- [ ] Restrict database access to localhost
- [ ] Set up regular backups
- [ ] Enable security headers in NGINX
- [ ] Validate and sanitize all user inputs
- [ ] Implement rate limiting (optional)
- [ ] Set up monitoring and alerting

### Firewall Configuration

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

### Rate Limiting (NGINX)

```nginx
# Add to http block in /etc/nginx/nginx.conf
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

# Add to location /api/ block
limit_req zone=api_limit burst=20 nodelay;
```

---

## Post-Deployment Verification

### Checklist

```bash
# 1. Check backend is running
curl https://yourdomain.com/api/health

# 2. Check frontend loads
curl -I https://yourdomain.com

# 3. Check WebSocket connection
# Use browser DevTools > Network > WS

# 4. Initialize agents
curl -X POST https://yourdomain.com/api/init

# 5. Test chat functionality
# Use the web interface

# 6. Check logs
sudo tail -f /var/log/virtualstartup/backend.log

# 7. Monitor resource usage
htop
```

---

## Troubleshooting Deployment Issues

### Backend Not Starting

```bash
# Check supervisor logs
sudo supervisorctl tail virtualstartup-backend stderr

# Check if port is in use
sudo netstat -tulpn | grep 5000

# Test manually
cd /var/www/virtual-startup/backend
uv run python run.py
```

### Database Connection Errors

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U virtualstartup -d virtualstartup_db -h localhost
```

### NGINX Errors

```bash
# Check configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Restart NGINX
sudo systemctl restart nginx
```

---

## Maintenance Tasks

### Regular Maintenance Schedule

**Daily:**
- Monitor logs for errors
- Check disk space: `df -h`
- Verify backups completed

**Weekly:**
- Review application performance
- Check for security updates: `sudo apt update && sudo apt upgrade`
- Analyze slow queries

**Monthly:**
- Review and rotate logs
- Database optimization: `VACUUM ANALYZE;`
- Update dependencies: `uv sync`

---

## Support and Resources

### Useful Commands

```bash
# Restart backend
sudo supervisorctl restart virtualstartup-backend

# Reload NGINX
sudo systemctl reload nginx

# View logs
sudo journalctl -u nginx -f
sudo tail -f /var/log/virtualstartup/backend.log

# Check disk usage
du -sh /var/www/virtual-startup/*

# Database shell
psql -U virtualstartup -d virtualstartup_db
```

### Additional Resources

- **NGINX Docs**: https://nginx.org/en/docs/
- **Gunicorn Docs**: https://docs.gunicorn.org/
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

**Version**: 1.0.0
**Last Updated**: October 18, 2025
**Maintainer**: Virtual Startup Team
**Questions?** Check `docs/TROUBLESHOOTING.md` for common issues
