import random, sys, math, argparse
from datetime import datetime
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus




class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=10):
        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected
        self.people = self._create_population()
        self.step_vaccine_saves = 0
        self.vaccine_saves = 0
        self.reason_for_ending = ''
        self.logger = Logger('simulation_log.md')

        # ending state attributes
        self.total_interactions = 0
        self.total_unique_infections = 0

        self.alive_per_step = [pop_size]
        self.deaths_per_step = [0] # setting starting condition with '0' because of where reads are taken
        self.vaccinated_per_step = [0]
        self.vaccine_saves_per_step = [0]
        self.current_alive = 0
        self.current_dead = 0
        self.current_infections = 0
        self.current_vaccinated = 0

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

    def _simulation_should_continue(self):
        # This method will return a boolean indicating if the simulation 
        # should continue. 
        # The simulation should not continue if all of the people are dead, 
        # or if all of the living people have been vaccinated. 
        if self.current_infections == 0:
            self.reason_for_ending = 'Virus burned out - no more infections.'
            return False
        if self.current_dead + self.current_vaccinated == len(self.people):
            self.reason_for_ending = 'Everyone is dead or vaccinated.'
            return False
        return True

    def run(self):
        # This method starts the simulation. It should track the number of 
        # steps the simulation has run and check if the simulation should 
        # continue at the end of each step. 

        self.time_step_counter = 0
        should_continue = True
        self.newly_infected = []
        count = 0
        while should_continue:
            self.time_step_counter += 1
            self.time_step()
            self._infect_newly_infected()
            count += 1
            should_continue = self._simulation_should_continue()

    def time_step(self):
        # This method will simulate interactions between people, calulate 
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other 
        # people in the population
        self.current_alive = 0
        self.current_dead = 0
        self.current_infections = 0
        self.current_vaccinated = 0
        self.step_number_of_interactions = 0
        self.step_death_counter = 0
        self.step_vacc_counter = 0
        step_time_start = datetime.now()
        k = 100

        # list of people still living 
        step_alive_people = []
        # list of dead people?
        step_dead_people = 0
        # list of infected people
        step_infected_people = []
        # list of healthy people?
        step_healthy_people = 0
        # list of vaccinated people?
        step_vaccinated_people = 0
        # list of unvaccinated people?
        step_unvaccinated_people = 0

        for person in self.people:
            if person.is_alive:
                step_alive_people.append(person)
                self.current_alive += 1
                if person.infection:
                    step_infected_people.append(person)
                    self.current_infections += 1 
                else: 
                    step_healthy_people += 1
                if person.is_vaccinated:
                    self.current_vaccinated += 1
                else:
                    step_unvaccinated_people += 1
            else:
                self.current_dead += 1
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
                        self.step_death_counter += 1
                    else:
                        self.step_vacc_counter += 1
                        person.is_vaccinated = True
                        person.infection = None
        self.alive_per_step.append(self.current_alive)

        ## step calculation time

        step_time_end = datetime.now()
        step_time_interval = step_time_end - step_time_start
        s = step_time_interval.seconds
        ms = f'00{int(step_time_interval.microseconds / 1000)}'[-3:]
        step_time_string = f'{s % 60}.{ms}'

        # matplotlib data array building

        self.deaths_per_step.append(self.step_death_counter)
        self.vaccinated_per_step.append(self.step_vacc_counter)
        self.vaccine_saves_per_step.append(self.step_vaccine_saves)
        
        self.logger.log_interactions(self.time_step_counter, self.step_number_of_interactions, len(self.newly_infected), self.step_death_counter, self.step_vacc_counter, self.step_vaccine_saves, step_time_string)
        
        self.total_interactions += self.step_number_of_interactions
        self.step_vaccine_saves = 0

        pct_alive_change = (self.alive_per_step[self.time_step_counter] - self.alive_per_step[self.time_step_counter - 1]) / self.alive_per_step[self.time_step_counter - 1] * 100

        if self.deaths_per_step[self.time_step_counter - 1] == 0:
            deaths_divisor = 1
        else:
            deaths_divisor = self.deaths_per_step[self.time_step_counter - 1]
        
        if self.vaccinated_per_step[self.time_step_counter - 1] == 0:
            vaccs_divisor = 1
        else:
            vaccs_divisor = vaccs_divisor = self.vaccinated_per_step[self.time_step_counter - 1]

        if self.vaccine_saves_per_step[self.time_step_counter - 1] == 0:
            vaccs_saves_divisor = 1
        else:
            vaccs_saves_divisor = self.vaccine_saves_per_step[self.time_step_counter - 1]

        deaths_pct_prev_step = (self.deaths_per_step[self.time_step_counter] - self.deaths_per_step[self.time_step_counter - 1]) / deaths_divisor * 100

        vaccinations_pct_prev_step = (self.vaccinated_per_step[self.time_step_counter] - self.vaccinated_per_step[self.time_step_counter - 1]) / vaccs_divisor * 100

        vacc_saves_pct_prev_step = (self.vaccine_saves_per_step[self.time_step_counter] - self.vaccine_saves_per_step[self.time_step_counter - 1]) / vaccs_saves_divisor * 100

        self.logger.log_percent_change(pct_alive_change, deaths_pct_prev_step, vaccinations_pct_prev_step, vacc_saves_pct_prev_step)

    def interaction(self, infected_person, random_person):
        self.step_number_of_interactions += 1
        if (random_person.infection == None) and (not random_person.is_vaccinated) and (random_person not in self.newly_infected):
            random_infection_chance = random.random()
            if random_infection_chance < self.virus.repro_rate:
                self.total_unique_infections += 1
                self.newly_infected.append(random_person)
        elif random_person.is_alive:
            self.step_vaccine_saves += 1
            self.vaccine_saves += 1

    def _infect_newly_infected(self):
        for person in self.newly_infected:
            person.infection = self.virus
        self.current_infections = len(self.newly_infected)
        self.newly_infected = []

