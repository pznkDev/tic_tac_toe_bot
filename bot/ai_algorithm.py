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

        victory_move = predict_victory(field, ai_symb)
        if victory_move:
            return victory_move

        avoid_loss_move = predict_victory(field, 'O' if start == 'ai' else 'X')
        if avoid_loss_move:
            return avoid_loss_move

        if start == 'ai':
            if step == 2:
                enemy_move = [key for key in field if field[key] == 'O'][0]

                if enemy_move in const.field_middle_el:
                    if enemy_move in ['2', '8']:
                        move = str(int(enemy_move) - 1)
                    else:
                        move = str(int(enemy_move) + 3)
                else:
                    free_pos_list = [str(i) for i in range(1, 10)]

                    free_pos_list.remove('5')
                    if enemy_move == '1':
                        free_pos_list.remove('9')
                    elif enemy_move == '3':
                        free_pos_list.remove('7')
                    elif enemy_move == '7':
                        free_pos_list.remove('3')
                    elif enemy_move == '9':
                        free_pos_list.remove('1')

                    move = random.choice(free_pos_list)

            elif step == 4:
                # find triangle
                for comb in const.field_triangle_combs:
                    row_symbs = [field[i] for i in comb[:-1]]

                    if row_symbs.count('X') == 2 and row_symbs.count('_') == 1 and field[comb[3]] != 'O':
                        return comb[row_symbs.index('_')]

                free_pos_list = [key for key in field if field[key] == '_']
                move = random.choice(free_pos_list)

            else:
                free_pos_list = [key for key in field if field[key] == '_']
                move = random.choice(free_pos_list)
        else:
            # if user first
            if step == 1:
                if field['5'] == '_':
                    return '5'
                else:
                    return random.choice(const.field_corner_el)
            else:
                free_pos_list = [key for key in field if field[key] == '_']
                move = random.choice(free_pos_list)

    return move
