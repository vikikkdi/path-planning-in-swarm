import numpy as np
import math

def calculate_cost(p, s, alpha, d, assignment):
	cost = 0
	for i, j in assignment:
		x = np.transpose(p[i]).dot(np.array(p[i])) 
		x += (alpha**2)*(np.transpose(s[j]).dot(np.array(s[j])))
		x += -2*alpha*np.transpose(p[i]).dot(s[j])
		x += 2*alpha*np.transpose(s[j]).dot(np.array(d))
		x += -2*np.transpose(p[i]).dot(np.array(d))
		x += np.transpose(d).dot(np.array(d))
		cost += x
	
	return cost

def calculate_cost_xy(p, s, alpha, d, assignment):
	cost = 0
	for i, j in assignment:
		x1, y1 = p[i][0], p[i][1]
		x2, y2 = s[j][0], s[j][1]
		x3, y3 = d[0], d[1]

		x = x1**2 + y1**2 
		x += ((alpha**2)*(x2**2)) + ((alpha**2)*(y2**2))
		x += (-2*alpha*x1*x2) + (-2*alpha*y1*y2)
		x += (2*alpha*x2*x3) + (2*alpha*y2*y3)
		x += (-2*x1*x3) + (-2*y1*y3)
		x += (x3**2 + y3**2)

		cost += x
	return cost

def calculate_distance(p, s, assignment):
	dist = 0
	for i, j in assignment:
		x = (p[i][0] - s[j][0])**2
		y = (p[i][1] - s[j][1])**2
		dist += math.sqrt(x+y)
	
	return dist

def differentiate_cost_with_alpha(p, s, assignment, alpha, d):
	val = 0
	for i, j in assignment:
		x = 2*alpha*np.transpose(s[j]).dot(np.array(s[j]))
		x += -2*np.transpose(p[i]).dot(np.array(s[j]))
		x += 2*np.transpose(s[j]).dot(np.array(d))
		val += x
	return val

def differentiate_cost_with_alpha_xy(p, s, assignment, alpha, d):
	val = 0
	for i, j in assignment:
		x1, y1 = p[i][0], p[i][1]
		x2, y2 = s[j][0], s[j][1]
		x3, y3 = d[0], d[1]

		x = (2*alpha*(x2**2)) + (2*alpha*(y2**2))
		x += (-2*x1*x2) + (-2*y1*y2)
		x += (2*x2*x3) + (2*y2*y3)
		val += x
	return val

def differentiate_cost_with_x(p, s, assignment, alpha, x):
	val = 0
	for i, j in assignment:
		c = 2*alpha*s[j][0]
		c += -2*p[i][0]
		c += 2*x
		val += c
	return val

def differentiate_cost_with_x_xy(p, s, assignment, alpha, x):
	val = 0
	for i, j in assignment:
		x1, y1 = p[i][0], p[i][1]
		x2, y2 = s[j][0], s[j][1]
		x3 = x

		c = 2*alpha*x2 - 2*x1 + 2*x3
		val += c
	return val

def differentiate_cost_with_y(p, s, assignment, alpha, y):
	val = 0
	for i, j in assignment:
		c = 2*alpha*s[j][1]
		c += -2*p[i][1]
		c += 2*y
		val += c
	return val

def differentiate_cost_with_y_xy(p, s, assignment, alpha, y):
	val = 0
	for i, j in assignment:
		x1, y1 = p[i][0], p[i][1]
		x2, y2 = s[j][0], s[j][1]
		y3 = y

		c = 2*alpha*y2 - 2*y1 + 2*y3
		val += c
	return val

def gradient_Descent(x_star, p, s):
	diff = 0.001
	alpha = np.random.rand()
	d = [np.random.rand(), np.random.rand()]
	curr_cost = calculate_cost_xy(p, s, alpha, d, x_star)
	flag = True
	prev_cost = 0
	learning_rate = 0.01
	while flag or abs(curr_cost-prev_cost)>=diff:
		flag = False
		c_with_alpha = differentiate_cost_with_alpha_xy(p, s, x_star, alpha, d)
		c_with_x = differentiate_cost_with_x_xy(p, s, x_star, alpha, d[0])
		c_with_y = differentiate_cost_with_y_xy(p, s, x_star, alpha, d[1])

		alpha = alpha - learning_rate*c_with_alpha
		d[0] = d[0] - learning_rate*c_with_x
		d[1] = d[1] - learning_rate*c_with_y

		prev_cost = curr_cost
		curr_cost = calculate_cost(p, s, alpha, d, x_star)
		print(c_with_alpha, c_with_x, c_with_y)

	print(alpha, d)


if __name__ == '__main__':
	from hungarian import Hungarian
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

	gradient_Descent(x_star, initial_pos, desired_shape)