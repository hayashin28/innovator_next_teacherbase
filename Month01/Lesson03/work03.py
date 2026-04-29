import time

def reply() -> str:
    print('もういいかーい？')
    ans = input('yes / no :')
    if ans == 'yes':
        print('もういいよ！')
    elif ans == 'no':
        print('まーだだよ！')
    return ans

def count_up() -> str:
    num = 10
    for i in range(num):
        print(i + 1)
        time.sleep(1)
    return reply()


while True:
    if count_up() == 'yes':
        break