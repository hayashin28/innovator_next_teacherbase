total = 0  # 合計金額を入れるための変数。
           # いまはまだ何も買っていないので、0 から始める。


def buy_pork():
    # ここが Work2 のいちばん大事な行。
    #
    # global total と書くことで、
    # 「この関数の中で使う total は、関数の中だけの新しい変数ではなく、
    #  外にある total を使います」
    # と Python に伝えている。
    #
    # Work1 では、これを書かなかったため、
    # 関数の中の total が「関数専用の変数」として扱われてしまい、
    # まだ値が入っていない total を読もうとして
    # UnboundLocalError になった。
    #
    # Work2 では global total を書くことで、
    # 「外にある total を、そのまま更新してよい」
    # という意味になる。
    global total

    # 豚肉の値段を変数 pork に入れる。
    # 今回は 200 円の商品を買う想定。
    pork = 200

    # 豚肉の値段を表示する。
    # f-string を使うことで、変数 pork の中身を
    # 文字列の中にそのまま埋め込める。
    print(f'豚肉{pork}円です')

    # 合計金額 total に、豚肉の値段 pork を足す。
    #
    # ここで大切なのは、
    # global total があるので、この total は
    # 「関数の外にある total」と同じものだということ。
    #
    # つまり、
    # 最初に total = 0
    # そのあと total = total + pork
    # なので、
    # total = 0 + 200
    # となり、合計金額は 200 になる。
    #
    # もし global total がなければ、
    # この total は「関数の中だけの total」と見なされ、
    # Work1 と同じエラーの原因になる。
    total = total + pork


# buy_pork() を実行する。
# これにより、関数の中の処理が順番に動く。
#
# 1. global total を確認する
# 2. pork = 200
# 3. 豚肉200円です と表示する
# 4. total に 200 を足す
buy_pork()

# 最後に、関数の外にある total を表示する。
#
# Work2 では global total を使って、
# 関数の中から外の total を更新している。
# そのため、ここで表示される total は 200 になっている。
#
# もし関数の中で外の total が更新されていなければ、
# ここは 0 のままになる。
print(f'合計{total}円のお買い上げです')