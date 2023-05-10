from aiogram.utils import executor
from create_bot import dp
from heandlers import register_handlers_other


async def on_startup(_):
    print('Бот онлайн')


register_handlers_other(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
