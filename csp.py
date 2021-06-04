import numpy as np
from copy import deepcopy

"""
Class for each decision node:
    Vairable -> Item
    Domain values -> Set of agents 
"""
class searchNode():
    def __init__(self):
        self.P


"""
Class for the depth-first-search tree:
    Each level -> a decision node
"""
class searchTree():
    def __init__(self, V):
        self.V = V
        self.num_agents, self.items = V.shape


    def prune(self):
    pass

    def deduce(self):
    pass

    def get_assignment(self,)
        pass


def CSP1(valuation_matrix):
	"""
	V_ij = the value agent i holds towards item j
	"""
	V = deepcopy(valuation_matrix)
	num_agents, num_items = V.shape
	
	P = np.zeros(shape=(num_agents, num_items))



    allocation = dict()
	for agent in range(num_agents):
		allocation[agent] = np.where(P[agent]==1)[0].tolist()

	envy_matrix = np.zeros(shape=(num_agents, num_agents))
	for agent in range(num_agents):
		for opponent in range(num_agents):
			envy_matrix[agent, opponent] = np.sum(valuation_matrix[agent] * P[opponent])

	return allocation, envy_matrix