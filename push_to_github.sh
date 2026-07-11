#!/usr/bin/env bash
# One-shot: initialise git and push this repo to GitHub.
# Usage:  ./push_to_github.sh git@github.com:USERNAME/REPO.git
#    or:  ./push_to_github.sh https://github.com/USERNAME/REPO.git
set -euo pipefail
REMOTE="${1:?Pass your repo URL, e.g. git@github.com:you/vaginal-microbiome-classifier.git}"

git init
git checkout -b main 2>/dev/null || git branch -M main
git add -A
git commit -m "Vaginal microbiome instability classifier — Lab Track submission

- Leakage-safe LOSO classifier for next-day CST transition and dysbiosis onset
- Honest negative: composition adds nothing beyond current state; onset unpredictable (memory does not help)
- Novel finding: L. iners marks community mobility, not decline (movement OR 5.87; recovery outruns descent 2.4x)
- Full data, scripts, results, figures, model card, submission writeup, video script"
git remote add origin "$REMOTE"
git push -u origin main
echo "Pushed to $REMOTE"
