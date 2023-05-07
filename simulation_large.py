import random
from copy import deepcopy
import heapq
import numpy as np
from packet import Packet
from server import Server
from plotting import * 

num_clients = 100
num_load_balancers = 6
num_servers = 10
LOAD_BALANCER_DROPS = False
heap = [(0, server) for server in range(num_servers)]
powers_of_x = 3
heapq.heapify(heap)
next_server = 0
weights = [random.randint(1, 10) for _ in range(num_servers)]
print(weights, "are the server weights")
curr_weights = deepcopy(weights)
next_weight_server = 0
num_flows = 150
mean_flow_size = 15
flow_size_stdev = 2
flow_duration = 0.05

class LoadBalancer:
    def __init__(self, address):
        self.id = address
        self.connection_table = {}

    def random_algo(self, packet, a=None, b=None):
        return random.randint(0, num_servers - 1)

    def consistent_hashing(self, packet, a=None, b=None):
        return hash((packet.client_id, packet.port_number)) % num_servers
    
    def roundrobin(self, packet, a=None, b=None):
        global next_server
        server_num = next_server
        next_server = (next_server + 1) % num_servers
        return server_num
    
    def weighted_roundrobin(self, packet, a=None, b=None):
        global curr_weights
        for i in range(len(curr_weights)):
            if curr_weights[i] > 0:
                curr_weights[i]-=1
                return i
        curr_weights = deepcopy(weights)
        return self.weighted_roundrobin(packet)

    def power_of_2_choices_no_memory(self, packet, servers, a=None):
        first_query_server = random.randint(0, num_servers - 1)
        second_query_server = random.randint(0, num_servers - 1)
        while (first_query_server == second_query_server):
            second_query_server = random.randint(0, num_servers - 1)
        first_query_load = servers[first_query_server].get_load(packet.start_time)
        second_query_load = servers[second_query_server].get_load(packet.start_time)
        if first_query_load < second_query_load:
            return first_query_server
        return second_query_server

    def power_of_2_choices_with_memory(self, packet, servers, _):
        mapping = (packet.client_id, packet.port_number)
        if mapping in self.connection_table:
            return self.connection_table[mapping]
        first_query_server = random.randint(0, num_servers - 1)
        second_query_server = random.randint(0, num_servers - 1)
        while (first_query_server == second_query_server):
            second_query_server = random.randint(0, len(servers) - 1)
        first_query_load = servers[first_query_server].get_load(packet.start_time)
        second_query_load = servers[second_query_server].get_load(packet.start_time)
        if first_query_load < second_query_load:
            self.connection_table[mapping] = first_query_server
            return first_query_server
        self.connection_table[mapping] = second_query_server
        return second_query_server

    def power_of_x_choices_with_memory(self, packet, servers, x):
        mapping = (packet.client_id, packet.port_number)
        if mapping in self.connection_table:
            return self.connection_table[mapping]
        if x > num_servers:
            print("Number of servers too low for power of " + str(x) + " choices.")
            return
        server_nums = random.sample(range(0, num_servers), x)
        loads = []
        for num in server_nums:
            loads.append(servers[num].get_load(packet.start_time))
        min_load_server_id = loads.index(min(loads))
        min_server_num = server_nums[min_load_server_id]
        self.connection_table[mapping] = min_server_num
        return min_server_num

    def __repr__(self):
        return "Load Balancer id: " + str(self.id)

def simulate_env_large(strategy):
    print("Simulated LARGE environment with load balance strategy: ", strategy)
    packets = []
    for i in range(num_flows):
        num_pkts_in_flow = int(np.random.normal(mean_flow_size, flow_size_stdev))
        client_of_flow = random.randint(0, num_clients-1)
        time_of_flow = random.random()
        port_number = random.randint(1024, 65536)
        for j in range(num_pkts_in_flow):
            time_of_packet = time_of_flow + (random.random() * (flow_duration) - flow_duration / 2)
            packet = Packet(client_of_flow, port_number, time_of_packet)
            packets.append(packet)
    packets.sort(key=lambda x: x.start_time, reverse=False)
    load_balancers = []
    for i in range(num_load_balancers):
        load_balancer = LoadBalancer(i)
        load_balancers.append(load_balancer)

    servers = []
    for i in range(num_servers):
        server = Server(i)
        servers.append(server)

    for i in range(len(packets)):
        packet = packets[i]
        if LOAD_BALANCER_DROPS:
            if i < len(packets)/2:
                lb_id = packet.client_id % num_load_balancers
            else: 
                lb_id = packet.client_id % (num_load_balancers - 1)
        else:
            lb_id = packet.client_id % num_load_balancers
        load_balancer = load_balancers[lb_id]
        if strategy == "Heaps":
            current_workload, current_worker = heapq.heappop(heap)
            new_workload = current_workload + packet.processing_time
            heapq.heappush(heap, (new_workload, current_worker))
            server = servers[current_worker]
            server.add_packet(packet)
        else:
            switcher = {
                "Random": load_balancer.random_algo,
                "RoundRobin": load_balancer.roundrobin,
                "WeightedRoundRobin": load_balancer.weighted_roundrobin,
                "ConsistentHashing": load_balancer.consistent_hashing,
                "PowersOfTwoNoMemory": load_balancer.power_of_2_choices_no_memory,
                "PowersOfTwoWithMemory": load_balancer.power_of_2_choices_with_memory,
                "PowersOfXWithMemory": load_balancer.power_of_x_choices_with_memory, 
            }
            lb_func = switcher.get(strategy)
            server_id = lb_func(packet, servers, powers_of_x)
            server = servers[server_id]
            server.add_packet(packet)
    loadVStime(servers, strategy, 'large')
    meanstdVStime(servers, strategy, 'large')
    throughputVStime(servers, strategy, 'large')
    responsetimeVStime(servers,strategy, 'large')
    consistencycheck(servers)
    print("**********************************************************************")