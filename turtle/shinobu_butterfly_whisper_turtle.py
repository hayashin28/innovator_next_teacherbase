# shinobu_butterfly_turtle_step06.py
# Python (CPython) の turtle で、しのぶさんモチーフの
# 「蝶エンブレム」が羽を少しずつ開きながら現れ、
# その後にごく小さく羽ばたきつつ、ほんの少し上下に浮き、
# 背景にはごく少数の淡い粒が静かに流れ、
# 最後は余韻を残しながら静かに収束する Step6
#
# なぜ:
# Step5 では、蝶本体と背景粒子の両方に静かな気配が入った。
# ただ、最後に急に「停止」すると、作品としてはやや機械的に見える。
# そこで Step6 では、羽ばたき・浮遊・背景粒子の動きを
# 少しずつ弱めるフェーズを追加し、
# 「ふっと落ち着いて完成図へ戻る」終わり方を作る。
#
# 前提:
# - Python 標準の turtle が使えること
# - 背景粒子は主役を邪魔しない控えめな演出に留める
# - フェードは透明化ではなく、「動きの振幅を弱める」方向で表現する
# - 今回の主眼は終幕演出であり、
#   新しい大きな見た目要素は追加しない
#
# 入出力:
# - 入力なし
# - turtle ウィンドウ上に、蝶が現れ、羽ばたき、少し浮遊し、
#   最後に静かな余韻を残して完成図へ収束する
#
# 副作用:
# - 描画ウィンドウを開く
# - タイマーで段階描画を進める
#
# 例外:
# - turtle 非対応環境では動かない
# - 描画環境によっては円弧や dot の見え方に差が出ることがある

import math
import random
import turtle


# =========================
# 見た目設定
# =========================
BG = "#241437"          # 濃い紫系の背景
WING = "#f4f0ff"        # 羽の明るい色
LINE = "#c7b8ff"        # 翅脈や輪郭の淡い紫
BODY = "#1a1a1a"        # 胴体の濃色
DOT = "#b79cff"         # 羽先の装飾色

# 背景粒子の色候補。
# 主役を食わないよう、暗めの淡色に留める。
PARTICLE_COLORS = [
    "#6f5b8f",
    "#7a67a3",
    "#8b79b5",
    "#9e8cc8",
]

# 出現フェーズの段数。
APPEAR_STEPS = 12

# 出現フェーズの待ち時間（ミリ秒）。
APPEAR_INTERVAL_MS = 45

# 羽ばたきフェーズのフレーム数。
FLAP_FRAMES = 18

# 羽ばたきフェーズの待ち時間（ミリ秒）。
FLAP_INTERVAL_MS = 40

# 余韻フェーズのフレーム数。
# 長すぎるとだれるため、短めで「静かに収束する」程度に留める。
SETTLE_FRAMES = 14

# 余韻フェーズの待ち時間（ミリ秒）。
SETTLE_INTERVAL_MS = 45

# 羽ばたきの開閉幅。
FLAP_AMPLITUDE = 0.10

# 上下移動の幅。
FLOAT_AMPLITUDE = 10

# 背景粒子数。
PARTICLE_COUNT = 10

# 粒子の流れる速さ。
PARTICLE_MIN_SPEED = 0.4
PARTICLE_MAX_SPEED = 1.2

# 粒子サイズの範囲。
PARTICLE_MIN_SIZE = 2
PARTICLE_MAX_SIZE = 5

# 画面サイズ。
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# =========================
# 画面初期化
# =========================
scr = turtle.Screen()
scr.title("Shinobu Butterfly - Step06")
scr.bgcolor(BG)
scr.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

t = turtle.Turtle(visible=False)
t.speed(0)
t.pensize(2)
t.penup()

# 自動更新を止め、見せたい瞬間だけ更新する。
turtle.tracer(False)


# =========================
# 背景粒子の準備
# =========================
def create_particle():
    """
    なぜ:
    背景粒子は複数個を同じルールで生成するため、
    初期化規則を一箇所へまとめるため。

    方針:
    - 画面内のどこかに初期配置する
    - ゆっくり上方向へ流す
    - ほんの少しだけ横へ揺れる位相を持たせる
    - 大きさと色は控えめにランダム化する

    入出力:
    - 入力なし
    - 出力: 粒子辞書 1個

    副作用:
    - なし
    """
    return {
        "x": random.uniform(-SCREEN_WIDTH / 2, SCREEN_WIDTH / 2),
        "y": random.uniform(-SCREEN_HEIGHT / 2, SCREEN_HEIGHT / 2),
        "speed": random.uniform(PARTICLE_MIN_SPEED, PARTICLE_MAX_SPEED),
        "size": random.uniform(PARTICLE_MIN_SIZE, PARTICLE_MAX_SIZE),
        "phase": random.uniform(0, math.pi * 2),
        "color": random.choice(PARTICLE_COLORS),
    }


