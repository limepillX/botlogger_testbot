import os

from aiogram import Bot, Dispatcher, executor, types
from botlogger import logger, MessageLogger
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

logger.bot_token = BOT_TOKEN
logger.url = os.getenv('BOTLOGGER_URL')
dp.setup_middleware(MessageLogger())


@dp.message_handler(commands='log')
async def log(message: types.Message):
    text = 'Test log message'
    await logger.send_log(text)
    await message.answer(f'Log message <b>{text}</b> sent was sent to the botlogger server')


@dp.message_handler(commands='error')
async def error(message: types.Message):
    example_error = Exception('Test error message')
    await logger.send_error(example_error)
    await message.answer(f'Error <b>{example_error}</b> sent was sent to the botlogger server')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f'Your message <b>{message.text}</b> was sent to the botlogger server')


async def on_startup(dispatcher):
    await logger.send_log('Bot started')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
