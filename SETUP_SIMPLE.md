# 🚀 Simple Setup - One API Key Only!

## What You Need

**Just ONE thing:** OpenAI API key

Get it here: https://platform.openai.com/api-keys

**New accounts get $5 free credit** = ~500 queries for free!

---

## Setup (5 Minutes)

### Step 1: Get OpenAI API Key (2 min)

1. Go to https://platform.openai.com/api-keys
2. Sign up / Log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-...`)

### Step 2: Run Setup (3 min)

```bash
cd "Enterprise SaaS insights/ask-lenny"
bash setup.sh
```

When prompted:
1. Create `.env` file
2. Paste your OpenAI API key
3. Press Y to ingest transcripts

### Step 3: Start Using!

```bash
streamlit run app.py
```

Opens browser at `http://localhost:8501`

---

## What Changed?

**Original version:** 2 API keys (OpenAI + Anthropic)  
**This version:** 1 API key (OpenAI only)

**Uses OpenAI for:**
- ✅ Embeddings (semantic search)
- ✅ GPT-4 (answer synthesis)

**Same features, simpler setup!**

---

## Cost

### One-Time Setup
- Embeddings for 269 episodes: **$0.50**

### Per Query  
- GPT-4 synthesis: **$0.02**

### 100 Queries
- Setup: $0.50
- 100 queries: $2.00
- **Total: $2.50**

**With $5 free credit:** 200+ queries before paying anything!

---

## Next Command

```bash
bash setup.sh
```

That's it! ✅
