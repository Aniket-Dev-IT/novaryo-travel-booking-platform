# Novaryo Production Deployment Guide

## Quick Deployment Options

### Option 1: Docker Deployment (Recommended)

1. **Prerequisites:**
   ```bash
   # Install Docker and Docker Compose
   docker --version
   docker-compose --version
   ```

2. **Environment Setup:**
   ```bash
   # Copy environment file
   cp .env.example .env
   
   # Edit environment variables for production
   nano .env
   ```

3. **Deploy with Docker:**
   ```bash
   # Build and start all services
   docker-compose up -d
   
   # Run migrations
   docker-compose exec web python manage.py migrate
   
   # Create superuser
   docker-compose exec web python manage.py createsuperuser
   
   # Setup loyalty data
   docker-compose exec web python manage.py setup_loyalty_data
   ```

4. **Access the application:**
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin/
   - API Docs: http://localhost:8000/api/docs/

### Option 2: Manual Server Deployment

1. **Server Requirements:**
   - Ubuntu 20.04+ / CentOS 8+
   - Python 3.11+
   - PostgreSQL 12+
   - Redis 6+
   - Nginx

2. **Install Dependencies:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and PostgreSQL
   sudo apt install python3.11 python3.11-venv python3-pip postgresql postgresql-contrib redis-server nginx -y
   
   # Start services
   sudo systemctl start postgresql redis-server nginx
   sudo systemctl enable postgresql redis-server nginx
   ```

3. **Setup Database:**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE novaryo;
   CREATE USER novaryo_user WITH ENCRYPTED PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE novaryo TO novaryo_user;
   \q
   ```

4. **Deploy Application:**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/novaryo.git
   cd novaryo
   
   # Create virtual environment
   python3.11 -m venv novaryo_env
   source novaryo_env/bin/activate
   
   # Install requirements
   pip install -r requirements.txt
   pip install gunicorn
   
   # Setup environment
   cp .env.example .env
   # Edit .env with production values
   
   # Collect static files
   python manage.py collectstatic --noinput
   
   # Run migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   
   # Setup loyalty data
   python manage.py setup_loyalty_data
   ```

5. **Configure Gunicorn:**
   ```bash
   # Create gunicorn socket
   sudo nano /etc/systemd/system/novaryo.socket
   ```
   
   Add:
   ```ini
   [Unit]
   Description=novaryo socket
   
   [Socket]
   ListenStream=/run/novaryo.sock
   
   [Install]
   WantedBy=sockets.target
   ```
   
   ```bash
   # Create gunicorn service
   sudo nano /etc/systemd/system/novaryo.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=novaryo daemon
   Requires=novaryo.socket
   After=network.target
   
   [Service]
   Type=notify
   User=www-data
   Group=www-data
   RuntimeDirectory=novaryo
   WorkingDirectory=/path/to/novaryo
   Environment=PATH=/path/to/novaryo_env/bin
   EnvironmentFile=/path/to/novaryo/.env
   ExecStart=/path/to/novaryo_env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/novaryo.sock novaryo.wsgi:application
   ExecReload=/bin/kill -s HUP $MAINPID
   
   [Install]
   WantedBy=multi-user.target
   ```

6. **Configure Nginx:**
   ```bash
   sudo nano /etc/nginx/sites-available/novaryo
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location = /favicon.ico { access_log off; log_not_found off; }
       location /static/ {
           root /path/to/novaryo;
       }
       location /media/ {
           root /path/to/novaryo;
       }
       
       location / {
           include proxy_params;
           proxy_pass http://unix:/run/novaryo.sock;
       }
   }
   ```
   
   ```bash
   # Enable site
   sudo ln -s /etc/nginx/sites-available/novaryo /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl reload nginx
   
   # Start services
   sudo systemctl start novaryo.socket
   sudo systemctl enable novaryo.socket
   sudo systemctl start novaryo
   sudo systemctl enable novaryo
   ```

### Option 3: Cloud Platform Deployment

#### Heroku Deployment
1. **Install Heroku CLI**
2. **Create Heroku app:**
   ```bash
   heroku create novaryo-app
   heroku addons:create heroku-postgresql:hobby-dev
   heroku addons:create heroku-redis:hobby-dev
   ```
3. **Configure environment variables:**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set ALLOWED_HOSTS=novaryo-app.herokuapp.com
   ```
4. **Deploy:**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   heroku run python manage.py setup_loyalty_data
   ```

#### AWS/DigitalOcean/Google Cloud
- Use the manual deployment steps above
- Configure load balancers, auto-scaling, and managed databases as needed
- Set up CloudFlare or AWS CloudFront for CDN

## Production Environment Variables

Essential production settings for `.env`:
```bash
# Security
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (Use managed database service)
DB_NAME=novaryo_prod
DB_USER=novaryo_user
DB_PASSWORD=secure_password
DB_HOST=your-db-host.com
DB_PORT=5432

# Redis (Use managed Redis service)
REDIS_URL=redis://your-redis-host:6379/0

# Email (Use production email service)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.your-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-app-password

# Security Headers
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Post-Deployment Checklist

- [ ] SSL Certificate configured (Let's Encrypt recommended)
- [ ] Database backups scheduled
- [ ] Monitoring setup (server metrics, error tracking)
- [ ] Log rotation configured
- [ ] Firewall rules applied
- [ ] Regular security updates scheduled
- [ ] Performance monitoring enabled
- [ ] CDN configured for static files
- [ ] Email service tested
- [ ] Payment gateway tested (if applicable)

## Maintenance Commands

```bash
# Backup database
pg_dump novaryo > backup_$(date +%Y%m%d).sql

# Update application
git pull origin main
source novaryo_env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart novaryo

# Monitor logs
sudo journalctl -u novaryo -f
tail -f /var/log/nginx/access.log
```

## Troubleshooting

### Common Issues:
1. **Static files not loading:** Check STATIC_ROOT and nginx configuration
2. **Database connection errors:** Verify DATABASE_URL and permissions
3. **Redis connection failed:** Check REDIS_URL and service status
4. **502 Bad Gateway:** Check Gunicorn socket and nginx proxy configuration

### Support:
- Check logs: `sudo journalctl -u novaryo -n 50`
- Test Gunicorn: `gunicorn --bind 0.0.0.0:8000 novaryo.wsgi:application`
- Verify database: `python manage.py dbshell`

---

**For additional support, please refer to the main README.md or create an issue on GitHub.**