import numpy as np
from copy import deepcopy

def roundRobin(valuation_matrix):
	"""
	V_ij = the value agent i holds towards item j
	"""
	V = deepcopy(valuation_matrix)
	num_agents, num_items = V.shape

	allocation = dict()
	for agent in range(num_agents):
		allocation[agent] = []
	
	P = np.zeros(shape=(num_agents, num_items))

	agent = 0
	while num_items > 0:
		choice = np.argmax(V[agent])
		allocation[agent].append(choice)
		P[agent, choice] = 1
		V[:,choice] = -999
		num_items -= 1
		agent = (agent + 1) % num_agents

	envy_matrix = np.zeros(shape=(num_agents, num_agents))
	for agent in range(num_agents):
		for opponent in range(num_agents):
			envy_matrix[agent, opponent] = np.sum(valuation_matrix[agent] * P[opponent])

	return allocation, envy_matrix

def doubleRoundRobin(valuation_matrix):
	"""
	Extended for indivisible chore division
	"""
	pass


