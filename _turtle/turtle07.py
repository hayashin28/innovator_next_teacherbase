# トライフォース
from turtle import *
import math
shape("turtle")

speed(0)
hideturtle()

L = 60
H = math.sqrt(3) * L / 2  # 正三角形の高さ

pencolor("black")
fillcolor("yellow")

def up_triangle(x, y):
    penup()
    goto(x, y)
    setheading(0)
    pendown()
    begin_fill()
    goto(x + L, y)
    goto(x + L / 2, y + H)
    goto(x, y)
    end_fill()

def down_triangle(x, y):
    penup()
    goto(x, y)
    setheading(0)
    pendown()
    begin_fill()
    goto(x + L, y)
    goto(x + L / 2, y - H)
    goto(x, y)
    end_fill()

# 1段目
up_triangle(-30, 2 * H)

# 2段目
up_triangle(-60, H)
down_triangle(-30, 2 * H)
up_triangle(0, H)

# 3段目
up_triangle(-90, 0)
down_triangle(-60, H)
up_triangle(-30, 0)
down_triangle(0, H)
up_triangle(30, 0)

hideturtle()      # カメを消す

done()