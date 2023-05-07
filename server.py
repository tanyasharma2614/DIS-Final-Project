# Processing time of a packet
processing_time = 0.004

class Server:
	def __init__(self, address):
		self.id = address
		self.packet_history = []
		self.last_time=0
		self.throughput_rate=0

	def add_packet(self, packet):
		self.packet_history.append(packet)

	def get_load(self, current_time):
		if len(self.packet_history) == 0:
			return 0
		time_2_finish = 0
		t = 0
		i = 0
		count=0
		while t < current_time:
			if i >= len(self.packet_history):
				break
			packet_i = self.packet_history[i]
			if packet_i.start_time > current_time:
				break
			if time_2_finish > 0:
				time_2_finish -= (packet_i.start_time - t)
				if time_2_finish < 0:
					count += 1
					time_2_finish = 0
			time_2_finish += processing_time
			t = packet_i.start_time
			i += 1
			packet_i.end_time = packet_i.start_time + time_2_finish
		time_2_finish -= (current_time - t)
		if time_2_finish < 0:
			time_2_finish = 0

		#calculating the throughput rate
		time_elapsed=current_time-self.last_time
		self.throughput_rate=count/time_elapsed if time_elapsed>0 else 0
		self.last_time=current_time
		return time_2_finish

	def __repr__(self):
		string = ""
		for packet in self.packet_history:
			string += str(round(packet.start_time,3)) + " "
		return "Server id -->" + str(self.id) +" and " + "Packet arrival times: " + string