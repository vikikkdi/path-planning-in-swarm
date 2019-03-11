import numpy as np
from hungarian import Hungarian
from tkinter import *

#this is the initial position matrix (matrix p as per the paper. its size is nx2)
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
#this is the desired shape matrix (matrix s as per the paper. its size is nx2)
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
#this is the cost matrix that has to be sent to hungarian algorithm for finding the assignment
k = [[0 for j in range(n)] for i in range(n)]

for i in range(n):
	for j in range(n):
		x = -np.transpose(initial_pos[i]).dot(np.array(desired_shape[j]))
		k[i][j] = x

hungarian = Hungarian(k)
hungarian.calculate()
#assignment X* as per the paper
x_star = hungarian.get_results()
#value K* as per the paper
k_star = hungarian.get_total_potential()

# initialize root Window and canvas and this is for visualisation
class Ball:
	def __init__(self, canvas, x1, y1, fill_col):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x1+5
		self.y2 = y1+5
		self.canvas = canvas
		self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=fill_col)

root = Tk()
root.title("Balls")
root.resizable(True,True)
canvas = Canvas(root, width = 800, height = 800)
canvas.pack()
color = ["red", "green", "black", "orange", "blue", "yellow", "purple", "grey", "brown", "magenta"]

#calculating the goal formation from the desired shape(matrix q as per paper)
ds = 0
for i in desired_shape:
	x = np.transpose(i).dot(np.array(i))
	ds += x

#calculating alpha star and d star as per equation 21 of the paper
alpha_star = (np.transpose(initial_pos).dot(np.array(desired_shape))+n*k_star)/(np.transpose(desired_shape).dot(np.array(desired_shape))-(n*ds))

d_star = (initial_pos - np.transpose(alpha_star.dot(np.transpose(desired_shape))))/n

#calculating the goal formation q matrix such that q = alphaStar * s + dStar
q = np.transpose(alpha_star.dot(np.transpose(desired_shape)) + np.transpose(d_star))

print(q)

_ = 0
for i, j in x_star:
	ball1 = Ball(canvas, initial_pos[i][0], initial_pos[i][1], color[_])
	ball2 = Ball(canvas, desired_shape[j][0], desired_shape[j][1], color[_])
	ball3 = Ball(canvas, q[j][0], q[j][1], color[0])
	_ = int(_ + 1)%10


root.mainloop()
