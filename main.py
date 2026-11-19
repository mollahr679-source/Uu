import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text(
      "বট রেডি! লিখুন:\n/record <stream_url> [seconds]"
  )


async def record(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not context.args:
    await update.message.reply_text("ব্যবহার: /record <stream_url> [seconds]")
    return

  stream_url = context.args[0]
  duration = context.args[1] if len(context.args) > 1 else "20"
  output_file = "clip.mp4"

  await update.message.reply_text(f"{duration} সেকেন্ড রেকর্ড করা হচ্ছে...")

  cmd = [
      "ffmpeg",
      "-y",
      "-i",
      stream_url,
      "-t",
      str(duration),
      "-c",
      "copy",
      output_file,
  ]

  try:
    subprocess.run(cmd, check=True, timeout=120)
    with open(output_file, "rb") as video:
      await update.message.reply_video(video=video)
  except Exception as e:
    await update.message.reply_text(f"সমস্যা হয়েছে: {e}")
  finally:
    if os.path.exists(output_file):
      os.remove(output_file)


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("record", record))
app.run_polling()
