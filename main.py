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
    await logger.send_log('Test log message')
    await message.answer('Log message sent')


@dp.message_handler(commands='error')
async def error(message: types.Message):
    await logger.send_error(Exception('Test error message'))
    await message.answer('Error message sent')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f'Your message <b>{message.text}</b> was sent to the botlogger server')


async def on_startup(dispatcher):
    await logger.send_log('Bot started')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
