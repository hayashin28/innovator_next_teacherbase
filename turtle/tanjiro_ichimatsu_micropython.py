# tanjiro_ichimatsu_turtle_step05.py
# Python (CPython) の turtle で「炭治郎柄（市松模様）」を
# 1マスずつ、さらに各マスが中心から四方へ広がり、
# その出現順も「画面中央から外側へ」広がる形で描く版
#
# なぜ:
# Step4 では、各マスそのものは中心から広がるようになったが、
# マス全体の出現順はまだ左上から右下への固定順だった。
# それだと「模様全体が咲く」感じよりも、
# ただ順番に処理している感じが強く残る。
# そこで Step5 では、描画順そのものを
# 「画面中央に近いマスから先に描く」ように変え、
# 全体としても中央から外へ模様が育つ見え方へ寄せる。
#
# 前提:
# - Python 標準の turtle が使えること
# - 背景は黒、描くのは緑マスのみ
# - 各マスの中身は Step4 と同様に、中心から四方へ広がる
# - 今回の主目的は「出現順の中心化」であり、
#   色変化・点滅・輪郭エフェクトはまだ入れない
#
# 入出力:
# - 入力なし
# - turtle ウィンドウ上に、市松模様の緑マスが
#   画面中央から外側へ向かって、1マスずつ広がりながら表示される
#
# 副作用:
# - 描画ウィンドウを開く
# - タイマーで段階描画を進める
#
# 例外:
# - turtle 非対応環境では動かない
# - 同距離のマスどうしは、距離順の次に座標順で決まるため、
#   完全な同心円状にはならないが、十分中央展開に見える

import math
import turtle


# =========================
# 見た目設定
# =========================
# 炭治郎柄らしい黒背景と青緑のマス色。
GREEN = "#0fa37f"
BLACK = "#000000"

# グリッド設定。
ROWS = 8
COLS = 10
SIZE = 36

# 1マスを何段階で育てるか。
GROW_STEPS = 8

# 各段階の待ち時間（ミリ秒）。
STEP_INTERVAL_MS = 25


# =========================
# 画面初期化
# =========================
scr = turtle.Screen()
scr.title("Tanjiro Ichimatsu Pattern - Step05")
scr.bgcolor(BLACK)

t = turtle.Turtle(visible=False)
t.speed(0)
t.pensize(1)
t.penup()

# 自動更新を止め、見せたい瞬間だけ update() する。
turtle.tracer(False)


# =========================
# 補助関数
# =========================
def move(x, y):
    """
    なぜ:
    ペンを汚さず座標移動する責務を独立させ、
    矩形描画側の意図を読みやすくするため。

    入出力:
    - 入力: 移動先座標 (x, y)
    - 出力: なし

    副作用:
    - turtle の現在位置が変わる
    """
    t.penup()
    t.goto(x, y)


def fill_rect_from_topleft(x, y, w, h, color):
    """
    なぜ:
    市松模様の基本単位は正方形だが、
    汎用的な矩形塗り関数として分離しておくと、
    今後の拡張でも責務が明確なまま使い回せるため。

    前提:
    - (x, y) は左上座標
    - 右方向へ w、下方向へ h の矩形を描く

    入出力:
    - 入力: 左上座標、幅、高さ、色
    - 出力: なし

    副作用:
    - 画面に塗り矩形が追加される
    - turtle の向きが変わる
    """
    move(x, y)
    t.setheading(0)
    t.color(color)

    t.begin_fill()
    t.pendown()
    for _ in range(2):
        t.forward(w)
        t.right(90)
        t.forward(h)
        t.right(90)
    t.end_fill()
    t.penup()


def build_green_cells(rows, cols, size):
    """
    なぜ:
    緑マスの配置そのものを先に確定し、
    その後の出現順制御を別責務として扱うため。

    前提:
    - (r + c) % 2 == 0 を緑マスとする
    - 背景黒は Screen 側へ任せる
    - 各マスの基準座標は左上

    入出力:
    - 入力: 行数、列数、1マスサイズ
    - 出力: [(x, y), ...] の緑マス左上座標リスト

    副作用:
    - なし
    """
    width = cols * size
    height = rows * size

    origin_x = -width // 2
    origin_y = height // 2

    cells = []

    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                x = origin_x + c * size
                y = origin_y - r * size
                cells.append((x, y))

    return cells


