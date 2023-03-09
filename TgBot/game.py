import random

def win(user_choice):
    bot_choice = random.choice(['камень', 'ножницы', 'бумагу'])
    rules: dict[str, str] = {'камень': 'ножницы', 'ножницы': 'бумагу', 'бумагу': 'камень'}
    if user_choice == bot_choice:
        return ' ничья!\nВ следующий раз кому-нибудь повезет :)'
    elif rules[user_choice] == bot_choice:
        return f' Вы победили!\nМой выбор пал на {bot_choice}.'
    else:
        return f' я победил!\nМой выбор пал на {bot_choice}.'