import numpy as np
from hungarian import Hungarian
from tkinter import *

n = int(input("Enter the number of UAVs"))
#n = 5
initial_pos = []
for i in range(n):
	x = int((np.random.rand()*10**5)%600)
	y = int((np.random.rand()*10**5)%600)
	initial_pos.append([x, y])

desired_shape = []
desired_shape.append([int((np.random.rand()*10**5)%600), int((np.random.rand()*10**5)%600)])
for i in range(n-1):
	desired_shape.append([int((desired_shape[-1][0]+10)%600), int((desired_shape[-1][1]+10)%600)])

k = [[0 for j in range(n)] for i in range(n)]

for i in range(n):
	for j in range(n):
		x = -np.transpose(initial_pos[i])*np.array(desired_shape[j])

		val = x[0]
		for _ in range(len(x)-1):
			val += x[_+1]

		k[i][j] = val
#		break
#	break

print(k)


hungarian = Hungarian(k)
hungarian.calculate()
x_star = hungarian.get_results()
k_star = hungarian.get_total_potential()


class Ball:
    def __init__(self, canvas, x1, y1, fill_col):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1+5
        self.y2 = y1+5
        self.canvas = canvas
        self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=fill_col)

    def move_ball(self):
        deltax = 1
        deltay = 1
        self.canvas.move(self.ball, deltax, deltay)
        self.canvas.after(50, self.move_ball)

# initialize root Window and canvas
root = Tk()
root.title("Balls")
root.resizable(True,True)
canvas = Canvas(root, width = 800, height = 800)
canvas.pack()

# create two ball objects and animate them
balls = []
color = ["red", "green", "black", "orange", "blue", "yellow", "purple", "grey", "brown", "magenta", "cyan"]
_ = 0
for i, j in x_star:
	ball1 = Ball(canvas, initial_pos[i][0], initial_pos[i][1], color[_])
	ball2 = Ball(canvas, desired_shape[j][0], desired_shape[j][1], color[_])
	balls.append([ball1, ball2])
	_ = _ + 1

root.mainloop()
