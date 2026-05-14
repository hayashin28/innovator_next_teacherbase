import random



print("ここは一度足を踏み入れたら戻れない森の迷宮....")
hp = 20
key = False

while True: # 無限ループ
    input("移動する：Enter")
    num = random.randint(1, 6)
    
    if num == 1:
        print("何事もなかった。")
    elif num == 2:
        print("罠にハマってしまった！")
        hp -= 5
    elif num == 3:
        print("草を拾ったったｗｗｗｗｗｗｗ。")
        num = random.randint(1, 6)
        if num % 2 == 1:
            print("薬草だった！")            
            hp += 4
        else:
            print("Vipperが現れた。大草原ｗｗｗ")
            hp -= 1
    elif num == 4:
        print("モンスターに襲われた！")
        hp -= 10
    elif num == 5:
        print("綺麗な泉を発見した。")
        num = random.randint(1, 6)

        if num % 2 == 0:
            print("泉で休憩をした。")
            hp += 9
        else:
            print("モンスターに襲われた！")
            hp -= 10
    else:
        if key == True:
            print("鍵で扉を開いた。")
            print("新しい大地を発見した！")
            print("～ Fin ～")
            break
        else:
            print("宝箱がある。")
            print("中から鍵を拾った")
            key = True
    
    
    # HPが上限を超えないように調整
    if hp > 20: hp = 20
    
    print(f"現在のHP：{hp}")
    
    if hp <= 0:
        print("淫夢神父：おおGの者よコ↑コ↓で力尽きるとはなさけない。")
        print("ギャル尼僧：マジウケる。大草原不可避なんですけど！。")
        print("碇神父：行かないなら帰りなさい。")
        print("やきう民：行くんゴ！")
        hp = 20
        key = False