#!/bin/bash

# Deployment script for Hugging Face Spaces
# Usage: ./deploy_to_hf.sh YOUR_USERNAME YOUR_SPACE_NAME

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <huggingface_username> <space_name>"
    echo "Example: $0 prem678 doc-analysis-api"
    exit 1
fi

USERNAME=$1
SPACE_NAME=$2
SPACE_URL="https://huggingface.co/spaces/${USERNAME}/${SPACE_NAME}"

echo "========================================="
echo "Deploying to Hugging Face Spaces"
echo "Space: ${USERNAME}/${SPACE_NAME}"
echo "========================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed"
    exit 1
fi

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: ${TEMP_DIR}"

# Clone the Space repository
echo "Cloning Space repository..."
git clone ${SPACE_URL} ${TEMP_DIR}
cd ${TEMP_DIR}

# Copy project files
echo "Copying project files..."
cp ${OLDPWD}/Dockerfile .
cp ${OLDPWD}/requirements.txt .
cp ${OLDPWD}/.env.example .
cp ${OLDPWD}/.gitignore .
cp -r ${OLDPWD}/src .

# Use Hugging Face README
if [ -f "${OLDPWD}/README_HF.md" ]; then
    cp ${OLDPWD}/README_HF.md README.md
    echo "Using Hugging Face README"
fi

# Commit and push
echo "Committing changes..."
git add .
git commit -m "Deploy AI Document Analysis API"

echo "Pushing to Hugging Face..."
git push

echo "========================================="
echo "Deployment complete!"
echo "Your Space will be available at:"
echo "https://${USERNAME}-${SPACE_NAME}.hf.space"
echo ""
echo "Don't forget to set environment variables:"
echo "1. Go to ${SPACE_URL}/settings"
echo "2. Add GEMINI_API_KEY secret"
echo "3. Add API_SECRET_KEY secret"
echo "========================================="

# Cleanup
cd ${OLDPWD}
rm -rf ${TEMP_DIR}
