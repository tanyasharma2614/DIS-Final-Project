from simulation_small import simulate_env_small
from simulation_large import simulate_env_large
from simulation_medium import simulate_env_medium

load_balance_strategies = ["Random", "RoundRobin", "WeightedRoundRobin", "ConsistentHashing", "PowersOfTwoNoMemory", "PowersOfTwoWithMemory", 
"PowersOfXWithMemory", "Heaps"]

print("*******SIMULATING SMALL SYSTEMS**************")
for strategy in load_balance_strategies:
	simulate_env_small(strategy)

print("*******SIMULATING MEDIUM SYSTEMS**************")
for strategy in load_balance_strategies:
	simulate_env_medium(strategy)

print("*******SIMULATING LARGE SYSTEMS**************")
for strategy in load_balance_strategies:
	simulate_env_large(strategy)