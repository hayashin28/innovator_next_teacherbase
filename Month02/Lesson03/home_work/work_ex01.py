import time


# お小遣いの残り金額を表す変数。
#
# pocket は「計算に使う金額」なので、2000 という数値で持つ。
# "2000円" のような文字列にしてしまうと、
# あとで商品の金額を引き算できなくなる。
pocket = 2000

# 現在のお小遣いを表示する。
#
# pocket は数値として持ち、
# 表示するときだけ f-string で「円」を付ける。
print(f"お小遣いは{pocket}円です。")


def judge(amount: int) -> bool:
    """
    商品を買えるかどうかを判定する関数。

    amount は、これから買おうとしている商品の合計金額。

    この関数の役割は、
    「お小遣い pocket が amount より少ないかどうか」
    を確認し、買えるか買えないかを True / False で返すこと。

    ここで大切なのは、
    print() でメッセージを出すだけでは、if文の判定には使えないということ。

    if judge(amount):
        return

    のように使いたいなら、
    judge() は True または False を返す必要がある。
    """

    # 関数の外側にある pocket を参照する。
    #
    # 今回は pocket の値を読むだけなので、本来 global は不要。
    # global が必要になるのは、関数の中で pocket を書き換える場合。
    #
    # ただし、教材の流れで global を意識させたい場合は、
    # yakisoba_shop() や omen_shop() の中だけで扱う方がよい。
    if pocket < amount:
        print("お小遣いが足りないよ")

        # 買えない場合は True を返す。
        #
        # ここで True を返すことで、
        # if judge(amount):
        #     return
        # が成立し、購入処理を途中で止められる。
        return True

    # お小遣いが足りている場合は False を返す。
    #
    # False が返ると、
    # if judge(amount):
    #     return
    # は成立しないため、そのまま購入処理へ進む。
    return False


def yakisoba_shop() -> bool:
    """
    焼きそば屋で買い物する関数。

    この関数の役割は、
    ・焼きそばを何人前買うか聞く
    ・合計金額を計算する
    ・お小遣いが足りるか判定する
    ・足りる場合だけ pocket から代金を引く
    こと。

    戻り値として、
    買えた場合は True、
    買えなかった場合は False を返す。

    こうしておくと、関数の外側で
    「買えたときだけ残金を表示する」
    という制御ができる。
    """

    # 関数の外側にある pocket を、この関数の中で変更するための宣言。
    #
    # pocket -= amount のように、外側の pocket を書き換えるため、
    # ここでは global が必要になる。
    global pocket

    # 焼きそば1人前の値段。
    yakisoba_price = 120

    time.sleep(1)

    # 焼きそばを何人前買うか入力してもらう。
    #
    # input() の戻り値は文字列なので、
    # int() で整数に変換してから count に入れる。
    count = int(input("焼きそばは何人前ですか？："))

    # 焼きそばの合計金額。
    #
    # 単価 × 個数 = 合計金額
    #
    # 例：
    # 120円 × 30人前 = 3600円
    amount = yakisoba_price * count

    # お小遣いが足りないか判定する。
    #
    # judge(amount) が True を返した場合、
    # 「買えない」という意味なので、ここで関数を終了する。
    #
    # return False にしておくことで、
    # 関数の外側でも「今回は買えなかった」と分かる。
    if judge(amount):
        return False

    time.sleep(1)

    # お小遣いが足りている場合だけ、購入内容を表示する。
    print(f"焼きそばは{count}人前{amount}円です。")

    # お小遣いから焼きそば代を引く。
    #
    # この行は、買える場合だけ実行される。
    pocket -= amount

    # 買えたことを関数の外側へ伝える。
    return True


def omen_shop() -> bool:
    """
    お面屋で買い物する関数。

    yakisoba_shop() と同じ流れで、
    ・個数を聞く
    ・合計金額を計算する
    ・買えるか判定する
    ・買える場合だけ pocket を減らす
    という処理を行う。

    商品が変わっても同じ型で処理できることを見せるための関数。
    """

    global pocket

    # お面1個の値段。
    omen_price = 100

    time.sleep(1)

    # お面をいくつ買うか入力してもらう。
    count = int(input("お面はいくつですか？："))

    # お面の合計金額。
    amount = omen_price * count

    # お小遣いが足りない場合は、購入処理を中断する。
    if judge(amount):
        return False

    time.sleep(1)

    # お小遣いが足りている場合だけ表示する。
    print(f"お面は{count}個{amount}円です。")

    # お小遣いからお面代を引く。
    #
    # はやしんさまの元コードでは pocket -= omen * count でも正しいが、
    # すでに amount を計算しているので、ここでは amount を使う。
    #
    # 同じ意味の計算を2回書かないことで、
    # 後から値段や計算方法を変えたときの修正漏れを防げる。
    pocket -= amount

    return True


# 焼きそば屋で買い物する。
#
# yakisoba_shop() が True を返した場合だけ、
# 残りのお小遣いを表示する。
#
# もしお小遣いが足りず False が返った場合は、
# 残金表示は行わず、次の屋台へ進む。
if yakisoba_shop():
    print(f"残りのお小遣いは{pocket}円です。")

print()

# お面屋で買い物する。
#
# こちらも、買えた場合だけ残金を表示する。
if omen_shop():
    print(f"残りのお小遣いは{pocket}円です。")