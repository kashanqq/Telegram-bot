import os

from aiogram import F, Router, Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import keyboards as kb
from pip import Image, ImageDraw, ImageFont
from io import BytesIO
import func as func


router = Router()

class new_mems(StatesGroup):
    photo_s = State()
    up_text_s = State()
    down_text_s = State()
    size_text_s = State()
    user_id = State()


@router.message(F.text.lower() == "создать мем")
async def new_meme(message: Message):
    await message.answer("Отправте нужное фото")


@router.message(F.photo)
async def add_photo(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(photo=message.text)
    user_photo = message.photo[-1]

    await state.update_data(user_id=message.from_user.id)
    user_id = message.from_user.id
    user_folder = os.path.join("kashtan_bot", str(user_id))

    os.makedirs(user_folder, exist_ok=True)
    
    save_path = f"kashtan_bot/{user_id}/user_photo.jpg"
    
    file = await bot.get_file(user_photo.file_id)
    file_path = file.file_path
    await bot.download_file(file_path, save_path)

    await message.answer('Введите текст сверху(если нету, то поставте "-")')
    await state.set_state(new_mems.up_text_s)

    del_path = f"kashtan_bot/{user_id}"

    await func.delete_file_later(del_path, 60)


@router.message(new_mems.up_text_s)
async def add_up_text(message: Message, state: FSMContext):
    await state.update_data(up_text=message.text)
    await message.answer('Введите нижний текст(если нету, то поставте "-")')
    await state.set_state(new_mems.down_text_s)

@router.message(new_mems.down_text_s)
async def app_down_text(message: Message, state: FSMContext):
    await state.update_data(down_text=message.text)
    await state.set_state(new_mems.size_text_s)
    await message.answer(text='Выберите размер текста', reply_markup=kb.photo_keyboard())

class LimitException(Exception):
    def __init__(self, message, extra_info):
        super().__init__(message)
        self.extra_info = extra_info

@router.message(F.text)
async def custom_size(message: Message, state: FSMContext, bot: Bot):
    try:
        if "px" in message.text:
            size_up_text = int(message.text.replace("px", "", 1))
        else:
            size_up_text = int(message.text)
        if size_up_text > 500:
            raise LimitException("Превышение лимита размера шрифта", "message.text > 500")
    except Exception as e:
        print(e)
        return await message.answer('Это должно быть число до 500 по шаблону "(число)px" или просто число')
    
    data = await state.get_data()
    up_text = data.get('up_text', "Верхний текст")
    down_text = data.get('down_text', "Нижний текст")

    try:
        with Image.open(f"kashtan_bot/{data['user_id']}/user_photo.jpg").convert("RGBA") as base:
            txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
            fnt = ImageFont.truetype('kashtan_bot/Attractive-Heavy.ttf', size_up_text)
            d = ImageDraw.Draw(txt)

            bbox_d = d.textbbox((0, 0), down_text, font=fnt)
            width = bbox_d[2] - bbox_d[0]
            height = bbox_d[3] - bbox_d[1]
            text_x_d = (base.width - width) // 2
            text_y_d = base.height - height - (8 * base.height / 100)

            bbox_up = d.textbbox((0, 0), up_text, font=fnt)
            width_up = bbox_up[2] - bbox_up[0]
            text_x_up = (base.width - width_up) // 2
            text_y_up = int(5 * base.height / 100)

            if up_text != '-':
                d.text((text_x_up, text_y_up), up_text, font=fnt, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
            if down_text != '-':
                d.text((text_x_d, text_y_d), down_text, font=fnt, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))

            out = Image.alpha_composite(base, txt)
            bio = BytesIO()
            out.save(bio, format="PNG")
            bio.seek(0)

            await bot.send_photo(message.chat.id, types.BufferedInputFile(bio.getvalue(), filename="user_photo.jpg"), caption="Вот ваше фото!", reply_markup=kb.main)

            try:
                await func.delete_file_later(f"kashtan_bot/{data['user_id']}", 1)
            except Exception as e:
                await message.answer(f"Ошибка {e}")
            
    except FileNotFoundError:
        await message.answer('Фото отсутствует, введите "Создать мем"', reply_markup=kb.main)
    await state.clear()