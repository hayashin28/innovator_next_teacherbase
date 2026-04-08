num = int(input('整数を入力：'))
for i in range(0, num, + 2):
    print(' ' * ((num - i) // 2), end='')
    print('☆' * (i + 1))