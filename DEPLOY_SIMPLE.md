# Deploy to Railway - Simple Guide

## 3 Steps, 5 Minutes

### 1️⃣ Install Railway CLI

```bash
# Choose one:
npm install -g @railway/cli
# OR
brew install railway
```

### 2️⃣ Deploy

```bash
cd "/Users/pawansevak/Enterprise SaaS insights/ask-lenny"

# Login (opens browser)
railway login

# Deploy
railway init
railway up
```

### 3️⃣ Add API Key

In Railway dashboard (opens automatically):
1. Click "Variables"
2. Add: `OPENAI_API_KEY` = `your_key_here`
3. App auto-redeploys

**Done!** Railway gives you a URL like:
`https://ask-lenny-production.up.railway.app`

---

## 🎯 Using the Automated Script

Or just run:
```bash
./deploy.sh
```

It handles git and Railway deployment automatically!

---

## 💡 Quick Tips

- **Free tier**: $5 credit = ~500 hours runtime
- **Updates**: Just run `railway up` again
- **Logs**: `railway logs` or check dashboard
- **Delete**: `railway down` or delete in dashboard

---

## ⚡ Ultra-Quick Alternative: Deploy via GitHub

1. Push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ask-lenny.git
git push -u origin main
```

2. In Railway:
   - New Project → Deploy from GitHub
   - Select repo
   - Add `OPENAI_API_KEY` variable
   - Done!

---

**Need help?** See `DEPLOY_RAILWAY.md` for detailed guide.
