# Deploying to Hugging Face Spaces

This guide will help you deploy the AI Document Analysis API to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (sign up at https://huggingface.co)
2. Git installed on your system
3. Hugging Face CLI installed (optional but recommended)

## Step 1: Create a New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose a name (e.g., `doc-analysis-api`)
4. Select "Docker" as the SDK
5. Choose "Public" or "Private" visibility
6. Click "Create Space"

## Step 2: Clone Your Space Repository

```bash
# Generate an access token from https://huggingface.co/settings/tokens
# Make sure it has "write" permissions

git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
```

## Step 3: Copy Project Files

Copy these files from your project to the Space directory:

```bash
# Copy essential files
cp /path/to/project/Dockerfile .
cp /path/to/project/requirements.txt .
cp /path/to/project/.env.example .
cp -r /path/to/project/src .

# Rename README for Hugging Face
cp /path/to/project/README_HF.md README.md
```

## Step 4: Configure Environment Variables

1. Go to your Space settings on Hugging Face
2. Navigate to "Settings" → "Variables and secrets"
3. Add these secrets:
   - `GEMINI_API_KEY`: Your Google Gemini API key (get from https://aistudio.google.com/app/apikey)
   - `API_SECRET_KEY`: sk_track2_987654321 (or your custom key)

## Step 5: Commit and Push

```bash
git add .
git commit -m "Initial deployment of AI Document Analysis API"
git push
```

## Step 6: Wait for Build

Your Space will automatically build and deploy. This may take 5-10 minutes.

Monitor the build logs in your Space's "Logs" tab.

## Step 7: Test Your Deployment

Once deployed, your API will be available at:
```
https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space
```

Test the health endpoint:
```bash
curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/health
```

Access the interactive docs:
```
https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/docs
```

## Important Notes

### Port Configuration
- Hugging Face Spaces require apps to run on port 7860
- The Dockerfile has been configured for this

### File Structure
Your Space should have this structure:
```
your-space/
├── README.md              # Hugging Face Space metadata
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── src/
    ├── main.py           # FastAPI application
    └── extractor.py      # Text extraction logic
```

### Environment Variables
- Never commit your `.env` file with real API keys
- Always use Hugging Face Secrets for sensitive data
- The `.env.example` file is safe to commit

### Tesseract OCR
- Tesseract is installed in the Dockerfile
- No additional configuration needed

### Free Tier Limitations
- Hugging Face Spaces free tier may have:
  - CPU-only instances (no GPU)
  - Sleep after inactivity
  - Limited concurrent requests
- For production use, consider upgrading to a paid tier

## Troubleshooting

### Build Fails
- Check the build logs in the "Logs" tab
- Verify all files are committed
- Ensure Dockerfile syntax is correct

### API Not Responding
- Check if the Space is "Running" (not "Sleeping")
- Verify environment variables are set
- Check application logs for errors

### Tesseract Errors
- Ensure Tesseract is installed in Dockerfile
- Check that image files are properly encoded

### Gemini API Errors
- Verify your API key is valid
- Check if you've exceeded free tier limits
- Ensure the key has proper permissions

## Alternative: Using Hugging Face CLI

Install the CLI:
```bash
curl -LsSf https://hf.co/cli/install.sh | bash
```

Login:
```bash
huggingface-cli login
```

Upload files:
```bash
huggingface-cli upload YOUR_USERNAME/YOUR_SPACE_NAME . --repo-type=space
```

## Updating Your Space

To update your deployed Space:

```bash
# Make changes to your files
git add .
git commit -m "Update: description of changes"
git push
```

The Space will automatically rebuild and redeploy.

## Custom Domain (Optional)

Hugging Face Spaces provides a default URL, but you can:
1. Use a custom domain (Pro feature)
2. Use a reverse proxy
3. Embed the Space in your website

## Support

- Hugging Face Spaces Documentation: https://huggingface.co/docs/hub/spaces
- Docker Spaces Guide: https://huggingface.co/docs/hub/spaces-sdks-docker
- Community Forum: https://discuss.huggingface.co
