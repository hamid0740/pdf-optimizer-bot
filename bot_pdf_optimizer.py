from dotenv import load_dotenv
load_dotenv()
import os
import requests

# bot_pdf_optimizer.py

import os
import subprocess
from pathlib import Path
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7440716887:AAFMYL_-GFWJLaCp-86iEo-VjchTAH1zFOw"  # Replace with your bot's token

def upload_to_transfersh(file_path):
    with open(file_path, 'rb') as f:
        response = requests.put(f"https://transfer.sh/{os.path.basename(file_path)}", data=f)
        return response.text.strip()

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = await update.message.reply_text("✅ PDF received. Starting compression...")
    await update.message.chat.send_action(action=ChatAction.UPLOAD_DOCUMENT)

    # Download file
    file = await update.message.document.get_file()
    input_path = f"/tmp/{file.file_id}.pdf"
    output_path = input_path.replace(".pdf", "_optimized.pdf")
    await file.download_to_drive(custom_path=input_path)

    try:
        # Compress the PDF using Ghostscript (your method)
        gs_command = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.5",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-dDetectDuplicateImages=true",
            "-dCompressFonts=true",
            f"-sOutputFile={output_path}",
            input_path
        ]
        subprocess.run(gs_command, check=True)

        link = upload_to_transfersh(output_path)
        await update.message.reply_text(f"✅ File compressed. Download here:\n{link}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

    finally:
        # Clean up
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a PDF and I’ll compress it for you.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.add_handler(MessageHandler(filters.COMMAND & filters.TEXT, start))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
