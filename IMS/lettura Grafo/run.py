from model import *
import numpy as np
import matplotlib.pyplot as plt
import sys 
from collections import defaultdict

graph = defaultdict(list) 

def parse_input(file):

	link = []
	const = []
	with open(file, 'r') as f:
		for i, line in enumerate(f):
			if i == 0: 
				N,L = line.split(' ')       
			else: 
				row = line.split(' ')
				n1,n2 = row[0].split('-')
				link.append((n1,n2))
				c = row[1],row[2],row[3],row[4]
				const.append(((n1,n2),c))

	return N, L, link, const

def built_graph(N,link):
	for n1,n2 in link:
		graph[n1].append(n2)
	print(graph)


if __name__ == '__main__':
	N,L,link,const = parse_input(sys.argv[1])
	built_graph(N,link)