if __name__ == "__main__":

    sim_time_start = datetime.now()

    # parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('pop_size', metavar='pop_size', type=int, help="Starting population size as int")
    parser.add_argument('vacc_percentage', metavar='vacc_percentage', type=float, help="Vaccination percentage as decimal number as float")
    parser.add_argument('virus_name', metavar='virus_name', type=str, help="Virus name as string")
    parser.add_argument('mortality_rate', metavar='mortality_rate', type=float, help="Mortality rate as a decimal number float")
    parser.add_argument('repro_num', metavar='repro_num', type=float, help="Reproduction number as a decimal number float")
    parser.add_argument('initial_infected', metavar='initial_infected', type=int, help="Intial number of infected people")
    args = parser.parse_args()
    
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
    pop_size = args.pop_size
    vacc_percentage = args.vacc_percentage
    initial_infected = args.initial_infected

    virus = Virus(virus_name, repro_num, mortality_rate)

    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.logger.write_metadata(pop_size, vacc_percentage, initial_infected, virus_name, mortality_rate, repro_num)
    sim.run()
    sim_time_end = datetime.now()
    sim_time_interval = sim_time_end - sim_time_start
    sim_s = sim_time_interval.seconds
    sim_ms = f'00{int(sim_time_interval.microseconds / 1000)}'[-3:]
    sim_time_string = f'{sim_s % 60}.{sim_ms}'

    # final_log(self, reason_for_ending, pop_size, total_deaths, pct_deaths_init, remaining_alive, initial_vacc, final_vacc, total_unique_infections, infect_pct_total, infect_pct_unvax,total_vaccine_saves, sim_time_string):

    initial_vaxxed = round(int(pop_size)*float(vacc_percentage))
    pct_deaths_init = sim.current_dead / sim.pop_size * 100
    remaining_alive = pop_size - sim.current_dead
    infect_pct_total = sim.total_unique_infections / sim.pop_size * 100

    sim.logger.final_log(sim.reason_for_ending, pop_size, sim.current_dead, pct_deaths_init, remaining_alive, initial_vaxxed, sim.current_vaccinated, sim.total_unique_infections, infect_pct_total, sim.vaccine_saves, sim_time_string)

    print("ending data arrays")
    print(sim.alive_per_step)
    print(len(sim.alive_per_step))
    print(sim.deaths_per_step)
    print(len(sim.deaths_per_step))
    print(sim.vaccinated_per_step)
    print(len(sim.vaccinated_per_step))
    print(sim.vaccine_saves_per_step)
    print(len(sim.vaccine_saves_per_step))

### NOTE:

