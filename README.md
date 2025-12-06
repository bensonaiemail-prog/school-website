# School Management System

A comprehensive, full-stack school management system built with Django REST Framework and React.

## 🎯 Features

### Core Features
- **User Management**: Role-based access control (Admin, Teacher, Parent)
- **Student Management**: Complete student lifecycle management
- **Teacher Management**: Profile management with approval workflow
- **Academic Management**: Classes, subjects, terms, and academic years
- **Results & Grading**: Automated grade calculation and report cards
- **Attendance Tracking**: Daily attendance with multiple status types
- **Fee Management**: Payment tracking and automated reminders
- **Announcements**: Role-based communication system
- **Gallery**: Event photo management with categories
- **PDF Reports**: Professional report card generation
- **Charts & Analytics**: Visual performance tracking
- **Email Notifications**: Automated alerts and reminders

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.x + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Task Queue**: Celery + Redis
- **PDF Generation**: ReportLab
- **CORS**: django-cors-headers

### Frontend
- **Framework**: React 18.x
- **UI Library**: Material-UI (MUI)
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Charts**: Recharts
- **State Management**: React Context API

## 📋 Prerequisites

- Python 3.10+
- Node.js 16+
- PostgreSQL 12+
- Redis (for Celery)
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bensonaiemail-prog/school-website.git
cd school-website
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

Create PostgreSQL database:

```sql
CREATE DATABASE school_db;
CREATE USER school_admin WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE school_db TO school_admin;
```

### 4. Environment Configuration

Create `.env` file in `backend/` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=school_db
DB_USER=school_admin
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@school.com

# Celery/Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Frontend Setup

```bash
cd ../frontend
npm install
```

## 🎮 Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # or source venv/bin/activate
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Terminal 3 - Celery Worker (Optional):**
```bash
cd backend
celery -A school_system worker -l info
```

**Terminal 4 - Celery Beat (Optional):**
```bash
cd backend
celery -A school_system beat -l info
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile
- `POST /api/auth/change-password/` - Change password

### Student Endpoints

- `GET /api/students/` - List students
- `POST /api/students/create/` - Create student
- `GET /api/students/{id}/` - Get student details
- `PUT /api/students/{id}/update/` - Update student
- `DELETE /api/students/{id}/delete/` - Delete student
- `GET /api/students/my-children/` - Get parent's children

### Results Endpoints

- `GET /api/results/` - List results
- `POST /api/results/create/` - Create result
- `GET /api/results/summary/{student_id}/{term_id}/` - Get performance summary
- `GET /api/results/report-card/{student_id}/{term_id}/` - Download PDF report

### Attendance Endpoints

- `GET /api/results/attendance/` - List attendance
- `POST /api/results/attendance/create/` - Mark attendance

### Fee Endpoints

- `GET /api/results/fees/` - List fees
- `POST /api/results/fees/create/` - Create fee record
- `PUT /api/results/fees/{id}/update/` - Update fee (record payment)

### Announcements Endpoints

- `GET /api/announcements/` - List announcements
- `POST /api/announcements/create/` - Create announcement
- `GET /api/announcements/{id}/` - Get announcement details

### Gallery Endpoints

- `GET /api/gallery/` - List published images
- `POST /api/gallery/create/` - Upload image
- `GET /api/gallery/categories/` - List categories

## 👥 User Roles & Permissions

### Admin
- Full system access
- User management
- Approve teachers
- Manage students, classes, fees
- Create announcements
- Upload gallery images

### Teacher
- Mark attendance
- Enter grades
- View assigned classes
- View announcements

### Parent
- View children's performance
- Check attendance
- View fee status
- Read announcements
- Download report cards

## 🔧 Configuration

### Email Setup (Gmail)

1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the app password in `.env` file

### Redis Setup

**Windows:**
- Download Redis from: https://github.com/microsoftarchive/redis/releases
- Run: `redis-server`

**Linux/Mac:**
```bash
sudo apt-get install redis-server  # Ubuntu
brew install redis  # Mac
redis-server
```

## 📊 Initial Data Setup

After running the application:

1. Login to admin panel
2. Create Academic Year (e.g., 2024-2025)
3. Create Terms (Term 1, 2, 3)
4. Create Subjects (Mathematics, English, etc.)
5. Create Classes (Grade 10A, etc.)
6. Add School Information in Public Info

## 🐛 Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

### CORS Error
- Check `CORS_ALLOWED_ORIGINS` in settings.py
- Ensure frontend URL is included

### Celery Not Working
- Ensure Redis is running
- Check Redis connection in `.env`
- Restart Celery worker and beat

## 📦 Production Deployment

### Using Docker (Recommended)

1. Build images
2. Use docker-compose for orchestration
3. Configure environment variables
4. Set up reverse proxy (Nginx)
5. Enable HTTPS with Let's Encrypt

### Manual Deployment

1. Set `DEBUG=False` in settings
2. Configure static/media file serving
3. Use production database
4. Set up Gunicorn/uWSGI
5. Configure Nginx
6. Set up SSL certificates
7. Configure firewall

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Benson AI

## 🙏 Acknowledgments

- Django REST Framework
- React & Material-UI
- ReportLab for PDF generation
- Recharts for data visualization

## 📧 Support

For support, email bensonaiemail@example.com or create an issue in the repository.

---

**Built with ❤️ for Education**
