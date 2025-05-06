#!/bin/bash
echo "Installing Ghostscript and dependencies..."
sudo apt update && sudo apt install -y ghostscript
pip install -r requirements.txt
echo "Running the bot..."
python bot_pdf_optimizer.py
