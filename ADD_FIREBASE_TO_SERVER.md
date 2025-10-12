# 🔑 Add Firebase Credentials to Production Server

## 🎯 **Required: Manually Upload Firebase Service Account**

The Firebase service account credentials were excluded from git for security. You need to manually add them to your production server.

---

## 📝 **Steps to Add Firebase Credentials:**

### **Option 1: Upload via SCP (Recommended)**

```bash
# From your local machine
cd /Users/mc/trading

# Upload to production server
scp fluxor_api/firebase_service_account.json user@your-server:/path/to/trading/fluxor_api/

# Example with specific server
scp fluxor_api/firebase_service_account.json root@fluxor.pro:/root/trading/fluxor_api/
```

### **Option 2: Copy Content Manually**

```bash
# On your local machine
cat /Users/mc/trading/fluxor_api/firebase_service_account.json

# Copy the output

# On production server
ssh user@your-server
cd /path/to/trading/fluxor_api
nano firebase_service_account.json

# Paste the content
# Save: Ctrl+O, Enter
# Exit: Ctrl+X
```

### **Option 3: Use Docker Copy**

```bash
# On production server
cd /path/to/trading

# Copy from local to container
docker cp ~/firebase_service_account.json trading-api-1:/app/firebase_service_account.json

# Or mount as volume (edit docker-compose.prod.yml)
```

---

## 🔍 **Verify File is Added:**

```bash
# On production server
cd /path/to/trading/fluxor_api

# Check file exists
ls -la firebase_service_account.json

# Should see something like:
# -rw-r--r-- 1 user user 2345 Oct 12 19:30 firebase_service_account.json

# Verify it's valid JSON
cat firebase_service_account.json | python -m json.tool | head -20
```

---

## 🔄 **After Adding File:**

### **Restart API Container:**

```bash
# On production server
cd /path/to/trading

# Restart API to pick up the file
docker-compose -f docker-compose.prod.yml restart api

# Or rebuild if needed
docker-compose -f docker-compose.prod.yml up -d --build api
```

---

## 🧪 **Test Firebase Authentication:**

```bash
# On production server
docker-compose -f docker-compose.prod.yml exec api python manage.py shell

# In Django shell
>>> from firebase_admin import credentials, auth
>>> print("Firebase initialized successfully!")
>>> exit()

# Should see no errors
```

---

## 📍 **File Location:**

### **Local:**
```
/Users/mc/trading/fluxor_api/firebase_service_account.json
```

### **Production:**
```
/path/to/trading/fluxor_api/firebase_service_account.json
```

### **Inside Container:**
```
/app/firebase_service_account.json
```

---

## ⚠️ **Important Security Notes:**

### **DO NOT:**
- ❌ Commit to git (already in .gitignore)
- ❌ Share publicly
- ❌ Post in chat/slack
- ❌ Send via email unencrypted

### **DO:**
- ✅ Use SCP for transfer
- ✅ Set proper file permissions (chmod 600)
- ✅ Keep backup in secure location
- ✅ Rotate credentials if exposed

---

## 🔐 **Set Proper Permissions:**

```bash
# On production server
cd /path/to/trading/fluxor_api

# Set restrictive permissions
chmod 600 firebase_service_account.json
chown www-data:www-data firebase_service_account.json  # Or your app user

# Verify
ls -la firebase_service_account.json
# Should show: -rw------- (600)
```

---

## 🚀 **Quick Command Reference:**

### **Upload File:**
```bash
# Replace with your actual server details
scp fluxor_api/firebase_service_account.json root@fluxor.pro:/root/trading/fluxor_api/
```

### **Verify Upload:**
```bash
ssh root@fluxor.pro
cd /root/trading/fluxor_api
ls -la firebase_service_account.json
```

### **Restart Services:**
```bash
cd /root/trading
docker-compose -f docker-compose.prod.yml restart api
```

### **Check Logs:**
```bash
docker-compose -f docker-compose.prod.yml logs api | grep -i firebase
```

---

## 🧪 **Test Authentication Works:**

### **Try Signing In:**
```
1. Navigate to: https://fluxor.pro/signin
2. Try Firebase authentication
3. Should work without errors
4. If errors, check API logs
```

---

## 📋 **Checklist:**

- [ ] Upload firebase_service_account.json to server
- [ ] Verify file exists in correct location
- [ ] Set proper permissions (chmod 600)
- [ ] Restart API container
- [ ] Test Firebase authentication
- [ ] Check API logs for errors
- [ ] Verify sign-in works on production

---

**🔑 Once you add the Firebase credentials, your authentication system will be fully operational!**

**Use the SCP command above to securely transfer the file to your server.**
