import time

def count_up():
    num = 10
    for i in range(num):
        print(i + 1)
        time.sleep(1)
        
    print('もういいかーい？')


count_up()
# 無限ループ -> while True:
# 一番近いループから抜け出す -> break
# while True:
#   if ????????:
#       break