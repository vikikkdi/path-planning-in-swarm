import math
import numpy as np
from hungarian import Hungarian
from tkinter import *
from vis import Ball

#n = int(input("Enter the number of UAVs"))
n = 9
initial_pos = []
x = 100
y = 10
initial_pos.append([x,y])
x = 100
y = 50
initial_pos.append([x,y])
x = 100
y = 100
initial_pos.append([x,y])
x = 150
y = 10
initial_pos.append([x,y])
x = 150
y = 50
initial_pos.append([x,y])
x = 150
y = 100
initial_pos.append([x,y])
x = 200
y = 10
initial_pos.append([x,y])
x = 200
y = 50
initial_pos.append([x,y])
x = 200
y = 100
initial_pos.append([x,y])

desired_shape = []
x = 100
y = 200
desired_shape.append([x,y])
x = 150
y = 250
desired_shape.append([x,y])
x = 200
y = 300
desired_shape.append([x,y])
x = 250
y = 350
desired_shape.append([x,y])
x = 300
y = 400
desired_shape.append([x,y])
x = 350
y = 350
desired_shape.append([x,y])
x = 400
y = 300
desired_shape.append([x,y])
x = 450
y = 250
desired_shape.append([x,y])
x = 500
y = 200
desired_shape.append([x,y])

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

ds = 0
for i in desired_shape:
	x = np.transpose(i).dot(np.array(i))
	ds += x
alpha_star = (np.transpose(initial_pos).dot(np.array(desired_shape))+n*k_star)/(np.transpose(desired_shape).dot(np.array(desired_shape))-(n*ds))

d_star = (initial_pos - np.transpose(alpha_star.dot(np.transpose(desired_shape))))/n

q = np.transpose(alpha_star.dot(np.transpose(desired_shape)) + np.transpose(d_star))
q = q%600

print(q)
_ = 0
for i, j in x_star:
	ball1 = Ball(canvas, initial_pos[i][0], initial_pos[i][1], color[_])
	ball2 = Ball(canvas, desired_shape[j][0], desired_shape[j][1], color[_])
	#ball2 = Ball(canvas, q[j][0], q[j][1], color[0])
	ball1.move_ball(desired_shape[j][0], desired_shape[j][1])
	_ = int(_ + 1)%10


root.mainloop()
