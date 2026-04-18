# GitHub Setup Guide for Railway Deployment

Your project needs to be on GitHub for Railway to deploy automatically. Here's how to set it up:

## Step 1: Initialize Git Locally

Open PowerShell in your project folder and run:

```powershell
cd "c:\Users\HP\Desktop\trident\MY_INVENTORY"
git init
git add .
git commit -m "Initial commit: Inventory management app"
```

**What this does:**
- `git init` - Creates `.git` folder (hidden)
- `git add .` - Stages all files
- `git commit` - Creates first commit

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Sign in (create account if needed)
3. Fill in:
   - **Repository name:** `my-inventory` (or your preferred name)
   - **Description:** `Inventory management app with mobile warehouse access`
   - **Visibility:** Public or Private (your choice)
   - **Add .gitignore:** Already have one ✅
   - **Add LICENSE:** Optional (MIT recommended)
4. Click **"Create repository"**

You'll see commands like:
```
git remote add origin https://github.com/YOUR-USERNAME/my-inventory.git
git branch -M main
git push -u origin main
```

## Step 3: Connect Local to GitHub

Copy the commands from GitHub and run in PowerShell:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/my-inventory.git
git branch -M main
git push -u origin main
```

**Replace:**
- `YOUR-USERNAME` - Your GitHub username
- `my-inventory` - Your repository name

**First time setup?** GitHub may ask you to:
- Sign in via browser (click the link)
- Or use Personal Access Token (generate at github.com/settings/tokens)

## Step 4: Verify on GitHub

1. Go to `https://github.com/YOUR-USERNAME/my-inventory`
2. You should see all your files
3. You're ready for Railway! ✅

---

## Railway Deployment (Now That You Have GitHub)

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Select **"GitHub Repo"**
4. Authorize Railway to access your GitHub
5. Select `my-inventory` repository
6. Click **"Deploy"**
7. Railway will automatically:
   - Build your Docker image
   - Deploy your app
   - Provide you a live URL

---

## Quick Commands Summary

```powershell
# One-time setup
cd "c:\Users\HP\Desktop\trident\MY_INVENTORY"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/my-inventory.git
git branch -M main
git push -u origin main

# After making changes (future)
git add .
git commit -m "Your message"
git push
```

**After first push, Railway will auto-redeploy when you push changes!** 🚀

---

## Troubleshooting

### "fatal: not a git repository"
- Run `git init` first
- Check you're in the right folder

### "fatal: Could not read from remote repository"
- Check GitHub URL is correct
- Verify SSH key or Personal Access Token is set up
- Or use HTTPS URL instead of SSH

### "Everything up-to-date"
- Good! Your changes are already committed
- Now go to Railway and deploy

### Can't sign in to GitHub
- Use email instead of username
- Or generate Personal Access Token: https://github.com/settings/tokens

---

## Next Steps

1. Run the git commands above ✅
2. Create GitHub repository ✅
3. Push to GitHub ✅
4. Deploy with Railway: See `RAILWAY_DEPLOYMENT.md` ✅

**You'll be live on mobile in 30 minutes total!** 🎉
