from aiogram import Bot, Dispatcher, types, executor
import requests

API_TOKEN = '7604655032:AAEUystQvEyGrL6YuKwj5b_hR_8i_kn9klk'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Valyutalar ro'yxati
CURRENCIES = {
    'USD': 'AQSh dollari',
    'EUR': 'Yevro',
    'RUB': 'Rossiya rubli',
    'GBP': 'Angliya funti',
    'CNY': 'Xitoy yuani'
}

def get_currency_rate(currency_code):
    response = requests.get('https://cbu.uz/oz/arkhiv-kursov-valyut/json/')
    data = response.json()
    for val in data:
        if val['Ccy'] == currency_code:
            return float(val['Rate'])
    return None

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📈 Hozirgi kurs", "💰 So'm kiriting")
    await message.answer("Botga xush kelibsiz! Kerakli bo'limni tanlang:", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "📈 Hozirgi kurs")
async def kurs_handler(message: types.Message):
    text = "💱 Valyuta kurslari (so'mda):\n"
    for code, name in CURRENCIES.items():
        rate = get_currency_rate(code)
        if rate:
            text += f"{name} ({code}): {rate} so'm\n"
    await message.answer(text)

@dp.message_handler(lambda message: message.text == "💰 So'm kiriting")
async def som_handler(message: types.Message):
    await message.answer("Necha so'm kiritmoqchisiz? (Faqat son kiriting)")

@dp.message_handler(lambda message: message.text.isdigit())
async def convert_handler(message: types.Message):
    som = float(message.text)
    text = f"💰 {som} so'm boshqa valyutalarda:\n"
    for code, name in CURRENCIES.items():
        rate = get_currency_rate(code)
        if rate:
            converted = round(som / rate, 2)
            text += f"{name} ({code}): {converted}\n"
    await message.answer(text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)