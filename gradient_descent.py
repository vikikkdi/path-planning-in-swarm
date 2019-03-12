import numpy as np
import math

def calculate_cost(p, s, d, assignment):
	cost = 0

	for i, j in assignment:
		x1, y1 = p[i][0], p[i][1]
		x2, y2 = s[j][0], s[j][1]
		x3, y3 = d[0], d[1]
		z1 = x1 - x2
		z2 = y1 - y2

		val = (z1-x3)**2 
		val += (z2-y3)**2

		cost += math.sqrt(val)
	return cost

def diff_with_x(p, s, assignment, d):
	val = 0

	for i, j in assignment:
		x1, y1 = p[i][0], p[i][1]
		x2, y2 = s[j][0], s[j][1]
		x3, y3 = d[0], d[1]

		c = (2*x3 + 2*x2 + -2*x1)
		val += c
	val = val*0.5
	val = val/calculate_cost(p, s, d, assignment)
	return val

def diff_with_y(p, s, assignment, d):
	val = 0

	for i, j in assignment:
		x1, y1 = p[i][0], p[i][1]
		x2, y2 = s[j][0], s[j][1]
		x3, y3 = d[0], d[1]

		c = (2*y3 + 2*y2 + -2*y1)
		val += c
	val = val*0.5
	val = val/calculate_cost(p, s, d, assignment)
	return val

def gradient_descent(p, s, assignment):
	diff = 0.001
	d = [int(np.random.rand()*1000), int(np.random.rand()*1000)]
	curr_cost = calculate_cost(p, s, d, assignment)
	flag = True
	prev_cost = 0
	learning_rate = 0.01
	
	while flag or abs(curr_cost-prev_cost)>=diff:
		flag = False
		c_with_x = diff_with_x(p, s, assignment, d)
		c_with_y = diff_with_y(p, s, assignment, d)

		d[0] = d[0] - learning_rate*c_with_x
		d[1] = d[1] - learning_rate*c_with_y

		prev_cost = curr_cost
		curr_cost = calculate_cost(p, s, d, assignment)


	return d
