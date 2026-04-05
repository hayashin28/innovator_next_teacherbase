

# -*- coding: utf-8 -*-
"""
雪の結晶（枝分かれタイプのみ）を 3x4=12個 並べて描画するサンプル
────────────────────────────────────────────
[なぜ]
- 氷の結晶は六方晶（六角格子）が基本 → 6方向に似た枝が伸びるため、タートルでも「同じ枝パターンを6回回す」だけで雪の結晶らしく見せられる。

[前提]
- MicroPython/CPython の turtle 双方で動くよう、未実装関数は try/except で回避。
- 速さ>見た目 を優先した軽量アルゴリズム（再帰の深さは2〜3）を採用。

[入出力]
- 入力：画面の行列数・間隔・枝パラメータ（angle/ratio/depth/size 等）
- 出力：画面に描画（戻り値なし）

[副作用]
- タートルの「現在位置・向き・ペン設定」を変更する（= 典型的な副作用）。描画ユーティリティは「呼び出し前の原点・向き」に極力戻す実装。

[例外]
- 一部環境で `tracer/title/bgcolor/pensize` が未実装の可能性 → その場合は安全に無視。
"""

import turtle as t

# ============= 画面初期化（環境差を丸める） =============
def setup_canvas(bg="skyblue", pencolor="white"):
    """画面の見た目を整える。未実装 API は穏当にスキップする。"""
    scr = t.Screen()
    try:
        scr.title("Snowflakes - Branching only")
        scr.bgcolor(bg)
    except Exception:
        pass

    t.hideturtle()      # タートルカーソルを隠す（描画が見やすい）
    t.speed(0)          # 0=最速（実装により最大値は異なる）
    t.pencolor(pencolor)

    # 高速化：描画更新を一時停止（未実装なら無視）
    try:
        t.tracer(False)
    except Exception:
        pass
    return scr

# ============= 枝（アーム）を1本だけ描く =============
def arm_branch(length, depth, angle=30, ratio=0.6):
    """
    1本の「主枝」上に左右対称の小枝を生やして戻ってくる。
    呼び出し前後で位置・向きが元に戻るよう配慮。

    Parameters
    ----------
    length : float
        主枝の長さ（ピクセル相当）
    depth : int
        枝分かれの再帰深さ（2〜3推奨、3にすると繊細だが重い）
    angle : float
        左右に分かれる小枝の開き角（度数法）
    ratio : float
        次世代の縮小率（0.55〜0.7程度。小さいほど繊細）

    仕組み
    ------
    - 幹の「前半」を進む → 左右に小枝（再帰） → 幹の「後半」を進む → 戻る。
    - depth==0 のときは単純に前進→後退（= 先端だけ表現）。
    """
    if depth == 0:
        t.forward(length)
        t.back(length)
        return

    # 幹の前半：半分だけ進む（途中に小枝を付けてから残り半分）
    t.forward(length * 0.5)

    # 左に小枝
    t.left(angle)
    arm_branch(length * ratio, depth - 1, angle, ratio)

    # 右に小枝（左右対称にするため、左に振った分+同角度で右へ）
    t.right(angle * 2)
    arm_branch(length * ratio, depth - 1, angle, ratio)

    # 向きを元に戻す（左へ angle）
    t.left(angle)

    # 幹の後半：残り半分を進み、根元まで戻る
    t.forward(length * 0.5)
    t.back(length)

# ============= 六方向に同じ枝を配置して「結晶」を作る =============
def draw_branchflake(x, y, size=70, depth=2, angle=30, ratio=0.6, pensize=2):
    """
    中心 (x,y) から上方向（北=90°）を初期向きとして、
    同じ枝（arm_branch）を60°ずつ回転させながら6回描く。

    パラメータ設計の目安
    ------------------
    - size  : 見た目のスケール。60〜80がアイコン向き。
    - depth : 2（軽快）/ 3（繊細だが重い）
    - angle : 24〜36で雰囲気が変わる。数値↑で開いた樹形に。
    - ratio : 0.55〜0.65。小さいほど細かく、全体は短めに。
    - pensize : 線の太さ（= width）。2〜3で十分視認性あり。
    """
    # 開始位置へ移動して北向きにセット
    t.penup()
    t.goto(x, y)
    t.setheading(90)  # 上向き=90°
    t.pendown()

    # ペン太さは環境により pensize()/width() 呼び名が違うため両対応
    try:
        t.pensize(pensize)
    except Exception:
        try:
            t.width(pensize)
        except Exception:
            pass

    # 六花：60°ずつ回して同じ枝を6回
    for _ in range(6):
        arm_branch(size, depth, angle, ratio)
        t.right(60)

# ============= グリッドに12個並べて描く =============
def draw_grid(cols=4, rows=3, gap_x=170, gap_y=140):
    """
    画面中央を原点に、等間隔グリッドで雪の結晶を敷き詰める。

    調整のコツ
    ----------
    - 隙間が詰まりすぎたら gap_x/gap_y を広げる。
    - 重い環境では最下段だけ depth=2 に落とすなど段ごと調整も可。
    """
    startx = -((cols - 1) * gap_x) / 2
    starty =  ((rows - 1) * gap_y) / 2

    # 列ごとに angle を変え、行ごとに ratio を変えるだけで
    # 12個の見た目に程よいバリエーションを作る。
    angle_choices = [24, 28, 32, 36]
    ratio_choices = [0.55, 0.60, 0.65]

    for r in range(rows):
        for c in range(cols):
            x = startx + c * gap_x
            y = starty - r * gap_y

            angle = angle_choices[c % len(angle_choices)]
            ratio = ratio_choices[r % len(ratio_choices)]

            # 下段だけ depth=3（繊細に）、他は depth=2（軽快に）
            depth = 3 if r == rows - 1 else 2
            size  = 58 if depth == 3 else 65
            pens  = 2 + ((r + c) % 2)  # 2 or 3

            draw_branchflake(x, y, size=size, depth=depth,
                            angle=angle, ratio=ratio, pensize=pens)

# ============= エントリポイント =============
def main():
    scr = setup_canvas(bg="white", pencolor="black")
    draw_grid(cols=4, rows=3, gap_x=170, gap_y=140)

    # バッファリングを戻す & 終了待ち（未実装なら無視）
    try:
        t.tracer(True)
    except Exception:
        pass
    try:
        t.done()                # CPython 標準
    except Exception:
        try:
            scr.exitonclick()   # 一部実装
        except Exception:
            pass


if __name__ == "__main__":
    main()
