# Vercel Deployment Guide

## Deployment Readiness Checklist ✓

This project is now ready for Vercel deployment. Here's the complete setup process:

### Prerequisites
- [Vercel Account](https://vercel.com/signup)
- Git repository (GitHub, GitLab, or Bitbucket)
- Google Gemini API Key

### Step 1: Prepare Your API Key

1. Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Copy the `.env.example` file to `.env` locally for testing:
   ```bash
   cp .env.example .env
   ```
3. Add your API key to the `.env` file

### Step 2: Push to Git Repository

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 3: Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
npm install -g vercel
vercel
```

#### Option B: Using Vercel Dashboard
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Select your Git repository
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (leave empty - Python apps don't need building)
   - **Output Directory**: (leave empty)
5. Add Environment Variables:
   - Name: `GEMINI_API_KEY`
   - Value: Your actual API key
6. Click "Deploy"

### Step 4: Verify Deployment

After deployment:
1. Visit your Vercel project URL
2. Test the documentation generation feature
3. Generate a PDF to ensure everything works

## Configuration Details

### Environment Variables
The project requires the following environment variable:
- `GEMINI_API_KEY`: Your Google Gemini API key for LLM-powered documentation generation

### File Structure
- `webapp.py`: Main Flask application
- `vercel.json`: Vercel configuration (pre-configured)
- `requirements.txt`: Python dependencies
- `.env.example`: Template for environment variables
- `templates/`: HTML templates for the web interface
- `output/`: Generated PDFs (stored temporarily)

### Known Limitations

1. **File Storage**: Generated PDFs are stored in `/tmp` which is ephemeral on Vercel
   - Files persist only during the request
   - Download immediately after generation
   
2. **Request Timeout**: Vercel serverless functions have a 25-60 second timeout
   - Large repositories might exceed this
   - Monitor documentation generation time
   
3. **Memory Constraints**: Vercel has memory limits
   - Very large codebases might hit memory limits
   - Consider splitting large projects

## Troubleshooting

### PDF Download Returns 404
- Regenerate the documentation
- Ensure the download happens immediately after generation

### "GEMINI_API_KEY not found" Error
- Verify the environment variable is set in Vercel Dashboard
- Check that the API key is valid and has access to Gemini API

### Timeout Errors
- Reduce file size limits in `repo_parser.py`
- Consider splitting large repositories

### File Permission Errors
- Ensure the app uses `/tmp` for temporary storage
- Check output/ directory permissions

## Performance Optimization Tips

1. **For Large Repositories**:
   - Limit code file size: `code[:6000]` in `webapp.py`
   - Filter file types: only parse essential files
   
2. **API Optimization**:
   - Cache frequently generated documentation
   - Use async processing if possible

## Support & Issues

For issues with:
- **Vercel Deployment**: Check [Vercel Docs](https://vercel.com/docs)
- **Google Gemini API**: See [Google AI Docs](https://ai.google.dev/docs)
- **Flask/Python Runtime**: Check [Vercel Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)

## Security Notes

⚠️ **Important**:
- Never commit `.env` file to repository
- Use Vercel Dashboard to set sensitive environment variables
- Rotate API keys periodically
- Monitor API usage to prevent unexpected charges
