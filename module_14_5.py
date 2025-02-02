from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from crud_functions import get_all_products, initiate_db, add_users
import crud_functions


api = "7737775950:AAF7gfk0oxs6D7-Kp01F9TV39vjUIyZuQB8"
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())
initiate_db()
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State(1000)

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    username = message.text
    if crud_functions.is_included(username):  # Проверка, существует ли пользователь
        await message.answer("Пользователь существует, введите другое имя")
        return  # Прерываем выполнение, чтобы не переходить к следующему состоянию
    await state.update_data(username=username)
    await message.answer("Введите свой email:")
    await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)


    # Получаем все данные
    user_data = await state.get_data()
    username = user_data['username']
    email = user_data['email']
    age = user_data['age']

    crud_functions.add_users(username, email, age)
    await state.finish()
#initiate_db()
gap = get_all_products()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

key1 = InlineKeyboardMarkup(resize_keyboard=True)

but1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
but2 = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')

key1.add(but1, but2)

catalog_prod = InlineKeyboardMarkup(row_width=4) # 4 кнопки в ряд
product_buttons = [
    InlineKeyboardButton("Product1", callback_data="product_buying"),
    InlineKeyboardButton("Product2", callback_data="product_buying"),
    InlineKeyboardButton("Product3", callback_data="product_buying"),
    InlineKeyboardButton("Product4", callback_data="product_buying"),
]
catalog_prod.add(*product_buttons)
#catalog_prod.add()
@dp.message_handler(commands=['start'])
async def start(message):
    #стартовое меню клавиатур
    start_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')],
                                               [KeyboardButton(text='Купить')],
                                               [KeyboardButton(text='Регистрация')]], resize_keyboard=True)

    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = start_menu)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=key1)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for prod in gap:
        i, title, description, price = prod[0], prod[1], prod[2], prod[3]

        with open(f'buyc{i}.jpg', 'rb') as image:
            await message.answer_photo(image, f'Название: {title} | Описание: {description} | Цена {price}')


    await message.answer("Выберите продукт для покупки:", reply_markup=catalog_prod)

# Callback хэндлер для кнопок "Product1", "Product2", "Product3", "Product4"

@dp.callback_query_handler(text='product_buying')
async def send_confirm_messages(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text='formulas') #связь с кнопкой but2
async def get_formulas(call):
    await call.message.answer('Норма калорий для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer() # чтобы кнопка не залипла, и стала доступной после нажатия

@dp.callback_query_handler(text='calories') #связь с кнопкой but1
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight) # реагирует на переданное состояние User.State.weight
async def send_calories(message, state):
    await state.update_data(weight=message.text) # обновляет данные в состоянии weight на message.text
    data = await state.get_data() # запоминает все введенные раннее состояния
    await message.answer(f"Ваша норма калорий {10*float(data['weight'])+6.25*float(data['growth'])-5*float(data['age'])+5}")

    await state.finish()
# для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)