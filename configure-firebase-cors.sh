#!/bin/bash

# Firebase Storage CORS Configuration Script
# This script configures CORS for Firebase Storage to allow requests from fluxor.pro

echo "Configuring Firebase Storage CORS..."

# Check if gsutil is installed
if ! command -v gsutil &> /dev/null; then
    echo "Error: gsutil is not installed. Please install Google Cloud SDK first."
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set the bucket name
BUCKET_NAME="fluxor-434ed.firebasestorage.app"

# Create CORS configuration
cat > cors.json << EOF
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
EOF

# Apply CORS configuration
echo "Applying CORS configuration to Firebase Storage bucket..."
gsutil cors set cors.json gs://$BUCKET_NAME

# Verify CORS configuration
echo "Verifying CORS configuration..."
gsutil cors get gs://$BUCKET_NAME

# Clean up
rm cors.json

echo "Firebase Storage CORS configuration complete!"
echo ""
echo "Next steps:"
echo "1. Update Firebase Storage rules in Firebase Console"
echo "2. Ensure Firebase Authentication is properly configured"
echo "3. Test file uploads from the website"
