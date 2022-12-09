import random, sys, math, argparse
from datetime import datetime
from simulation import Simulation
from person import Person
from logger import Logger
from virus import Virus

if __name__ == "__main__":
    virus_name = 'Ebola'
    pop_size = 100000
    vacc_percentage = 0.90
    initial_infected = 10
    repro_rate = 0.25
    mortality_rate = 0.70

    # test virus instantiation

    virus = Virus(virus_name, repro_rate, mortality_rate)
    
    assert virus.name == 'Ebola'
    assert virus.repro_rate == 0.25
    assert virus.mortality_rate == 0.70
    
    # test sim instantiation

    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    assert sim.virus.name == 'Ebola'
    assert sim.virus.repro_rate == 0.25
    assert sim.virus.mortality_rate == 0.70

    # test _create_population():

    assert len(sim.people) == pop_size

    infected_people = 0
    healthy_people = 0
    vaccinated_people = 0
    unvaccinated_people = 0
    alive_people = 0
    dead_people = 0

    for person in sim.people:
        if person.is_alive:
            alive_people += 1
            if person.infection:
                infected_people += 1
            else:
                healthy_people += 1
            if person.is_vaccinated:
                vaccinated_people += 1
            else:
                unvaccinated_people += 1
        else:
            dead_people += 1
    
    assert infected_people == sim.initial_infected
    assert healthy_people == (sim.pop_size - sim.initial_infected)
    assert alive_people == sim.pop_size
    assert dead_people == 0
    assert vaccinated_people == round(sim.pop_size * sim.vacc_percentage)
    assert unvaccinated_people == pop_size - round(sim.pop_size * sim.vacc_percentage)

    # test _simulation_should_continue():

    sim.current_infections == 0
    sim._simulation_should_continue()
    assert sim._simulation_should_continue() == False
    assert sim.reason_for_ending == 'Virus burned out - no more infections.'

    sim.current_infections = 1
    sim.current_dead = 10000
    sim.current_vaccinated = 90000
    
    assert sim._simulation_should_continue() == False
    assert sim.reason_for_ending == 'Everyone is dead or vaccinated.'

    sim.current_infections = 10
    sim.current_dead = 0
    sim.current_vaccinated = 90000

    assert sim._simulation_should_continue() == True

    # test _infect_newly_infected():

    sim.people[91000].infection
    person = sim.people[91000]
    sim.newly_infected = []
    sim.newly_infected.append(person)
    
    sim._infect_newly_infected()
    assert sim.people[91000].infection == sim.virus