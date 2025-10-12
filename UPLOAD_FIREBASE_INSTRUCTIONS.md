# 🔑 Upload Firebase Credentials to Server

## 🎯 **Server IP: 31.97.103.64**

---

## 📤 **Upload Command:**

### **From Your Local Machine:**

```bash
# Upload firebase credentials to server
scp /Users/mc/trading/fluxor_api/firebase_service_account.json root@31.97.103.64:/root/trading/fluxor_api/

# Enter your password when prompted
```

---

## ✅ **After Upload, SSH into Server:**

```bash
# Connect to server
ssh root@31.97.103.64

# Navigate to project
cd /root/trading

# Verify file exists
ls -la fluxor_api/firebase_service_account.json

# Set proper permissions
chmod 600 fluxor_api/firebase_service_account.json

# Restart API container
docker-compose -f docker-compose.prod.yml restart api

# Check container is running
docker-compose -f docker-compose.prod.yml ps api

# Check logs for any errors
docker-compose -f docker-compose.prod.yml logs api | tail -50
```

---

## 🧪 **Test Firebase Authentication:**

```bash
# On server, test in Django shell
docker-compose -f docker-compose.prod.yml exec api python manage.py shell

# In shell
>>> from firebase_admin import credentials, auth
>>> print("Firebase initialized successfully!")
>>> exit()
```

---

## 🌐 **Your Production URLs:**

- **Main App:** https://fluxor.pro
- **API:** https://api.fluxor.pro  
- **Dashboard:** https://dashboard.fluxor.pro
- **Advanced Orders:** https://fluxor.pro/index/advanced-orders

---

**🔑 Run the SCP command above to upload Firebase credentials!**
