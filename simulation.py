import itertools
import networkx as nx
import copy
import sys
import random

## --------------------------------------- ##
## ------------ class Agents ------------- ##
## --------------------------------------- ##

# @Class Agents
class Agents:

    # auto increment agent ID
    # https://stackoverflow.com/questions/1045344/how-do-you-create-an-incremental-id-in-a-python-class
    id_iter = itertools.count()
    instances = []

    def __init__(self, G, source_node, destination_node = None):
        self.id = next(Agents.id_iter)          # automatic agent ID
        self.current_node = source_node         # current node where agent is at the moment
        self.path = [source_node]               # path stores all the nodes until the sink is reached
        self.node_wait = {self.current_node: 0} # every visited node gets a wait counter
        if destination_node in G.nodes:         # gets a fixed destination_node
            self.destination_node = destination_node
        else:
            self.destination_node = None
        self.blocked = False                    # True: agent is blocked | False: agent can do action
        self.status = True                      # True: waiting | False: traversed
        self.detour_counter = 0                 # number of times, agent took a detour instead of optimal route instead
        Agents.instances.append(self)           # add instance to list in class

        G.nodes[self.current_node]['agents'].append(self.id)
        #add_agent(G, self.current_node, self.id)   # add agent to dictionary and update agent in network
        print('Successfully created agent', self.id)

    # find index of node in path[]
    # -- don't need this anymore because self.node_wait is dictionary --
    def get_node_index(self, node):
        # look at every entry of path[index] for 'node' and return index
        for index in range(len(self.path)):
            if self.path[index] == node:
                return index

        # error message - debugging
        print('Node can not be found in the current path of node', node)
        print('Path:', list(self.path))
        return None


    # update waiting time in current node
    def waiting(self):
        self.node_wait[self.current_node] += 1

    # add next node to path, update agent's current node, and initialize waiting node
    def add_to_path(self, next_node):
        self.path.append(next_node)
        self.current_node = next_node
        self.node_wait[next_node] = 0


    # https://stackoverflow.com/questions/53449804/python-find-instance-of-a-class-by-value
    # get function: get agent instance with agent_id as input
    @classmethod
    def get(cls, id):
        for inst in cls.instances:
            if inst.id == id:
                return inst
    # example: agent0 = Agents(G, 0)   // id = 0 (auto incr id)
    #          agent1 = Agents(G, 0)   // id = 1 (auto incr id)
    #          agent2 = Agents(G, 0)   // id = 2 (auto incr id)
    #          instance = Agents.get(2) // get agent with id = 2
    #          print(instance[0].id)
    #       >> 2

    # returns list of all agent_ids
    @classmethod
    def get_agent_list(cls):
      return [inst.id for inst in cls.instances]



# update the following:
#       current_node
#       path
#       initialize waiting couner
#       status
def update_agent(agent, next_node):

    agent.current_node = next_node
    agent.path.append(next_node)
    agent.node_wait[next_node] = 0
    agent.status = False
    agent.blocked = True



# Run simulation for one time step.
# Iterates through the nodes recursively until it reaches a sink node.
# After the sink node it will return capacity and node information to the previous node.
# Every other node will then update agents depending on whether the successor node has available capacity
def simulation(G, current_list):

    function_value = 0
    breaker = True
    successor_list = []
    sink_list = get_type_list(G, 'sink')


    for current_node in current_list: # current list only consists of multiple elements when first called with source nodes

            # call simulation recursively and update network from back (sink) to front (source)
            for suc_node in G.successors(current_node):
                if G.nodes[suc_node]['type'] == 'sink' or G.nodes[suc_node]['blocked']:
                    # do nothing
                    continue
                else:
                    simulation(G, [suc_node])

            ## recursion ends here - now update agents in node ##

            # get agents (front to back) in node until blocked agent
            agent_list = []
            for agent_id in G.nodes[current_node]['agents']:
                if Agents.get(agent_id).blocked:
                    break
                else:
                    agent_list.append(agent_id)

            # if agent_list is empty then there are no agents or first agent is blocked
            if not agent_list:
                continue # nothing further to do with this node go to next iteration in current_list

            # temporary dictionary that keeps track of capacity and flow value
            suc_node_capacity_flow_count = {}
            for suc_node in G.successors(current_node):
                capacity    = G.nodes[suc_node]['total_cap'] - len(G.nodes[suc_node]['agents'])
                flow        = G[current_node][suc_node]['flow']
                suc_node_capacity_flow_count[suc_node] = {'capacity': capacity, 'flow': flow}

            # work through all agents now
            for agent_id in agent_list:
                blocked = False
                agent = Agents.get(agent_id)
                if agent.blocked:
                    break
                destination_node = agent.destination_node
                # sort successor node in p_value order
                sorting_dict = {}
                for suc_node in G.successors(agent.current_node):
                    p_value = G.nodes[suc_node]['p_value'].get(destination_node)
                    if p_value != None:
                        sorting_dict[suc_node] = p_value
                    else:
                        continue # successor node doesn't lead to sink node so we skip

                # sort successor list by p_value
                successor_list = sorted(sorting_dict, key = lambda x: sorting_dict[x], reverse = False)

                detour_status = False

                # check if capacity and flow allows agent to drive to suc_node otherwise check next suc_node
                for suc_node, counter in zip(successor_list, reversed(range(0,len(successor_list)))):
                    capacity    = suc_node_capacity_flow_count[suc_node]['capacity']
                    flow        = suc_node_capacity_flow_count[suc_node]['flow']
                    if capacity != 0 and flow != 0:
                        # do update
                        update_node(agent, G, suc_node, agent_list)
                        update_agent(agent, suc_node)
                        suc_node_capacity_flow_count[suc_node]['capacity']  -= 1
                        suc_node_capacity_flow_count[suc_node]['flow']      -= 1
                        if detour_status:
                            agent.detour_counter += 1
                        break
                    else:
                        detour_status = True
                        if counter == 0:
                            # block agent, because no node is available
                            detour_status = False # all detour options are blocked as well
                            agent.blocked = True
                            blocked = True
                            tmp_agent_list = G.nodes[current_node]['agents'].copy()
                        continue


                if blocked:
                    # agent is blocking node. other agents have to wait as well
                    for tmp_agent_id in tmp_agent_list:
                        tmp_agent = Agents.get(tmp_agent_id)
                        tmp_agent.blocked = True

                    break

    # function value = number of all agents that did not reach a sink node yet
    for node in G.nodes:
        if G.nodes[node]['type'] != 'sink':
            function_value += len(G.nodes[node]['agents'])

    return G, function_value


