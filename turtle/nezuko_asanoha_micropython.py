# nezuko_asanoha_turtle_step04.py
# Python (CPython) の turtle で「ねずこ柄（麻の葉）」を
# 1セルずつ、さらに各線が中心から両側へ伸びて完成する形で描く版
#
# なぜ:
# Step3 では、一本線が始点から終点へ一方向に伸びていた。
# しかし麻の葉模様の印象としては、六角中心から放射状に開く見え方のほうが自然である。
# そこで Step4 では、各線を「中心を起点に左右へ同時に伸ばす」ように変更し、
# 柄が中心から咲くような成立順を見せる。
#
# 前提:
# - Python 標準の turtle が使えること
# - 麻の葉1セルは、六角の向かい合う頂点を結ぶ三本線で表す
# - 各線はセル中心を通るため、中心から両端へ分けて描ける
# - 今回は「中心から伸びる表現」が主目的であり、
#   色変化・完成時エフェクト・全体スライドはまだ入れない
#
# 入出力:
# - 入力なし
# - turtle ウィンドウ上に、麻の葉模様が
#   1セルずつ・1本ずつ・中心から両側へ伸びて表示される
#
# 副作用:
# - 描画ウィンドウを開く
# - タイマーで段階描画を進める
#
# 例外:
# - turtle 非対応環境では動かない
# - 分割数が多いと環境によっては遅く見える

import math
import turtle


# =========================
# 見た目設定
# =========================
# 背景はねずこ柄らしい桃色、線は白で固定する。
PINK = "#f2b4c9"
LINE = "#ffffff"
LINE_WIDTH = 2

# 六角セルの半径。
R = 28

# グリッド数。
COLS = 10
ROWS = 8

# 半分の線を何段階で伸ばすか。
# Step3 と違い、今回は「中心→片端」の半区間を分割する。
HALF_SEGMENT_STEPS = 6

# 1ステップごとの待ち時間（ミリ秒）。
STEP_INTERVAL_MS = 20


# =========================
# 画面初期化
# =========================
scr = turtle.Screen()
scr.title("Nezuko Asanoha Pattern - Step04")
scr.bgcolor(PINK)

t = turtle.Turtle(visible=False)
t.speed(0)
t.pencolor(LINE)
t.pensize(LINE_WIDTH)
t.penup()

# 自前で更新タイミングを制御するため、自動更新を止める。
turtle.tracer(False)


# =========================
# 補助関数
# =========================
def line(x1, y1, x2, y2):
    """
    なぜ:
    一本線を描く最小責務を独立させるため。
    線の進行制御側では「どこからどこまで描くか」に集中し、
    実際のペン操作はこの関数へ閉じ込める。

    入出力:
    - 入力: 始点(x1, y1), 終点(x2, y2)
    - 出力: なし

    副作用:
    - turtle の位置が終点へ移動する
    """
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.goto(x2, y2)
    t.penup()


def interpolate_point(x1, y1, x2, y2, ratio):
    """
    なぜ:
    線を一気に描かず、途中点まで少しずつ伸ばすため。
    直線区間上の任意比率位置を得る。

    前提:
    - ratio は 0.0 〜 1.0 を想定する
    - 0.0 なら始点、1.0 なら終点

    入出力:
    - 入力: 始点・終点・進行率
    - 出力: 途中点 (x, y)

    副作用:
    - なし
    """
    x = x1 + (x2 - x1) * ratio
    y = y1 + (y2 - y1) * ratio
    return x, y


def make_cell_segments(cx, cy, r):
    """
    なぜ:
    セルの幾何形状生成と、描画進行制御を分離するため。
    今回も、まずは「1セルがどの三本線で構成されるか」を返す。

    前提:
    - フラットトップ六角
    - 麻の葉の最小表現は三本の直径
    - どの直径もセル中心(cx, cy)を通る

    入出力:
    - 入力: セル中心(cx, cy), 半径 r
    - 出力: [((x1, y1), (x2, y2)), ...] の三本線リスト

    副作用:
    - なし
    """
    angs = [0, 60, 120, 180, 240, 300]

    verts = [
        (
            cx + r * math.cos(math.radians(a)),
            cy + r * math.sin(math.radians(a))
        )
        for a in angs
    ]

    segments = []
    for i in range(3):
        a = verts[i]
        b = verts[i + 3]
        segments.append((a, b))

    return segments


