from aiogram.types import  (InlineKeyboardMarkup , InlineKeyboardButton, 
                            ReplyKeyboardMarkup,KeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Рулетка")],
    [KeyboardButton(text="Когда дамой")],
    [KeyboardButton(text="Создать мем")],
    [KeyboardButton(text='GPT')]
],
resize_keyboard="True",
input_field_placeholder="Выберите пункт меню:")

setting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1️⃣", callback_data="1")],
    [InlineKeyboardButton(text="2️⃣", callback_data="2")],
    [InlineKeyboardButton(text="3️⃣", callback_data="3")],
    [InlineKeyboardButton(text="4️⃣", callback_data="4")],
    [InlineKeyboardButton(text="5️⃣", callback_data="5")],
    [InlineKeyboardButton(text="6️⃣", callback_data="6")]
])


def get_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Поделиться номером", request_contact=True)]
    ], resize_keyboard=True)

def photo_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="10px")],
        [KeyboardButton(text="20px"), KeyboardButton(text="30px")],
        [KeyboardButton(text="40px"), KeyboardButton(text="50px")],
        [KeyboardButton(text="60px"), KeyboardButton(text="70px")],
        [KeyboardButton(text="80px"), KeyboardButton(text="90px")],
        [KeyboardButton(text="100px"), KeyboardButton(text="110px")],
        [KeyboardButton(text="120px"), KeyboardButton(text="130px")],
        [KeyboardButton(text="140px")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Введите размер шрифта")

def roullete_keyboard(button_list):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=btn, callback_data=btn)]
            for btn in button_list
        ]
    )

def gpt_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="gpt-4o", callback_data="gpt-4o"), InlineKeyboardButton(text="gpt-4.1", callback_data="gpt-4.1")],
        [InlineKeyboardButton(text="gpt-4.1-mini", callback_data="gpt-4.1-mini"), InlineKeyboardButton(text="o1", callback_data="o1")],
        [InlineKeyboardButton(text="o3", callback_data="o3"), InlineKeyboardButton(text="o4-mini", callback_data="o4-mini")],
        [InlineKeyboardButton(text="o3-mini", callback_data="o3-mini"), InlineKeyboardButton(text="o1-mini", callback_data="o1-mini")]
    ])