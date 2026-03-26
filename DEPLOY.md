# Deploy to Railway (Cloud) - Step by Step

This guide will get your Oil Price Game live in 10 minutes so you can share a public link with anyone.

## Prerequisites

You need:
- A GitHub account (free at https://github.com)
- A Railway account (free at https://railway.app)

Both take 2 minutes to create if you don't have them.

---

## Step 1: Initialize Git & Push to GitHub

### 1a. Open PowerShell in your project folder:
```
cd c:\code\Oil_Price_Game
```

### 1b. Initialize git repository:
```
git init
git add .
git commit -m "Initial commit: Oil Price Game"
```

### 1c. Create GitHub repository:
1. Go to https://github.com/new
2. Name it: `Oil_Price_Game`
3. **Do NOT initialize with README** (you already have one)
4. Click "Create repository"
5. Copy the HTTPS URL from the page

### 1d. Add GitHub remote and push:
```
git remote add origin https://github.com/YOUR_USERNAME/Oil_Price_Game.git
git branch -M main
git push -u origin main
```

**Enter your GitHub username and password when prompted.**

✅ Your code is now on GitHub!

---

## Step 2: Deploy to Railway

### 2a. Go to https://railway.app

### 2b. Sign in with GitHub (click "Deploy with GitHub")

### 2c. Click "New Project" → "Deploy from GitHub repo"

### 2d. Select your `Oil_Price_Game` repository

### 2e. Railway will auto-detect it's a Python app and deploy!

⏳ **Wait 2-3 minutes for deployment to complete**

---

## Step 3: Get Your Public Link

Once deployed:
1. Go to your Railway dashboard
2. Click on the "Oil_Price_Game" project
3. Click the **Networking** tab on the left
4. You'll see a public URL like: `https://oil-price-game-production.up.railway.app`

**This is your shareable link!** 🎉

---

## Step 4: Share the Link

Send this link to anyone:
```
https://oil-price-game-production.up.railway.app
```

They can:
- Register with any username/password
- Submit predictions each week
- See the leaderboard in real-time

All data syncs automatically!

---

## Updating the App

After making changes locally:

```
git add .
git commit -m "Your changes"
git push origin main
```

Railway automatically redeploys! The link stays the same, but your changes go live immediately.

---

## Admin Commands

To set the weekly price on your local machine:

```
python admin.py --week 13 --fetch-price
```

Or manually:
```
python admin.py --week 13 --price 75.50
```

This updates the database and results appear on the live app immediately.

---

## Troubleshooting

**Deployment failed?**
- Check Railway dashboard for error logs
- Make sure all files are committed to GitHub

**App crashes on Railway?**
- View logs in Railway dashboard
- Common issue: PORT environment variable (already fixed in this version)

**Data lost?**
- SQLite database persists on Railway
- Check the Railway Storage section

**Need to rollback?**
- Railway keeps deployment history
- Click a previous deployment to revert

---

## Done! 🚀

You now have a live app anyone can access. Share the Railway URL and enjoy!
