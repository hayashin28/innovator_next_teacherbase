# 関数を作りました。
def work02():
    num = 4
    for i in range(num):
        if num - i - 1 == 0:
            print(str(num) + ' - ' + str(i) + ' - 1 = '  + 'GO!!')
        else:      
            print(str(num) + ' - ' + str(i) + ' - 1 = ' + str(num - i - 1))

# 作った関数は呼び出してあげましょう。
work02()