particles = [create_particle() for _ in range(PARTICLE_COUNT)]


def update_particles(speed_scale=1.0):
    """
    なぜ:
    背景粒子は毎フレーム少しずつ位置を変える必要がある。
    ただし Step6 では、終盤で粒子の動きも少し落ち着かせたいので、
    speed_scale を導入して移動量を弱められるようにする。

    方針:
    - y をゆっくり増やして上へ流す
    - x には位相つきの微小な横揺れを加える
    - 上端を抜けたら下側へ静かに再出現させる
    - 終盤では speed_scale < 1.0 にして、気配を穏やかにする

    入出力:
    - 入力: 粒子速度の倍率 speed_scale
    - 出力: なし

    副作用:
    - 粒子辞書の座標や位相が更新される
    """
    for p in particles:
        p["y"] += p["speed"] * speed_scale
        p["phase"] += 0.05 * speed_scale

        # 横揺れも主張しすぎない程度に留める。
        p["x"] += math.sin(p["phase"]) * 0.18 * speed_scale

        if p["y"] > SCREEN_HEIGHT / 2 + 20:
            p["x"] = random.uniform(-SCREEN_WIDTH / 2, SCREEN_WIDTH / 2)
            p["y"] = -SCREEN_HEIGHT / 2 - random.uniform(10, 40)
            p["speed"] = random.uniform(PARTICLE_MIN_SPEED, PARTICLE_MAX_SPEED)
            p["size"] = random.uniform(PARTICLE_MIN_SIZE, PARTICLE_MAX_SIZE)
            p["phase"] = random.uniform(0, math.pi * 2)
            p["color"] = random.choice(PARTICLE_COLORS)


def draw_particles():
    """
    なぜ:
    背景粒子は前景の蝶より後ろに見せたい。
    そのため、毎フレーム蝶より先に描いておく。

    入出力:
    - 入力なし
    - 出力: なし

    副作用:
    - 背景粒子が画面へ描画される
    """
    for p in particles:
        move(p["x"], p["y"])
        t.dot(p["size"], p["color"])


# =========================
# 補助関数
# =========================
def move(x, y):
    """
    なぜ:
    ペン跡を出さずに座標だけを合わせる責務を分離し、
    描画関数側を読みやすく保つため。

    入出力:
    - 入力: 移動先座標 (x, y)
    - 出力: なし

    副作用:
    - turtle の現在位置が変わる
    """
    t.penup()
    t.goto(x, y)


def ease_out_quad(x):
    """
    なぜ:
    余韻フェーズでは、動きを急に止めるのではなく、
    少しずつ弱くして静止へ向かわせたい。
    そのため、0→1 の線形進行を「最初に大きく、最後は穏やか」
    へ変える補間関数を用いる。

    前提:
    - x は 0.0〜1.0 を想定する

    入出力:
    - 入力: 進行率 x
    - 出力: イージング後の値

    副作用:
    - なし
    """
    return 1 - (1 - x) * (1 - x)


def draw_body(offset_y=0):
    """
    なぜ:
    胴体は蝶全体の中心軸であり、
    羽の変形や浮遊の基準として明確に置く必要があるため。

    Step6 でも、蝶全体の上下移動へ追従できるよう
    offset_y を受け取る。

    入出力:
    - 入力: 上下オフセット量 offset_y
    - 出力: なし

    副作用:
    - 画面中央付近に胴体、頭、触角を描く
    """
    t.color(BODY)
    t.pensize(4)

    move(0, 20 + offset_y)
    t.setheading(-90)
    t.pendown()
    t.forward(110)
    t.penup()

    move(0, 32 + offset_y)
    t.dot(14, BODY)

    t.pensize(2)
    move(2, 36 + offset_y)
    t.setheading(65)
    t.pendown()
    t.circle(28, 45)
    t.penup()

    move(-2, 36 + offset_y)
    t.setheading(115)
    t.pendown()
    t.circle(-28, 45)
    t.penup()


