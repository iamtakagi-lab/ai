import numpy as np
import parse

def dice(dice_size):
    num = np.random.randint(1, int(dice_size))
    return num

def simple_dice(dice_size, dice_num):
    if (dice_size.isnumeric() and dice_num.isnumeric()):
        dice_size = int(dice_size)
        dice_num = int(dice_num)
        dice_val = np.array([], dtype=np.int64)
        for i in range(dice_num):
            dice_val = np.append(dice_val, dice(dice_size))

        if len(str(np.sum(dice_val))) > 100:
            msg = '🎲: ' + str(dice_val)
        else:
            msg = '🎲: ' + str(np.sum(dice_val)) + ' = ' + str(dice_val)
    else:
        msg = '🎲: オプションが不正です。'
    return msg

def get_dice(text):
    parsed = parse.parse('@{} {}d{}', text)
    if parsed is None:
        parsed = parse.parse('@{} {}D{}', text)

    reply_msg = simple_dice(parsed[2], parsed[1])

    return reply_msg
