#############################################
#
# this file contains the network structure and agent distribution (incl. destination preferences)
#
#############################################


# TODO: manually type in flow in each edge

# sperate flow definition
limited     = 1
semilimited = 5
unlimited   = 10


# nodes and edges
fatsodta_nodes = [
    ("Q1", {'type': 'source', 'total_cap': -1, 'agents': []}),
    ("Q2", {'type': 'source', 'total_cap': -1, 'agents': []}),
    ("Q3", {'type': 'source', 'total_cap': -1, 'agents': []}),
    ("C1", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C2", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C3", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C4", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C5", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C6", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C7", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C8", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C9", {'type': 'merging', 'total_cap': 10, 'agents': []}), ##
    ("C10", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C11", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C12", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C13", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C14", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C15", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C16", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C17", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C18", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C19", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C20", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C21", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C22", {'type': 'merging', 'total_cap': 10, 'agents': []}),
    ("C23", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C24", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C25", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C26", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C27", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C28", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C29", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C30", {'type': 'diverging', 'total_cap': 10, 'agents': []}),
    ("C31", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C32", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("C33", {'type': 'ordinary', 'total_cap': 10, 'agents': []}),
    ("S1", {'type': 'sink', 'total_cap': -1, 'agents': []}),
    ("S2", {'type': 'sink', 'total_cap': -1, 'agents': []}),
    ("S3", {'type': 'sink', 'total_cap': -1, 'agents': []}),
    ("Super", {'type': 'sink', 'total_cap': -1, 'agents': []})
]
fatsodta_edges = [
    ("Q1","C1", {'flow': -1}),
    ("C1","C2", {'flow': unlimited}),
    ("C2","C3", {'flow': unlimited}),
    ("C2","C4", {'flow': semilimited}),         #- semilimited
    ("C3","C5", {'flow': unlimited}),
    ("C4","C9", {'flow': unlimited}),
    ("C5","C6", {'flow': unlimited}),
    ("C6","C7", {'flow': unlimited}),
    ("C7","C8", {'flow': unlimited}),
    ("C8","C9", {'flow': unlimited}),
    ("C9","C10", {'flow': unlimited}),
    ("C10","C11", {'flow': unlimited}),
    ("C11","C12", {'flow': unlimited}),
    ("C11","C13", {'flow': limited}),           ## limited
    ("C11","C14", {'flow': semilimited}),       #- semilimited
    ("C12","C15", {'flow': unlimited}),
    ("C13","C18", {'flow': unlimited}),
    ("C14","C31", {'flow': unlimited}),
    ("C15","C16", {'flow': limited}),           ## limited
    ("C15","C17", {'flow': semilimited}),       #- semilimited
    ("C16","C20", {'flow': unlimited}),
    ("C17","C21", {'flow': unlimited}),
    ("C17","C22", {'flow': limited}),           ## limited
    ("C18","C19", {'flow': unlimited}),
    ("C19","C22", {'flow': unlimited}),
    ("C20","S1", {'flow': unlimited}),
    ("C21","S2", {'flow': -1}),
    ("C22","S3", {'flow': -1}),
    ("C23","C1", {'flow': limited}),            ## limited
    ("C23","C24", {'flow': unlimited}),
    ("C24","C25", {'flow': unlimited}),
    ("C25","C26", {'flow': unlimited}),
    ("C26","C27", {'flow': unlimited}),
    ("C27","C28", {'flow': unlimited}),
    ("C28","C29", {'flow': unlimited}),
    ("C29","C30", {'flow': unlimited}),
    ("C30","C10", {'flow': semilimited}),       #- semilimited
    ("C30","C14", {'flow': unlimited}),
    ("C31","C32", {'flow': unlimited}),
    ("C32","C33", {'flow': unlimited}),
    ("C33","C19", {'flow': unlimited}),
    ("Q2","C23", {'flow': -1}),
    ("Q3","C12", {'flow': limited}),            ## limited
    ("S1","Super", {'flow': -1}),
    ("S2","Super", {'flow': -1}),
    ("S3","Super", {'flow': -1})
]

# Input for FATSODTA network
source_nodes = ["Q1","Q2","Q3"] # source nodes, where agents start
sink_nodes = ["S1", "S2", "S3"] # sink nodes, where agents end

# number of agents with (o,d) for all specified (o,d) pairings
demand_dict = {
    source_nodes[0]: {sink_nodes[0]: 10, sink_nodes[1]: 10, sink_nodes[2]: 10},
    source_nodes[1]: {sink_nodes[0]: 10, sink_nodes[1]: 10, sink_nodes[2]: 10},
    source_nodes[2]: {sink_nodes[0]: 10, sink_nodes[1]: 30, sink_nodes[2]: 10}
}


# generated with random.seed(4844130552041760)
# agent_dict = create_agent_dict(source_nodes, sink_nodes, demand_dict)
#      agent ID: ('source node', 'sink preference')
agent_dict = {
    0: ('Q1', 'S1'),
    1: ('Q1', 'S1'),
    2: ('Q1', 'S2'),
    3: ('Q1', 'S2'),
    4: ('Q1', 'S3'),
    5: ('Q1', 'S2'),
    6: ('Q1', 'S3'),
    7: ('Q1', 'S3'),
    8: ('Q1', 'S1'),
    9: ('Q1', 'S2'),
    10: ('Q1', 'S2'),
    11: ('Q1', 'S2'),
    12: ('Q1', 'S2'),
    13: ('Q1', 'S1'),
    14: ('Q1', 'S3'),
    15: ('Q1', 'S2'),
    16: ('Q1', 'S3'),
    17: ('Q1', 'S2'),
    18: ('Q1', 'S3'),
    19: ('Q1', 'S1'),
    20: ('Q1', 'S2'),
    21: ('Q1', 'S3'),
    22: ('Q1', 'S1'),
    23: ('Q1', 'S1'),
    24: ('Q1', 'S1'),
    25: ('Q1', 'S1'),
    26: ('Q1', 'S3'),
    27: ('Q1', 'S3'),
    28: ('Q1', 'S1'),
    29: ('Q1', 'S3'),
    30: ('Q2', 'S1'),
    31: ('Q2', 'S2'),
    32: ('Q2', 'S2'),
    33: ('Q2', 'S2'),
    34: ('Q2', 'S2'),
    35: ('Q2', 'S2'),
    36: ('Q2', 'S3'),
    37: ('Q2', 'S3'),
    38: ('Q2', 'S1'),
    39: ('Q2', 'S3'),
    40: ('Q2', 'S1'),
    41: ('Q2', 'S2'),
    42: ('Q2', 'S1'),
    43: ('Q2', 'S2'),
    44: ('Q2', 'S2'),
    45: ('Q2', 'S3'),
    46: ('Q2', 'S1'),
    47: ('Q2', 'S3'),
    48: ('Q2', 'S3'),
    49: ('Q2', 'S3'),
    50: ('Q2', 'S1'),
    51: ('Q2', 'S2'),
    52: ('Q2', 'S1'),
    53: ('Q2', 'S1'),
    54: ('Q2', 'S1'),
    55: ('Q2', 'S3'),
    56: ('Q2', 'S3'),
    57: ('Q2', 'S2'),
    58: ('Q2', 'S1'),
    59: ('Q2', 'S3'),
    60: ('Q3', 'S2'),
    61: ('Q3', 'S2'),
    62: ('Q3', 'S3'),
    63: ('Q3', 'S2'),
    64: ('Q3', 'S2'),
    65: ('Q3', 'S2'),
    66: ('Q3', 'S1'),
    67: ('Q3', 'S2'),
    68: ('Q3', 'S2'),
    69: ('Q3', 'S2'),
    70: ('Q3', 'S2'),
    71: ('Q3', 'S2'),
    72: ('Q3', 'S3'),
    73: ('Q3', 'S1'),
    74: ('Q3', 'S1'),
    75: ('Q3', 'S3'),
    76: ('Q3', 'S3'),
    77: ('Q3', 'S2'),
    78: ('Q3', 'S1'),
    79: ('Q3', 'S2'),
    80: ('Q3', 'S2'),
    81: ('Q3', 'S3'),
    82: ('Q3', 'S2'),
    83: ('Q3', 'S2'),
    84: ('Q3', 'S2'),
    85: ('Q3', 'S1'),
    86: ('Q3', 'S2'),
    87: ('Q3', 'S2'),
    88: ('Q3', 'S1'),
    89: ('Q3', 'S2'),
    90: ('Q3', 'S3'),
    91: ('Q3', 'S3'),
    92: ('Q3', 'S2'),
    93: ('Q3', 'S3'),
    94: ('Q3', 'S1'),
    95: ('Q3', 'S2'),
    96: ('Q3', 'S2'),
    97: ('Q3', 'S3'),
    98: ('Q3', 'S3'),
    99: ('Q3', 'S2'),
    100: ('Q3', 'S2'),
    101: ('Q3', 'S2'),
    102: ('Q3', 'S2'),
    103: ('Q3', 'S1'),
    104: ('Q3', 'S1'),
    105: ('Q3', 'S1'),
    106: ('Q3', 'S2'),
    107: ('Q3', 'S2'),
    108: ('Q3', 'S2'),
    109: ('Q3', 'S2')
}
