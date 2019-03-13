import math
import numpy as np
from hungarian import Hungarian
from tkinter import *
from vis import Ball
import gradient_descent
from time import sleep
import coordinates
from path import *

# initialize root Window and canvas
root = Tk()
root.title("Balls")
root.resizable(True,True)
canvas = Canvas(root, width = 800, height = 800)
canvas.pack()

n = 9
balls = []
color = ["red", "green", "black", "orange", "blue", "yellow", "purple", "grey", "brown", "magenta"]
initial_pos = coordinates.initial_pos
_ = 0
for i in initial_pos:
	ball1 = Ball(canvas, i[0], i[1], color[_])
	balls.append(ball1)
	_ = int(_ + 1)%10

button1 = Button(root, text = "Circle", command = lambda: form_circle(balls, n), anchor = W)
button1_window = canvas.create_window(700, 700, anchor=NW, window=button1)

button2 = Button(root, text = "V", command = lambda: form_v(balls, n), anchor = W)
button2_window = canvas.create_window(750, 700, anchor=NW, window=button2)

root.mainloop()