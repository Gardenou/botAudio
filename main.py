import os
import openai
import tempfile
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Carrega les variables d'entorn
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Comanda /lavoz amb frase
async def lavoz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        text = " ".join(context.args)
        await update.message.reply_text("🎧 Generant l'àudio, espera uns segons...")

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
    else:
        await update.message.reply_text("ℹ️ Usa la comanda així:\n`/lavoz Aquesta és la frase que vull escoltar.`", parse_mode="Markdown")

# Arrenca el bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("lavoz", lavoz_command))
    print("✅ Bot en marxa! Esperant missatges...")
    app.run_polling()
