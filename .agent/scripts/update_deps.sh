#!/bin/bash
# .agent/scripts/update_deps.sh
# Automates dependency freezing for SODA environment.

echo "🧊 Freezing dependencies..."
if [ -d ".agent/venv" ]; then
    source .agent/venv/bin/activate
    pip freeze > requirements.txt
    echo "✅ requirements.txt updated."
    
    # Optional: Generate a lock file if using uv later, but for now pip freeze is the baseline.
    echo "📦 Current packages:"
    tail -n 5 requirements.txt
else
    echo "❌ Virtualenv not found at .agent/venv"
    exit 1
fi
