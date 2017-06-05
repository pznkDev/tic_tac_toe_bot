import random

import telebot
import bot.bot_config as config
import bot.const as const


bot = telebot.TeleBot(config.BOT_TOKEN)

history = {}


def send_msg_type(chat_id):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('vs AI', 'vs human')
    bot.send_message(chat_id, const.msg_choose_type, reply_markup=markup_start)


def send_msg_wrong_type(chat_id):
    bot.send_message(chat_id, const.msg_wrong_type)


def send_msg_difficulty(chat_id):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row(const.var_game_diff_easy, const.var_game_diff_norm, const.var_game_diff_hard)
    bot.send_message(chat_id, const.msg_choose_difficulty, reply_markup=markup_start)


def send_msg_wrong_difficulty(chat_id):
    bot.send_message(chat_id, const.msg_wrong_difficulty)


output_field = lambda field: "{0} | {1} | {2}\n{3} | {4} | {5}\n{6} | {7} | {8}".format(*[field[key] for key in sorted(field)])


def send_msg_field(chat_id):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('1', '2', '3')
    markup_start.row('4', '5', '6')
    markup_start.row('7', '8', '9')
    bot.send_message(chat_id, output_field(history[str(chat_id)]['field']), reply_markup=markup_start)


def bot_start():
    print('bot is activated')

    @bot.message_handler(commands=['start'])
    def handle_command(message):
        history[str(message.chat.id)] = {'state': const.state_choose_type}
        send_msg_type(message.chat.id)

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
                    history[str(message.chat.id)]['state'] = const.state_playing

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
                        first_pos = random.randint(1, 9)

                        # add check for difficulty !!!
                        history[str(message.chat.id)]['field'][str(first_pos)] = 'X'
                    else:
                        # user starts
                        bot.send_message(message.chat.id, 'First - you')

                    send_msg_field(message.chat.id)
                else:
                    send_msg_wrong_difficulty(message.chat.id)
                    print('incorrect difficulty')

            elif cur_state == const.state_playing:
                print(message)
            else:
                pass
        else:
            bot.send_message(message.chat.id, 'enter /start - to start the game')

    bot.polling(none_stop=True, interval=0.5)


if __name__ == '__main__':
    bot_start()
