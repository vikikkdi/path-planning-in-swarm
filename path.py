import math
import numpy as np
from hungarian import Hungarian
from tkinter import *
from vis import Ball
import gradient_descent
from time import sleep
import coordinates

n = 9
initial_pos = coordinates.initial_pos
desired_shape = coordinates.generate_V(n)

k = [[0 for j in range(n)] for i in range(n)]

for i in range(n):
	for j in range(n):
		x = -np.transpose(initial_pos[i]).dot(np.array(desired_shape[j]))
		k[i][j] = x

hungarian = Hungarian(k)
hungarian.calculate()
x_star = hungarian.get_results()
k_star = hungarian.get_total_potential()

# initialize root Window and canvas
root = Tk()
root.title("Balls")
root.resizable(True,True)
canvas = Canvas(root, width = 800, height = 800)
canvas.pack()

# create two ball objects and animate them
balls = []
color = ["red", "green", "black", "orange", "blue", "yellow", "purple", "grey", "brown", "magenta"]

d = gradient_descent.gradient_descent(initial_pos, desired_shape, x_star)
qq = np.array(d) + np.array(desired_shape)

_ = 0
for i, j in x_star:
	ball1 = Ball(canvas, initial_pos[i][0], initial_pos[i][1], color[_])
	ball2 = Ball(canvas, qq[j][0], qq[j][1], color[_])
#	ball2 = Ball(canvas, desired_shape[j][0], desired_shape[j][1], color[2])
	ball1.move_ball(qq[j][0], qq[j][1])
	_ = int(_ + 1)%10

root.mainloop()