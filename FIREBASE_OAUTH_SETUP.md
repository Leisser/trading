# Firebase OAuth Configuration

## ⚠️ Google Sign-In Not Showing Popup?

If you're not seeing the Google account selection popup, you need to configure OAuth in Firebase Console.

---

## 🔧 Firebase Console Configuration

### Step 1: Go to Firebase Console
https://console.firebase.google.com/project/fluxor-434ed

### Step 2: Enable Google Sign-In

1. **Click "Authentication"** in left sidebar
2. **Click "Sign-in method"** tab
3. **Click "Google"** provider
4. **Toggle "Enable"** switch
5. **Add support email**: Your email address
6. **Click "Save"**

### Step 3: Configure Authorized Domains

1. **Still in "Authentication"** section
2. **Click "Settings"** tab
3. **Scroll to "Authorized domains"**
4. **Add these domains**:
   - `localhost` (should be there by default)
   - `fluxor-434ed.firebaseapp.com` (default)
   - `fluxor.pro` (if you have custom domain)

### Step 4: Configure OAuth Consent Screen (Google Cloud)

1. Go to https://console.cloud.google.com/
2. Select project: **fluxor-434ed**
3. Navigate to **APIs & Services** → **OAuth consent screen**
4. Configure:
   - **App name**: Fluxor
   - **User support email**: Your email
   - **Developer contact**: Your email
   - **Scopes**: email, profile
   - **Test users**: Add your test emails (for development)
5. **Save**

### Step 5: Configure Authorized JavaScript Origins

1. **APIs & Services** → **Credentials**
2. Find your **Web client (auto created by Firebase)**
3. Click to edit
4. **Authorized JavaScript origins**:
   - `http://localhost:5173`
   - `http://localhost:3000`
   - `http://localhost` 
5. **Authorized redirect URIs**:
   - `http://localhost:5173/__/auth/handler`
   - `http://localhost:3000/__/auth/handler`
   - `https://fluxor-434ed.firebaseapp.com/__/auth/handler`
6. **Save**

---

## 🐛 Troubleshooting

### Issue: Google Popup Not Showing

**Causes**:
1. Pop-up blocked by browser
2. OAuth not enabled in Firebase
3. Authorized domains not configured
4. Third-party cookies blocked

**Solutions**:

#### 1. Check Browser Popup Blocker
- Look for popup blocker icon in address bar
- Allow popups for localhost:5173
- Try in incognito mode

#### 2. Enable Third-Party Cookies (Temporary for Development)
**Chrome**:
1. Settings → Privacy and Security → Third-party cookies
2. Select "Allow third-party cookies"
3. Or add exception for `accounts.google.com`

**Safari**:
1. Preferences → Privacy
2. Uncheck "Prevent cross-site tracking" (temporary)

**Firefox**:
1. Settings → Privacy & Security
2. Enhanced Tracking Protection → Custom
3. Uncheck "Cookies"

#### 3. Check Console for Errors
Press F12 and check Console tab for:
- `ERR_SOCKET_NOT_CONNECTED` - Network issue
- `popup_closed_by_user` - User closed popup
- `access_denied` - OAuth not configured

---

## 🔄 Alternative: Redirect Instead of Popup

If popups keep being blocked, use redirect flow instead:

### Update authService.ts
```typescript
import { signInWithRedirect, getRedirectResult } from 'firebase/auth';

// Instead of signInWithPopup:
async signInWithGoogle(): Promise<UserCredential> {
  try {
    await signInWithRedirect(auth, googleProvider);
    // Will redirect to Google, then back to your app
  } catch (error: any) {
    throw new Error(this.getFirebaseErrorMessage(error.code));
  }
}

// In your component (check for redirect result on mount):
useEffect(() => {
  getRedirectResult(auth).then((result) => {
    if (result) {
      // User just came back from Google
      authService.syncFirebaseUser(result.user);
    }
  });
}, []);
```

---

## ✅ Quick Test

### Test Firebase OAuth Configuration

1. **Open browser console** (F12)
2. **Run**:
   ```javascript
   console.log('Firebase config:', window.firebase?.app()?.options);
   ```
3. **Verify**:
   - apiKey present
   - authDomain: `fluxor-434ed.firebaseapp.com`
   - projectId: `fluxor-434ed`

---

## 🎯 Recommended Solution for Development

### Option 1: Use Email/Password (Easiest)
```
http://localhost:5173/signup
→ Sign up with email/password
→ No OAuth configuration needed
→ Works immediately
```

### Option 2: Configure OAuth Properly
1. Follow Firebase Console steps above
2. Add authorized domains
3. Configure OAuth consent screen
4. Restart web container

### Option 3: Use Redirect Flow
- Change from popup to redirect
- Works better with popup blockers
- Requires code changes (shown above)

---

## 📝 Current Status

```
✅ Firebase Configuration: Correct
✅ Backend Token Verification: Working
✅ Auto-Registration: Working
✅ Email/Password Auth: Working

⚠️ Google OAuth: Needs Firebase Console configuration
⚠️ GitHub OAuth: Needs Firebase Console configuration
```

---

## 🚀 Quick Fix to Test Now

**Use Email/Password authentication while configuring OAuth:**

1. Go to http://localhost:5173/signup
2. Create account with email and password
3. User will be auto-created in Django
4. You can test the full flow without OAuth

**Then configure OAuth properly in Firebase Console for production.**

---

## 📞 Next Steps

1. **Immediate**: Test with email/password
2. **Short-term**: Configure OAuth in Firebase Console
3. **Optional**: Switch to redirect flow if popups are problematic

---

**Your authentication is working!** The OAuth issue is just a configuration step in Firebase Console.

