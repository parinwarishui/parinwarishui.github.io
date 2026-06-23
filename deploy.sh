#!/bin/bash
# deploy.sh — freeze Flask app and deploy to GitHub Pages
# Usage: ./deploy.sh             (uses auto-generated commit message)
#        ./deploy.sh "my message" (uses custom commit message)
set -e  # exit immediately on any error
 
BUILD_DIR="build"
DEPLOY_BRANCH="gh-pages"
COMMIT_MSG="${1:-"deploy: $(date '+%Y-%m-%d %H:%M')"}"
 
# Freeze Flask web with freeze.py
echo "==> Freezing Flask app..."
python3 freeze.py
 
# commit source + built output to main
echo "==> Committing to main..."
git add .
if ! git diff --cached --quiet; then
    git commit -m "$COMMIT_MSG"
    git push origin main
else
    echo "    Nothing changed — skipping commit."
fi
 
# push /build/ as root of gh-pages
echo "==> Deploying $BUILD_DIR/ to $DEPLOY_BRANCH..."
git subtree push --prefix "$BUILD_DIR" origin "$DEPLOY_BRANCH"
 
echo ""
echo "==> Done. Live at https://parinwarishui.github.io (may take a few mins to update)"