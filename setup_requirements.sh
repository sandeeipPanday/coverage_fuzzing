#!/bin/bash

echo "📦 Setting up Python dependencies..."

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install core modules
pip install atheris
pip install pytest pytest-html hypothesis
pip install langchain  # Optional: for advanced generative testing or chaining later
pip install psutil      # For performance and memory monitoring
pip install rich        # Optional: for prettier CLI output
pip install tiktoken    # Optional: if you're using LLMs with LangChain
pip install openai      # Optional: if LangChain needs API integration

echo "✅ All dependencies installed."



🧪 To Run It
chmod +x setup_requirements.sh
./setup_requirements.sh


Pro Tip: you can comment out anything you don’t need yet—like the LangChain or OpenAI lines—if you're not diving into that part just yet.

Would you like me to generate a requirements.txt alongside this for CI/CD purposes? Or even bundle a Makefile to run your whole fuzz-report pipeline in one go? I’d be happy to wire it up for smooth automation.
