#!/bin/bash

echo "Setting up KYC directories for Fluxor..."

# Create KYC directories
mkdir -p fluxor_api/media/kyc
mkdir -p fluxor_api/media/verification_documents

# Set proper permissions
chmod 755 fluxor_api/media/kyc
chmod 755 fluxor_api/media/verification_documents

# Create .gitkeep files to ensure directories are tracked
touch fluxor_api/media/kyc/.gitkeep
touch fluxor_api/media/verification_documents/.gitkeep

echo "KYC directories created successfully!"
echo "Directory structure:"
echo "  fluxor_api/media/kyc/ - For KYC uploads"
echo "  fluxor_api/media/verification_documents/ - For verification documents"

# Show permissions
echo ""
echo "Directory permissions:"
ls -la fluxor_api/media/