def draw_wing(side=1, progress=1.0, offset_y=0):
    """
    なぜ:
    左右の羽は同じロジックを反転して使えるため、
    side による左右反転で共通化する。
    また、progress と offset_y によって
    出現・羽ばたき・浮遊・収束の各段階へ対応させる。

    入出力:
    - 入力: 左右指定、進行率、上下オフセット
    - 出力: なし

    副作用:
    - 羽の塗り図形を描く
    """
    p = max(0.08, progress)

    t.color(LINE, WING)
    t.pensize(2)

    move(0, 5 + offset_y)
    t.setheading((12 + 23 * p) * side)
    t.begin_fill()
    t.pendown()
    t.circle((30 + 50 * p) * side, 18 + 37 * p)
    t.circle((16 + 29 * p) * side, 18 + 47 * p)
    t.circle((-18 - 37 * p) * side, 18 + 37 * p)
    t.goto(0, 5 + offset_y)
    t.end_fill()
    t.penup()

    move(0, -20 + offset_y)
    t.setheading((-6 - 14 * p) * side)
    t.begin_fill()
    t.pendown()
    t.circle((24 + 41 * p) * side, 18 + 32 * p)
    t.circle((12 + 23 * p) * side, 20 + 50 * p)
    t.circle((-18 - 37 * p) * side, 16 + 29 * p)
    t.goto(0, -20 + offset_y)
    t.end_fill()
    t.penup()


def draw_veins(side=1, progress=1.0, offset_y=0):
    """
    なぜ:
    翅脈は蝶らしさを決めるが、
    羽が小さい段階で完成長の線を引くと不自然になる。
    そのため progress に応じて長さを変え、
    offset_y によって全体の浮遊へ追従させる。

    入出力:
    - 入力: 左右指定、進行率、上下オフセット
    - 出力: なし

    副作用:
    - 羽の内部に翅脈線を描く
    """
    p = max(0.0, progress)

    t.color(LINE)
    t.pensize(2)

    for angle, length in [(35, 70), (55, 62), (78, 52)]:
        move(0, 5 + offset_y)
        t.setheading(angle * side)
        t.pendown()
        t.forward(length * p)
        t.penup()

    for angle, length in [(-20, 55), (-42, 48)]:
        move(0, -18 + offset_y)
        t.setheading(angle * side)
        t.pendown()
        t.forward(length * p)
        t.penup()


def draw_decorations(side=1, progress=1.0, offset_y=0):
    """
    なぜ:
    羽先の装飾点は蝶のシンボル性を高めるが、
    最初から完成位置・完成サイズで出すと成長がずれる。
    そのため progress に応じて位置とサイズを育て、
    offset_y によって全体の浮遊にも追従させる。

    入出力:
    - 入力: 左右指定、進行率、上下オフセット
    - 出力: なし

    副作用:
    - 羽先の装飾点を描く
    """
    p = max(0.0, progress)

    decorations = [
        (92, 55, 8),
        (78, 8, 6),
        (58, -52, 7),
    ]

    for x, y, size in decorations:
        current_x = (x * p) * side
        current_y = y * p + offset_y
        current_size = max(2, size * p)

        move(current_x, current_y)
        t.dot(current_size, DOT)


def draw_frame(progress, offset_y=0):
    """
    なぜ:
    1フレームぶんの再構成責務を一箇所へ集め、
    フェーズ制御側を単純に保つため。

    方針:
    - 毎フレーム clear() して描き直す
    - 背景粒子を先に描く
    - その上に蝶本体を描く
    - 蝶本体は progress と offset_y に応じて変化させる

    入出力:
    - 入力:
        progress : 羽の開閉や出現度合い
        offset_y : 蝶全体の上下移動量
    - 出力: なし

    副作用:
    - 画面全体が現在フレーム状態へ更新される
    """
    t.clear()

    draw_particles()

    draw_body(offset_y=offset_y)
    draw_wing(side=-1, progress=progress, offset_y=offset_y)
    draw_wing(side=1, progress=progress, offset_y=offset_y)
    draw_veins(side=-1, progress=progress, offset_y=offset_y)
    draw_veins(side=1, progress=progress, offset_y=offset_y)
    draw_decorations(side=-1, progress=progress, offset_y=offset_y)
    draw_decorations(side=1, progress=progress, offset_y=offset_y)

    turtle.update()


# =========================
# アニメーション状態
# =========================
# 全体は3段階で進む。
# 1. 出現フェーズ
# 2. 羽ばたき＋上下浮遊フェーズ
# 3. 余韻を残しながら収束するフェーズ
phase = "appear"

current_appear_step = 0
current_flap_frame = 0
current_settle_frame = 0


