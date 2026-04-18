# Railway Deployment Guide

Railway.app is the easiest way to deploy your Django app with free tier support. Takes ~10 minutes.

## Step 1: Prepare Your Code for Railway

Your project is already configured! Verify these files exist:
- ✅ `requirements.txt` - Dependencies
- ✅ `Dockerfile` - Container config
- ✅ `docker-compose.yml` - Local testing

## Step 2: Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub account (recommended - easier deployment)
3. Verify email

## Step 3: Create New Project

1. Click **"Start a New Project"**
2. Select **"GitHub Repo"** option
3. Authorize Railway to access your GitHub
4. Select your repository
5. Click **"Deploy Now"**

*If using local files (not GitHub):*
1. Click **"Create Project"** → **"Deploy from GitHub"** isn't available
2. Use Railway CLI instead (see Step 7)

## Step 4: Configure Environment Variables

After deployment starts:

1. Go to project settings
2. Click **"Variables"** tab
3. Add these environment variables:

```
DEBUG=False
SECRET_KEY=your-super-secret-key-here-use-random-characters
ALLOWED_HOSTS=your-app-name.railway.app,localhost
DATABASE_URL=(auto-generated if you add PostgreSQL)
```

**To generate SECRET_KEY:**
- Run in Python: `from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())`
- Or use: https://djecrety.ir/

## Step 5: Add PostgreSQL Database (Optional)

For production reliability:

1. In Railway project dashboard, click **"Add Database"**
2. Select **"PostgreSQL"**
3. Wait for database to start (~30 seconds)
4. `DATABASE_URL` will auto-populate in Variables

*Skip this if you want to use SQLite (simpler, but less robust)*

## Step 6: Run Migrations

After deployment completes:

1. Go to **"Deployments"** tab
2. Click the latest deployment
3. Click **"Logs"** to watch progress
4. Once running, click **"Shell"** tab
5. Run in the shell:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

## Step 7: Deploy via CLI (If Not Using GitHub)

If your code is not on GitHub:

### Install Railway CLI
```bash
npm install -g @railway/cli
```
*or* download from https://railway.app/cli

### Deploy
```bash
cd c:\Users\HP\Desktop\trident\MY_INVENTORY
railway login
railway init
railway up
```

### Create .railwayignore (Optional)
Create file in project root:
```
db.sqlite3
*.pyc
__pycache__/
venv/
.venv/
.env
.env.local
```

## Step 8: Access Your App

1. After deployment completes (status = "Success")
2. Click **"View Logs"** in top right
3. Find the URL line showing: `your-app-xxxx.railway.app`
4. Visit: `https://your-app-xxxx.railway.app`
5. Log in with superuser credentials you created

## Step 9: Custom Domain (Optional)

To use your own domain:

1. In Railway project, go to **"Settings"**
2. Find **"Domain"** section
3. Click **"Add Domain"**
4. Enter your domain: `inventory.yourdomain.com`
5. Follow DNS configuration steps
6. Point your domain's DNS to Railway nameservers

## Access from Mobile

Once deployed:
- **Local Network**: `http://your-machine-ip:8000`
- **Mobile via Railway**: `https://your-app-xxxx.railway.app` ✅ Works anywhere!
- **With Custom Domain**: `https://inventory.yourdomain.com` ✅ Professional!

## Troubleshooting

### App crashes after deploy
- Check logs: Click deployment → "Logs" tab
- Common issue: Missing `SECRET_KEY` environment variable
- Solution: Add all variables from Step 4

### Static files not loading (broken CSS/images)
- Run: `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` in settings

### Database locked error
- If using SQLite: Switch to PostgreSQL (Step 5)
- Restart deployment

### Can't connect from mobile
- Check `ALLOWED_HOSTS` includes your Railway domain
- Verify `DEBUG=False` in production
- Check firewall settings

## Monitoring & Maintenance

**View Logs**: Deployments → Latest → Logs tab

**Monitor Resources**: Settings → Metrics tab shows CPU/Memory usage

**Update App**: 
- If on GitHub: Push to `main` branch → Railway auto-redeploys
- If using CLI: Run `railway up` again

**Backup Database**: 
- Railway → Settings → Backups
- PostgreSQL automatically backed up
- Download backup if needed

## Cost (as of April 2026)

Railway free tier includes:
- 5GB egress/month
- $5 credit/month
- Plenty for small warehouse app

Paid plans start at $5/month if you exceed free tier.

## Next Steps: Add Cloudflare Pages Frontend (Optional)

Once backend is running on Railway, you can:
1. Extract frontend assets to separate repo
2. Deploy to Cloudflare Pages
3. Configure API calls to Railway backend

See `CLOUDFLARE_PAGES_SETUP.md` for detailed steps.

---

**Need Help?** 
- Railway Docs: https://docs.railway.app
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
- Community: https://railway.app/community
