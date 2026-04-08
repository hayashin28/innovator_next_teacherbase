num = int(input('整数を入力：'))
for i in range(num, 0, -1):
    print(' ' * (num - i), end='')
    print('☆' * i)