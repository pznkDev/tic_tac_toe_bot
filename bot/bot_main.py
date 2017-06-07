import random

import telebot
import time

import bot.bot_config as config
import bot.const as const
import bot.ai_algorithm as ai


bot = telebot.TeleBot(config.BOT_TOKEN)

history = {}


def send_msg_type(chat_id):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('vs AI', 'vs human')
    bot.send_message(chat_id, const.msg_choose_type, parse_mode='Markdown', reply_markup=markup_start)


def send_msg_wrong_type(chat_id):
    bot.send_message(chat_id, const.msg_wrong_type, parse_mode='Markdown')


def send_msg_difficulty(chat_id):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row(const.var_game_diff_easy, const.var_game_diff_norm, const.var_game_diff_hard)
    bot.send_message(chat_id, const.msg_choose_difficulty, parse_mode='Markdown', reply_markup=markup_start)


def send_msg_wrong_difficulty(chat_id):
    bot.send_message(chat_id, const.msg_wrong_difficulty, parse_mode='Markdown')


def send_msg_winner(info, winner, chat_id):
    winner_name = 'You'
    if info['start'] == 'ai' and winner == 'X':
        winner_name = 'AI'
    elif info['start'] == 'user' and winner == 'O':
        winner_name = 'AI'
    bot.send_message(chat_id, '*%s*' % winner_name + ' won.', parse_mode='Markdown')


output_field = lambda field: "{0} | {1} | {2}\n{3} | {4} | {5}\n{6} | {7} | {8}".format(*[field[key] for key in sorted(field)])


def send_msg_field(chat_id):
    markup_field = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_field.row('1', '2', '3')
    markup_field.row('4', '5', '6')
    markup_field.row('7', '8', '9')
    bot.send_message(chat_id, output_field(history[str(chat_id)]['field']), reply_markup=markup_field)


def check_victory(f, chat_id):
    for comb in const.victory_combs:
        if (f[comb[0]] == f[comb[1]]) and (f[comb[1]] == f[comb[2]]) and f[comb[0]] != '_':
            return f[comb[0]]


def send_msg_separator(chat_id):
    bot.send_message(chat_id, '--------------------------------------------------------')


def is_free_place(field):
    if len([1 for key in field if field[key] == '_']) > 0:
        return True


def send_msg_draw(chat_id):
    bot.send_message(chat_id, '*Победила дружба!*', parse_mode='Markdown')


def send_msg_busy_cell(chat_id):
    markup_field = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_field.row('1', '2', '3')
    markup_field.row('4', '5', '6')
    markup_field.row('7', '8', '9')
    bot.send_message(chat_id, '*Cell is busy*, try another one', parse_mode='Markdown', reply_markup=markup_field)


def bot_start():
    print('bot is activated')

    @bot.message_handler(commands=['start'])
    def handle_command(message):
        history[str(message.chat.id)] = {'state': const.state_choose_type}
        send_msg_type(message.chat.id)

    @bot.message_handler(commands=['help'])
    def handle_command(message):
        bot.send_message(message.chat.id, const.msg_help, parse_mode='Markdown')

    @bot.message_handler(content_types=['text'])
    def handle_command(message):
        if str(message.chat.id) in history:
            cur_state = history[str(message.chat.id)]['state']
            print('cur_state:::', cur_state)

            if cur_state == const.state_choose_type:
                if message.text == const.var_vs_ai:
                    history[str(message.chat.id)]['enemy'] = 'ai'
                    history[str(message.chat.id)]['state'] = const.state_choose_difficulty
                    send_msg_difficulty(message.chat.id)

                elif message.text == const.var_vs_human:
                    history[str(message.chat.id)]['enemy'] = 'human'
                    bot.send_message(message.chat.id, const.msg_warning_multiple, parse_mode='Markdown')
                    bot.send_message(message.chat.id, const.msg_try_again, parse_mode='Markdown')

                else:
                    send_msg_wrong_type(message.chat.id)
                    print('type incorrect')

            elif cur_state == const.state_choose_difficulty:
                if message.text == const.var_game_diff_easy or message.text == const.var_game_diff_norm or message.text == const.var_game_diff_hard:
                    history[str(message.chat.id)]['diff'] = message.text
                    history[str(message.chat.id)]['state'] = const.state_playing
                    history[str(message.chat.id)]['field'] = {'1': '_', '2': '_', '3': '_',
                                                              '4': '_', '5': '_', '6': '_',
                                                              '7': '_', '8': '_', '9': '_'}

                    # choose who starts with random
                    if bool(random.getrandbits(1)):
                        # bot starts
                        bot.send_message(message.chat.id, 'First - bot')
                        send_msg_separator(message.chat.id)

                        first_pos = 5 if history[str(message.chat.id)]['diff'] == const.var_game_diff_hard else random.randint(1, 9)

                        history[str(message.chat.id)]['field'][str(first_pos)] = 'X'
                        history[str(message.chat.id)]['step'] = 1
                        history[str(message.chat.id)]['start'] = 'ai'

                    else:
                        # user starts
                        bot.send_message(message.chat.id, 'First - you')
                        send_msg_separator(message.chat.id)

                        history[str(message.chat.id)]['start'] = 'user'
                        history[str(message.chat.id)]['step'] = 0

                    send_msg_field(message.chat.id)
                    send_msg_separator(message.chat.id)
                else:
                    send_msg_wrong_difficulty(message.chat.id)
                    print('incorrect difficulty')

            elif cur_state == const.state_playing:
                if message.text in const.field_all:
                    if history[str(message.chat.id)]['field'][message.text] == '_':
                        history[str(message.chat.id)]['field'][message.text] = 'X' if history[str(message.chat.id)]['start'] == 'user' else 'O'
                        history[str(message.chat.id)]['step'] += 1

                        send_msg_field(message.chat.id)
                        send_msg_separator(message.chat.id)
                        time.sleep(1)

                        winner = check_victory(history[str(message.chat.id)]['field'], message.chat.id)
                        is_free = is_free_place(history[str(message.chat.id)]['field'])
                        if winner:
                            send_msg_winner(history[str(message.chat.id)], winner, message.chat.id)
                            bot.send_message(message.chat.id, const.msg_try_again)
                            history[str(message.chat.id)]['state'] = const.state_start

                        elif not is_free:
                            send_msg_draw(message.chat.id)
                            bot.send_message(message.chat.id, const.msg_try_again)
                            history[str(message.chat.id)]['state'] = const.state_start

                        else:
                            move = ai.next_step(history[str(message.chat.id)])
                            history[str(message.chat.id)]['step'] += 1
                            history[str(message.chat.id)]['field'][move] = 'X' if history[str(message.chat.id)]['start'] == 'ai' else 'O'

                            winner = check_victory(history[str(message.chat.id)]['field'], message.chat.id)
                            is_free = is_free_place(history[str(message.chat.id)]['field'])

                            send_msg_field(message.chat.id)
                            send_msg_separator(message.chat.id)

                            if winner:
                                send_msg_winner(history[str(message.chat.id)], winner, message.chat.id)
                                bot.send_message(message.chat.id, const.msg_try_again)
                                history[str(message.chat.id)]['state'] = const.state_start

                            elif not is_free:
                                send_msg_draw(message.chat.id)
                                bot.send_message(message.chat.id, const.msg_try_again)
                                history[str(message.chat.id)]['state'] = const.state_start
                    else:
                        # cell is not empty
                        send_msg_busy_cell(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'enter /start - to start the game')

    bot.polling(none_stop=True, interval=1)


if __name__ == '__main__':
    bot_start()
