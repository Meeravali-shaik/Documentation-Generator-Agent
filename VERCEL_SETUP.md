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

## Known Issues & Fixes

### Read-Only File System Error

On Vercel, the file system is read-only except for `/tmp`. This has been fixed in the application:

- **GitHub cloning**: Now uses `/tmp` directory automatically
- **PDF generation**: Now saves to `/tmp` directory automatically
- **No manual fix needed**: The code handles this automatically

If you still see "Read-only file system" errors, make sure you have the latest version of the code deployed.

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

### Issue: "Read-only file system" Error

This is fixed automatically. Make sure:
1. You're running the latest version
2. Redeploy if you just pulled new changes
3. Check Vercel logs for the specific error

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
├── github_loader.py       # GitHub cloning (uses /tmp automatically)
├── templates/
│   └── index.html         # Web interface
├── static/
│   └── favicon.svg        # Favicon
└── [other files...]
```

## How Vercel Compatibility Works

### Temporary File Handling
- Cloned repositories are stored in `/tmp` (automatically)
- Generated PDFs are stored in `/tmp` (automatically)
- Both are cleaned up automatically after a short period

### Important Limitations
- Maximum execution time: 60 seconds per request
- File system is read-only except `/tmp`
- Cold starts may take 1-2 seconds (normal)

## Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| 404 Not Found | Flask entrypoint missing | Ensure `app.py` exists and imports from `webapp.py` |
| Connection error | GEMINI_API_KEY not set | Add to Vercel environment variables and redeploy |
| Generation hangs | API rate limit or timeout | Wait and try with fewer files, check logs |
| Favicon 404s | Favicon not found | Should be fixed, in `/static/favicon.svg` |
| Read-only file system | Old code version | Update code and redeploy |

## Support

If you're still having issues:
1. Check Vercel function logs
2. Visit `/debug` endpoint to see configuration
3. Review this guide's troubleshooting section
4. Make sure all steps in "Quick Setup" are completed in order
5. Try the local testing steps to isolate the issue


