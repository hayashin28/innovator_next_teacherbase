import time
def go(num:int):
    for i in range(num):
        if (num - i - 1) == 0:
            print('GO!!')
        else:
            print(num - i - 1)
        time.sleep(1)


go(4)