import matplotlib.pyplot as plt
import numpy as np


def loadVStime(servers, lb_strategy, system_type):
    fig, ax = plt.subplots()

    for server in servers:
        times = np.linspace(0, 1, 500)
        loads = np.array([server.get_load(t) for t in times])
        ax.plot(times, loads, label=f"Server {server.id}")

    ax.legend(loc="best")
    ax.set_xlabel('Time')
    ax.set_ylabel('Load (Time to finish)')
    ax.set_title('Load vs. Time for Servers:'+lb_strategy)

    fig.savefig(f'plots/{system_type}/{lb_strategy}/LoadVsTimeForServers_{lb_strategy}.png')
    plt.close(fig)

def responsetimeVStime(servers, lb_strategy, system_type):
    fig, ax = plt.subplots()
    for server in servers:
        response_times = []
        for t in [x / 500 for x in range(1, 500)]:
            packets_finished = [packet for packet in server.packet_history if packet.end_time <= t]
            if packets_finished:
                response_times.append(sum(packet.end_time - packet.start_time for packet in packets_finished) / len(packets_finished))
            else:
                response_times.append(0)
        ax.plot([t for t in range(1, 500)], response_times, label=f"Server {server.id}")
    ax.legend(loc="best")
    ax.set_xlabel('Time')
    ax.set_ylabel('Response Time')
    ax.set_title('Response Time vs. Time for Servers:'+lb_strategy)
    fig.savefig('plots/{}/{}/ResponseTimeVsTimeForServers_{}.png'.format(system_type, lb_strategy, lb_strategy))
    plt.clf()


def meanstdVStime(servers, lb_strategy, system_type):
    times = []
    means = []
    stdevs = []
    for t in [x/500 for x in range(1, 500)]:
        times.append(t)
        mean = sum([x.get_load(t) for x in servers]) / len(servers)
        stdev = pow( sum([((x.get_load(t) - mean) ** 2) for x in servers]) / (len(servers) - 1), 1/2)
        means.append(mean)
        stdevs.append(stdev)

    plt.plot(np.array([x for x in times]), np.array([y for y in means]), label="mean")
    plt.plot(np.array([x for x in times]), np.array([y for y in stdevs]), label="stdev")

    avg_mean = sum(means)/len(means)
    avg_stdev = sum(stdevs)/len(stdevs)

    print("Mean load: %5.3f" % avg_mean)
    print("Mean standard deviation: %5.3f" % avg_stdev)

    plt.legend(loc="upper right")  # specify location of legend
    plt.xlabel('Time')
    plt.ylabel('Mean / stdev server load')
    plt.title('Mean and Stdev of Load vs. Time for Servers:'+lb_strategy)
    plt.axis([0, 1, 0, 0.6])

    plt.savefig('plots/{}/{}/MeanAndStdevLoadVsTimeForServers_{}.png'.format(system_type, lb_strategy, lb_strategy))
    plt.clf()

	
def throughputVStime(servers, lb_strategy, system_type):
    for server in servers:
        times = []
        throughputs = []  # initialize list to store throughput values
        for t in [x / 500 for x in range(1, 500)]:
            load = server.get_load(t)
            throughput = server.throughput_rate  # get the throughput rate from the server object
            times.append(t)
            throughputs.append(throughput)  # add the throughput rate to the lis
	
        plt.plot(np.array([x for x in times]), np.array([y for y in throughputs]), label=str("Server" + str(server.id)) + ' Throughput')
        plt.legend(loc="best")
        plt.xlabel('Time')
        plt.ylabel(' Throughput')
        plt.title('Throughput vs. Time for Servers:'+lb_strategy)

    plt.savefig('plots/{}/{}/ThroughputVsTimeForServers_{}.png'.format(system_type, lb_strategy, lb_strategy))
    plt.clf()

def consistencycheck(servers):
	perFlowConsistent = True
	for server in servers:
		for otherServer in servers:
			if server.id != otherServer.id:
				for packet in server.packet_history:
					if (packet.client_id, packet.port_number) in [(pckt.client_id, pckt.port_number) for pckt in otherServer.packet_history]:
						perFlowConsistent = False
						break

	if perFlowConsistent:
		print("Per-Flow Consistency Maintained")
	else:
		print("Per-Flow Consistency Not Maintained")