import random, sys, math, argparse
from datetime import datetime
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus




class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=10):
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        
        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected
        self.people = self._create_population()
        self.step_vaccine_saves = 0
        self.vaccine_saves = 0
        # self.logger = Logger()

        # TODO: Store the virus in an attribute
        # TODO: Store pop_size in an attribute
        # TODO: Store the vacc_percentage in a variable
        # TODO: Store initial_infected in a variable
        
        # You need to store a list of people (Person instances)
        # Some of these people will be infected some will not. 
        # Use the _create_population() method to create the list and 
        # return it storing it in an attribute here. 
        # TODO: Call self._create_population() and pass in the correct parameters.

    def _create_population(self):
        people = []
        for i in range(1, self.pop_size + 1): ## need to start at i = 1 for non-zero ID
            people.append(Person(i, False))
        for i in range(0, math.floor(self.pop_size * self.vacc_percentage)):
            people[i].is_vaccinated = True
        start_index = (self.pop_size - self.initial_infected)
        for i in range(start_index, (self.pop_size)):
            people[i].infection = virus
        return people

        # TODO: Create a list of people (Person instances). This list 
        # should have a total number of people equal to the pop_size. 
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        # TODO: Return the list of people

    def _simulation_should_continue(self):
        current_infections = 0
        for person in self.people:
            if person.is_alive and person.infection:
                current_infections += 1
            # if person.is_alive and not person.is_vaccinated:
            #     return True
        print('current infections:')
        print(current_infections)
        if current_infections == 0:
            return False
        return True
        # This method will return a boolean indicating if the simulation 
        # should continue. 
        # The simulation should not continue if all of the people are dead, 
        # or if all of the living people have been vaccinated. 
        # TODO: Loop over the list of people in the population. Return True
        # if the simulation should continue or False if not.

    def run(self):
        # This method starts the simulation. It should track the number of 
        # steps the simulation has run and check if the simulation should 
        # continue at the end of each step. 

        self.time_step_counter = 0
        should_continue = True
        number_dead = 0
        number_infected = 0
        self.dead_people = []
        self.newly_infected = []
        count = 0
        while should_continue:
            # TODO: Increment the time_step_counter
            # TODO: for every iteration of this loop, call self.time_step() 
            # Call the _simulation_should_continue method to determine if 
            # the simulation should continue
            number_infected = 0
            number_vaccinated = 0
            for person in self.people:
                if person.infection:
                    number_infected += 1
                if person.is_vaccinated:
                    number_vaccinated += 1
            self.time_step_counter += 1
            number_dead = len(self.dead_people)
            self.time_step()
            self._infect_newly_infected()
            count += 1
            should_continue = self._simulation_should_continue()

        # TODO: Write meta data to the logger. This should be starting 
        # statistics for the simulation. It should include the initial
        # population size and the virus. 
        
        # TODO: When the simulation completes you should conclude this with 
        # the logger. Send the final data to the logger. 

    def time_step(self):
        # This method will simulate interactions between people, calulate 
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other 
        # people in the population
        # TODO: Loop over your population
        # For each person if that person is infected
        # have that person interact with 100 other living people 
        # Run interactions by calling the interaction method below. That method
        # takes the infected person and a random person
        self.number_of_interactions = 0
        self.death_counter = 0
        self.vacc_counter = 0
        time_start = datetime.now()
        k = 100

        step_alive_people = []
        step_dead_people = []
        step_infected_people = []
        step_healthy_people = []
        step_vaccinated_people = []
        step_unvaccinated_people = []
        for person in self.people:
            if person.is_alive:
                step_alive_people.append(person)
                if person.infection:
                    step_infected_people.append(person)
                else: step_healthy_people.append(person)
                if person.is_vaccinated:
                    step_vaccinated_people.append(person)
                else:
                    step_unvaccinated_people.append(person)
            else:
                step_dead_people.append(person)
        #debugging
        print(f"Length of people array: {len(self.people)} vs Len of alive + dead: {len(step_alive_people) + len(step_dead_people)}")
        print(f"len alive: {len(step_alive_people)}")
        print(f"len dead: {len(step_dead_people)} // {len(self.dead_people)}")
        print(f"len vaccinated: {len(step_vaccinated_people)}")
        print(f"len unvaccinated: {len(step_unvaccinated_people)}")
        print(f"len infected: {len(step_infected_people)}")
        print(f"len healthy: {len(step_healthy_people)}")
        ##
        if (len(step_alive_people)) < 100:
            k = len(step_alive_people)
        for person in step_infected_people:
            random_sample = random.sample(step_alive_people, k)
            for random_person in random_sample:
                self.interaction(person, random_person)
        for person in self.people:
            if person.is_alive:
                if person.infection:
                    if not person.did_survive_infection():
                        person.is_alive = False
                        person.infection = None
                        self.death_counter += 1
                        self.dead_people.append(person)
                    else:
                        self.vacc_counter += 1
                        person.is_vaccinated = True
                        person.infection = None
        print(f"Length newly infected: {len(self.newly_infected)}")
        time_end = datetime.now()
        time_interval = time_end - time_start
        s = time_interval.seconds
        ms = int(time_interval.microseconds / 1000)
        time_string = f'{s % 60}.{ms}'
        logger.log_interactions(self.time_step_counter, self.number_of_interactions, len(self.newly_infected), self.death_counter, self.vacc_counter, self.step_vaccine_saves, time_string)
        self.step_vaccine_saves = 0

    def interaction(self, infected_person, random_person):
        # TODO: Finish this method.
        # The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0.0 and 1.0.  If that number is smaller
            #     than repro_rate, add that person to the newly infected array
            #     Simulation object's newly_infected array, so that their infected
            #     attribute can be changed to True at the end of the time step.
        # if random_person.is_vaccinated:
        #     pass
        # elif random_person.infection:
        #     pass
        self.number_of_interactions += 1
        if (random_person.infection == None) and (not random_person.is_vaccinated) and (random_person not in self.newly_infected):
            random_infection_chance = random.random()
            if random_infection_chance < self.virus.repro_rate:
                self.newly_infected.append(random_person)
        elif random_person.is_alive:
            self.step_vaccine_saves += 1
            self.vaccine_saves += 1


    def _infect_newly_infected(self):
        for person in self.newly_infected:
            person.infection = self.virus
        self.newly_infected = []

