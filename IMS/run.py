from model import *
from collections import defaultdict
from colorama import init, Back,Style
from tabulate import tabulate
import sys
import networkx as nx
import matplotlib.pyplot as plt
import time
import threading
import os


init()
sleep_time = 1

class myThread (threading.Thread):
    def __init__(self, threadID, name,g):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.g = g

    def run(self):
        G = nx.Graph()
        for k, v in self.g.items():
            G.add_node(k)
            for edge in v:
                G.add_edge(k, edge)
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.show()

    def close(self):
        plt.close('all')

def parse_input(file):
    links = []
    constraints = []
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                N, L = line.split(' ')
            else:
                row = line.split(' ')
                n1, n2 = row[0].split('-')
                links.append((n1, n2))
                c = row[1], row[2], row[3], row[4]
                constraints.append((n1, n2))
                constraints.append(c)
                constraints.append((n2, n1))
                constraints.append(c)

    return N, L, links, constraints


def built_graph(N, link):
    for n1, n2 in link:
        graph[n1].append(n2)
        graph[n2].append(n1)

    return graph

if __name__ == '__main__':
    file_name = sys.argv[1]
    N, L, link, const = parse_input(file_name)

    step = sys.argv[2]
    if len(sys.argv) == 4:
        sleep_time = sys.argv[3]

    graph = defaultdict(list)
    graph = built_graph(N, link)

    thread1 = myThread(1, "Thread-1",graph)
    thread1.start()

    # draw_graph(graph)

    file = open(file_name.split('.')[0] + '_Constraints.txt', "w")

    for i in range(0,len(const),4):
        x1 = const[i][0]
        x2 = const[i][1]
        file.write(tabulate([['0', '0', const[i+1][0] ], ['0', '1', const[i+1][1] ],['1', '0', const[i+1][2] ],['1', '1', const[i+1][3] ]], headers=['x'+x1, 'x'+x2,'F'+x1+'-'+x2], tablefmt='orgtbl'))
        file.write('\n\n')

    file.close()
    time.sleep(1)
    model = Model(int(N), graph, const)
    stop = False
    '''
    for i in range(int(step)):
        if (stop is True):
            break

        print(Back.RED + '\n' + '-' * 45 + 'STEP ' + str(i) + ' ' + '-' * 45)
        print(Style.RESET_ALL)
        stop = model.step()
        time.sleep(int(sleep_time))
    '''
    while model.schedule.steps < int(step) and (stop is not True) :

        print(Back.RED + '\n' + '-' * 45 + 'STEP ' + str(model.schedule.steps+1) + ' ' + '-' * 45)
        print(Style.RESET_ALL)
        stop = model.step()
        time.sleep(int(sleep_time))

    print(Back.YELLOW + '\n' + 'FINAL OUTCOME \nDONE IN ' + str(model.schedule.steps ) + ' STEPS' )
    # model.to_string_actual_solution()
    print(Style.RESET_ALL)
    print()
    os.system("pause")
