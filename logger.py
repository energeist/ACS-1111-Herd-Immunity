from datetime import datetime

class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.date_invoked = (datetime.now().astimezone().strftime("%b/%d/%Y %H:%M:%S"))

    def write_metadata(self, pop_size, vacc_percentage, initial_infected, virus_name, mortality_rate, basic_repro_num):
        outfile = open(self.file_name, 'w')
        outfile.write(f'# SIMULATION SUMMARY\nThis output file was generated at {self.date_invoked}\n##Starting conditions\n- Initial population size: {pop_size}\n- Population vaccination rate: {vacc_percentage*100}%\n- Initial infected people: {initial_infected}\n- Virus name: {virus_name}\n- Virus mortality rate: {mortality_rate}\n- Virus reproduction number: {basic_repro_num}\n')
        outfile.close()

    def log_interactions(self, step_number, number_of_interactions, number_of_new_infections, number_new_dead, number_new_vaccinated, step_vaccine_saves, time_interval):
        outfile = open(self.file_name, 'a')
        outfile.write(f'\n## End of time step {step_number}\n- Number of interactions: {number_of_interactions}\n- Number of new infections: {number_of_new_infections}\n- Number of people that died on this timestep: {number_new_dead}\n- Number of people vaccinated on this timestep: {number_new_vaccinated}\n- Number of times a vaccine prevented infection on this timestep: {step_vaccine_saves} \n- Sim calculation time for this step: {time_interval} second(s)\n')
        outfile.close()

    def log_infection_survival(self, step_number, population_count, number_of_new_fatalities):
        outfile = open(self.file_name, 'a')
        outfile.write(f'\nCurrent time step: {step_number}\nNumber of interactions: {number_of_interactions}\n Number of new infections: {number_of_new_infections}\n')
        outfile.close()