def build_cells(cols, rows, r):
    """
    なぜ:
    セル配置計算を独立させ、
    演出順と配置責務を分けるため。

    前提:
    - フラットトップ六角グリッド
    - 奇数列を半段下げるオフセット配置

    入出力:
    - 入力: 列数、行数、半径
    - 出力: [(cx, cy), ...] の中心座標リスト

    副作用:
    - なし
    """
    sqrt3 = math.sqrt(3)

    dx = 1.5 * r
    dy = sqrt3 * r

    width = int((cols - 1) * dx + 2 * r)
    height = int((rows - 1) * dy + 2 * r)
    ox = -width // 2
    oy = height // 2

    cells = []

    for c in range(cols):
        for row in range(rows):
            cx = ox + r + c * dx
            cy = oy - r - (row * dy + (dy / 2 if (c % 2) else 0))
            cells.append((cx, cy))

    return cells


# =========================
# 描画対象の準備
# =========================
# Step4 の肝は、
# 「一本線を中心から左右へ伸ばす」こと。
#
# そのため、状態は
#   - どのセルか
#   - そのセル内の何本目か
#   - その線を中心から何段目まで伸ばしたか
# の三つで持つ。
cells = build_cells(COLS, ROWS, R)
segments_per_cell = [make_cell_segments(cx, cy, R) for cx, cy in cells]

current_cell_index = 0
current_line_index = 0
current_step_index = 0


def draw_next_growth_step():
    """
    なぜ:
    Step3 は「線分を始点→終点へ刻む」方式だったが、
    Step4 は「中心から両端へ同時に伸ばす」方式へ変えるため。

    状態管理:
    - current_cell_index:
        どのセルを描いているか
    - current_line_index:
        そのセル内の何本目の線か
    - current_step_index:
        中心から何段目まで伸ばしたか

    入出力:
    - 入力: なし
    - 出力: なし

    副作用:
    - 画面に短い線分が2本追加される
      （中心から片側へ1本、反対側へ1本）
    - 描画進行状態が更新される
    - 次回描画がタイマー予約される
    """
    global current_cell_index
    global current_line_index
    global current_step_index

    # 全セル描き終えたら終了。
    if current_cell_index >= len(segments_per_cell):
        turtle.update()
        return

    current_segments = segments_per_cell[current_cell_index]
    (x1, y1), (x2, y2) = current_segments[current_line_index]

    # この直径の中心点。
    # 理論上はセル中心と一致するが、
    # 幾何的に「線の中点」を毎回求めておくと、
    # 線データだけから完結できて責務が明確になる。
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    # 今回は「中心→片端」の半分区間を少しずつ伸ばす。
    #
    # たとえば 6分割なら、
    # 0段目: 0/6 → 1/6
    # 1段目: 1/6 → 2/6
    # ...
    # の区間を左右それぞれに描く。
    start_ratio = current_step_index / HALF_SEGMENT_STEPS
    end_ratio = (current_step_index + 1) / HALF_SEGMENT_STEPS

    # 中心から端A側への現在区間
    ax1, ay1 = interpolate_point(mx, my, x1, y1, start_ratio)
    ax2, ay2 = interpolate_point(mx, my, x1, y1, end_ratio)

    # 中心から端B側への現在区間
    bx1, by1 = interpolate_point(mx, my, x2, y2, start_ratio)
    bx2, by2 = interpolate_point(mx, my, x2, y2, end_ratio)

    # 左右へ同時に1段伸ばす。
    line(ax1, ay1, ax2, ay2)
    line(bx1, by1, bx2, by2)

    turtle.update()

    # 同じ線の次段へ進む。
    current_step_index += 1

    # 半区間の伸び切りが終わったら、次の線へ移る。
    if current_step_index >= HALF_SEGMENT_STEPS:
        current_step_index = 0
        current_line_index += 1

    # 三本線が終わったら、次のセルへ移る。
    if current_line_index >= len(current_segments):
        current_line_index = 0
        current_cell_index += 1

    scr.ontimer(draw_next_growth_step, STEP_INTERVAL_MS)


# =========================
# 実行開始
# =========================
draw_next_growth_step()
turtle.done()