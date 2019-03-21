import math
import numpy as np
from hungarian import Hungarian
from tkinter import *
from vis import Ball
import gradient_descent
from time import sleep
import coordinates
from path import *

root = Tk()
root.title("Path Planning in Swarm")
root.resizable(True,True)
canvas = Canvas(root, width = 800, height = 800)
canvas.pack()

n = 10
balls = []
color = ["red", "green", "black", "orange", "blue", "yellow", "purple", "grey", "brown", "magenta"]
initial_pos = coordinates.generate_initial(n)
_ = 0
for i in initial_pos:
	ball1 = Ball(canvas, i[0], i[1], color[_])
	balls.append(ball1)
	_ = int(_ + 1)%10

button1 = Button(root, text = "Circle", command = lambda: form_circle(balls, n), anchor = W)
button1_window = canvas.create_window(650, 700, anchor=NW, window=button1)

button2 = Button(root, text = "V", command = lambda: form_v(balls, n), anchor = W)
button2_window = canvas.create_window(700, 700, anchor=NW, window=button2)

button3 = Button(root, text = "Line", command = lambda: form_line(balls, n), anchor = W)
button3_window = canvas.create_window(610, 700, anchor=NW, window=button3)

button4 = Button(root, text = "Square", command = lambda: form_square(balls, n), anchor = W)
button4_window = canvas.create_window(550, 700, anchor=NW, window=button4)

button5 = Button(root, text = "Star", command = lambda: form_diamond(balls, n), anchor = W)
button5_window = canvas.create_window(510, 700, anchor=NW, window=button5)

button6 = Button(root, text = "Initial", command = lambda: form_n_init(balls, n), anchor = W)
button6_window = canvas.create_window(720, 700, anchor=NW, window=button6)

root.mainloop()