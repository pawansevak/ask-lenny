#!/bin/bash

echo "🚀 Ask Lenny - Railway Deployment Helper"
echo "========================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo ""
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "⚠️  Railway CLI not found!"
    echo ""
    echo "Install with:"
    echo "  npm install -g @railway/cli"
    echo "  or"
    echo "  brew install railway"
    echo ""
    exit 1
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit
echo "💾 Creating commit..."
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Update Ask Lenny app"
fi
git commit -m "$commit_msg"

# Deploy to Railway
echo ""
echo "🚢 Deploying to Railway..."
railway up

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Check Railway dashboard for your app URL"
echo "2. Set OPENAI_API_KEY in Railway project variables"
echo "3. Visit your app URL to test"
echo ""
