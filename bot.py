import os
import random
import string
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import json
from dotenv import load_dotenv  

load_dotenv()  

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot=Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
 
users_data = {}

def load_users_data():
    global users_data
    if os.path.exists("users_data.json"):
        with open("users_data.json", "r") as f:
            users_data = json.load(f)
            
def save_users_data():
    global users_data
    with open("users_data.json", "w") as f:
        json.dump(users_data, f)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Assalawma áleykum\\! Botimizģa xosh kelipsiz\\. \n\n>/start \\- Botti iske túsiriw \n>/help \\- Járdem aliw \n>/myphotos \\- Fotolarimdi basqariw \n>/dev \\- Developer", parse_mode="MarkdownV2")
    
@dp.message_handler(commands=['dev'])
async def developers_handler(message: types.Message):
	keyboard = types.InlineKeyboardMarkup()
	button = types.InlineKeyboardButton("Developer", url="https://t.me/tileumuratoviich")
	keyboard.add(button)
	await message.answer(">Bot islew ||200 000UZS|| \n>Bot 1\\-2 hàpte araliģinda tayin boladi \n\nQalģan maģliwmatlar kelisim waqtinda aytiladi, developer menen baylanisiń:", parse_mode="MarkdownV2", reply_markup=keyboard)

@dp.message_handler(commands=['myphotos'])
async def my_photos(message: types.Message):
    user_id = message.from_user.id
    load_users_data()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    save_photos = types.KeyboardButton("Fotolarimdi saqlaw")
    get_photos = types.KeyboardButton("Fotolarimdi aliw")
    markup.add(save_photos, get_photos)
    await message.reply("Fotolarińizdi basqariw ushin tańlań:", reply_markup=markup)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    admin_kb = types.InlineKeyboardMarkup()
    admin_kb.add(types.InlineKeyboardButton("Admin", url="https://t.me/tileumuratoviich"))
    await message.reply("Bottan paydalaniw ushin /myphotos buyriģin jiberiń. \n\nEger sizde basqada mashqalalar bolsa admin menen baylanisiń:", reply_markup=admin_kb)

@dp.message_handler(lambda message: message.text == "Fotolarimdi saqlaw")
async def save_photos(message: types.Message):
    user_id = message.from_user.id
    load_users_data()

    await message.reply("Iltimas, fotolarińizdi jiberiń!")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handler_photos(message: types.Message):
    user_id = message.from_user.id
    load_users_data()

    user_folder = os.path.join("photos", str(user_id))
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    photo_id = message.photo[-1].file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path
    file_name = os.path.join(user_folder, f"{photo_id}.jpg")

    downloaded_file = await bot.download_file(file_path)
    with open(file_name, "wb") as f:
        f.write(downloaded_file.getvalue())

    await message.reply("Foto saqlandi!")

@dp.message_handler(lambda message: message.text == "Fotolarimdi aliw")
async def get_photos(message: types.Message):
    user_id = message.from_user.id
    load_users_data()

    photo_folder = os.path.join(os.getcwd(), 'photos', str(user_id))
    
    if os.path.exists(photo_folder):
        await message.reply("Sizdiń fotońiz jiberilmekte...")

        for photo in os.listdir(photo_folder):
            photo_path = os.path.join(photo_folder, photo)
            if os.path.isfile(photo_path):
                with open(photo_path, "rb") as f:
                    await bot.send_photo(chat_id=message.chat.id, photo=f)
    else:
        await message.reply("Siz ele fotolarińizdi saqlamaģansiz, Iltimas aldin óz fotolarińizdi saqlań.")

if __name__ == '__main__':
    load_users_data()
    executor.start_polling(dp, skip_updates=True)