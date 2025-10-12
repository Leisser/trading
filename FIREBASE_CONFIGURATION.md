# Firebase Authentication Configuration

This document explains the Firebase authentication setup for the Fluxor trading platform.

## Overview

The platform uses Firebase Authentication for user authentication with the Firebase Admin SDK on the backend and Firebase Client SDK on the frontend.

## Configuration Files

### 1. Backend Configuration (Django)

#### Service Account File
- **Location**: `/fluxor_api/firebase_service_account.json`
- **Purpose**: Contains Firebase Admin SDK credentials for server-side authentication
- **Security**: This file is gitignored and should NEVER be committed to version control

#### Environment Variables
Add the following to your `.env` file:

```bash
FIREBASE_PROJECT_ID=fluxor-434ed
FIREBASE_API_KEY=AIzaSyC2EjPY7nG7uFyu6l2ymNlTGxTecOD69gU
```

#### Django Settings
The Firebase configuration is automatically loaded from:
- `fluxor_api/fluxor_api/settings.py` - Contains Firebase settings
- `fluxor_api/accounts/firebase_auth.py` - Firebase authentication service

### 2. Frontend Configuration

#### Web Application (Next.js)
- **Location**: `/web/src/config/firebase.ts`
- **Configuration**:
  ```typescript
  const firebaseConfig = {
    apiKey: "AIzaSyC2EjPY7nG7uFyu6l2ymNlTGxTecOD69gU",
    authDomain: "fluxor-434ed.firebaseapp.com",
    projectId: "fluxor-434ed",
    storageBucket: "fluxor-434ed.firebasestorage.app",
    messagingSenderId: "665456308175",
    appId: "1:665456308175:web:a990ace4d8dcaf91b62cba",
    measurementId: "G-6Y3S97KP7T"
  };
  ```

#### Dashboard (Vue.js)
- Firebase client SDK should be configured similarly if needed
- Currently uses API authentication through the backend

## Firebase Admin SDK Setup

### Service Account Details
- **Project ID**: fluxor-434ed
- **Service Account Email**: firebase-adminsdk-fbsvc@fluxor-434ed.iam.gserviceaccount.com
- **Client ID**: 104442175894934154676

### How It Works

1. **Client Authentication**:
   - User signs in through Firebase on the frontend
   - Firebase returns an ID token

2. **Backend Verification**:
   - Client sends ID token to Django backend
   - Django uses Firebase Admin SDK to verify the token
   - If valid, Django creates/updates user and returns session token

3. **User Management**:
   - Firebase UID is stored in Django User model
   - User data synced between Firebase and Django
   - Supports email/password, Google, and GitHub authentication

## Authentication Flow

```
┌─────────┐          ┌──────────┐          ┌─────────┐
│ Client  │          │ Firebase │          │ Django  │
└────┬────┘          └────┬─────┘          └────┬────┘
     │                    │                     │
     │  Sign In Request   │                     │
     ├───────────────────>│                     │
     │                    │                     │
     │  ID Token          │                     │
     │<───────────────────┤                     │
     │                    │                     │
     │  Verify Token      │                     │
     ├────────────────────┴─────────────────────>│
     │                                           │
     │  Validate with Firebase Admin SDK         │
     │                    ┌─────────────────────>│
     │                    │                      │
     │                    │  User Data           │
     │                    │<─────────────────────┤
     │                                           │
     │  Create/Update User & Return Session      │
     │<──────────────────────────────────────────┤
     │                                           │
```

## Security Considerations

1. **Service Account Security**:
   - Never commit `firebase_service_account.json` to git
   - Rotate service account keys periodically
   - Limit service account permissions in Firebase Console

2. **API Keys**:
   - Frontend API keys are public (by design)
   - Backend uses service account for privileged operations
   - Always verify tokens on the backend

3. **Token Verification**:
   - All Firebase tokens are verified using Admin SDK
   - Expired/revoked tokens are rejected
   - Token verification includes certificate validation

## Setup Instructions

### Development Environment

1. **Install Dependencies**:
   ```bash
   cd fluxor_api
   pip install -r requirements.txt
   ```

2. **Verify Service Account File**:
   - Ensure `firebase_service_account.json` exists in `fluxor_api/`
   - Verify file permissions are restrictive (644 or 600)

3. **Configure Environment**:
   ```bash
   cp env.example .env
   # Edit .env and add Firebase variables
   ```

4. **Test Authentication**:
   ```bash
   python manage.py shell
   >>> from accounts.firebase_auth import firebase_auth_service
   >>> # Service should initialize without errors
   ```

### Production Deployment

1. **Secure Service Account**:
   - Store service account JSON in secure location
   - Use environment variables or secrets management
   - Never expose in logs or error messages

2. **Update Settings**:
   ```python
   # In production settings
   FIREBASE_SERVICE_ACCOUNT_PATH = os.environ.get('FIREBASE_SERVICE_ACCOUNT_PATH')
   ```

3. **Configure Firewall Rules**:
   - Restrict access to Firebase Admin endpoints
   - Use HTTPS for all authentication requests

## Troubleshooting

### Common Issues

1. **"Firebase service account file not found"**
   - Verify file exists at `fluxor_api/firebase_service_account.json`
   - Check file permissions

2. **"Invalid Firebase ID token"**
   - Verify frontend is using correct Firebase config
   - Check token hasn't expired
   - Ensure time sync between client and server

3. **"Failed to initialize Firebase Admin SDK"**
   - Verify service account JSON is valid
   - Check network connectivity to Firebase
   - Verify project ID matches

### Debug Mode

Enable Firebase debug logging:

```python
import logging
logging.getLogger('firebase_admin').setLevel(logging.DEBUG)
```

## API Endpoints

### Firebase Authentication Endpoints

- `POST /api/accounts/firebase-auth/` - Authenticate with Firebase token
- `POST /api/accounts/firebase-register/` - Register new user with Firebase
- `GET /api/accounts/firebase-user/` - Get current Firebase user info

## Testing

### Manual Testing

1. **Test Frontend Auth**:
   ```bash
   # Start development servers
   cd web && npm run dev
   # Navigate to sign-in page
   # Test Google/Email authentication
   ```

2. **Test Backend Verification**:
   ```bash
   # Use test scripts
   python test-auth-flow.py
   python test-firebase-auth.html (in browser)
   ```

### Automated Testing

```bash
cd fluxor_api
pytest accounts/tests/test_firebase_auth.py -v
```

## References

- [Firebase Admin SDK Documentation](https://firebase.google.com/docs/admin/setup)
- [Firebase Authentication](https://firebase.google.com/docs/auth)
- [Django REST Framework](https://www.django-rest-framework.org/)

## Support

For issues or questions:
1. Check Firebase Console for service status
2. Review application logs for errors
3. Verify all configuration files are properly set up

