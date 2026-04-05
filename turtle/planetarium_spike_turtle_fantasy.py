# planetarium_spike_turtle_fantasy.py
# MicroPython (SPIKE 3.0) / CPython タートル想定
# 星々が瞬き、中央に“渦を巻く天の川”が流れるプラネタリウム（幻想寄り）

# --- 互換初期化 ---
try:
    import turtle
    scr = getattr(turtle, "Screen", lambda: None)()
    t = getattr(turtle, "Turtle", turtle.Turtle)()
except Exception:
    from turtle import *
    t = Turtle()
    try:
        scr = Screen()
    except:
        scr = None

# --- time互換 ---
try:
    import time
    _sleep = time.sleep
except Exception:
    _sleep = None

# --- 乱数互換 ---
try:
    import random
    randint = random.randint
    random_ = random.random
except Exception:
    def random_(): return 0.5
    def randint(a, b): return (a + b) // 2

# --- 見た目調整 ---
try: t.hideturtle()
except: pass
try: t.speed(0)
except: pass
try: t.penup()
except: pass
try:
    if scr:
        scr.bgcolor("#000010")
except: pass

# --- dot互換（dotが無い環境でも点っぽく） ---
def dot_like(size=2):
    try:
        t.dot(size)
        return
    except:
        pass
    try:
        t.pendown()
    except: pass
    try:
        t.pensize(size)
    except: pass
    try:
        t.forward(1)
    except: pass
    try:
        t.penup()
    except: pass

def goto_xy(x, y):
    try:
        t.goto(x, y)
    except:
        pass

# --- 画面サイズ（取れない場合は固定） ---
W, H = 240, 180
try:
    if scr:
        W = int(scr.window_width())
        H = int(scr.window_height())
except:
    pass

# --------------------------
# パラメータ（幻想寄り）
# --------------------------
STAR_COUNT = 120
TWINKLE_PER_STEP = 3

# 渦天の川（“川筋”用の粒子）
STREAM_COUNT = 70          # 動く粒子数（増やしすぎ注意）
STREAM_SPEED = 0.030       # 進む速さ（大きいと速く流れる）
STREAM_WIDTH = H // 8      # 川の幅（見た目の太さ）
STREAM_SWIRL = 1.35        # 渦の強さ（大きいほど巻く）
CENTER_Y = 0

# --------------------------
# 星（固定）
# --------------------------
stars = []
for _ in range(STAR_COUNT):
    x = randint(-W//2 + 5, W//2 - 5)
    y = randint(-H//2 + 5, H//2 - 5)
    base = randint(1, 3)
    stars.append([x, y, base])

def draw_starfield():
    for x, y, base in stars:
        goto_xy(x, y)
        try: t.pencolor("#dfe9ff")
        except: pass
        dot_like(base)

# --------------------------
# 天の川：渦の“静的な霞”を描く（軽めの点群）
# --------------------------
def draw_milkyway_haze():
    # 中央を横断する“もや”を、渦っぽい曲線沿いに薄く散布
    haze_points = 220
    for i in range(haze_points):
        # xは広く
        x = randint(-W//2, W//2)
        # 基本帯（中心付近に集める）
        y = randint(-STREAM_WIDTH, STREAM_WIDTH)

        # 渦変形：xに応じてyを波打たせ、巻き込みを足す
        # sinが無い環境もあるので、軽い“擬似波”にする
        # （xを区間で折り返すだけ）
        fold = (x // 20) % 6
        wobble = (fold - 3) * 2  # -6..+6くらい
        y2 = int(y + wobble)

        # 斜め流れも少し
        y2 += int(x * 0.10)

        if y2 < -H//2 or y2 > H//2:
            continue

        goto_xy(x, y2)

        # 色は2色だけ（環境差に強く）
        col = "#c9c8ff" if (i % 2 == 0) else "#e8f7ff"
        try: t.pencolor(col)
        except: pass

        s = 1 if (i % 5) else 2
        dot_like(s)

# --------------------------
# 天の川：動く粒子（“川が流れる”）
# --------------------------
# 粒子はパラメトリックに持つ：u（進行）と、横ズレ（w）
# uが増えると右へ流れ、渦で上下にうねる
streams = []
for _ in range(STREAM_COUNT):
    u = random_() * 2.0 - 1.0          # -1..+1（左〜右の初期位置）
    w = (random_() * 2.0 - 1.0) * 1.0  # -1..+1（帯の中での横ズレ）
    streams.append([u, w])

def stream_pos(u, w):
    # u: -1..+1 を画面Xへ
    x = int(u * (W * 0.55))

    # 帯の基本y（中心へ寄せる）
    base = int(w * STREAM_WIDTH)

    # 渦：uに応じて巻く（sinが無い想定なので“折返し渦”で擬似）
    # 巻き込み：uの区間で上下方向を切替える
    phase = int((u + 1.0) * 10)  # 0..20
    swirl = (phase % 4) - 2      # -2,-1,0,1
    y = int(base + swirl * STREAM_SWIRL * 6)

    # 斜め流れ
    y += int(x * 0.12)

    return x, y

def draw_streams(step):
    # 少数の粒子だけを上描きして“流れ”に見せる
    for i in range(STREAM_COUNT):
        u, w = streams[i]

        # 進める（右へ流れる）。端を越えたら左へ戻す
        u += STREAM_SPEED
        if u > 1.15:
            u = -1.15
            w = (random_() * 2.0 - 1.0)

        streams[i][0] = u
        streams[i][1] = w

        x, y = stream_pos(u, w)
        if y < -H//2 or y > H//2:
            continue

        goto_xy(x, y)

        # 粒子の明滅（ステップでゆらす）
        bright = ((step + i) % 3 == 0)
        try:
            t.pencolor("#ffffff" if bright else "#c9c8ff")
        except: pass

        dot_like(2 if bright else 1)

# --------------------------
# 星の瞬き（少数だけ）
# --------------------------
def twinkle_step(step):
    for k in range(TWINKLE_PER_STEP):
        idx = randint(0, STAR_COUNT - 1)
        x, y, base = stars[idx]
        goto_xy(x, y)

        if (step + k) % 2 == 0:
            try: t.pencolor("#ffffff")
            except: pass
            dot_like(base + 1)
        else:
            try: t.pencolor("#000010")
            except: pass
            dot_like(base + 1)
            goto_xy(x, y)
            try: t.pencolor("#dfe9ff")
            except: pass
            dot_like(base)

# --------------------------
# 実行
# --------------------------
draw_starfield()
draw_milkyway_haze()

step = 0
while True:
    # 星の瞬き
    twinkle_step(step)
    # 天の川の“流れ”
    draw_streams(step)

    step += 1
    if _sleep:
        try: _sleep(0.06)
        except: pass
