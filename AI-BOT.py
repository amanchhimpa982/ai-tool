import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sarvamai import SarvamAI
import requests

# === Apni Keys Yahan Daal Do ===
SARVAM_API_KEY = "your_sarvam_api_key_here"          # ← Sarvam dashboard se
TELEGRAM_TOKEN = "your_telegram_bot_token_here"      # ← @BotFather se

# Image generation ke liye (optional) - yahan example ke liye ek free/public endpoint ya apna use kar sakte ho
# Agar Grok API hai toh usko bhi add kar sakte ho. Abhi placeholder hai.

client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste! Main Sarvam AI based bot hoon 🇮🇳\n"
        "Koi bhi sawal poochho (Hindi/English me best).\n"
        "Image generate karne ke liye bolo: 'ek sundar Taj Mahal ki image banao'"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("Soch raha hoon...")

    try:
        # Sarvam se Chat Completion
        response = client.chat.completions(
            messages=[{"role": "user", "content": user_text}],
            model="sarvam-105b",        # ya "sarvam-30b" (faster)
            max_tokens=500,
            temperature=0.7
        )
        
        text_reply = response.choices[0].message.content
        await update.message.reply_text(text_reply)

        # Image generation detect karo (simple keyword)
        lower_text = user_text.lower()
        if any(word in lower_text for word in ["image", "photo", "picture", "banao", "generate", "banado", "draw", "imag"]):
            await update.message.reply_text("Image generate kar raha hoon... (thoda time lagega)")

            # Yahan image generation logic daal do
            # Example: Agar tumhare paas Grok ya Replicate API hai toh use karo
            # Abhi placeholder - real mein yeh replace kar dena

            prompt = user_text  # original prompt
            
            # Example with a hypothetical image API (replace with real one)
            # img_url = generate_image_with_external_api(prompt)
            
            # Temporary message
            await update.message.reply_text(f"Image generation abhi Sarvam mein nahi hai. Prompt: {prompt}\nAgar Grok API hai toh usse combine kar sakte hain.")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}\nSarvam key sahi hai? Ya credits khatam hue?")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & \~filters.COMMAND, handle_message))
    
    print("Sarvam AI Bot chal raha hai... /start karo Telegram pe")
    app.run_polling()

if __name__ == "__main__":
    main()