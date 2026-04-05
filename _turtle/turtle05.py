# 六芒星
from turtle import *
shape("turtle")

speed(0)

# 上向き三角形
penup()
goto(-100, -58)
pendown()

goto(0, 115)
goto(100, -58)
goto(-100, -58)

# 下向き三角形
penup()
goto(-100, 58)
pendown()

goto(100, 58)
goto(0, -115)
goto(-100, 58)

hideturtle()
done()