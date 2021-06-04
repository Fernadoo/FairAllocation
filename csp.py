import numpy as np
from copy import deepcopy

"""
Class for each decision node:
    Vairable -> Item
    Domain values -> Set of agents 
"""
class searchNode():
    def __init__(self, var, value):
        self.var = var
        self.value = value
        self.children = []

"""
Class for the depth-first-search tree:
    Each level -> a decision node
"""
class searchTree():
    def __init__(self, V):
        self.V = V
        self.num_agents, self.items = V.shape
        self.P = np.zeros(shape=(self.num_agents, self.num_items))

        # For tree search
        self.tree = searchNode(None, None)
        self.current = self.tree

        # For dependency graph
        self.dependency = []

        # For symmetry breaking
        # TODO!!!
    
    def decide_next(self):
    '''
    Decide the next unvisited var (item) to try values (agents)
    '''
        return var

    def prune(self, partial_assignment, var, value):
    '''
    Given current partial policy, see if assigning value to var 
    is consistent with the partial_policy.
    Return True if the value should be pruned, return False otherwise.

    Rule 1. After deciding *var->value*, there exists one agent such
            that she will E1 (envy-up-to-one-good) some other agents even
            if all rest items are allocated to her.
    Rule 2. TODO!!!
    '''
        pass

    def deduce(self, decision_var, decision_value):
    '''
    After deciding *decision_var->decision_value*, for rest of 
    unvisited vars, see if there exists any var only getting one
    feasible value, i.e. item-i can only be allocated to agent-j.
    '''
        pass

    def get_partial_assignment(self):
        return self.P

    def constrained_search(self):
    '''
    If one consistent assignment is found, return the allocation matrix P;
    else, return None.
    ''' 
        pass

"""
Model a relaxed fair solution as a consistent assignment for CSP formulation.
CSP1 -> return once a consistent solution is found;
CSPx -> return until all solutions are found and the best one will be returned.
"""
def CSP1(valuation_matrix):
	"""
	V_ij = the value agent i holds towards item j
	"""
	V = deepcopy(valuation_matrix)
    num_agents, num_items = V.shape
    P = np.zeros(shape=(num_agents, num_items))

    search_tree = searchTree(V)
    P = search_tree.constrained_search() # An EF1 allocation always exists.

    allocation = dict()
	for agent in range(num_agents):
		allocation[agent] = np.where(P[agent]==1)[0].tolist()

	envy_matrix = np.zeros(shape=(num_agents, num_agents))
	for agent in range(num_agents):
		for opponent in range(num_agents):
			envy_matrix[agent, opponent] = np.sum(valuation_matrix[agent] * P[opponent])

	return allocation, envy_matrix

def CSPx(valuation_matrix):
	"""
	V_ij = the value agent i holds towards item j
	"""
	V = deepcopy(valuation_matrix)
    num_agents, num_items = V.shape
    P = np.zeros(shape=(num_agents, num_items))

    search_tree = searchTree(V)
    all_assignments = []
    while True:
        P = search_tree.constrained_search()
        all_assignments.append(P)

    # Choose the one that maximizes Nash welfare
    # TODO!!!

	return allocation, envy_matrix