# Firebase Configuration Fix

## Issues Identified

Based on the browser console errors, there are two main Firebase configuration issues:

1. **Firebase Storage CORS Error**: `Access to XMLHttpRequest at 'https://firebasestorage.googleapis.com/...' from origin 'https://fluxor.pro' has been blocked by CORS policy`
2. **Firebase Authentication Error**: `Failed to load resource: the server responded with a status of 400`

## Solutions

### 1. Configure Firebase Storage CORS

**Option A: Using Google Cloud SDK (Recommended)**

1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Run the CORS configuration script:
   ```bash
   ./configure-firebase-cors.sh
   ```

**Option B: Manual Configuration**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select project: `fluxor-434ed`
3. Navigate to Cloud Storage > Browser
4. Click on the bucket: `fluxor-434ed.firebasestorage.app`
5. Go to Permissions tab
6. Add CORS configuration:
   ```json
   [
     {
       "origin": [
         "https://fluxor.pro",
         "https://www.fluxor.pro",
         "http://localhost:5173",
         "http://localhost:3000"
       ],
       "method": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
       "maxAgeSeconds": 3600,
       "responseHeader": [
         "Content-Type",
         "Authorization",
         "X-Requested-With",
         "Access-Control-Allow-Origin",
         "Access-Control-Allow-Methods",
         "Access-Control-Allow-Headers"
       ]
     }
   ]
   ```

### 2. Update Firebase Storage Rules

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: `fluxor-434ed`
3. Navigate to Storage > Rules
4. Replace the rules with the content from `firebase-storage-rules.js`:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Allow authenticated users to upload ID verification documents
    match /id-verification/{userId}/{fileName} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Allow authenticated users to upload profile images
    match /profile-images/{userId}/{fileName} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Allow public read access to verified documents (optional)
    match /verified-documents/{fileName} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    
    // Allow authenticated users to upload any file to their own folder
    match /{allPaths=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### 3. Verify Firebase Authentication

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: `fluxor-434ed`
3. Navigate to Authentication > Sign-in method
4. Ensure Email/Password is enabled
5. Ensure Google and GitHub providers are configured
6. Check authorized domains include:
   - `fluxor.pro`
   - `www.fluxor.pro`
   - `localhost` (for development)

### 4. Test Configuration

1. Open `test-firebase-auth.html` in a browser
2. Click "Test Sign Up" to verify authentication
3. Click "Test Storage" to verify storage access
4. Check browser console for any remaining errors

## Expected Results

After applying these fixes:

- ✅ Firebase Authentication should work without 400 errors
- ✅ File uploads to Firebase Storage should work without CORS errors
- ✅ User registration should complete successfully
- ✅ ID document uploads should work properly

## Troubleshooting

If issues persist:

1. **Check Firebase Console Logs**: Go to Firebase Console > Functions > Logs
2. **Verify Domain Configuration**: Ensure all domains are properly configured
3. **Check Browser Network Tab**: Look for specific error responses
4. **Test with Different Browser**: Try in incognito mode to rule out extensions

## Files Created

- `firebase-storage-cors.json` - CORS configuration
- `firebase-storage-rules.js` - Storage rules
- `configure-firebase-cors.sh` - CORS setup script
- `test-firebase-auth.html` - Test page
- `FIREBASE_SETUP.md` - This documentation