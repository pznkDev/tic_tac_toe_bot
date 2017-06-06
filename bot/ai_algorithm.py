import random

import bot.const as const


def predict_victory(f, symb):
    for comb in const.victory_combs:
        row_symbs = [f[i] for i in comb]

        if row_symbs.count(symb) == 2 and row_symbs.count('_') == 1:
           return comb[row_symbs.index('_')]


def next_step(info_full):
    print(info_full)

    field = info_full['field']
    difficulty = info_full['diff']
    start = info_full['start']
    step = info_full['step']
    ai_symb = 'X' if start == 'ai' else 'O'

    move = None

    if difficulty == const.var_game_diff_easy:
        free_pos_list = [key for key in field if field[key] == '_']
        move = random.choice(free_pos_list)

    elif difficulty == const.var_game_diff_norm:

        # predict victory of ai
        victory_move = predict_victory(field, ai_symb)
        if victory_move:
            return victory_move

        # avoid loss
        avoid_loss_move = predict_victory(field, 'O' if start == 'ai' else 'X')
        if avoid_loss_move:
            return avoid_loss_move

        free_pos_list = [key for key in field if field[key] == '_']
        move = random.choice(free_pos_list)

    elif difficulty == const.var_game_diff_hard:
        pass

    return move