# executes simulation() multiple times until evacuation finishes or max_time is reached
# @Input max_time: maximum time of executing the simulation
# @Input G: Graph G
# @Input population: number of agents in source node at time t_0
# @Output T: list of graph for each time step
# @Output time: last time step
def run_simulation(max_time, G):

    time = 0                                            # time variable
    T = [None]*(max_time+1)                             # T[] holds graph G at every time step
    T[0] = copy.deepcopy(G)                             # T[0] holds initial state of G
    population = sum_attribute(G, 'source', 'agents')   # entire evacuation population (time = 0)
    result_function_value_list = [population]                # sum of function value after every simulation
    tmp_function_value = 0
    source_list = get_type_list(G, 'source')

    # runs simulation() multiple times until evacuation finishes or max_time is reached
    while time < max_time and sum_attribute(G, 'sink', 'agents') < population:
        # prints starting text for every simulation run
        # starting_text(time)

        agent_list = Agents.get_agent_list()            # get list of all agent ids
        H, tmp_value = simulation(G, source_list)       # execute simulation()


        #print('Successfully executed simulation', time)
        time += 1
        T[time] = copy.deepcopy(H)                      # T[time] holds graph state at each timepoint "time"

        result_function_value_list.append(tmp_value)         # list of function value for every timestep

        # update waiting counter for all waiting agents
        for agent_id in Agents.get_agent_list():
            agent = Agents.get(agent_id)                # get agent instance
            if agent.status:                            # status = True: waiting | False: traversed
                agent.waiting()                         # increase waiting count by 1
            else:
                agent.status = True

        # unblock all agents that are not in sink node
        for agent_id in Agents.get_agent_list():
            agent = Agents.get(agent_id)                # get agent instance
            if G.nodes[agent.current_node]['type'] != 'sink':
                agent.blocked = False                   # unblock agent (for next time step)

        # simulation ending
        if time == max_time:
            print_newline()
            print('Simulation has been exited due to maximum number of simulation reached.')
            print('Resulting function value:', sum(result_function_value_list))
        elif sum_attribute(G, 'sink', 'agents') == population:
            print_newline()
            print('Simulation has been completed as every agent reached a sink node.')
            print('Resulting time:', time)
            print('Resulting function value:', sum(result_function_value_list))

#   result_function_value = sum(result_function_value_list)
    # prints number of agents that reached sink node
    print(sum_attribute(G, 'sink', 'agents'), 'agents reached a sink node of a total of', population, 'agents.')
    return T, time, result_function_value_list



# output: agent_dict
# creates a dictionary the following: {'agent_id': ('source_node', 'sink_node')}
#   example: {0: ("Q1", "S3"), 1: ("Q1", "S1"), 2: ("Q2", "S2"), 3: ("Q3", "S1")}
def create_agent_dict(source_nodes, sink_nodes, demand_dict):
    agent_list_dict = {}

    for source_node, i in zip(demand_dict,range(len(demand_dict))):
        agent_list_dict[source_node] = [] # {"Q1": ["S2","S2","S1","S3"], "Q2": ["S1","S3","S1","S1","S2"], ...}
        for sink_node in demand_dict[source_node]:
            for j in range(demand_dict[source_node][sink_node]):
                agent_list_dict[source_node].append(sink_node)

    agent_dict = {}

    agent_id = 0
    for source_node in agent_list_dict:
        random.shuffle(agent_list_dict[source_node]) # for every source shuffle the order of the destination list
        for sink_node in agent_list_dict[source_node]:
            agent_dict[agent_id] = (source_node,sink_node)
            agent_id += 1

    return agent_dict


