# Cloudflare Pages + Django Backend Setup

This combines Cloudflare Pages (fast static frontend) with Railway/Render (Python backend API).

## Architecture Overview

```
Phone/Browser
    ↓
Cloudflare Pages (Frontend - HTML/CSS/JS)
    ↓
Railway Backend (Django REST API)
    ↓
SQLite/PostgreSQL Database
```

## Part 1: Prepare Django Backend as API

Your Django backend is already ready! It serves API endpoints that the frontend will consume.

### Verify Backend is Running on Railway

1. Complete **RAILWAY_DEPLOYMENT.md** first
2. Your Django app at `https://your-app-xxxx.railway.app` is your backend

### Enable CORS (Cross-Origin Requests)

Since frontend will be on `*.pages.dev` domain and backend on Railway, we need CORS.

1. Install CORS package:
   ```bash
   pip install django-cors-headers
   ```

2. Add to `requirements.txt`

3. Update `myinventory/settings.py`:
   ```python
   INSTALLED_APPS = [
       'corsheaders',  # Add this
       'django.contrib.admin',
       # ... rest of apps
   ]

   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',  # Add this at TOP
       'django.middleware.common.CommonMiddleware',
       # ... rest of middleware
   ]

   CORS_ALLOWED_ORIGINS = [
       "https://*.pages.dev",  # Cloudflare Pages
       "http://localhost:3000",  # Local dev
       "https://your-app-xxxx.railway.app",  # Your backend
   ]
   ```

4. Redeploy to Railway:
   ```bash
   railway up
   ```

## Part 2: Create Frontend for Cloudflare Pages

Since your current app uses Django templates, you have two options:

### Option A: Keep Current Setup (RECOMMENDED FOR NOW)
- **Just use Railway** to host the entire app
- **Skip Cloudflare Pages** - Railway is already fast with CDN
- This is simpler and works perfectly for mobile warehouse access

### Option B: Migrate to Cloudflare Pages (Advanced)
Requires rebuilding UI as static HTML + JavaScript that calls API endpoints.

If you want to pursue Option B, you'd need to:
1. Extract frontend HTML/CSS/JS
2. Convert to static site (Astro, Next.js, or vanilla HTML)
3. Update JavaScript to call API endpoints instead of rendering server-side
4. Deploy to Cloudflare Pages

This is more work but gives you:
- Cloudflare's global CDN
- Automatic HTTPS
- Faster page loads
- Easier caching

## Part 3: Deploy to Cloudflare Pages (If Choosing Option B)

### Create Static Frontend Repo

Create new folder `inventory-frontend`:
```
inventory-frontend/
├── index.html
├── css/
│   └── style.css
├── js/
│   ├── app.js (API calls)
│   └── api.js (API client)
└── pages/
    ├── items.html
    ├── items/
    │   ├── create.html
    │   └── [id].html
```

### Sample Frontend Code

**js/api.js** (API client):
```javascript
const API_URL = 'https://your-app-xxxx.railway.app/api';

export async function getItems() {
  const response = await fetch(`${API_URL}/items/`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  });
  return response.json();
}

export async function createItem(itemData) {
  const response = await fetch(`${API_URL}/items/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify(itemData)
  });
  return response.json();
}
```

### Deploy to Cloudflare Pages

1. Push frontend code to GitHub
2. Go to https://pages.cloudflare.com
3. Select your frontend repository
4. Build command: (none for static HTML)
5. Build output directory: `.` (root)
6. Add environment variable:
   ```
   API_URL=https://your-app-xxxx.railway.app
   ```
7. Click "Save and Deploy"

### Access Your App

- Frontend: `https://your-project.pages.dev`
- Backend: `https://your-app-xxxx.railway.app`
- Mobile: Both URLs work from anywhere!

---

## RECOMMENDED QUICK PATH (START HERE)

For fastest results:

✅ **Step 1:** Deploy to Railway using `RAILWAY_DEPLOYMENT.md`
- Takes 10-15 minutes
- Works on mobile immediately
- No complex frontend setup needed

⏭️ **Step 2 (Later):** Optionally migrate frontend to Cloudflare Pages
- Only if you want additional CDN benefits
- Can be done anytime without affecting backend

---

## Why This Matters for Warehouse

**Current setup (Django on Railway):**
- ✅ Works on phone anywhere
- ✅ Database is always in sync
- ✅ Fast enough for warehouse use
- ⚠️ Slightly slower initial page load

**Future setup (Cloudflare Pages + Railway API):**
- ✅ Works on phone anywhere
- ✅ Database always in sync
- ✅ Lightning-fast page loads via CDN
- ✅ Better offline capabilities possible
- ⚠️ More complex to set up

---

## Troubleshooting

### CORS errors in browser console
- Check `CORS_ALLOWED_ORIGINS` includes Cloudflare Pages domain
- Verify frontend domain matches Railway CORS settings
- Backend must include `Access-Control-Allow-*` headers

### Frontend can't reach API
- Check API URL in frontend JavaScript
- Verify Railway backend is running (check logs)
- Test API directly in browser: `https://your-app-xxxx.railway.app/api/items/`

### Static files (CSS/JS) not loading
- Use absolute URLs in Cloudflare Pages HTML
- Or use relative paths with proper folder structure

---

## Next Steps

1. **Now**: Deploy to Railway (10 min) → See `RAILWAY_DEPLOYMENT.md`
2. **Later (Optional)**: If you want Cloudflare Pages, rebuild frontend

**For immediate mobile warehouse access: Just use Railway!** 🚀
