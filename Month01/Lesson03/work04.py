import random

def count_down():
    num = 5
    for i in range(num):
        print(num - i)
        if num - i == 1:
            return

def chose_code():
    print('赤いコードと青いコードのどちらを切りますか？')
    color = input('red / blue')
    print('チョキン')
    count_down()

    if color == 'red':
        print('大爆発')
    elif color == 'blue':
        print('')
    elif color == 'green':
        print()

    print('---------------別物------------------')

#    if color != 'red':
#        print()
        
        
        
chose_code()
