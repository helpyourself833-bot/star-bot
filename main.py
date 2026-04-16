import os
from aiogram import Bot, Dispatcher, types, executor

TOKEN = os.getenv("TOKEN")
STAR_RATE = 1.4

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

pending = {}

def price(stars):
    return round(stars * STAR_RATE, 2)

@dp.message_handler(commands=['start'])
async def start(m: types.Message):
    await m.answer("👋 Магазин звёзд\nНапиши /shop")

@dp.message_handler(commands=['shop'])
async def shop(m: types.Message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    for s in [50, 100, 250, 500]:
        kb.add(types.InlineKeyboardButton(f"{s} ⭐", callback_data=f"buy_{s}"))
    await m.answer("🛒 Выбери:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("buy_"))
async def buy(c: types.CallbackQuery):
    stars = int(c.data.split("_")[1])
    pending[c.from_user.id] = stars
    await c.message.answer(f"⭐ {stars}\n💰 {stars*1.4}\n\nНапиши /pay")
    await c.answer()

@dp.message_handler(commands=['pay'])
async def pay(m: types.Message):
    if m.from_user.id in pending:
        stars = pending.pop(m.from_user.id)
        await m.answer(f"✅ Оплата прошла\n⭐ +{stars}")
    else:
        await m.answer("❌ Нет заказа")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
