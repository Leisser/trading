# Fluxor Trading Platform - Quick Start Guide

## 🎉 Firebase Authentication Configured!

Your Fluxor trading platform is now running with Firebase authentication fully configured.

## 🚀 Services Running

| Service | URL | Description |
|---------|-----|-------------|
| **API Server** | http://localhost:8000 | Django REST API with Firebase auth |
| **Web Frontend** | http://localhost:5173 | Next.js marketing/auth site |
| **Dashboard** | http://localhost:3001 | Vue.js trading dashboard |
| **PostgreSQL** | localhost:5432 | Database |
| **Redis** | localhost:6379 | Cache & message broker |
| **PgAdmin** | http://localhost:5050 | Database management |
| **Nginx** | http://localhost | Reverse proxy |

## 🔥 Firebase Configuration

### Configured Components

✅ **Service Account**: `firebase_service_account.json`
- Project ID: `fluxor-434ed`
- Service Email: `firebase-adminsdk-fbsvc@fluxor-434ed.iam.gserviceaccount.com`

✅ **Backend (Django)**
- Firebase Admin SDK initialized
- Token verification enabled
- User sync enabled

✅ **Frontend (Next.js)**
- Firebase Client SDK configured
- Auth providers: Email/Password, Google, GitHub

## 🔐 Authentication Flow

1. **User signs in** via frontend (Web or Dashboard)
2. **Firebase returns** ID token
3. **Frontend sends** token to Django API
4. **Backend verifies** token with Firebase Admin SDK
5. **Django creates/updates** user and returns session token
6. **User authenticated** in both systems

## 📝 API Endpoints

### Firebase Authentication

```bash
# Authenticate with Firebase token
POST http://localhost:8000/api/accounts/firebase-auth/
Content-Type: application/json
{
  "id_token": "YOUR_FIREBASE_ID_TOKEN"
}

# Register new user
POST http://localhost:8000/api/accounts/firebase-register/
Content-Type: application/json
{
  "id_token": "YOUR_FIREBASE_ID_TOKEN",
  "additional_data": {}
}

# Get current user
GET http://localhost:8000/api/accounts/firebase-user/
Authorization: Bearer YOUR_SESSION_TOKEN
```

## 🛠️ Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f api          # API logs
docker-compose logs -f web          # Web frontend logs
docker-compose logs -f dashboard    # Dashboard logs

# Restart a service
docker-compose restart api

# Execute commands in container
docker-compose exec api python manage.py migrate
docker-compose exec api python manage.py createsuperuser
docker-compose exec api python manage.py shell
```

## 🔍 Testing Firebase Authentication

### Test from Command Line

```bash
# Check Firebase initialization
docker-compose exec api python manage.py shell -c "from accounts.firebase_auth import firebase_auth_service; print('Project:', firebase_auth_service.project_id)"

# Test token verification (need real token from frontend)
curl -X POST http://localhost:8000/api/accounts/firebase-auth/ \
  -H "Content-Type: application/json" \
  -d '{"id_token": "YOUR_TOKEN_HERE"}'
```

### Test from Frontend

1. Open http://localhost:5173
2. Click "Sign In" or "Sign Up"
3. Use Email/Password or OAuth (Google/GitHub)
4. Token automatically sent to backend
5. Check browser console for auth flow

## 📊 Database Management

### Access Django Admin

1. Create superuser:
   ```bash
   docker-compose exec api python manage.py createsuperuser
   ```

2. Open http://localhost:8000/admin
3. Log in with superuser credentials

### Access PgAdmin

1. Open http://localhost:5050
2. Login:
   - Email: `admin@fluxor.com`
   - Password: `admin`
3. Add server connection:
   - Host: `db`
   - Port: `5432`
   - Database: `fluxor`
   - Username: `fluxor`
   - Password: `fluxor123`

## 🐛 Troubleshooting

### Container Issues

```bash
# Check container status
docker-compose ps

# View container logs
docker-compose logs api

# Restart problematic container
docker-compose restart api

# Rebuild containers
docker-compose up -d --build
```

### Firebase Issues

**Issue**: "Firebase service account file not found"
```bash
# Verify file exists in container
docker-compose exec api ls -la firebase_service_account.json
```

**Issue**: "Invalid Firebase ID token"
- Token expired (expires after 1 hour)
- Get new token from frontend
- Check system time is synchronized

**Issue**: "Failed to initialize Firebase Admin SDK"
```bash
# Check Firebase initialization logs
docker-compose logs api | grep -i firebase
```

### Database Issues

```bash
# Run migrations
docker-compose exec api python manage.py migrate

# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
docker-compose exec api python manage.py migrate
```

## 📚 Environment Configuration

Your environment is configured in `.env`:

```bash
# Database
DATABASE_URL=postgresql://fluxor:fluxor123@localhost:5432/fluxor

# Firebase
FIREBASE_PROJECT_ID=fluxor-434ed
FIREBASE_API_KEY=AIzaSyC2EjPY7nG7uFyu6l2ymNlTGxTecOD69gU

# Redis
REDIS_URL=redis://localhost:6379/0

# Django
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
```

## 🔒 Security Notes

1. **Service Account Security**
   - ✅ Already gitignored
   - ⚠️ Never commit to version control
   - 🔄 Rotate keys periodically in production

2. **API Keys**
   - Frontend API keys are public (by design)
   - Backend uses service account for verification
   - Always verify tokens server-side

3. **Production Deployment**
   - Change `SECRET_KEY`
   - Set `DEBUG=False`
   - Use HTTPS
   - Configure proper firewall rules
   - Use environment variables for secrets

## 📖 Documentation

- **Firebase Configuration**: `FIREBASE_CONFIGURATION.md`
- **Firebase Setup**: `FIREBASE_SETUP_INSTRUCTIONS.md`
- **Deployment**: `DEPLOYMENT.md`
- **Server Setup**: `SERVER_DEPLOYMENT.md`

## 🎯 Next Steps

1. **Create Superuser**:
   ```bash
   docker-compose exec api python manage.py createsuperuser
   ```

2. **Test Authentication**:
   - Open http://localhost:5173
   - Sign up / Sign in
   - Verify user created in Django admin

3. **Develop Features**:
   - API: `fluxor_api/`
   - Web: `web/src/`
   - Dashboard: `fluxor-dashboard/src/`

4. **Deploy to Production**:
   - Review `DEPLOYMENT.md`
   - Configure production environment
   - Set up SSL certificates
   - Deploy using provided scripts

## 📞 Support

Need help? Check:
1. Container logs: `docker-compose logs -f [service]`
2. Firebase Console: https://console.firebase.google.com/project/fluxor-434ed
3. Documentation files in project root

---

**Status**: ✅ All systems operational with Firebase authentication configured!

