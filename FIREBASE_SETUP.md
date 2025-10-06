# Firebase Authentication Setup Guide

This guide will help you set up Firebase Authentication for the Fluxor trading platform.

## 1. Firebase Project Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Enable Authentication in the Firebase console
4. Go to Project Settings > Service Accounts
5. Generate a new private key (JSON file)

## 2. Environment Variables

Create a `.env` file in the root directory with the following variables:

### Backend (Django) Environment Variables:
```bash
# Firebase Admin SDK
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
```

### Frontend (Next.js) Environment Variables:
```bash
# Firebase Client SDK
NEXT_PUBLIC_FIREBASE_API_KEY=your-firebase-api-key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-firebase-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-messaging-sender-id
NEXT_PUBLIC_FIREBASE_APP_ID=your-firebase-app-id
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 3. Firebase Authentication Methods

Enable the following authentication methods in Firebase Console:

1. **Email/Password**: For traditional signup/signin
2. **Google**: For Google OAuth
3. **GitHub**: For GitHub OAuth (requires GitHub OAuth app setup)

## 4. Firebase Storage Setup

1. Enable Firebase Storage in the console
2. Set up storage rules for ID verification images:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /id-verification/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## 5. Authentication Flow

### Registration Flow:
1. User fills out signup form with ID images
2. Firebase creates user account
3. ID images uploaded to Firebase Storage
4. Backend creates user record with Firebase UID
5. User is signed out and prompted to sign in

### Sign-in Flow:
1. User signs in with Firebase (email/password, Google, or GitHub)
2. Frontend gets Firebase ID token
3. Frontend sends token to backend `/api/auth/convert-token/`
4. Backend verifies token and returns access/refresh tokens
5. Frontend stores tokens for API requests

## 6. API Endpoints

### Authentication Endpoints:
- `POST /api/auth/register/firebase/` - Register user with Firebase
- `POST /api/auth/convert-token/` - Convert Firebase token to backend tokens
- `POST /api/auth/refresh-token/` - Refresh access token
- `POST /api/auth/logout/` - Logout and revoke session

### User Management:
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile
- `GET /api/auth/sessions/` - List user sessions
- `POST /api/auth/sessions/{id}/revoke/` - Revoke specific session

### Verification:
- `GET /api/auth/verification/status/` - Get verification status
- `POST /api/auth/verification/documents/` - Upload verification documents

## 7. Security Features

- **ID Verification**: Required for all users
- **Session Management**: Track and revoke sessions
- **Token-based Authentication**: Secure API access
- **Firebase Integration**: Industry-standard authentication
- **Multi-factor Support**: Ready for 2FA implementation

## 8. Testing

1. Start the backend: `docker-compose up -d`
2. Start the frontend: `npm run dev` (in web directory)
3. Visit `http://localhost:5173/signup`
4. Test registration with ID upload
5. Test sign-in with different methods

## 9. Production Considerations

- Use environment variables for all Firebase credentials
- Set up proper Firebase Storage security rules
- Enable Firebase App Check for additional security
- Configure CORS properly for production domains
- Use HTTPS in production
- Set up Firebase monitoring and alerts
