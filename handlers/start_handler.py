import asyncio



from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup , InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from random import randint
import keyboards as kb
import func as func

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply("Hello",
                        reply_markup=kb.main )

@router.message(F.text.lower() == "когда дамой")
async def cmd_info(message: Message, bot: Bot):
    thinking = await message.answer("Думаю...")
    await asyncio.sleep(2)
    await bot.delete_message(chat_id=message.chat.id, message_id=thinking.message_id)
    if randint(0,1):
        await message.answer("Дамой")
    else:
        await message.answer("Сиди, лошара")

class registration(StatesGroup):
    name = State()
    email = State()
    number = State()

@router.message(Command("reg"))
async def reg_one(message: Message ,state: FSMContext):
    await state.set_state(registration.name)
    await message.answer("Enter your name")

@router.message(registration.name)
async def reg_two(message: Message ,state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(registration.email)
    await message.answer("Enter your email")

@router.message(registration.email)
async def reg_three(message: Message ,state: FSMContext):
    if "@" in message.text:
        await state.update_data(email=message.text)
        await state.set_state(registration.number)
        await message.answer("Enter your phone number",
                         reply_markup=kb.get_keyboard())
    else:
        await message.answer("Введите реальный email")

@router.message(registration.number)
async def reg_end(message: Message ,state: FSMContext):
    await state.update_data(number=registration.number)
    data = await state.get_data()
    await message.answer(f"Спасибо за регистрацию,\nИмя: {data['name']}\nEmail: {data['email']}\nNumber: {data['number']}",
                         reply_markup=None)
    