# input: agent_dict = {agent: {'source', 'sink'}}, Graph G
# creates instances of class Agents (create agents with specified (o,d) for our simulation)
def create_agents(agent_dict, G):
    for agent in agent_dict.keys():
        Agents(G, agent_dict[agent][0], agent_dict[agent][1])


# each node in graph G gets a p_value per sink node (as attribute) which represents the distance between each node with each sink_node
# sink nodes only have their own p_value = 0
def assign_p_value(G,sink_list):
    # add dictionary in each node that holds the p value for each sink node
    for node in G.nodes:
        nx.set_node_attributes(G,{node: {'p_value': {}}})


    for sink_node in sink_list:
        for node in G.nodes:
            if node != "Super":
                try:
                    p_value = nx.shortest_path_length(G,node,sink_node)
                    G.nodes[node]['p_value'][sink_node] = p_value
                except Exception as e:
                    G.nodes[node]['p_value'][sink_node] = None
                #print(e)


# adds a block attribute to every node
# default value is False
def assign_block_status(G):
    for node in G.nodes:
        nx.set_node_attributes(G,{node: {'blocked': False}})


# get a list of nodes of a specified type
# example get_type_list(G, 'source') returns a list of all 'source' nodes
def get_type_list(G, type):

    # get list of every node in graph G
    nodes_list = list(G.nodes)

    # create a temporary graph (empty)
    H = nx.Graph()

    # check each node in graph G if it is the specified type
    # if node matches to specified type -> add it to temporary graph
    for node in nodes_list:
        if G.nodes[node]['type'] == type:

            # check if node is already in temporary graph
            if node not in H:

                # add node to temporary graph
                H.add_nodes_from([
                    (node, {'type': type})
                    ])
    # returns list of nodes with specified type (input)
    return list(H.nodes)


# return sum of specified attribute of certain types of nodes
# example: g_sum_attribute(G, 'source', 'capacity') returns sum of capacity
def sum_attribute(G, type, attribute):
    sum = 0
    for node in G.nodes:
        if G.nodes[node]['type'] == type:
            if isinstance(G.nodes[node][attribute], list):
                sum += len(G.nodes[node][attribute])
            else:
                sum += G.nodes[node][attribute]
    return sum


# update current_node and successor node when agent goes to next node
# @Input agent: is instance of class 'Agents'
# @Input agent_node_dict: is global dictionary with information about {nodes: {agents, {prenodes: 'flow'}}}
# @Input next_node: is successor node for agent
def update_node(agent, G, next_node, agent_list):
    if G.nodes[agent.current_node]['agents'][0] != agent.id:
        print(agent.id)
        print(G.nodes[next_node]['agents'][0])
        print(G.nodes[next_node]['agents'])
        print(G.nodes[next_node])
        print('agent to be removed that is not first in queue!')
        sys.exit()
    G.nodes[next_node]['agents'].append(agent.id)               # add agent in next node queue
    G.nodes[agent.current_node]['agents'].pop(0)                # removes agent from current node



# shows the result: every node at specific time 't' and their attributes; node type, total capacity, number of agents in node
# @Input time: is the number of times that the simulation has been executed
# @Input Results[]: holds the resulting graphs at every time step t in [0,time]
def show_result(time, Results = []):

    # check if simulation has been executed at least once
    if not Results:
        print('No results available.')
        print('You need to run the simulation first. Choose option [run] by typing: run')
        return

    else:
        while True:
            # pick a time 't' between [0,time] where time is the number of times the simulation was executed
            print('At what time t do you want to see the result?')
            print('Choose t between [ 0,', time, ']: ')
            t = input()

            # check if input is numeric and in [0,time]
            if not t.isnumeric() or int(t) < 0 or int(t) > time:
                print('Invalid input.')
            else:

                t = int(t)
                print('TIME:', t)

                # Results: print nodes
                print('-- Nodes of graph --')
                for node in Results[t].nodes:
                    print('node', node, ':', Results[t].nodes[node])

                # Results: print edges
                print('-- Edges of graph --')
                for edge_start, edge_end in Results[t].edges:
                    print('edge (', edge_start, ',', edge_end, '):', Results[t][edge_start][edge_end])

                break



# some basic functions
def print_newline():
    print('\n')
def starting_text(time):
    print_newline()
    print('######################################')
    print('#######  start simulation', time, ' #########')
    print('######################################')

#################################
## ----- to be featured ------ ##
#################################

# condition function is used for additional special case traversal -> e.g. human behaviour
def condition(G, agent, current_node, suc_node, agent_list):
    wait = agent.node_wait[current_node]
    capacity = G.nodes[suc_node]['total_cap'] - len(G.nodes[suc_node]['agents'])
    flow = G[current_node][suc_node]['flow']

    base_condition = False
    if flow != 0 and capacity != 0 and agent.id in agent_list:
        base_condition = True

    # insert additional condition(s) after base_condition
    if base_condition and wait > 1:
        return True
    else:
        return False
