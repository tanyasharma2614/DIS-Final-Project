class Packet:
    def __init__(self, client_id, port_number, start_time):
        self.client_id = client_id
        self.port_number = port_number
        self.start_time = start_time
        self.end_time = start_time
        self.processing_time = 0.004
        #self.processing_time = random.uniform(0.001, 0.1)
        
    def __repr__(self):
        return "Packet from the client--->" + str(self.client_id) + "from port--->" + str(self.port_number) +  " at time: " + str(round(self.start_time, 3))