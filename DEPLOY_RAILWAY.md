# Deploy Ask Lenny to Railway

## 🚀 Quick Deploy (5 minutes)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub (recommended) or email
3. You get **$5 free credit** (no credit card required)

### Step 2: Initialize Git Repo
```bash
cd "/Users/pawansevak/Enterprise SaaS insights/ask-lenny"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Ask Lenny RAG system"
```

### Step 3: Deploy to Railway

**Option A: Deploy via Railway CLI** (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Or with Homebrew
brew install railway

# Login to Railway
railway login

# Create new project and deploy
railway init
railway up
```

**Option B: Deploy via GitHub** (Alternative)

1. Push your code to GitHub:
```bash
# Create new repo on GitHub (https://github.com/new)
# Then:
git remote add origin https://github.com/YOUR_USERNAME/ask-lenny.git
git branch -M main
git push -u origin main
```

2. In Railway dashboard:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `ask-lenny` repo
   - Railway will auto-detect it's a Python/Streamlit app

### Step 4: Set Environment Variables

In Railway dashboard:
1. Go to your project
2. Click "Variables" tab
3. Add variable:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** `your_openai_api_key_here`
4. Click "Deploy" to restart with new env var

### Step 5: Access Your App

Railway will give you a URL like:
```
https://ask-lenny-production.up.railway.app
```

---

## 📊 Important Notes

### ✅ What's Included
- ✅ All transcript data (in `data/vector_db/`)
- ✅ ChromaDB vector database (pre-populated)
- ✅ Streamlit web interface
- ✅ OpenAI integration for synthesis

### ⚠️ Limitations
- **Ephemeral storage**: Railway's free tier has ephemeral storage. Your vector DB is currently ~10MB and will persist, but if you rebuild the app, you may need to re-upload the data folder.
- **Cold starts**: First request after inactivity may take 10-20 seconds
- **Rate limits**: OpenAI free tier limits apply

### 💰 Cost Estimate
- **Railway**: $5 free credit covers ~500 hours of runtime
- **OpenAI**: ~$0.01 per query (embeddings + synthesis)
- **Total**: Effectively free for demos and testing

---

## 🔧 Troubleshooting

### Issue: "Module not found" errors
**Fix:** Railway should auto-detect `requirements.txt`. If not, add a `runtime.txt`:
```
python-3.13
```

### Issue: Vector database not found
**Fix:** Make sure `data/` folder is committed to git:
```bash
git add data/
git commit -m "Add vector database"
git push
```

### Issue: App won't start
**Check Railway logs:**
- Click "Deployments" tab in Railway
- Click latest deployment
- Check logs for error messages

### Issue: OpenAI API errors
**Fix:** Double-check your `OPENAI_API_KEY` in Railway variables

---

## 🎯 Post-Deployment Checklist

- [ ] App accessible at Railway URL
- [ ] Can ask a test question
- [ ] Receives synthesized answer with citations
- [ ] Export to markdown works
- [ ] No errors in Railway logs

---

## 🔄 Updating the App

To deploy updates:

```bash
# Make changes to code
git add .
git commit -m "Your update message"
git push

# Railway auto-deploys on push (if using GitHub)
# Or if using CLI:
railway up
```

---

## 🌐 Custom Domain (Optional)

To use your own domain:
1. In Railway dashboard, go to "Settings"
2. Add custom domain
3. Update DNS records as instructed
4. Railway provides free SSL certificate

---

## 📞 Support

- Railway docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- OpenAI docs: https://platform.openai.com/docs
