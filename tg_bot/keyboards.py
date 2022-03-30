from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

butt1 = KeyboardButton('Привет! 👋', callback_data='start')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(butt1)

inline_yesno = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Да', callback_data='1')).add(InlineKeyboardButton('Нет', callback_data='0'))
btn_cont = InlineKeyboardButton('Да, хочу', callback_data='compete')
btn_ncont = InlineKeyboardButton('Не хочу', callback_data='finish')
inline_contno = InlineKeyboardMarkup(row_width=2).add(btn_cont).add(btn_ncont)
inline_kb_full = InlineKeyboardMarkup(row_width=2)
inline_kb_full.add(InlineKeyboardButton('Посоревноваться со мной', callback_data='compete'))
inline_btn_2 = InlineKeyboardButton('Проверить мое знание Солженицына', callback_data='guess')
inline_kb_full.add(inline_btn_2)
inline_kb_full.add(InlineKeyboardButton('Об авторе', url='https://en.wikipedia.org/wiki/Aleksandr_Solzhenitsyn'))
