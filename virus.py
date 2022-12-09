class Virus(object):
    # Properties and attributes of the virus used in Simulation.
    def __init__(self, name, repro_rate, mortality_rate):
        # Define the attributes of your your virus
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate

# Test this class
if __name__ == "__main__":
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3

    # 2 extra tests
    
    virus2 = Virus("Sniffles", 0.04, 0.12)
    assert virus2.name == "Sniffles"
    assert virus2.repro_rate == 0.04
    assert virus2.mortality_rate == 0.12

    virus3 = Virus("Brain Problems", 0.5, 0.99)
    assert virus3.name == "Brain Problems"
    assert virus3.repro_rate == 0.5
    assert virus3.mortality_rate == 0.99

