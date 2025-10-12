# 🧪 Local KYC File Upload Testing Guide

## **Quick Start - Test the System**

### **1. Access the Application**
- **Frontend (Next.js)**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **API Health Check**: http://localhost:8000/api/health/

### **2. Test the Registration Flow**

#### **Step 1: Open the Signup Page**
1. Go to http://localhost:5173
2. Click "Sign Up" button
3. You should see the registration form with file upload options

#### **Step 2: Test File Upload (Without Authentication)**
The system should properly reject uploads without authentication.

#### **Step 3: Test with Firebase Authentication**
You'll need to set up Firebase authentication to test the complete flow.

## **🔧 Manual Testing Methods**

### **Method 1: Browser Testing**

1. **Open Browser Developer Tools**
   - Press F12 or right-click → Inspect
   - Go to Network tab

2. **Navigate to Signup Page**
   - Go to http://localhost:5173
   - Click "Sign Up"

3. **Test File Upload**
   - Try to upload a file
   - Check Network tab for API calls
   - Should see 401 Unauthorized responses (expected)

### **Method 2: API Testing with curl**

#### **Test API Health**
```bash
curl http://localhost:8000/api/health/
```

#### **Test KYC Upload Endpoint (Should Fail)**
```bash
curl -X POST http://localhost:8000/api/upload/kyc/upload/ \
  -F "file=@/path/to/test/image.png" \
  -F "document_type=id_front"
```

#### **Test KYC Status Endpoint (Should Fail)**
```bash
curl http://localhost:8000/api/upload/kyc/status/
```

### **Method 3: Database Testing**

#### **Check Database Models**
```bash
docker-compose exec api python manage.py shell -c "
from file_uploads.models import KYCUpload
from accounts.models import User
print('KYCUpload model:', KYCUpload)
print('Document types:', [choice[0] for choice in KYCUpload.DOCUMENT_TYPES])
print('User model has firebase_uid:', hasattr(User, 'firebase_uid'))
"
```

#### **Check Media Directories**
```bash
docker-compose exec api ls -la /app/media/
```

## **🔥 Advanced Testing**

### **Test with Real Firebase Authentication**

1. **Set up Firebase Project**
   - Go to https://console.firebase.google.com
   - Create a new project
   - Enable Authentication
   - Get your Firebase config

2. **Update Firebase Config**
   - Edit `web/src/config/firebase.ts`
   - Add your Firebase config

3. **Test Complete Flow**
   - Register a new user
   - Upload ID documents
   - Check database for records

### **Test File Upload with Mock Authentication**

Create a test script to simulate the complete flow:

```python
import requests
import tempfile
import os

# Create test image
def create_test_image():
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_file.write(png_data)
    temp_file.close()
    return temp_file.name

# Test file upload
test_file = create_test_image()
with open(test_file, 'rb') as f:
    files = {'file': ('test_id.png', f, 'image/png')}
    data = {'document_type': 'id_front'}
    response = requests.post(
        'http://localhost:8000/api/upload/kyc/upload/',
        files=files,
        data=data
    )
    print(f"Upload response: {response.status_code}")
    print(f"Response: {response.text}")

# Clean up
os.unlink(test_file)
```

## **📊 Expected Test Results**

### **✅ What Should Work:**
- API health check returns 200 OK
- KYC endpoints return 401 Unauthorized (correct behavior)
- Frontend loads without errors
- File upload form is present
- Database models are accessible

### **❌ What Should Fail (Expected):**
- File uploads without authentication (401 error)
- KYC status requests without authentication (401 error)
- Registration without proper Firebase token (400/401 error)

## **🐛 Troubleshooting**

### **Common Issues:**

1. **"Connection refused" errors**
   ```bash
   # Check if containers are running
   docker-compose ps
   
   # Restart if needed
   docker-compose restart
   ```

2. **"Authentication required" errors**
   - This is expected behavior
   - You need Firebase authentication to test uploads

3. **File upload not working**
   - Check if media directories exist
   - Verify file permissions
   - Check Docker container logs

### **Check Container Logs:**
```bash
# API logs
docker-compose logs api

# Web logs
docker-compose logs web

# Database logs
docker-compose logs db
```

## **🎯 Success Criteria**

Your local testing is successful if:

1. ✅ **Frontend loads** at http://localhost:5173
2. ✅ **API responds** at http://localhost:8000/api/health/
3. ✅ **KYC endpoints require authentication** (401 errors)
4. ✅ **File upload form is present** in signup page
5. ✅ **Database models work** correctly
6. ✅ **Media directories exist** in container

## **🚀 Next Steps After Local Testing**

1. **Set up Firebase Authentication** for complete testing
2. **Test with real file uploads** using Firebase tokens
3. **Deploy to production** when ready
4. **Configure SSL certificates** for production

## **📞 Need Help?**

If you encounter issues:
1. Check the container logs
2. Verify all services are running
3. Test individual components
4. Check the implementation documentation

The system is designed to be secure by default - authentication errors are expected and correct behavior!
