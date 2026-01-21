# ✅ Git Ready! Now Create GitHub Repo & Deploy

Your code is committed and ready to push. Follow these steps:

---

## 🎯 Step 1: Create GitHub Repository

### Option A: Via GitHub Website (Easiest)

1. Go to https://github.com/new

2. Fill in:
   - **Repository name:** `ask-lenny`
   - **Description:** `RAG-powered chat for Lenny's Podcast transcripts`
   - **Visibility:** Public (or Private)
   - **DO NOT** initialize with README (we already have one)

3. Click **"Create repository"**

4. You'll see quick setup commands. Copy the URL (looks like: `https://github.com/YOUR_USERNAME/ask-lenny.git`)

5. Run these commands in your terminal:

```bash
cd "/Users/pawansevak/Enterprise SaaS insights/ask-lenny"

# Add GitHub as remote (use YOUR URL from step 4)
git remote add origin https://github.com/YOUR_USERNAME/ask-lenny.git

# Push to GitHub
git push -u origin main
```

### Option B: Install gh CLI (Alternative)

```bash
# Install GitHub CLI
brew install gh

# Login
gh auth login

# Create repo and push
gh repo create ask-lenny --public --source=. --remote=origin --push
```

---

## 🚀 Step 2: Deploy to Railway

1. Go to https://railway.app

2. Click **"New Project"**

3. Select **"Deploy from GitHub repo"**

4. Authorize Railway to access your GitHub

5. Select **`ask-lenny`** repo

6. Railway auto-detects it's a Python/Streamlit app and starts deploying

7. Click **"Variables"** tab

8. Add environment variable:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** (paste your OpenAI API key)

9. Railway redeploys automatically

10. Click **"Settings"** → **"Generate Domain"** to get your public URL

---

## ✅ Done!

Your app will be live at something like:
```
https://ask-lenny-production.up.railway.app
```

Test it by asking: 
*"What do product leaders say about building for enterprise vs. startups?"*

---

## 🔄 Future Updates

To push updates:

```bash
cd "/Users/pawansevak/Enterprise SaaS insights/ask-lenny"

git add .
git commit -m "Your update description"
git push
```

Railway auto-deploys on every push to `main`!

---

## 💡 Quick Status Check

Run to verify everything:

```bash
cd "/Users/pawansevak/Enterprise SaaS insights/ask-lenny"
git status
git log --oneline -5
```

You should see:
- ✅ On branch main
- ✅ Initial commit created
- ✅ 26 files tracked
