import asyncio

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import func as func
import keyboards as kb
from random import randint


router = Router()


class RouletteState(StatesGroup):
    waiting_for_choice = State()


buttons = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]


vocab = {}

@router.message(F.text.lower() == "рулетка")
async def ruletka(message: Message, state: FSMContext):
    correct_answer = randint(1, 6)
    await message.answer(text="Выбери число",
        reply_markup=kb.roullete_keyboard(buttons))
    await state.update_data(correct_answer=correct_answer, buttons=buttons.copy())
    await state.set_state(RouletteState.waiting_for_choice)
    for index, btn in enumerate(buttons):
        vocab[index + 1] = btn
    

    
@router.callback_query(RouletteState.waiting_for_choice)
async def button_preesed(callback: CallbackQuery, state: FSMContext):
    user_choice = callback.data

    await state.update_data(choice=user_choice)
    data = await state.get_data()

    correct_answer = data["correct_answer"]
    user_buttons = data["buttons"]

    if correct_answer == next(key for key, value in vocab.items() if value == user_choice):
        await callback.message.edit_text("Ты умер, лох")

    else:
        new_buttons = [btn for btn in user_buttons if btn != user_choice]
        if new_buttons != user_buttons:
            await state.update_data(buttons=new_buttons)
            updated_data = await state.get_data()
            print(correct_answer)
            await callback.message.edit_reply_markup(reply_markup=kb.roullete_keyboard(updated_data["buttons"]))
        else:
            await callback.answer("Нажатие не изменило клавиатуру", show_alert=True)

    await callback.answer()