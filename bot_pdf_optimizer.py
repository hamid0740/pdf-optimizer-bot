from dotenv import load_dotenv
load_dotenv()
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# bot_pdf_optimizer.py

import os
import subprocess
from pathlib import Path
from telegram import Update, ChatAction
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your bot's token

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

        await message.edit_text("✅ Compression complete. Uploading optimized PDF...")
        await update.message.reply_document(document=open(output_path, "rb"), filename="compressed.pdf")

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
