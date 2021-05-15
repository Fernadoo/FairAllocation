import numpy as np
from copy import deepcopy
from mip import *

""" 
[Maximum Utilitarian Welfare]

In fact, one can compute maximum utilitarian welfare within O(n) time
by simply assign the item to the agent who values it most.

Here is a standard MIP formulation as well as the implementation via CBC solver.
"""
def MUtilW(valuation_matrix):
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

"""
[Maximizing Nash Welfare] 

NP-hardness is obtained due to the reduction from Exact Cover by 3-Sets (X3C).

Here is the non-trivial MIP formulation proposed by [Caragiannis et al., 2016]
The key idea is to approximate log function with piecewise linear functions,
while no error at integral points is incurred.
"""
def MNW_opt(valuation_matrix): #TODO precision issues
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

"""
[MNW by local search]

A simpler iterative apporach proposed by [Nongaillard et al., 2009],
but may not guarantee to obtain global optima
"""
def rational_trans(V, P, i, trans, j):
	# print(trans)
	ex = np.zeros(V.shape[1]); ex[trans] = 1
	P_ = deepcopy(P)
	P_[i] = P[i] - ex + P[j]
	P_[j] = 0 + ex

	if V[i] @ P_[i] > V[i] @ P[i] and V[j] @ P_[j] > V[j] @ P[j]:
		return True
	else:
		return False

def social_trans(V, P, i, trans, j):
	utility = [V[i] @ P[i] for i in range(V.shape[0])]
	nw = np.prod(utility)

	ex = np.zeros(V.shape[1]); ex[trans] = 1
	P_ = deepcopy(P)
	P_[i] = P[i] - ex + P[j]
	P_[j] = 0 + ex
	utility_ = [V[i] @ P_[i] for i in range(V.shape[0])]
	nw_ = np.prod(utility_)

	if nw_ >= nw:
		return True
	else:
		return False

def MNW_local(valuation_matrix):
	V = deepcopy(valuation_matrix)
	num_agents, num_items = V.shape

	'''
	Negotiate with neighbors via contact network (currently assumed as complete graph)
	In every transaction (for agent i):
		1. Sort the bundle by the increasing order of utility
		2. Append one more to the TRANS and launch an negotiation to swap the whole bundle of another agent.
		3. If benificial, do the transaction.
	'''
	P_prev = np.zeros(shape=(num_agents, num_items))
	P = np.zeros(shape=(num_agents, num_items))
	agent = 0
	for item in range(num_items):
		P[agent, item] = 1
		agent = (agent + 1) % num_agents

	while np.any(P_prev != P):
		# print(P)
		P_prev = deepcopy(P)
		for agent in range(num_agents):
			bundle = np.where(P[agent]==1)[0].tolist()
			bundle.sort(key=lambda x: V[agent, x])
			trans = []
			for item in bundle:
				trans.append(item)
				for opponent in range(num_agents):
					if rational_trans(V, P, agent, trans, opponent) and social_trans(V, P, agent, trans, opponent):
							ex = np.zeros(num_items); ex[trans] = 1
							P_ = deepcopy(P)
							P_[agent] = P[agent] - ex + P[opponent]
							P_[opponent] = 0 + ex
							P = P_

	allocation = dict()
	for agent in range(num_agents):
		allocation[agent] = np.where(P[agent]==1)[0].tolist()

	envy_matrix = np.zeros(shape=(num_agents, num_agents))
	for agent in range(num_agents):
		for opponent in range(num_agents):
			envy_matrix[agent, opponent] = np.sum(valuation_matrix[agent] * P[opponent])

	return allocation, envy_matrix