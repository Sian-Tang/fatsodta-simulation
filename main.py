import itertools
import networkx as nx
import copy
import sys
import random
from fatsodta_network import *
from simulation import *


# Generate a graph
G = nx.DiGraph()
G.add_nodes_from(fatsodta_nodes)
G.add_edges_from(fatsodta_edges)
sink_list = sink_nodes
source_list = source_nodes
assign_p_value(G, sink_list)
assign_block_status(G)
create_agents(agent_dict,G)

max_time = 80

Results, time_result, result_function_value_list = run_simulation(max_time, G)

agents_list = Agents.get_agent_list()

for node in G.nodes:
    print(node, G.nodes[node]['agents'])
    #print('\n')

sum_detour = 0
for agent_id in agents_list:
    agent = Agents.get(agent_id)
    print('\nAgent', agent_id, '('+str(agent.path[0])+','+str(agent.destination_node)+')')
    print('Detour counter:', agent.detour_counter)
    sum_detour += agent.detour_counter
    print('{path: wait}:', agent.node_wait)

print('\nEvacuation time:', len(result_function_value_list)-2)  # t starts at 0 and goes until every agent reaches sink
print('Resulting function value:', sum(result_function_value_list))
print('Number of times a detour was taken:', sum_detour)
print('Number of agent not in sink for every t:',result_function_value_list)
while True:
    print('\nChoose one of the following options:')
    print('[result]: show result of simulation')
    print('default: exit program')
    input_end = input()
    if input_end == 'result':
        show_result(time_result, Results)
    else:
        break

# TODO: *optional
#     i. conditional node transition of agents || conditions: waiting timer, stress level, age, driving experience, etc. (examples)
#    ii. agent or node priority in merging node
#   iii. extend network with loops (direction of travel going two ways like in real szenario)
