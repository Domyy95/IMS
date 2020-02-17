from mesa import Agent, Model
from mesa.time import SimultaneousActivation
import random
from colorama import init,Fore, Back,Style

init()

class Message:
    def __init__(self, mit, rec, const, other_mex):

        self.mit = mit
        self.rec = rec
        self.const = list(const)
        self.other_mex = other_mex.copy()

        self.f1 = 0  # value of the best option variable from mit to rec with xrec = 0
        self.f2 = 0  # value of the best option variable from mit to rec with xrec = 1

        # if the receiver has a uniqueID < then the sender is useful to change the 2 line in the center of the
        # constraint
        if (int(mit) < int(rec)):
            self.const[1], self.const[2] = self.const[2], self.const[1]

        # const with the variable rec = 0
        n1 = self.const[0]
        n2 = self.const[1]

        # const with the variable rec = 1
        n3 = self.const[2]
        n4 = self.const[3]

        for m in self.other_mex:

            n1 = float(n1) + float(m.f1)
            n2 = float(n2) + float(m.f2)
            n3 = float(n3) + float(m.f1)
            n4 = float(n4) + float(m.f2)

        # print('-----------------------------------------------')

        self.f1 = float(max(n1, n2))
        self.f2 = float(max(n3, n4))

        # print(self.f1,self.f2)

        # term to normalize otherwise the algorithm never stop
        alpha = (self.f1 + self.f2) / 2
        self.f1 = self.f1 - alpha
        self.f2 = self.f2 - alpha

    def equal(self, m):
        if (m.f1 == self.f1 and m.f2 == self.f2):
            return True

    def to_string(self):
        # print('from ' + str(self.mit) + ' to ' + str(self.rec) + ': ' + str(self.f1) + ' , ' + str(self.f2))
        print('from ' + str(self.mit) + ': ' + str(self.f1) + ' , ' + str(self.f2))
        # per controllare es quaderno 
        # print('from ' + str(int ( self.mit) + 1) + ' to ' + str( int (self.rec) + 1) + ': ' + str(self.f1) + ' - ' + str(self.f2))


class Agent(Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, neighbors, const):
        super().__init__(unique_id, model)

        self.best_value = 0
        self.neighbors = neighbors
        self.const = const

        # IMPORTANT: For each constraints i assume that the first variable  
        # is always the one with the lower uniqueID  

        self.last_mex = []  # Last saved messages to control the end conditions
        self.mex = []  # received messages
        self.to_send_mex = []

    def to_string_neighbors(self):
        print("Agent: " + str(self.unique_id))
        j = 0
        for i in self.neighbors:
            print(i + " " + str(self.const[j]))
            j = j + 1

    def to_string_received_messages(self):
        print(" -- Agent " + str(self.unique_id) + ' --')
        j = 0
        print('     x' + str ( self.unique_id )  + '   0     1')
        for i in self.mex:
            i.to_string()

    def to_string_actual_result(self):
        print(" -- Agent " + str(self.unique_id) + ': ' + str(self.best_value))

    def can_stop(self):
        stop = True
        for i in range(len(self.mex)):
            stop = stop and self.mex[i].equal(self.last_mex[i])

        return stop

    def find_mex_receiver(self, list_mex, n):
        for m in list_mex:
            if (m.rec == n):
                return m

    def find_mex_sender(self, list_mex, n):
        for m in list_mex:
            if (int(m.mit) == int(n)):
                return m

    def compute_new_best_value(self):
        x0 = 0
        x1 = 0
        for m in self.mex:
            x0 = x0 + m.f1
            x1 = x1 + m.f2

        if (x0 > x1):
            self.best_value = 0
        elif (x1 > x0):
            self.best_value = 1
        else:
            self.best_value = random.randint(0, 1)

    # compute messages to all my neighbors
    def step(self):

        self.last_mex.clear()
        self.last_mex = self.mex.copy()
        self.mex.clear()
        self.to_send_mex.clear()

        for to in self.neighbors:
            last = self.last_mex.copy()
            # i don't have to take into account the message from rec received before
            for d in last:
                if (int(d.mit) == int(to)):
                    last.remove(self.find_mex_sender(last, to))

            # i built the message
            m = Message(self.unique_id, to, self.const[self.neighbors.index(str(to))], last)
            # m.to_string()
            self.to_send_mex.append(m)

        # for a in self.to_send_mex:
        #    print(a.to_string())

        # self.to_string_received_messages()

    # Compute my best variable value and send all the messages for the next step
    def advance(self):
        for to in self.neighbors:
            a = self.model.schedule.agents[int(to)]
            a.mex.append(self.find_mex_receiver(self.to_send_mex, to))

        # self.to_string_received_messages()


class Model(Model):
    """A model with some number of agents."""

    def __init__(self, N, graph, const):
        self.num_agents = N
        self.schedule = SimultaneousActivation(self)
        self.const = const

        # Create agents
        for i in range(self.num_agents):
            l = []
            conn = []
            for n in graph[str(i)]:
                l.append(n)
                conn.append(const[const.index((n, str(i))) + 1])

            a = Agent(i, self, l, conn)
            self.schedule.add(a)

    def to_string_actual_message_situation(self):
        print(Back.BLUE +'\nReceived messages: ')
        print(Style.RESET_ALL)
        for a in self.schedule.agents:
            a.to_string_received_messages()

    def to_string_actual_solution(self):

        print(Back.GREEN + '\nActual Solution: ')
        print(Style.RESET_ALL)
        for a in self.schedule.agents:
            a.to_string_actual_result()
        total = 0
        for i in range(0,len ( self.const ),4):
            v1 = self.schedule.agents[int ( self.const[i][0] )].best_value
            v2 = self.schedule.agents[int ( self.const[i][1] )].best_value
            r = 0
            if    v1==0 and v2==0: r = 0
            elif  v1==0 and v2==1: r = 1
            elif  v1==1 and v2==0: r = 2
            else:                  r = 3
            # print('adding '+self.const[i+1][r])
            total = total + int (self.const[i+1][r])

        print('    Sum(Fij) = ' + str( total ))


    def can_stop(self):
        stop = True
        for a in self.schedule.agents:
            stop = stop and a.can_stop()

        return stop

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

        for a in self.schedule.agents:
            a.compute_new_best_value()

        self.to_string_actual_message_situation()
        self.to_string_actual_solution()

        if (self.schedule.steps == 1):
            return False

        return self.can_stop()