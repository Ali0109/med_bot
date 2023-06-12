from aiogram import Bot, Dispatcher
from settings import API_KEY
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=API_KEY, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

