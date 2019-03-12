initial_pos = []
x = 300
y = 300
initial_pos.append([x,y])
x = 300
y = 400
initial_pos.append([x,y])
x = 300
y = 500
initial_pos.append([x,y])
x = 400
y = 300
initial_pos.append([x,y])
x = 400
y = 400
initial_pos.append([x,y])
x = 400
y = 500
initial_pos.append([x,y])
x = 500
y = 300
initial_pos.append([x,y])
x = 500
y = 400
initial_pos.append([x,y])
x = 500
y = 500
initial_pos.append([x,y])

def generate_V(n):
	v = []
	x, y = 100, 100
	diff = 50
	for i in range(int(n/2)):
		if i==0:
			v.append([x,y])
		else:
			v.append([v[-1][0]+diff, v[-1][1]+diff])
	if (int(n)%2)==1:
		v.append([v[-1][0]+diff, v[-1][1]+diff])
		for i in range(int(n/2)+1, n):
			v.append([v[-1][0]+diff, v[-1][1]-diff])
	else:
		v.append([v[-1][0]+2*diff, v[-1][1]])
		for i in range(int(n/2)+1, n):
			v.append([v[-1][0]+diff, v[-1][1]-diff])

	return v

def generate_circle(n):
	import math
	r = 200
	pi = math.pi
	x = [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n+1)]
	#x = [(i[0]+500, i[1]+500) for i in x]
	return x


if __name__=='__main__':
	from vis import Ball
	from tkinter import *
	n = int(input("Enter uav number"))
	des = generate_circle(n)

	root = Tk()
	root.title("Balls")
	root.resizable(True,True)
	canvas = Canvas(root, width = 800, height = 800)
	canvas.pack()

	# create two ball objects and animate them
	balls = []
	color = ["red", "green", "black", "orange", "blue", "yellow", "purple", "grey", "brown", "magenta"]
	_ = 0
	for i in des:
		ball2 = Ball(canvas, i[0], i[1], color[_])
		_ = int(_ + 1)%10

	root.mainloop()