if __name__ == "__main__":

    #parse CLI arguments

    parser = argparse.ArgumentParser()
    parser.add_argument('pop_size', metavar='pop_size', type=int, help="Starting population size as int")
    parser.add_argument('vacc_percentage', metavar='vacc_percentage', type=float, help="Vaccination percentage as decimal number as float")
    parser.add_argument('virus_name', metavar='virus_name', type=str, help="Virus name as string")
    parser.add_argument('mortality_rate', metavar='mortality_rate', type=float, help="Mortality rate as a decimal number float")
    parser.add_argument('repro_num', metavar='repro_num', type=float, help="Reproduction number as a decimal number float")
    parser.add_argument('initial_infected', metavar='initial_infected', type=int, help="Intial number of infected people")
    args = parser.parse_args()

    logger = Logger('simulation_log.md')
    
    # Test your simulation here
    # virus_name = "Sniffles"
    # repro_num = 0.04
    # mortality_rate = 0.12
    # # Set some values used by the simulation
    # pop_size = 100000
    # vacc_percentage = 0.11
    # initial_infected = 3000
    
    virus_name = args.virus_name
    repro_num = args.repro_num
    mortality_rate = args.mortality_rate
    virus = Virus(virus_name, repro_num, mortality_rate)


    pop_size = args.pop_size
    vacc_percentage = args.vacc_percentage
    initial_infected = args.initial_infected

    # Make a new instance of the simulation
    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
    print(len(sim.people))
    print(sim._simulation_should_continue())
    logger.write_metadata(pop_size, vacc_percentage, initial_infected, virus_name, mortality_rate, repro_num)
    sim.run()

### NOTE:

