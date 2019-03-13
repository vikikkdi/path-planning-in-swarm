from tkinter import *
from random import randint

class Ball:
	def __init__(self, canvas, x1, y1, col):
		self.x1 = x1 - 5
		self.y1 = y1 - 5
		self.x2 = x1 + 5
		self.y2 = y1 + 5
		self.x = x1
		self.y = y1
		self.canvas = canvas
		self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=col)

	def move_ball(self, x_aug, y_aug):
		if self.x == x_aug and self.y == y_aug:
			return
		elif self.x == x_aug:
			deltax = 0
			if self.y < y_aug:
				deltay = min(1, y_aug - self.y)
			else:
				deltay = max(-1, y_aug - self.y)
		elif self.y == y_aug:
			deltay = 0
			if self.x < x_aug:
				deltax = min(1, x_aug - self.x)
			else:
				deltax = max(-1, x_aug - self.x)
		else:
			x1 = self.x
			x2 = x_aug
			y1 = self.y
			y2 = y_aug

			c = (x2*y1 - x1*y2)/(x2-x1)
			m = (y1-c)/x1

			if x2 > x1:
				deltax = min(1, x2 - x1)
			else:
				deltax = max(-1, x2 - x1)
			x = x1 + deltax
			y = m*x + c
			deltay = y - y1
		self.x = self.x + deltax
		self.y = self.y + deltay
		self.canvas.move(self.ball, deltax, deltay)
		self.canvas.after(50, self.move_ball, x_aug, y_aug)

if __name__ == '__main__':
	# initialize root Window and canvas
	root = Tk()
	root.title("Balls")
	root.resizable(True,True)
	canvas = Canvas(root, width = 600, height = 600)
	canvas.pack()

	# create two ball objects and animate them
	ball1 = Ball(canvas, 300, 300)
	ball2 = Ball(canvas, 100, 100)

	ball1.move_ball(ball2.x, ball2.y)
	#ball2.move_ball()

	root.mainloop()