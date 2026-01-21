# Vibe Coding Learnings: Building "Ask Lenny" RAG System

**Date:** January 20, 2026  
**Project:** RAG-powered chat interface for Lenny's Podcast transcripts  
**Goal:** Understand where AI-assisted rapid development falls short of enterprise requirements

---

## What We Built

A functional RAG (Retrieval Augmented Generation) system that:
- Indexes 303 podcast transcripts (~35MB of content)
- Semantic search using OpenAI embeddings
- GPT-4 synthesis with citations
- Streamlit web interface
- Export to markdown
- Deployed to Railway with auto-scaling

**Total Active Development Time:** ~4-6 hours  
**Lines of Code:** ~800 across 4 Python files  
**Cost:** ~$15 in OpenAI credits + $0/month hosting (free tier)

---

## What "Vibe Coding" Got Right

### ✅ The 80% That Was Fast

1. **Core functionality** - RAG system worked first try with OpenAI + ChromaDB
2. **UI/UX** - Streamlit gave us a beautiful interface in 100 lines of code
3. **Vector database** - ChromaDB "just worked" with zero config
4. **Deployment** - Railway detected everything automatically
5. **AI assistance** - Claude/Cursor wrote 90% of the boilerplate

**This part felt like magic.** From idea to working prototype in hours.

---

## Where Vibe Coding Hit Walls

### ❌ The 20% That Consumed 80% of Time

### 1. **Environment Hell** (2+ hours)
**Problem:** Python virtual environments, dependency conflicts, version mismatches
- `ModuleNotFoundError` after successful `pip install`
- Python 3.9 vs 3.13 mismatch between system and venv
- `tiktoken` requiring Rust compiler
- `label-studio` dependency conflicts

**Learning:** *Dependency management is still manual, brittle, and error-prone. No AI can fix "it works on my machine."*

### 2. **GitHub Large File Limits** (1+ hour)
**Problem:** Pre-computed vector DB was 208MB, GitHub limit is 100MB
- First push failed spectacularly
- Had to restructure deployment strategy mid-stream
- Chose to regenerate DB on Railway instead of Git LFS
- This added 10-15 min to every deployment

**Learning:** *Rapid prototyping ignores production realities like data persistence, storage limits, and deployment architecture.*

### 3. **Path Resolution Issues** (30 minutes)
**Problem:** Transcripts path worked locally but broke on Railway
- `../lennys-podcast-transcripts` → `./transcripts/episodes` → `./transcripts`
- Took 3 iterations to get right
- Only discovered via production logs

**Learning:** *Relative paths, working directories, and environment differences are invisible until deployment. No amount of AI assistance catches these.*

### 4. **Rate Limiting & API Costs** (30 minutes + ongoing risk)
**Problem:** OpenAI rate limits hit during ingestion
- 1M tokens/min limit
- Had to add exponential backoff, retry logic
- Each failed ingestion costs real money
- No easy way to estimate costs upfront

**Learning:** *Third-party API dependencies create unpredictable costs and reliability issues. Enterprise systems need SLAs, not "retry and hope."*

### 5. **Deployment State Management** (45 minutes)
**Problem:** Railway's ephemeral storage + first-run ingestion
- Vector DB doesn't persist across rebuilds on free tier
- `start.sh` logic to detect and regenerate
- 15-minute "cold start" on first deploy
- No clear feedback to user during ingestion

**Learning:** *Stateful applications need real infrastructure. Rapid tools abstract away storage, persistence, and lifecycle management until you hit production.*

---

## The Enterprise Gaps We Experienced First-Hand

### 🚫 What's Missing for Real Use

| **Gap** | **Our Experience** | **Enterprise Need** |
|---------|-------------------|-------------------|
| **Authentication** | Anyone with URL can access | SSO, RBAC, audit logs |
| **Data governance** | Transcripts in public GitHub repo | Data residency, encryption at rest/in transit |
| **Reliability** | API calls fail → manual retry | 99.9% uptime SLA, automatic failover |
| **Observability** | `print()` statements in logs | APM, distributed tracing, alerting |
| **Cost control** | No guardrails on API spending | Budget caps, usage alerts, chargeback |
| **Multi-tenancy** | Single shared vector DB | Isolated data per customer/org |
| **Compliance** | No audit trail | SOC2, GDPR, HIPAA compliance |
| **Support** | No documentation beyond README | Professional services, SLAs, on-call support |
| **Testing** | Manual QA via UI | Unit tests, integration tests, load tests, CI/CD |
| **Versioning** | No API versioning | Backward compatibility, migration paths |

