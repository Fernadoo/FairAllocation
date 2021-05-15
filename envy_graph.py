import numpy as np
from copy import deepcopy

"""
Helper functions for graph operators
"""
def construct_envy_graph(V, P):
	"""
	Agent i envies agent j, i.e. V_i(P_j) > V_i(P_i)
	=> envy_graph[i, j] = 1 
	"""
	num_agents = V.shape[0]
	envy_graph = np.zeros(shape=(num_agents, num_agents))
	for agent in range(num_agents):
		for opponent in range(num_agents):
			if np.sum(V[agent] * P[opponent]) > np.sum(V[agent] * P[agent]):
				envy_graph[agent, opponent] = 1
	return envy_graph

def get_source_node(envy_graph):
	num_agents = envy_graph.shape[0]
	for agent in range(num_agents):
		if envy_graph[:,agent].tolist() == [0] * num_agents:
			return agent

def get_cycle(envy_graph): #TODO seems correct
	"""
	Suppose cycle looks as follows
		--> *1 --> 4
		|	       |
		|	       |
		5 <-- 6 <---
	then cycle = [1, 4, 6, 5]
	"""
	def DFS(curr, pred, G):
		neighbors = np.where(G[curr]==1)[0]
		for suc in neighbors:
			if suc in pred:
				return pred[pred.index(suc):]
			next_pred = deepcopy(pred)
			next_pred.append(suc)
			cycle = DFS(suc, next_pred, G)
			if cycle:
				return cycle
		return None

	num_agents = envy_graph.shape[0]
	for agent in range(num_agents):
		cycle = DFS(agent, [], envy_graph)
		if cycle:
			return cycle
	return None

def swap(P, cycle):
	i = 0
	tmp = deepcopy(P[cycle[0]])
	for i in range(len(cycle)):
		if i == len(cycle) - 1:
			P[cycle[i]] = tmp
		else:
			P[cycle[i]] = deepcopy(P[cycle[i+1]])

"""
Allocation algorithms based on envy graph
"""
def envyGraph(valuation_matrix):
	"""
	V_ij = the value agent i holds towards item j
	"""
	V = deepcopy(valuation_matrix)
	num_agents, num_items = V.shape
	
	P = np.zeros(shape=(num_agents, num_items))

	for item in range(num_items):
		# 0. construct the envy graph
		envy_graph = construct_envy_graph(V, P) # represented as an adjacent matrix
		
		# 1. get a source node
		src_agent = get_source_node(envy_graph)
		
		# 2. allocate one item and update the envy graph
		P[src_agent, item] = 1
		envy_graph = construct_envy_graph(V, P)
		# print(f'--- Round {item} ---')
		# print(P)
		# print(envy_graph)
		
		# 3. find a cycle and swap the bundles along the reversed direction
		cycle = get_cycle(envy_graph) # a list of agent-indices in the cycle
		if cycle:
			# print(cycle)
			swap(P, cycle)

	allocation = dict()
	for agent in range(num_agents):
		allocation[agent] = np.where(P[agent]==1)[0].tolist()

	envy_matrix = np.zeros(shape=(num_agents, num_agents))
	for agent in range(num_agents):
		for opponent in range(num_agents):
			envy_matrix[agent, opponent] = np.sum(valuation_matrix[agent] * P[opponent])

	return allocation, envy_matrix

def genEnvyGraph():
	"""
	Genralize envyGraph to allocate indivisible chores
	"""
	pass
