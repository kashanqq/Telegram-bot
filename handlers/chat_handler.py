import os

import openai
from openai import OpenAI
import asyncio

from aiogram import F, Router, Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import keyboards as kb
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import func as func
import httpx
from dotenv import load_dotenv

router = Router()
load_dotenv()

class gpt_inpt(StatesGroup):
    gpt_version = State()

OPENAI_API_KEY = os.getenv('TOKEN_GPT')

client = OpenAI(api_key=OPENAI_API_KEY)


@router.message(F.text.lower() == 'gpt')
async def chat_gpt(message: Message, state: FSMContext):
    await message.answer("Выберите модель", reply_markup=kb.gpt_keyboard())
    await state.set_state(gpt_inpt.gpt_version)

@router.callback_query()
async def user_inpt(callback: CallbackQuery, state: FSMContext):
    gpt_version = callback.data

    await state.update_data(gpt_version_=gpt_version)

    await callback.message.edit_text(text="Введите ваш запрос", reply_markup=None)
    


thinking_tasks = {}

async def animate_thinking(message: Message, task_id: str):
    dots = ["💭 Думаю.", "💭 Думаю..", "💭 Думаю..."]
    i = 0
    while thinking_tasks.get(task_id, True):
        new_text = dots[i % len(dots)]
        if message.text != new_text:
            await message.edit_text(new_text)
        i += 1
        await asyncio.sleep(0.8)

@router.message(F.text)
async def gpt_input(message: Message, state: FSMContext):
    data = await state.get_data()
    user_input = message.text
    gpt_version = data.get("gpt_version_", "gpt-4o")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": f"{gpt_version}",
        "messages": [
            {"role": "system", "content": "Write without *, don't highlight words in bold, instead of — put -"},
            {"role": "user", "content": user_input}
        ]
    }

    thinking_msg = await message.answer("💭 Думаю.")
    task_id = str(message.message_id)


    thinking_tasks[task_id] = True
    animation_task = asyncio.create_task(animate_thinking(thinking_msg, task_id))

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

    except httpx.ReadTimeout:
        content = "❌ Сервер не ответил вовремя."
    except httpx.HTTPStatusError as e:
        content = f"❌ Ошибка: {e.response.status_code}\n{e.response.text}"
    except Exception as e:
        content = f"⚠️ Произошла ошибка: {str(e)}"


    thinking_tasks[task_id] = False
    await animation_task

    if message.text != content:
        await thinking_msg.edit_text(content)
    thinking_msg = {}
    await state.clear()