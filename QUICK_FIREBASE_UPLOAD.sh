#!/bin/bash

# Quick Firebase Upload Script
# Server IP: 31.97.103.64

echo "🔑 Uploading Firebase credentials to server..."

# Upload firebase credentials
scp /Users/mc/trading/fluxor_api/firebase_service_account.json root@31.97.103.64:/root/trading/fluxor_api/

if [ $? -eq 0 ]; then
    echo "✅ Upload successful!"
    echo ""
    echo "Now SSH into server and run:"
    echo "ssh root@31.97.103.64"
    echo "cd /root/trading"
    echo "chmod 600 fluxor_api/firebase_service_account.json"
    echo "docker-compose -f docker-compose.prod.yml restart api"
else
    echo "❌ Upload failed. Please check your password and try again."
fi

