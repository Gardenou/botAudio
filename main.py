import os
import openai
import tempfile
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Carrega variables d'entorn
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def tts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        await update.message.reply_text("Envia'm una frase per convertir-la en àudio.")
        return

    await update.message.reply_text("🎤 Generant l'àudio, espera uns segons...")

    try:
        response = openai.audio.speech.create(
            model="tts-1",
            input=text,
            voice="nova"
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(response.content)
            f.flush()
            audio_path = f.name

        with open(audio_path, "rb") as audio_file:
            await update.message.reply_audio(audio=audio_file)

        os.remove(audio_path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), tts_handler))
    print("✅ Bot en marxa! Esperant missatges...")
    app.run_polling()
