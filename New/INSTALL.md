# 📦 Novaryo Installation Guide

**⚠️ IMPORTANT: This software is proprietary. Contact the developer for authorization before proceeding.**

---

## 📞 Developer Contact (REQUIRED FIRST STEP)

**Before installation, you MUST contact:**

**Aniket Kumar**  
📧 **Email:** aniket.kumar.devpro@gmail.com  
📱 **WhatsApp:** +91 8318601925  
🐙 **GitHub:** @Aniket-Dev-IT

**You must obtain written permission before using this software.**

---

## 🔧 System Requirements

### **Minimum Requirements**
- **OS:** Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+ recommended)
- **Python:** 3.11 or higher (3.13 recommended)
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 2GB free space
- **Internet:** Required for dependencies and API integrations

### **Recommended Setup**
- **Python:** 3.13
- **Database:** PostgreSQL 13+ (SQLite for development)
- **Cache:** Redis 6+ (optional but recommended)
- **Web Server:** Nginx (for production)
- **Process Manager:** Gunicorn + Supervisor (for production)

---

## 🚀 Installation Steps

### **Step 1: Prerequisites Installation**

#### **Python Installation**
```bash
# Windows (using Chocolatey)
choco install python313

# macOS (using Homebrew)
brew install python@3.13

# Ubuntu/Debian
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-pip
```

#### **PostgreSQL Installation (Optional)**
```bash
# Windows
choco install postgresql

# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib
```

#### **Redis Installation (Optional)**
```bash
# Windows
choco install redis-64

# macOS
brew install redis

# Ubuntu/Debian
sudo apt install redis-server
```

### **Step 2: Project Setup**

1. **Navigate to project directory:**
   ```bash
   cd path/to/novaryo
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

### **Step 3: Dependencies Installation**

```bash
# Install Python packages
pip install -r requirements.txt

# If you encounter issues, install individually:
pip install Django==5.2
pip install djangorestframework
pip install django-allauth
pip install django-cors-headers
pip install drf-yasg
pip install django-filters
pip install python-decouple
pip install Pillow
pip install psycopg2-binary  # For PostgreSQL
```

### **Step 4: Environment Configuration**

1. **Create environment file:**
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. **Edit .env file with your configuration:**
   ```env
   # Basic Settings
   SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   
   # Database (SQLite for development)
   USE_SQLITE=True
   
   # PostgreSQL (if using)
   DB_NAME=novaryo
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # Email Configuration
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   
   # Social Authentication (Optional)
   GOOGLE_OAUTH2_KEY=your-google-oauth-key
   GOOGLE_OAUTH2_SECRET=your-google-oauth-secret
   FACEBOOK_APP_ID=your-facebook-app-id
   FACEBOOK_APP_SECRET=your-facebook-app-secret
   
   # Payment Configuration (Optional)
   STRIPE_PUBLIC_KEY=your-stripe-public-key
   STRIPE_SECRET_KEY=your-stripe-secret-key
   
   # API Keys (Optional)
   GOOGLE_MAPS_API_KEY=your-google-maps-key
   AMADEUS_API_KEY=your-amadeus-api-key
   AMADEUS_API_SECRET=your-amadeus-api-secret
   ```

### **Step 5: Database Setup**

1. **Create and apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create superuser account:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Load initial data (optional):**
   ```bash
   python manage.py loaddata initial_data.json
   ```

### **Step 6: Static Files**

```bash
# Collect static files
python manage.py collectstatic --noinput
```

### **Step 7: Verification**

1. **Run system checks:**
   ```bash
   python manage.py check
   ```

2. **Test the installation:**
   ```bash
   python manage.py runserver
   ```

3. **Access the application:**
   - **Website:** http://127.0.0.1:8000
   - **Admin Panel:** http://127.0.0.1:8000/admin
   - **API Documentation:** http://127.0.0.1:8000/api/docs

---

## 🗄️ Database Configuration

### **SQLite (Default for Development)**
No additional setup required. Database file will be created automatically.

### **PostgreSQL (Recommended for Production)**

1. **Create database:**
   ```sql
   sudo -u postgres psql
   CREATE DATABASE novaryo;
   CREATE USER novaryo_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE novaryo TO novaryo_user;
   \q
   ```

2. **Update .env file:**
   ```env
   USE_SQLITE=False
   DB_NAME=novaryo
   DB_USER=novaryo_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

---

## 🔧 Optional Services Setup

### **Redis Configuration**
```env
REDIS_URL=redis://localhost:6379/0
```

### **Celery Setup (Background Tasks)**
```bash
# Start Celery worker (in separate terminal)
celery -A novaryo worker -l info

# Start Celery beat (for scheduled tasks)
celery -A novaryo beat -l info
```

---

## 🚀 Production Deployment

### **Environment Variables**
```env
DEBUG=False
SECRET_KEY=production-secret-key-very-long-and-random
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### **Web Server (Nginx)**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    # SSL configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    location /static/ {
        alias /path/to/novaryo/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/novaryo/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### **Process Manager (Gunicorn + Supervisor)**
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn novaryo.wsgi:application --bind 127.0.0.1:8000
```

---

## 🔍 Troubleshooting

### **Common Issues**

**1. ImportError: No module named 'xyz'**
```bash
pip install xyz
# or
pip install -r requirements.txt --force-reinstall
```

**2. Database connection errors**
```bash
# Check if PostgreSQL is running
sudo service postgresql status

# Reset migrations (if needed)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
python manage.py makemigrations
python manage.py migrate
```

**3. Static files not loading**
```bash
python manage.py collectstatic --clear --noinput
```

**4. Permission denied errors**
```bash
# Fix file permissions
chmod -R 755 /path/to/novaryo
chown -R www-data:www-data /path/to/novaryo  # Linux
```

### **Debug Mode**
```bash
# Run with verbose output
python manage.py runserver --verbosity=2

# Check for issues
python manage.py check --deploy
```

---

## 📞 Support

**If you encounter any issues during installation:**

**Aniket Kumar**  
📧 **Email:** aniket.kumar.devpro@gmail.com  
📱 **WhatsApp:** +91 8318601925  
🐙 **GitHub:** @Aniket-Dev-IT

**Include in your support request:**
- Operating system and version
- Python version
- Error messages (full traceback)
- Steps you've already tried
- Your environment configuration (without sensitive data)

---

## ⚖️ License Reminder

This software is proprietary and copyrighted by Aniket Kumar. Installation and use require explicit written permission. See [LICENSE.md](LICENSE.md) for full terms.

**© 2025 Aniket Kumar - All Rights Reserved**

---

*Installation guide last updated: September 27, 2025*