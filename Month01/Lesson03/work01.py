import time

def count_up():
    num = 10
    for i in range(num):
        print(i + 1)
        time.sleep(1)
        
    print('もういいかーい？')


count_up()
