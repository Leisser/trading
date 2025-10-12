# Firebase Setup Instructions

## ✅ Configuration Complete

Firebase authentication has been successfully configured for your Fluxor trading platform. Here's what was set up:

### What Was Configured

1. **✅ Firebase Service Account** - Created and configured
   - Location: `fluxor_api/firebase_service_account.json`
   - Project ID: `fluxor-434ed`
   - Service Account: `firebase-adminsdk-fbsvc@fluxor-434ed.iam.gserviceaccount.com`

2. **✅ Backend Integration** - Updated Django to use Firebase Admin SDK
   - Updated `fluxor_api/accounts/firebase_auth.py` to use Firebase Admin SDK
   - Configured `fluxor_api/fluxor_api/settings.py` with Firebase settings
   - Firebase Admin SDK v6.4.0 is already installed

3. **✅ Frontend Configuration** - Already configured
   - Web app: `web/src/config/firebase.ts`
   - Project matches backend configuration

4. **✅ Security** - Properly secured
   - Service account JSON is gitignored
   - Private keys are not exposed in code
   - Environment variables configured

## 🔧 Final Setup Step

**Add Firebase configuration to your .env file:**

```bash
# Option 1: Append to existing .env file
cat env.firebase >> .env

# Option 2: Manually add these lines to .env
echo "FIREBASE_PROJECT_ID=fluxor-434ed" >> .env
echo "FIREBASE_API_KEY=AIzaSyC2EjPY7nG7uFyu6l2ymNlTGxTecOD69gU" >> .env
```

## 🧪 Testing

### 1. Verify Configuration
```bash
python test_firebase_config.py
```

### 2. Start Development Server
```bash
# Terminal 1 - Backend
cd fluxor_api
python manage.py runserver

# Terminal 2 - Frontend (Web)
cd web
npm run dev

# Terminal 3 - Dashboard (Optional)
cd fluxor-dashboard
npm run dev
```

### 3. Test Authentication

1. **Frontend Authentication**:
   - Navigate to your web app (usually http://localhost:3000)
   - Try signing in with:
     - Email/Password
     - Google OAuth
     - GitHub OAuth

2. **Backend Verification**:
   - Check Django logs for: "Firebase authentication successful for user: [email]"
   - Verify user is created in Django admin

3. **API Testing**:
   ```bash
   # Test Firebase auth endpoint
   curl -X POST http://localhost:8000/api/accounts/firebase-auth/ \
     -H "Content-Type: application/json" \
     -d '{"id_token": "YOUR_FIREBASE_ID_TOKEN"}'
   ```

## 📁 File Structure

```
trading/
├── fluxor_api/
│   ├── firebase_service_account.json    # ✅ Service account (gitignored)
│   ├── accounts/
│   │   └── firebase_auth.py             # ✅ Updated to use Admin SDK
│   └── fluxor_api/
│       └── settings.py                  # ✅ Firebase settings added
│
├── web/
│   └── src/
│       └── config/
│           └── firebase.ts              # ✅ Already configured
│
├── .env                                 # ⚠️ Add Firebase vars
├── env.firebase                         # 📋 Template for .env
├── env.example                          # ✅ Updated with Firebase vars
├── FIREBASE_CONFIGURATION.md            # 📖 Full documentation
└── test_firebase_config.py              # 🧪 Configuration test script
```

## 🔑 Key Configuration Details

### Service Account
- **Type**: service_account
- **Project ID**: fluxor-434ed
- **Client Email**: firebase-adminsdk-fbsvc@fluxor-434ed.iam.gserviceaccount.com

### Frontend Config
- **API Key**: AIzaSyC2EjPY7nG7uFyu6l2ymNlTGxTecOD69gU
- **Auth Domain**: fluxor-434ed.firebaseapp.com
- **Storage Bucket**: fluxor-434ed.firebasestorage.app

### Authentication Backends
Django is configured with:
1. `ModelBackend` - Standard Django auth
2. `TokenAuthentication` - Custom token auth
3. `FirebaseAuthentication` - Firebase token verification

## 🔒 Security Best Practices

1. **Never Commit Service Account**:
   - ✅ Already gitignored
   - Keep `firebase_service_account.json` secure
   - Don't share in logs or error messages

2. **Rotate Keys Periodically**:
   - Generate new service account keys in Firebase Console
   - Update `firebase_service_account.json`
   - Revoke old keys

3. **Use Environment Variables in Production**:
   ```bash
   # Production deployment
   export FIREBASE_PROJECT_ID=fluxor-434ed
   export FIREBASE_API_KEY=your-api-key
   ```

4. **Verify Tokens Server-Side**:
   - ✅ Already implemented
   - All Firebase tokens verified using Admin SDK
   - Invalid/expired tokens rejected

## 🚀 Authentication Flow

```
User (Frontend)
    ↓
    1. Sign in with Firebase
    ↓
Firebase Authentication
    ↓
    2. Returns ID Token
    ↓
Django Backend (/api/accounts/firebase-auth/)
    ↓
    3. Verify token with Firebase Admin SDK
    ↓
    4. Get/Create Django user
    ↓
    5. Return session/JWT token
    ↓
User authenticated in both Firebase and Django
```

## 📚 API Endpoints

### Firebase Authentication
- **POST** `/api/accounts/firebase-auth/`
  - Body: `{"id_token": "firebase_token"}`
  - Returns: User data and Django session token

- **POST** `/api/accounts/firebase-register/`
  - Body: `{"id_token": "firebase_token", "additional_data": {}}`
  - Returns: Created user and session token

- **GET** `/api/accounts/firebase-user/`
  - Headers: `Authorization: Bearer <token>`
  - Returns: Current user Firebase info

## 🐛 Troubleshooting

### Issue: "Firebase service account file not found"
**Solution**: Verify file exists at `fluxor_api/firebase_service_account.json`

### Issue: "Invalid Firebase ID token"
**Solution**:
1. Check token hasn't expired (tokens expire after 1 hour)
2. Verify frontend is using correct project configuration
3. Ensure system time is synchronized

### Issue: "Failed to initialize Firebase Admin SDK"
**Solution**:
1. Verify service account JSON is valid
2. Check internet connectivity
3. Ensure firebase-admin package is installed: `pip install firebase-admin`

### Issue: "CORS errors when authenticating"
**Solution**: Add frontend origin to `CORS_ALLOWED_ORIGINS` in settings.py

## 📖 Additional Documentation

- **Full Configuration Details**: `FIREBASE_CONFIGURATION.md`
- **Environment Setup**: `env.example`
- **Firebase Template**: `env.firebase`

## ✅ Quick Start Checklist

- [x] Firebase service account created
- [x] Backend Firebase Admin SDK configured
- [x] Frontend Firebase Client SDK configured
- [x] Service account gitignored
- [x] Environment variables configured in env.example
- [ ] **Add Firebase vars to .env** (Run: `cat env.firebase >> .env`)
- [ ] Test authentication flow
- [ ] Verify user creation in Django admin

## 🎉 You're Ready!

Your Firebase authentication is configured and ready to use. Simply complete the final setup step (adding vars to .env) and test the authentication flow.

For questions or issues, refer to:
1. `FIREBASE_CONFIGURATION.md` - Detailed configuration guide
2. `test_firebase_config.py` - Configuration verification
3. Firebase Console - https://console.firebase.google.com/project/fluxor-434ed

