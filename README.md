# 🏨 Novaryo - Travel Booking Platform

**"Discover Comfort. Discover Novaryo."**

A comprehensive, professional travel booking platform built with Django, featuring hotel bookings, flight reservations, travel packages, activities, and a complete loyalty program system.

![Novaryo Logo](https://img.shields.io/badge/Novaryo-Travel%20Platform-blue?style=for-the-badge)
![Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)

---

## 📞 Developer Contact

**Created by:** Aniket Kumar  
📧 **Email:** [aniket.kumar.devpro@gmail.com](mailto:aniket.kumar.devpro@gmail.com)  
📱 **WhatsApp:** [+91 8318601925](https://wa.me/918318601925)  
🐙 **GitHub:** [@Aniket-Dev-IT](https://github.com/Aniket-Dev-IT)

---

## ⚖️ LICENSE & COPYRIGHT

**🚨 IMPORTANT: This project is proprietary and copyrighted.**

© 2025 **Aniket Kumar**. All rights reserved.

**⛔ USAGE RESTRICTIONS:**
- This project is **NOT open source**
- Commercial use is **STRICTLY PROHIBITED** without explicit written permission
- Redistribution, modification, or derivative works require **PRIOR AUTHORIZATION**
- For licensing inquiries, contact: **aniket.kumar.devpro@gmail.com**

**Before using this project in any capacity, you MUST:**
1. Contact the developer for permission
2. Obtain written authorization
3. Comply with all licensing terms

**Unauthorized use may result in legal action.**

---

## 🌟 Features

### 🏨 **Hotel Booking System**
- Advanced search with filters (location, dates, guests, price range)
- Hotel details with high-quality images and reviews
- Real-time availability checking
- Responsive booking interface

### ✈️ **Flight Booking System**
- Domestic and international flight search
- Flexible date selection with return/one-way options
- Passenger management system
- Seat preference selection

### 📦 **Travel Packages**
- Curated travel packages combining flights, hotels, and activities
- Pre-designed popular destinations (Paris, Bali, Japan)
- Package customization options
- Comprehensive package details

### 🎯 **Activities & Experiences**
- Local activity bookings and tours
- Category-based browsing (sightseeing, adventure, cultural, food)
- Activity ratings and reviews
- Booking management system

### ⭐ **Loyalty Program**
- 4-tier loyalty system (Bronze, Silver, Gold, Platinum)
- Points earning on every booking
- Exclusive member benefits and discounts
- Comprehensive rewards catalog
- Points redemption system

### 👤 **User Management**
- Complete user registration and authentication
- Profile management with preferences
- Security settings and account verification
- Saved hotels and wishlist functionality
- Booking history and management

### 🛡️ **Security Features**
- Django Allauth integration
- Email verification system
- Secure password management
- Session security
- CSRF protection

### 📊 **Admin Panel**
- Comprehensive Django admin interface
- User management with detailed analytics
- Booking management system
- Loyalty program administration
- Content management capabilities

---

## 🛠️ Technology Stack

### **Backend**
- **Framework:** Django 5.2
- **Language:** Python 3.13
- **Authentication:** Django Allauth
- **API:** Django REST Framework
- **Documentation:** drf-yasg (Swagger/OpenAPI)

### **Frontend**
- **Framework:** Bootstrap 5.3
- **Icons:** Bootstrap Icons
- **Styling:** Custom CSS with Novaryo branding
- **JavaScript:** Vanilla JS with Bootstrap components
- **Responsive:** Mobile-first design

### **Database**
- **Primary:** PostgreSQL (configurable)
- **Fallback:** SQLite3 for development
- **ORM:** Django ORM

### **Additional Technologies**
- **Task Queue:** Celery (configured)
- **Caching:** Redis support
- **Email:** SMTP configuration
- **File Storage:** Configurable (local/cloud)
- **Payment:** Skip Payment System (Smart Development Approach)

---

## 📊 Development Status

### ✅ **ALL MODULES COMPLETE (8/8)**

| Module | Status | Progress | Features |
|--------|--------|----------|----------|
| **Users** | ✅ Complete | 100% | Authentication, Profiles, Preferences |
| **Hotels** | ✅ Complete | 100% | Search, Booking, Management |
| **Flights** | ✅ Complete | 100% | Search, Booking, Seat Selection |
| **Packages** | ✅ Complete | 100% | Travel Packages, Booking System |
| **Activities** | ✅ Complete | 100% | Local Tours, Activity Booking |
| **Bookings** | ✅ Complete | 100% | Unified Booking Management |
| **Reviews** | ✅ Complete | 100% | Rating System, User Feedback |
| **Loyalty** | ✅ Complete | 100% | Points System, Tiers, Rewards |

### 🎨 **Frontend Pages Status**

| Page Category | Completed | Total | Status |
|---------------|-----------|-------|--------|
| **Authentication** | 5/5 | 5 | ✅ Complete |
| **Hotel Pages** | 8/8 | 8 | ✅ Complete |
| **Flight Pages** | 12/12 | 12 | ✅ Complete |
| **Package Pages** | 6/6 | 6 | ✅ Complete |
| **Activity Pages** | 6/6 | 6 | ✅ Complete |
| **Booking Pages** | 10/10 | 10 | ✅ Complete |
| **Loyalty Pages** | 5/5 | 5 | ✅ Complete |
| **User Dashboard** | 8/8 | 8 | ✅ Complete |

**Total: 60/60 pages completed (100%)**

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- PostgreSQL (optional, SQLite fallback available)
- Redis (for caching and Celery)

### Installation

**⚠️ IMPORTANT: Contact developer for authorization before proceeding**

1. **Contact the developer for permission:**
   ```
   Email: aniket.kumar.devpro@gmail.com
   WhatsApp: +91 8318601925
   ```

2. **After receiving authorization, set up the project:**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup:**
   ```bash
   # Create .env file with your configuration
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Database setup:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Website: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin
   - API Docs: http://127.0.0.1:8000/api/docs

---

## 📁 Project Structure

```
novaryo/
├── 📁 novaryo/              # Project settings
├── 📁 users/               # User management app
├── 📁 hotels/              # Hotel booking system
├── 📁 flights/             # Flight booking system
├── 📁 packages/            # Travel packages
├── 📁 activities/          # Activities & experiences
├── 📁 loyalty/             # Loyalty program
├── 📁 bookings/            # Booking management
├── 📁 reviews/             # Review system
├── 📁 payments/            # Payment processing (Skip Payment)
├── 📁 templates/           # HTML templates
├── 📁 static/              # Static files
├── 📁 media/               # User uploaded files
├── 📄 requirements.txt     # Python dependencies
├── 📄 manage.py           # Django management
└── 📄 README.md           # This file
```

---

## 🎨 Design System

### **Novaryo Brand Colors**
- **Primary:** `#2c5282` (Novaryo Blue)
- **Secondary:** `#3182ce` (Light Blue)
- **Accent:** `#ed8936` (Orange)
- **Light:** `#f7fafc` (Light Gray)
- **Dark:** `#2d3748` (Dark Gray)

### **Features Overview**
- 🔍 **Advanced Search:** Find exactly what you're looking for
- 💝 **Save Favorites:** Wishlist hotels and activities
- ⭐ **Earn Points:** Loyalty rewards on every booking
- 📱 **Mobile Ready:** Perfect experience on any device
- 🔒 **Secure Booking:** Protected payments and data

---

## 🚀 Production Ready

This project is **100% complete** and ready for production deployment with:
- ✅ All 8 core modules fully implemented
- ✅ Complete database schema and migrations
- ✅ Professional admin interface
- ✅ Smart payment system (skip payment for development)
- ✅ Responsive design for all devices
- ✅ Security features implemented
- ✅ API documentation available

---

## 🤝 Support & Contact

**For any questions, issues, or licensing inquiries:**

**Developer:** Aniket Kumar  
📧 **Email:** aniket.kumar.devpro@gmail.com  
📱 **WhatsApp:** +91 8318601925  
🐙 **GitHub:** @Aniket-Dev-IT  

**Business Hours:** Monday - Friday, 9:00 AM - 6:00 PM IST

---

## ⚖️ Legal Notice

This software is proprietary and confidential. Any unauthorized access, use, reproduction, or distribution is strictly prohibited and may result in severe civil and criminal penalties. All rights reserved.

**© 2025 Aniket Kumar - All Rights Reserved**

---

*Built with ❤️ by [Aniket Kumar](mailto:aniket.kumar.devpro@gmail.com)*