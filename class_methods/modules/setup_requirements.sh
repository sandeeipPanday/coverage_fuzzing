#!/bin/bash
echo "📦 Installing required Python packages..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install atheris matplotlib rich
echo "✅ Setup complete."
