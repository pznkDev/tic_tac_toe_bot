state_start = 'state_start'
state_choose_type = 'state_choose_type'
state_choose_difficulty = 'state_choose_difficulty'
state_playing = 'state_playing'

msg_choose_type = 'Choose your *enemy* !'
msg_wrong_type = '*Wrong type!* Enter /start to try again'
msg_warning_multiple = '*Sorry*, but only _single game_ available :('

msg_choose_difficulty = 'Choose difficulty !'
msg_wrong_difficulty = '*Wrong difficulty!* Enter /start to try again'
msg_try_again = 'Enter /start to try again'

msg_help = '''\r
Hello, this is *tic-tac-toe bot*.\n
This game has two types:
\t - *vs human* (unfortunately unavailable)
\t - *vs ai* (playing against algorithm)\n
Game has 3 *difficulties*:
\t - *easy* (full random)
\t - *normal* (random, but with prediction of win)
\t - *hard* (predicts win combination, avoid losses, builds strategy)\n
Field has next structure:
1 | 2 | 3
4 | 5 | 6
7 | 8 | 9
Just enter code-number of cell to make move.

_PS It's unreal to win in hard level, good luck )_
'''

var_vs_ai = 'vs AI'
var_vs_human = 'vs human'


var_game_diff_easy = 'easy'
var_game_diff_norm = 'normal'
var_game_diff_hard = 'hard'

field_all = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
victory_combs = [['1', '2', '3'],
                 ['4', '5', '6'],
                 ['7', '8', '9'],
                 ['1', '4', '7'],
                 ['2', '5', '8'],
                 ['3', '6', '9'],
                 ['1', '5', '9'],
                 ['3', '5', '7']]
field_middle_el = ['2', '4', '6', '8']
field_corner_el = ['1', '3', '7', '9']

field_triangle_combs = [['1', '5', '3', '2'],
                        ['3', '5', '9', '6'],
                        ['9', '5', '7', '8'],
                        ['1', '5', '7', '4']]
