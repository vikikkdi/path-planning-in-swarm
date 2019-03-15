import math
import numpy as np
from hungarian import Hungarian
from tkinter import *
from vis import Ball
import gradient_descent
from time import sleep
import coordinates

def pseudo_cost_function(initial_pos, desired_shape, n):
	k = [[0 for j in range(n)] for i in range(n)]

	for i in range(n):
		for j in range(n):
			x = -np.transpose(initial_pos[i]).dot(np.array(desired_shape[j]))
			k[i][j] = x

	hungarian = Hungarian(k)
	hungarian.calculate()
	x_star = hungarian.get_results()
	k_star = hungarian.get_total_potential()

	return [x_star, k_star]

def optimal_goal_formation(initial_pos, desired_shape, x_star):
	d = gradient_descent.gradient_descent(initial_pos, desired_shape, x_star)
	qq = np.array(d) + np.array(desired_shape)
	return qq

def form_circle(balls, n):
	print("Desired shape is circle")
	initial_pos = [[i.x, i.y] for i in balls]
	desired_shape = coordinates.generate_circle(n)

	a = pseudo_cost_function(initial_pos, desired_shape, n)
	x_star = a[0]
	k_star = a[1]

	qq = optimal_goal_formation(initial_pos, desired_shape, x_star)

	for i, j in x_star:
		balls[i].move_ball(qq[j][0], qq[j][1])
	print("Circle shape formed")

def form_v(balls, n):
	print("Desired shape is V")
	initial_pos = [[i.x, i.y] for i in balls]
	desired_shape = coordinates.generate_V(n)

	a = pseudo_cost_function(initial_pos, desired_shape, n)
	x_star = a[0]
	k_star = a[1]

	qq = optimal_goal_formation(initial_pos, desired_shape, x_star)

	for i, j in x_star:
		balls[i].move_ball(qq[j][0], qq[j][1])
	print("V shape formed")

def form_n_init(balls, n):
	print("Desired shape is n*n")
	initial_pos = [[i.x, i.y] for i in balls]
	desired_shape = coordinates.initial_pos

	a = pseudo_cost_function(initial_pos, desired_shape, n)
	x_star = a[0]
	k_star = a[1]

	qq = optimal_goal_formation(initial_pos, desired_shape, x_star)

	for i, j in x_star:
		balls[i].move_ball(qq[j][0], qq[j][1])
	print("n*n shape formed")