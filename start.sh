#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Running the bot..."
python bot_pdf_optimizer.py
