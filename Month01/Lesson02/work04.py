import time


def traffic_light(): # Script系でよく扱われる→スネーク型
    print('赤です。しばらくお待ちください。')
    
    for i in range(10, 0, -1):
        time.sleep(1)
        print(i)



traffic_light()