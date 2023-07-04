from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_app import keyboards, text, api, functions, async_functions
from bot_app.app import bot, dp


class MedState(StatesGroup):
    start = State()
    distributor = State()
    csv = State()
    upload_csv = State()


# --- Start ---
@dp.message_handler(commands=['start'], state=['*'])
async def start_handler(message: types.Message, state: FSMContext):
    await MedState.start.set()
    async with state.proxy() as data:
        await bot.send_message(
            message.from_user.id,
            f"Привет, я бот парсер медицинских дистрибьютеров! 🤟",
            reply_markup=keyboards.distributor_keyboard(),
        )


@dp.message_handler(lambda message: message.text in functions.all_distributors_name(), state=[MedState.start])
async def distributor_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['distributor'] = {"name": message.text.lower()}
        await MedState.distributor.set()
        await bot.send_message(
            message.from_user.id,
            f"Теперь скачай последний загруженный файл или загрузи новый файл csv дистрибьютера {data['distributor']['name']}.",
            reply_markup=keyboards.csv_keyboard(),
        )


@dp.message_handler(content_types=['text'], state=[MedState.distributor])
async def csv_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # BACK
        await async_functions.back_to_start(message, state)
        if message.text == text.download_csv:
            get_csv_filepath = api.get_csv(data['distributor']['name'])
            with open(get_csv_filepath, "r") as f:
                file = f.read()
                await bot.send_document(
                    message.from_user.id,
                    (get_csv_filepath, file),
                )
            await bot.send_message(
                message.from_user.id,
                "Все я пошел чилить.",
                reply_markup=keyboards.csv_keyboard(),
            )
        if message.text == text.upload_csv:
            await MedState.csv.set()
            await bot.send_message(
                message.from_user.id,
                f"Загрузи файл csv 📎 {data['distributor']['name']} и смотри, чтобы все поля были правильные и "
                f"разделитель был ; я не хочу твои ошибки искать, мне за это не платят.",
                reply_markup=keyboards.upload_keyboard(),
            )


@dp.message_handler(
    content_types=['document', 'text'],
    state=[MedState.csv],
)
async def upload_csv_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # BACK
        await async_functions.back_to_distributor(message, state)
        if message.document:
            # GET FILE
            file_id = message.document.file_id
            file_data = await bot.get_file(file_id)
            file_path = str(file_data['file_path'])
            # SEND API
            upload_csv_api = api.upload_csv(file_path, data['distributor']['name'], message.from_user.id)
            await MedState.distributor.set()
            if upload_csv_api.status_code == 200:
                await bot.send_message(
                    message.from_user.id,
                    f"Ого, ну ты меня и загрузил! Идика, попей чайку тут походу придется рукава засучивать. Закончу напишу.",
                    reply_markup=keyboards.csv_keyboard(),
                )
            elif upload_csv_api.status_code == 400:
                await bot.send_message(
                    message.from_user.id,
                    f"Ты втираешь мне какую то дичь... что я тебе говорил на счет ошибок? Проверь файл и попробуй еще раз",
                    reply_markup=keyboards.csv_keyboard(),
                )
            else:
                await bot.send_message(
                    message.from_user.id,
                    f"Чтото похерилось, ты оплатил за сервак??? или опять разраб рукожоп, сервак уронил.",
                    reply_markup=keyboards.csv_keyboard(),
                )