def sort_cells_from_center(cells, size):
    """
    なぜ:
    Step5 の主目的は「中央から外へ」広がる見え方を作ることにある。
    そのためには、配置済みマスをそのまま描くのではなく、
    画面中心に近い順へ並べ替える必要がある。

    方針:
    - 各マスの左上ではなく「マス中心」を使って距離を測る
    - 画面中心 (0, 0) からの距離が近い順にソートする
    - 同距離時の揺れを抑えるため、補助キーとして y, x も使う

    入出力:
    - 入力: 緑マス左上座標リスト、1マスサイズ
    - 出力: 中央近傍順に並んだ座標リスト

    副作用:
    - なし
    """
    def sort_key(cell):
        x, y = cell

        # 完成マスの中心座標。
        center_x = x + size / 2
        center_y = y - size / 2

        # 原点からの距離を比較基準にする。
        distance = math.hypot(center_x, center_y)

        # 同距離時の順序が毎回ぶれないように補助キーを足す。
        return (distance, center_y, center_x)

    return sorted(cells, key=sort_key)


def draw_growing_square(x, y, size, step_index, total_steps, color):
    """
    なぜ:
    Step4 と同様に、マスが一瞬で現れるのではなく、
    中心から外側へ育つ見え方を作るため。

    方針:
    - 完成マスの中心を基準にする
    - 現在段階に応じた小さい正方形を描く
    - 同色で大きく上書きしながら完成へ近づける

    前提:
    - (x, y) は完成マスの左上
    - step_index は 0 〜 total_steps-1
    - 最終段で size x size の完成形になる

    入出力:
    - 入力: 左上座標、完成サイズ、現在段階、総段数、色
    - 出力: なし

    副作用:
    - 画面に現在段階の小正方形が描かれる
    """
    ratio = (step_index + 1) / total_steps
    current_size = size * ratio

    center_x = x + size / 2
    center_y = y - size / 2

    current_x = center_x - current_size / 2
    current_y = center_y + current_size / 2

    fill_rect_from_topleft(current_x, current_y, current_size, current_size, color)


# =========================
# 描画対象の準備
# =========================
# Step5 の核心は、「どの順でマスを描くか」を変えること。
#
# まずは緑マスを通常配置で作り、
# それを「中央に近い順」に並べ替えてから描画対象にする。
base_cells = build_green_cells(ROWS, COLS, SIZE)
green_cells = sort_cells_from_center(base_cells, SIZE)

# いまどのマスを描いているか。
current_cell_index = 0

# そのマスを何段目まで育てたか。
current_step_index = 0


def draw_next_growth_step():
    """
    なぜ:
    Step4 までは、マスそのものの成長だけを制御していた。
    Step5 ではそれに加えて、
    「次にどのマスを育てるか」も中央近傍順へ変えたいため。

    状態管理:
    - current_cell_index:
        いま描いている緑マス番号
    - current_step_index:
        そのマスを何段目まで育てたか

    入出力:
    - 入力: なし
    - 出力: なし

    副作用:
    - 現在対象マスが1段成長する
    - 画面更新が走る
    - 次回描画がタイマー予約される
    """
    global current_cell_index
    global current_step_index

    # 全マス描き終えたら終了。
    if current_cell_index >= len(green_cells):
        turtle.update()
        return

    x, y = green_cells[current_cell_index]

    draw_growing_square(x, y, SIZE, current_step_index, GROW_STEPS, GREEN)
    turtle.update()

    current_step_index += 1

    # 現在マスが完成したら、次のマスへ移る。
    if current_step_index >= GROW_STEPS:
        current_step_index = 0
        current_cell_index += 1

    scr.ontimer(draw_next_growth_step, STEP_INTERVAL_MS)


# =========================
# 実行開始
# =========================
draw_next_growth_step()
turtle.done()