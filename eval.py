import numpy as np
import sys
import argparse

from round_robin import roundRobin


def get_args():
	parser = argparse.ArgumentParser(description='Allocating indivisible items.')

	parser.add_argument('--alg', dest='algorithm', type=str, default='roundRobin', choices=['roundRobin', 'envyGraph', 'MNW', 'CSP1', 'CSPx'],
						help='Select the allocation algorithm')
	parser.add_argument('--num_agents', dest='num_agents', type=int, default='3',
						help='Specify the number of agents')
	parser.add_argument('--num_items', dest='num_items', type=int, default='7',
						help='Specify the number of items')
	parser.add_argument('--round', dest='rd', type=int, default='2',
						help='Specify the degree of rounding')

	return parser.parse_args()

def init_instance(num_agents, num_items, rd, visual=False):
	valuation_matrix = np.round(np.random.rand(num_agents, num_items), rd) * (10 ** rd)

	if visual:
		print('-----> Valuation Matrix: ')
		print(valuation_matrix)

	return valuation_matrix

def get_allocation(valuation_matrix, alg, visual=False):
	algorithm = None
	if alg == 'roundRobin':
		algorithm = roundRobin
	# # elif alg == 'envyGraph':
	# # 	algorithm = envyGraph
	# # elif alg == 'MNW':
	# # 	algorithm = MNW
	# # elif alg == 'CSP1':
	# # 	algorithm = CSP1
	# # elif alg == 'CSPx':
	# # 	algorithm = CSPx

	allocation, envy_matrix = algorithm(valuation_matrix)

	if visual:
		print('-----> Allocation Result: ')
		print(allocation)
		print('-----> Envy Result: ')
		print(envy_matrix)

	return allocation, envy_matrix


if __name__ == '__main__':
	args = get_args()
	V = init_instance(args.num_agents, args.num_items, args.rd, visual=True)
	P, envy = get_allocation(V, args.algorithm, visual=True)

