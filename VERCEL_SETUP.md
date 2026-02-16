# Vercel Deployment Instructions

## Quick Setup

1. Go to your Vercel project dashboard: https://vercel.com/dashboard
2. Navigate to **Settings** → **Environment Variables**  
3. Add the following variable:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** Your Google Gemini API key
4. Redeploy or push a new commit to trigger deployment

## Getting Your Gemini API Key

1. Visit https://makersuite.google.com/app/apikey
2. Click **"Create API Key"** (choose existing project or create new)
3. Copy the generated key
4. Paste it in Vercel's Environment Variables

**IMPORTANT:** The API key must be set BEFORE deployment, or the app will show "Connection error".

## Deployment Steps

1. **Push Code to GitHub**
   ```bash
   git push origin main
   ```

2. **Verify Vercel Deployment**
   - Vercel automatically deploys when you push
   - Check your Vercel dashboard for build status
   - Wait for the build to complete (usually 2-3 minutes)

3. **Set Environment Variable on Vercel**
   - Go to **Project Settings** → **Environment Variables**
   - Add `GEMINI_API_KEY`
   - Click **Save**
   - **Redeploy** (click the latest deployment → **Redeploy**)

## Testing Your Deployment

1. Open your Vercel app URL (e.g., `https://documentation-generator-xxxx.vercel.app`)
2. You should see the Documentation Generator interface
3. Try entering a GitHub repo URL or local folder path
4. Click **Generate Documentation**

### Debug Endpoint
If something isn't working, visit:
```
https://documentation-generator-xxxx.vercel.app/debug
```

This will show you:
- Whether GEMINI_API_KEY is set
- Current Flask environment
- Other configuration info

## Troubleshooting

### Issue: "Connection error. Please try again."

**Solution 1: Check API Key**
- Go to Vercel Dashboard → **Settings** → **Environment Variables**
- Verify `GEMINI_API_KEY` is set
- Make sure the key is correct (copy from https://makersuite.google.com/app/apikey)
- **Redeploy** after adding/changing the variable

**Solution 2: Verify API Key is Valid**
- Your Gemini API key might have expired or been revoked
- Get a fresh key from https://makersuite.google.com/app/apikey
- Update the environment variable in Vercel
- Redeploy

**Solution 3: Check Vercel Logs**
- Go to your Vercel project
- Click on the latest deployment
- Click **View Function Logs** or **Runtime Logs**
- Look for error messages

### Issue: Still Getting Errors After 30 Seconds

1. Check your Gemini API quota hasn't been exceeded
2. Try with a simpler repository first (fewer files)
3. Wait a moment and try again (API might be temporarily overloaded)

## Local Testing Before Deployment

```bash
# 1. Create .env file
cp .env.example .env

# 2. Edit .env and add your real GEMINI_API_KEY
nano .env  # or use your editor

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run locally
python webapp.py

# 5. Open http://localhost:5000
```

## Environment Variables Needed

| Variable | Value | Where to Get |
|----------|-------|--------------|
| `GEMINI_API_KEY` | Your API key | https://makersuite.google.com/app/apikey |

## File Structure for Vercel

```
.
├── app.py                 # Flask entrypoint (required by Vercel)
├── wsgi.py                # WSGI entrypoint (alternative)
├── webapp.py              # Main Flask application
├── requirements.txt       # Python dependencies
├── vercel.json            # Vercel configuration
├── templates/
│   └── index.html         # Web interface
├── static/
│   └── favicon.svg        # Favicon
└── [other files...]
```

## Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| 404 Not Found | Flask entrypoint missing | Ensure `app.py` exists and imports from `webapp.py` |
| Connection error | GEMINI_API_KEY not set | Add to Vercel environment variables and redeploy |
| Generation hangs | API rate limit | Wait and try with fewer files |
| Favicon 404s | Static files not served | Should be fixed, favicon is in `/static/favicon.svg` |

## Support

If you're still having issues:
1. Check Vercel function logs
2. Visit `/debug` endpoint to see configuration
3. Review this guide's troubleshooting section
4. Make sure all steps in "Quick Setup" are completed in order

