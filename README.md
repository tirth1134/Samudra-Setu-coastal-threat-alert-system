# 🌊 Samudra Setu - Coastal Safety Gujarat

A comprehensive coastal safety and alert system for Gujarat, India. This project provides real-time coastal alerts, SMS notifications, and safety information for coastal communities.

## 🚀 Features

### Core Functionality
- **Real-time Coastal Alerts** - Monitor and manage coastal safety alerts
- **SMS Alert System** - Send instant SMS notifications to subscribers
- **Admin Dashboard** - Comprehensive admin interface for alert management
- **User Subscriptions** - Allow users to subscribe to SMS alerts
- **Multi-severity Alerts** - Low, Medium, High, and Critical alert levels

### Safety Information
- **Safe Places Directory** - Information about safe locations during emergencies
- **Fisheries Information** - Coastal fisheries data and safety guidelines
- **Pollution Reporting** - System for reporting coastal pollution incidents

### Technical Features
- **Real-time Updates** - Auto-refreshing dashboard every 30 seconds
- **Responsive Design** - Mobile-friendly interface using TailwindCSS
- **RESTful API** - Clean API endpoints for frontend-backend communication
- **Database Management** - SQLite database with Django ORM

## 🛠️ Technology Stack

- **Backend**: Django 5.2.1 (Python)
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Database**: SQLite3
- **SMS Service**: Twilio Integration
- **Deployment**: Development server (ready for production)

## 📋 Prerequisites

Before running this project, make sure you have:

- **Python 3.8+** installed
- **pip** package manager
- **Git** for version control
- **Twilio Account** (for SMS functionality)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd SAMUNDRASETU
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here

# Django Configuration
SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## 📱 SMS Setup (Twilio)

### 1. Get Twilio Credentials
- Sign up at [https://www.twilio.com/](https://www.twilio.com/)
- Get your Account SID and Auth Token from the dashboard
- Purchase a Twilio phone number

### 2. Update Settings
Replace the placeholder values in `backend/settings.py`:
```python
TWILIO_ACCOUNT_SID = 'your_actual_account_sid'
TWILIO_AUTH_TOKEN = 'your_actual_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'
```

## 🗂️ Project Structure

```
SAMUNDRASETU/
├── backend/                 # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── mainapp/                # Main Django application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URL patterns
│   ├── admin.py           # Admin interface
│   └── utils.py           # Utility functions
├── templates/              # HTML templates
│   ├── index.html         # Home page
│   ├── alerts.html        # Alerts dashboard
│   ├── adminfrontend.html # Admin interface
│   ├── fisheries.html     # Fisheries information
│   ├── pollution.html     # Pollution reporting
│   └── safeplaces.html    # Safe places directory
├── static/                 # Static files
│   └── images/            # Image assets
├── manage.py              # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🌐 Available Pages

- **Home** (`/`) - Main landing page with SMS subscription
- **Alerts** (`/alerts/`) - Real-time alerts dashboard
- **Admin Dashboard** (`/adminfrontend/`) - Alert management interface
- **Fisheries** (`/fisheries/`) - Fisheries information
- **Pollution** (`/pollution/`) - Pollution reporting system
- **Safe Places** (`/safeplaces/`) - Emergency safe locations
- **Django Admin** (`/admin/`) - Database management

## 🔌 API Endpoints

### SMS Management
- `POST /api/subscribe-sms/` - Subscribe to SMS alerts
- `POST /api/unsubscribe-sms/` - Unsubscribe from SMS alerts
- `GET /api/subscribers/` - Get all SMS subscribers

### Alert Management
- `GET /api/alerts/` - Get all active alerts
- `POST /api/create-alert/` - Create new alert (Admin only)
- `POST /api/test-sms/` - Test SMS functionality

## 📊 Database Models

### Core Models
- **Alert** - Coastal safety alerts with severity levels
- **SMSSubscriber** - Users subscribed to SMS notifications
- **NotificationLog** - Log of sent SMS notifications
- **Fishery** - Fisheries information
- **SafePlace** - Emergency safe locations
- **PollutionReport** - Pollution incident reports

## 🎨 Customization

### Styling
- Uses TailwindCSS for responsive design
- Custom color scheme with ocean-themed colors
- Responsive grid layouts for mobile and desktop

### Alert Types
- **Low** - Normal conditions
- **Medium** - Potential concern, monitor
- **High** - High risk, prepare
- **Critical** - Severe, evacuate if told

## 🚨 Emergency Features

### SMS Alert System
- Instant notifications to all subscribers
- Configurable alert severity levels
- Real-time delivery status tracking

### Safety Information
- Emergency contact numbers
- Safe evacuation routes
- Coastal safety guidelines

## 🔧 Development

### Adding New Features
1. Create models in `mainapp/models.py`
2. Add views in `mainapp/views.py`
3. Update URLs in `mainapp/urls.py`
4. Create templates in `templates/` directory
5. Test thoroughly before deployment

### Code Style
- Follow PEP 8 Python guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Comment complex logic

## 🚀 Deployment

### Production Considerations
- Set `DEBUG = False` in production
- Use environment variables for sensitive data
- Configure proper database (PostgreSQL recommended)
- Set up static file serving
- Configure HTTPS
- Use production WSGI server (Gunicorn)

### Environment Variables
```bash
export DJANGO_SETTINGS_MODULE=backend.settings
export SECRET_KEY=your_production_secret_key
export ALLOWED_HOSTS=yourdomain.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🙏 Acknowledgments

- **Coastal Communities** - For inspiration and feedback
- **Django Community** - For the excellent framework
- **TailwindCSS** - For the beautiful UI components
- **Twilio** - For reliable SMS services

## 📈 Future Enhancements

- [ ] Weather integration
- [ ] Tide monitoring
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with government APIs
- [ ] Real-time weather alerts
- [ ] Community reporting system

---

**Built with ❤️ for Coastal Safety in Gujarat, India**

*Last updated: August 2025*
