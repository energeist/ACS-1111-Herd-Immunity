import random, sys, math
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
        pass

    def _create_population(self):
        people = []
        for i in range(1, self.pop_size + 1): ## need to start at i = 1 for non-zero ID
            people.append(Person(i, False))
        for i in range(0, math.floor(self.pop_size * self.vacc_percentage)):
            people[i].is_vaccinated = True
        print('pop_size - self.initial_infected - 1')
        print(f'{self.pop_size} - {self.initial_infected}')
        print(pop_size - self.initial_infected - 1)
        start_index = (self.pop_size - self.initial_infected)
        for i in range(start_index, (self.pop_size)):
            # print(f'{people[i]._id} {people[i].infection}')
            people[i].infection = virus
            # print(f'{people[i]._id} {people[i].infection}')
        # print ('ID | is_alive | is_vax | infection')
        # for person in people:
        #     print (f'{person._id} | {person.is_alive} | {person.is_vaccinated} | {person.infection}')   
        return people

        # TODO: Create a list of people (Person instances). This list 
        # should have a total number of people equal to the pop_size. 
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        # TODO: Return the list of people
        pass

    def _simulation_should_continue(self):
        for person in self.people:
            if person.is_alive and not person.is_vaccinated and not person.infection:
                return True
        return False
        # This method will return a booleanb indicating if the simulation 
        # should continue. 
        # The simulation should not continue if all of the people are dead, 
        # or if all of the living people have been vaccinated. 
        # TODO: Loop over the list of people in the population. Return True
        # if the simulation should continue or False if not.
        pass

    def run(self):
        # This method starts the simulation. It should track the number of 
        # steps the simulation has run and check if the simulation should 
        # continue at the end of each step. 

        time_step_counter = 0
        should_continue = True
        number_dead = 0
        number_infected = 0
        self.dead_people = []
        self.newly_infected = []

        while should_continue:
            # TODO: Increment the time_step_counter
            # TODO: for every iteration of this loop, call self.time_step() 
            # Call the _simulation_should_continue method to determine if 
            # the simulation should continue
            # make people die here?
            number_infected = 0
            number_vaccinated = 0
            for person in self.people:
                if person.infection:
                    number_infected += 1
                if person.is_vaccinated:
                    number_vaccinated += 1
            print(f"Timestep: {time_step_counter}")
            print(f"Number alive: {(len(self.people))}")
            print(f"Number healthy: {(len(self.people) - number_infected)}")
            print(f"Number vaccinated: {number_vaccinated}")
            time_step_counter += 1
            number_dead = len(self.dead_people)
            self.time_step()
            # NEED TO GENERATE RANDOM PEOPLE AND DO INTERACTIONS THEN INFECT NEWLY INFECTED
            self._infect_newly_infected()
            should_continue = self._simulation_should_continue()
            pass

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
        k = 100
        if (len(self.people)) < 100:
            k = len(self.people)
        print(f'k = {k}')
        print(len(self.people))
        for person in self.people:
            random_sample = random.sample(self.people, k)
            if person.infection:
                for random_person in random_sample:
                    self.interaction(person, random_person)
            random_death = random.random()
            if random_death < virus.mortality_rate:
                print('o no im ded')
                person.is_alive = False
                self.dead_people.append(self.people.remove(person))
            else:
                print('yay not ded')
                person.is_vaccinated = True
                person.infection = None

        ###TODO: Add in a time counter so that a person gets vaccinated status after x number of days?
        pass

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
        if (random_person.infection == None) and (not random_person.is_vaccinated):
            random_infection_chance = random.random()
            if random_infection_chance < self.virus.repro_rate:
                self.newly_infected.append(random_person)
            
        # TODO: Call logger method during this method.
        pass

    def _infect_newly_infected(self):
        print('len(self.newly_infected)')
        print(len(self.newly_infected))
        for person in self.newly_infected:
            person.infection = self.virus
        self.newly_infected = []
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        pass


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.02
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 200
    vacc_percentage = 0.11
    initial_infected = 20

    # Make a new instance of the simulation
    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
    print(len(sim.people))
    print(sim._simulation_should_continue())
    sim.run()

### NOTE:
# Simulation keeps running past point where everyone should have been infected, need to figure that out
