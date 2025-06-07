import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import httpx

# 1) Загрузка переменных окружения из файла .env
load_dotenv()
TELEGRAM_TOKEN  = os.getenv("TELEGRAM_TOKEN")
FLOWISE_URL     = os.getenv("FLOWISE_URL", "").rstrip("/")   # например "http://localhost:3000"
FLOWISE_API_KEY = os.getenv("FLOWISE_API_KEY")
CHATFLOW_ID     = os.getenv("CHATFLOW_ID")

# 2) Базовая настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start: приветствует пользователя.
    """
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Отправь мне любой вопрос, и я обращусь к твоим заметкам Obsidian через Flowise. 🙂"
    )

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик текстовых сообщений: пересылает вопрос пользователя в Flowise и отвечает.
    """
    question = update.message.text.strip()
    if not question:
        return

    # Собираем URL для запроса к Flowise Prediction API
    endpoint = f"{FLOWISE_URL}/api/v1/prediction/{CHATFLOW_ID}"
    payload = {"question": question}
    headers = {
        "Content-Type": "application/json",
        "x-api-key": FLOWISE_API_KEY or ""
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(endpoint, json=payload, headers=headers, timeout=30.0)
            resp.raise_for_status()
            data = resp.json()
        # Пытаемся извлечь ответ из возможных форматов JSON
        nested = data.get("data") or {}
        answer = (
            nested.get("text")
            or nested.get("answer")
            or data.get("text")
            or data.get("answer")
            or data.get("response")
        )
        if not answer:
            answer = "❌ Flowise вернул пустой ответ."
    except httpx.HTTPStatusError as hx:
        status = hx.response.status_code
        body = hx.response.text
        logger.error(f"Flowise вернул HTTP {status}: {body}")
        if status == 401:
            answer = "🚨 Ошибка авторизации: проверьте FLOWISE_API_KEY и CHATFLOW_ID."
        else:
            answer = f"🚨 Ошибка Flowise {status}: {body}"
    except Exception as e:
        logger.error(f"Ошибка при обращении к Flowise: {e}")
        answer = "🚨 Не удалось связаться с Flowise. Попробуйте позже."

    # Отправляем ответ пользователю
    await update.message.reply_text(answer)

def main():
    """
    Инициализация и запуск Telegram-бота.
    """
    if not TELEGRAM_TOKEN or not FLOWISE_URL or not CHATFLOW_ID:
        logger.error("Отсутствуют обязательные переменные окружения. Проверьте файл .env.")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))

    logger.info("Бот запущен. Ожидание сообщений...")
    application.run_polling()

if __name__ == "__main__":
    main()