def calc_flap_progress(frame_index, total_frames, base=1.0, amplitude=0.10):
    """
    なぜ:
    羽ばたきでは完成形を基準に、
    少しだけ開閉する progress を自然に作りたい。
    そのため sin 波を使って急な切り替わりを避ける。

    入出力:
    - 入力: 現在フレーム、総フレーム、基準 progress、振幅
    - 出力: 羽ばたき用 progress

    副作用:
    - なし
    """
    if total_frames <= 1:
        return base

    theta = (frame_index / (total_frames - 1)) * (2 * math.pi)
    value = math.sin(theta)

    progress = base + amplitude * value
    return max(0.86, min(1.0, progress))


def calc_float_offset(frame_index, total_frames, amplitude=10):
    """
    なぜ:
    羽だけでなく蝶全体も少し上下させたいが、
    跳ねるのではなく静かに漂わせたい。
    そのため cos 波でなめらかな上下量を作る。

    入出力:
    - 入力: 現在フレーム、総フレーム、上下振幅
    - 出力: 上下オフセット量

    副作用:
    - なし
    """
    if total_frames <= 1:
        return 0

    theta = (frame_index / (total_frames - 1)) * (2 * math.pi)
    return amplitude * math.cos(theta)


def animate():
    """
    なぜ:
    出現・羽ばたき・余韻収束の各フェーズを一つの入口で管理し、
    全体の流れを一箇所で追えるようにするため。

    フェーズ:
    - appear:
        0.0 から 1.0 へ段階的に現れる
    - flap:
        完成状態付近で、ごく小さく羽ばたきつつ少し上下する
    - settle:
        羽ばたき・浮遊・背景粒子の動きを徐々に弱めて静止へ向かう

    入出力:
    - 入力: なし
    - 出力: なし

    副作用:
    - 背景粒子と蝶の状態が1フレームぶん進む
    - 次回フレームがタイマー予約される
    """
    global phase
    global current_appear_step
    global current_flap_frame
    global current_settle_frame

    if phase == "appear":
        # 出現中は背景粒子も通常速度で流す。
        update_particles(speed_scale=1.0)

        if current_appear_step > APPEAR_STEPS:
            phase = "flap"
            current_flap_frame = 0
            scr.ontimer(animate, FLAP_INTERVAL_MS)
            return

        progress = current_appear_step / APPEAR_STEPS
        draw_frame(progress=progress, offset_y=0)

        current_appear_step += 1
        scr.ontimer(animate, APPEAR_INTERVAL_MS)
        return

    if phase == "flap":
        update_particles(speed_scale=1.0)

        if current_flap_frame >= FLAP_FRAMES:
            phase = "settle"
            current_settle_frame = 0
            scr.ontimer(animate, SETTLE_INTERVAL_MS)
            return

        progress = calc_flap_progress(
            frame_index=current_flap_frame,
            total_frames=FLAP_FRAMES,
            base=0.95,
            amplitude=FLAP_AMPLITUDE,
        )
        offset_y = calc_float_offset(
            frame_index=current_flap_frame,
            total_frames=FLAP_FRAMES,
            amplitude=FLOAT_AMPLITUDE,
        )

        draw_frame(progress=progress, offset_y=offset_y)

        current_flap_frame += 1
        scr.ontimer(animate, FLAP_INTERVAL_MS)
        return

    if phase == "settle":
        # 余韻フェーズでは、フレームが進むほど動きを弱めていく。
        if current_settle_frame >= SETTLE_FRAMES:
            # 最後は完成図へ静かに戻して終了。
            update_particles(speed_scale=0.25)
            draw_frame(progress=1.0, offset_y=0)
            return

        raw = current_settle_frame / max(1, (SETTLE_FRAMES - 1))

        # 0→1 の進行を、止まり際が穏やかになるように変換する。
        eased = ease_out_quad(raw)

        # 振幅は、開始時 1.0 → 終了時 0.0 へ落とす。
        damping = 1.0 - eased

        # 背景粒子も少しずつ落ち着かせる。
        particle_speed_scale = 0.25 + 0.75 * damping
        update_particles(speed_scale=particle_speed_scale)

        # 余韻フェーズでも、少しだけ羽ばたきと浮遊の波形を使う。
        # ただし振幅に damping を掛けて、徐々に静止へ寄せる。
        progress = calc_flap_progress(
            frame_index=current_settle_frame,
            total_frames=SETTLE_FRAMES,
            base=0.97,
            amplitude=FLAP_AMPLITUDE * damping,
        )
        offset_y = calc_float_offset(
            frame_index=current_settle_frame,
            total_frames=SETTLE_FRAMES,
            amplitude=FLOAT_AMPLITUDE * damping,
        )

        draw_frame(progress=progress, offset_y=offset_y)

        current_settle_frame += 1
        scr.ontimer(animate, SETTLE_INTERVAL_MS)
        return


# =========================
# 実行開始
# =========================
animate()
turtle.done()