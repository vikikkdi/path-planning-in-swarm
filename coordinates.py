import numpy as np

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

def compute_product(n):
	x = 2
	l = []
	while n!=1:
		if int(n%x)==0:
			l.append(x)
			n = n/x
		else:
			x += 1
	if len(l)<=1:
		l = [1] + l

	return l

def generate_initial(n):
	l = compute_product(n)
	if int(len(l)%2) == 0:
		x1 = l[:int(len(l)/2)]
		x2 = l[int(len(l)/2):]
	else:
		x1 = l[:int(len(l)/2)+1]
		x2 = l[int(len(l)/2)+1:]
	row = col = 1	
	for i in x1:
		row = row*i
	for j in x2:
		col = col*j
	x, y = 100, 200
	diff = 100
	initial_pos = []

	for i in range(col):
		y = 200
		for j in range(row):
			initial_pos.append([x,y])
			y += diff
		x += diff

	return initial_pos

def generate_line(n):
	l = [[200, 200]]
	for i in range(n-1):
		l.append([l[-1][0]+50, l[-1][1]+50])
	return l

def generate_square(n):
	if n<4:
		print("Unable to form square")
		return
	tx, ty = 100, 100
	bx, by = 500, 500
	sq = []
	sq.append([tx, ty])
	sq.append([bx, ty])
	sq.append([bx, by])
	sq.append([tx, by])
	n -= 4
	_ = 0

	while n!=0:
		x, y = (sq[_][0] + sq[int((_+1)%len(sq))][0])/2, (sq[_][1] + sq[int((_+1)%len(sq))][1])/2
		sq = sq[:_+1] + [[x, y]] + sq[_+1:]
		_ = int(int(_+2)%len(sq))
		n -= 1

	return sq

def generate_diamond(n):
	dia = [[400,400]]
	dia.append([dia[0][0]-50, dia[0][1]+100])
	dia.append([dia[0][0]+50, dia[0][1]+100])
	dia.append([dia[1][0]-100, dia[1][1]+20])
	dia.append([dia[2][0]+100, dia[2][1]+20])
	dia.append([dia[1][0]-30, dia[1][1]+100])
	dia.append([dia[2][0]+30, dia[2][1]+100])
	dia.append([dia[0][0], dia[5][1]+50])
	dia.append([dia[5][0]-20, dia[5][1]+100])
	dia.append([dia[6][0]+20, dia[6][1]+100])

	return dia



if __name__=='__main__':
	print(generate_initial(int(input('Enter uav count'))))