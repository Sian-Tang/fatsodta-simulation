## Introduction ##
Main part of bachelor thesis was to implement a simulation in the field of evacuation planning. 
An agentbased simulation based on the model fixed arrival time system optimal dynamic traffic assignment (FATSODTA) with the additional feature of human behaviour.

## Tools ##
The simulation is implemented with python using NetworkX. 


## Description ##
The simulation runs on a graph model (represents traffic network) with nodes (road sections) and edges (links road sections). 
Goal of the model is to minimize the function that sums up the number of agents on the network that have not reached a sink (safe zone).

Two human behaviours were introduced in the simulation: 
1. each agent has a preffered sink (multiple sources/sinks in network)
Challenge of this behaviour is the introduction of the FIFO (first in, first out) principle. The order of agents with their pref. sinks has to be taken into account 
when updating the network. Therefore a queue is introduced in every node, which prevents improper overtakes in congestions.
2. agents are allowed to drive detour 
The capacity of the nodes are limited, therefore agents can drive a detour if the optimal route is blocked (e.g. due to congestion, accidents, etc)

The calculation of the optimal route is based on a greedy algorithm. Each agent takes the next node depending on the distance to the pref. sink. If the first next node
(optimal) is blocked the agent will try to drive a detour (second behaviour). If the first agent in queue decides to wait (e.g. no nodes available) all other agents in 
that node have to wait as well because of the FIFO principle. 


## FILES description (short) below ##
## FATSODTA.py ##
FATSODTA.py was implemented by my supervisor. 
This file contains the FATSODTA model which is the basis for the simulation. 
The results of this file (FATSODTA-Solve.sol) are used in comparison to the results of the simulation.

## fatsodta_network.py ##
This file contains the network structure and the agent distribution.

## main.py ##
This file runs the simulation.

## simulation.py ##
This file contains all implementations of the simulation:
- class Agents
- functions to update/reset values
- simulation algorithm
