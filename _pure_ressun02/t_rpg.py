import random
import time

hp = 20

print('ここは一度足を踏み入れたら二度と戻れない森の迷宮')

key:bool = False

while True:
    print(f'現在のHP：{hp}')
    n = random.randint(1, 6)
    input('移動する。: Enter')

    time.sleep(3)

    if n == 1:
        print('薬草を見つけた。HPが3回復した。')
        hp += 3
    elif n == 2:
        print('罠に掛かってしまった！HPが5減ってしまった！')
        hp -= 5
    elif n == 3:
        print('魔物に襲われた！HPが8減ってしまった！')
        hp -= 8
    elif n == 4:
        print('綺麗な泉を発見した。')
        time.sleep(3)
        n = random.randint(1, 6)
        if n / 2 == 1:
            print('体を休めることが出来た。HPが10回復した。')
            hp += 10
        else:
            print('奥から魔物が現れた！HPが8減ってしまった！')
            hp -= 8
    elif n == 5:
            print('特に何もなかった。')
    else:
        if key:
            print('大きな扉がある。鍵を使って扉を開けると見たこともない綺麗な大地が広がっていた。')
            print('～ Fin ～')
            break
        else:
            print('宝箱がある。宝箱から『鍵』を取り出した。')
            key = not key
        
    if hp > 20:
        hp = 20
    elif hp < 0:
        print('力尽きてしまった。')
        break