---

## Time Breakdown: Prototype vs. Production

```
Prototype (What We Built):
├─ Core logic: 2 hours        ████████
├─ UI/UX: 1 hour              ████
├─ Deployment: 1 hour         ████
└─ Debugging: 2 hours         ████████
   Total: 6 hours             ████████████████████████

Production-Ready (Estimated):
├─ Core logic: 2 hours        ██
├─ Auth & security: 40 hours  ████████████████████████████████████████
├─ Data governance: 32 hours  ████████████████████████████████
├─ Testing & QA: 48 hours     ████████████████████████████████████████████████
├─ Monitoring: 24 hours       ████████████████████████
├─ Documentation: 16 hours    ████████████████
├─ Compliance: 80 hours       ████████████████████████████████████████████████████████████████████████████████████
└─ Maintenance: ∞             ∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞
   Total: ~240+ hours         (40x the prototype)
```

**The math checks out: Vibe-coding gets you 5% of the way to enterprise-ready.**

---

## Quotable Insights (From Our Own Experience)

> "The vector database worked perfectly... until we tried to put it in git. Then we learned about storage limits, state management, and deployment architectures the hard way."

> "Python dependencies are the new DLL hell. Even with perfect AI-generated code, `ModuleNotFoundError` doesn't care."

> "Railway gave us a URL in 5 minutes. But 'deployed' isn't the same as 'production-ready.' We have no auth, no logging, no SLA, and no idea if it'll work tomorrow."

> "OpenAI's rate limits forced us to add retry logic, exponential backoff, and cost monitoring. Enterprises don't accept 'wait 32 seconds and try again.'"

> "The code was easy. The environment, dependencies, deployment, and state management consumed 70% of our time."

---

## Implications for Adobe CJA Positioning

### What This Exercise Proves

1. **Rapid prototyping is real and impressive**
   - We built a working RAG system in hours
   - Streamlit + OpenAI + Railway = magic demo
   - Perfect for hackathons, MVPs, and internal tools

2. **But the last mile is 80% of the work**
   - Enterprise auth, compliance, SLAs
   - Multi-tenancy, data governance, audit logs
   - Professional services, migration support
   - These aren't features—they're **table stakes**

3. **Vibe-coding reveals the moat**
   - If we could vibe-code CJA in a weekend, Adobe would be in trouble
   - We can't, because CJA's value isn't the features—it's the **infrastructure, trust, and support**
   - Enterprises pay for what breaks at 3am and who they can call

### Positioning Message

**"Anyone can build a demo. Adobe builds systems enterprises trust with their business."**

Show this exercise to prospects:
- "Here's what we vibe-coded in 6 hours"
- "Here's what it's missing to run your business"
- "That gap is where CJA lives"

---

## Recommendations

### For This Project
- ✅ Use as internal demo for VP/SVP conversations
- ✅ Show it running, then walk through the gaps
- ❌ Don't present it as customer-ready
- ❌ Don't claim it's comparable to CJA

### For CJA Positioning
- Lead with "build vs. buy" math: 6 hours → 240+ hours → ongoing maintenance
- Emphasize invisible requirements: compliance, SLAs, multi-tenancy
- Use our war stories: environment hell, rate limits, state management
- Quantify the risk: "What happens when your rapid prototype crashes during earnings week?"

### For Future Vibe-Coding Exercises
- Set time limits (4-6 hours max)
- Document failures as aggressively as successes
- Focus on gaps, not just features
- Use it to articulate value, not replace products

---

## Conclusion

**Vibe-coding is incredible for the first 5%.** We built something genuinely useful in hours.

**But enterprise software is the other 95%.** Auth, compliance, reliability, support, SLAs, maintenance—these aren't sexy, but they're why enterprises pay premium prices.

**The gap between "works on my laptop" and "runs the business" is Adobe's moat.**

This exercise didn't threaten CJA. It validated it.

---

**Next Steps:**
1. Show this to VP/SVP with live demo
2. Use recommended questions to showcase the RAG system
3. Transition to "here's what's missing" conversation
4. Position CJA as the answer to the gaps we experienced

**Files to bring:**
- This document (VIBE-CODING-LEARNINGS.md)
- Original analysis (lenny-transcript-analysis.md)
- Executive brief (executive-brief-vibe-code-vs-cja.md)
- Live Railway URL for demo

---

**Built by:** Cursor (Claude Sonnet 4) + Human  
**Total cost:** ~$15 (OpenAI credits)  
**Total value:** Priceless strategic clarity  
**Enterprise-ready:** Not even close 😄
