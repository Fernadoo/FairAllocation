import numpy as np
from copy import deepcopy
from mip import *


def MNW(valuation_matrix):
	V = deepcopy(valuation_matrix)
	num_agents, num_items = V.shape
	
	model = Model(sense=MAXIMIZE, solver_name=CBC)
	
	"""
	Constraints:
		1.	P[i,j] => {0,1}
		2.  sum_j P[i,j] <= 1
	"""
	P = np.array([[model.add_var(var_type=BINARY) for i in range(num_items)] for j in range(num_agents)])
	for item in range(num_items):
		model += np.sum(P[:, item]) == 1

	"""
	Onjective: max prod_i sum_j (V[i,j] * P[i,j])
	"""
	obj = np.sum(V[i, j] * P[i, j] for i in range(num_agents) for j in range(num_items))
	model.objective = maximize(obj)

	"""
	Solve and check
	"""
	model.write('model.lp')
	model.optimize()
	P_ = np.zeros(shape=(num_agents, num_items))
	for agent in range(num_agents):
		for item in range(num_items):
			P_[agent, item] = P[agent, item].x
	P = deepcopy(P_)

	allocation = dict()
	for agent in range(num_agents):
		allocation[agent] = np.where(P[agent]==1)[0].tolist()

	envy_matrix = np.zeros(shape=(num_agents, num_agents))
	for agent in range(num_agents):
		for opponent in range(num_agents):
			envy_matrix[agent, opponent] = np.sum(valuation_matrix[agent] * P[opponent])

	return allocation, envy_matrix