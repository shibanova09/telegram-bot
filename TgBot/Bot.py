import forec as f
import buttons as b
import game as g
import cat as c
import film as ff
import asyncio
from aiogram import Bot, Dispatcher, types
from conf_reader import config
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=MemoryStorage())
coun = []
class WaitMovie(StatesGroup):
    waiting_for_year = State()
    waiting_for_country = State()
    waiting_for_genre = State()

async def start(message: types.Message):
    await message.answer(f"Здравствуй, {message.from_user.first_name}!\nПомочь выбрать фильм?\N{winking face}",
                         reply_markup=b.kb_yn)

async def help(msg: types.Message):
    await msg.answer('_Приветствую! 👋_\n'
                     'Я могу помочь Вам выбрать фильм, если Вы не знаете, что хотите посмотреть. Рекомендация фильмов '
                     'будет основана на Ваших предпочтениях. Например, страна происхождения или год выпуска.\n\n'
                     'Также я могу развлечь Вас или сделать что-то полезное: отправить картинку милого котёнка, '
                     'показать прогноз погоды на ближайшие 12 часов или поиграть с Вами в игру.\n\n'
                     '_Список быстрых команд_:\n/help - вывод справки\n/start - начать общение\n/restart - перезапустить бота\n'
                     '/game - сыграть в игру\n/forecast - показать прогноз погоды\n/cat - генератор котика\n',
                     parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'but_weather')
async def location(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Давай определимся с твоим местоположением :)",
                           reply_markup=b.kb_sh_loc)

@dp.callback_query_handler(lambda c: c.data == 'but_no')
async def command_no(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Чем хочешь заняться?', reply_markup=b.kb_gfc)

@dp.callback_query_handler(lambda c: c.data == 'but_film', state='*')
@dp.callback_query_handler(lambda c: c.data == 'but_yes', state='*')
async def command_yes(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, 'Отлично, начнём!\nВыбирай диапазон лет выхода фильма.', reply_markup=b.kb_years)
    await state.set_state(WaitMovie.waiting_for_year.state)

@dp.message_handler(Text({"1950-1958", "1959-1967", "1968-1976", "1977-1985", "1986-1994", "1995-2003", "2004-2012", "2013-2017"}), state='*')
async def film_years(message: types.Message, state: FSMContext):
    await state.update_data(chosen_year=message.text.title())
    await message.answer('Теперь давай определимся со страной происхождения.\nНапиши, в какой стране должен быть снят фильм?', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(WaitMovie.waiting_for_country.state)
    @dp.message_handler(state='*')
    async def film_country(message: types.Message, state: FSMContext):
        await state.update_data(chosen_country=message.text.title())
        await state.set_state(WaitMovie.waiting_for_genre.state)
        await message.answer('Как насчет предпочтительного жанра?', reply_markup=b.kb_genres)

@dp.message_handler(Text({'аниме', 'биография', 'боевик', 'военный', 'детектив', 'детский', 'документальный', 'драма', 'история', 'комедия', 'криминал', 'мелодрама', 'мультфильм', 'мюзикл', 'приключения', 'спорт', 'триллер', 'ужасы', 'фантастика', 'фильм-нуар', 'фэнтези'}), state='*')
async def film_genre(message: types.Message, state: FSMContext):
    await state.update_data(chosen_genre=message.text.lower())
    user_data = await state.get_data()
    await message.answer('Я подобрал фильм для тебя :)', reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f'Название: {ff.fill(user_data["chosen_year"], user_data["chosen_country"], user_data["chosen_genre"])}', reply_markup=b.kb_gffc)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'but_game')
async def game(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Поиграем в "Камень, ножницы, бумага"?\nВыбирай!',
                           reply_markup=b.kb_ssp)

@dp.callback_query_handler(lambda c: c.data == 'бумага')
async def game1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f'Результат:{g.win(user_choice="бумагу")}')
    await bot.send_message(callback_query.from_user.id, 'Чем хочешь заняться?', reply_markup=b.kb_gffc)

@dp.callback_query_handler(lambda c: c.data == 'камень')
async def game2(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f'Результат:{g.win(user_choice="камень")}')
    await bot.send_message(callback_query.from_user.id, 'Чем хочешь заняться?', reply_markup=b.kb_gffc)

@dp.callback_query_handler(lambda c: c.data == 'ножницы')
async def game3(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f'Результат:{g.win(user_choice="ножницы")}')
    await bot.send_message(callback_query.from_user.id, 'Чем хочешь заняться?', reply_markup=b.kb_gffc)

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    await message.answer(f"Погода для региона\N{world map}:\n{f.get_location(lat, lon)}",
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Чем хочешь заняться теперь?', reply_markup=b.kb_gcf)

@dp.callback_query_handler(lambda c: c.data == 'but_cats')
async def command_cats(callback_query: types.CallbackQuery):
    await bot.send_photo(callback_query.from_user.id, photo=c.getcat(coun))
    await bot.send_message(callback_query.from_user.id, 'Глянь, какая милота :3\nЧем хочешь заняться?',
                           reply_markup=b.kb_gffc)

async def main():
    dp.register_message_handler(start, commands={'start', 'restart'})
    dp.register_message_handler(help, commands='help')
    dp.register_message_handler(game, commands='game')
    dp.register_message_handler(command_cats, commands='cat')
    dp.register_message_handler(location, commands='forecast')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
