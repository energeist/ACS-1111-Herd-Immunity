import random, sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        
        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected
        self.people = self._create_population()

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
        for i in range(1, ((pop_size + 1) - initial_infected)):
            people.append(Person(i, False))
            last_id = i
        for j in range(initial_infected):
            people.append(Person((j + last_id), False, virus))
        return people

        # TODO: Create a list of people (Person instances). This list 
        # should have a total number of people equal to the pop_size. 
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        # TODO: Return the list of people
        pass

    def _simulation_should_continue(self):
        for person in self.people:
            if person.is_alive and not person.is_vaccinated:
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

        while should_continue:
            # TODO: Increment the time_step_counter
            # TODO: for every iteration of this loop, call self.time_step() 
            # Call the _simulation_should_continue method to determine if 
            # the simulation should continue
            time_step_counter += 1
            # make people die here?
            self.time_step()
            for person in self.people:
                if person.infection and person.is_alive:
                    number_infected += 1
                    random_death = random.random()
                    if random_death < virus.mortality_rate:
                        person.is_alive = False
                        number_dead += 1
            print(f"Timestep: {time_step_counter}")
            print(f"Number alive: {(len(self.people)) - number_dead}")
            print(f"Number healthy: {(len(self.people) - number_infected)}")
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
        for person in self.people:
            random_sample = random.sample(self.people, k)
            if person.infection:
                for random_person in random_sample:
                    self.interaction(person, random_person)
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
        self.newly_infected = []
        # if random_person.is_vaccinated:
        #     pass
        # elif random_person.infection:
        #     pass
        if not random_person.is_vaccinated and (random_person.infection == None):
            random_infection_chance = random.random()
            if random_infection_chance < virus.repro_rate:
                self.newly_infected.append(random_person)
            
        # TODO: Call logger method during this method.
        pass

    def _infect_newly_infected(self):
        for person in self.newly_infected:
            person.infection = virus
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        pass


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10

    # Make a new instance of the simulation
    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
    print(len(sim.people))
    print(sim._simulation_should_continue())
    sim.run()

### NOTE:
# Simulation keeps running past point where everyone should have been infected, need to figure that out
