import numpy as np
from copy import deepcopy
from mip import *

def MUtilW(valuation_matrix):
	"""
	In fact, one can compute maximum utilitarian welfare within O(n) time
	by simply assign the item to the agent who values it most.

	Here is a standard MIP formulation as well as the implementation via CBC solver.
	"""
	V = deepcopy(valuation_matrix)
	num_agents, num_items = V.shape
	
	model = Model(solver_name=CBC)
	
	'''
	Constraints:
		1.	P[i,j] => {0,1}
		2.  sum_j P[i,j] <= 1
	'''
	P = np.array([[model.add_var(var_type=BINARY) for i in range(num_items)] for j in range(num_agents)])
	for item in range(num_items):
		model += np.sum(P[:, item]) == 1

	'''
	Onjective: max prod_i sum_j (V[i,j] * P[i,j])
	'''
	obj = np.sum(V[i, j] * P[i, j] for i in range(num_agents) for j in range(num_items))
	model.objective = maximize(obj)

	'''
	Solve and check
	'''
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

def MNW_opt(valuation_matrix):
	"""
	Maximizing Nash welfare is NP-hard due to the reduction 
	from Exact Cover by 3-Sets (X3C).

	Here is the non-trivial MIP formulation proposed by [Caragiannis et al., 2016]
	The key idea is to approximate log function with piecewise linear functions,
	while no error at integral points is incurred.
	"""
	V = deepcopy(valuation_matrix)
	num_agents, num_items = V.shape
	
	model = Model(solver_name=CBC)
	
	'''
	Constraints:
		1.	P[i,j] => {0,1}
		2.  sum_j P[i,j] <= 1
	'''
	W = np.array([model.add_var(name=f'W_{i}', var_type=CONTINUOUS) for i in range(num_agents)])
	P = np.array([[model.add_var(name=f'P_{i},{j}', var_type=BINARY) for j in range(num_items)] for i in range(num_agents)])
	
	for agent in range(num_agents):
		for k in range(1,10):
			K = 2 ** k - 1
			model += W[agent] <= np.log2(K) + (np.log2(K+1) - np.log2(K)) * (V[agent] @ P[agent] - K)
		model += V[agent] @ P[agent] >= 1
	for item in range(num_items):
		model += np.sum(P[:, item]) == 1

	'''
	Onjective: max prod_i sum_j (V[i,j] * P[i,j])
	'''
	obj = np.sum(W)
	model.objective = maximize(obj)

	'''
	Solve and check
	'''
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

def MNW_local(valuation_matrix):

	return allocation, envy_matrix