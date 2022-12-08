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

    def log_percent_change():
        outfile = open(self.file_name, 'a')
        outfile.write(f'')
        outfile.close()

    def final_log(self, reason_for_ending, pop_size, total_deaths, remaining_alive, initial_vacc, final_vacc, total_unique_infections, total_vaccine_saves, sim_time_string):
        outfile = open(self.file_name, 'a')
        outfile.write(f'\n## END OF SIMULATION SUMMARY:\n- Reason for simulation ending: {reason_for_ending}\n- Initial population: {pop_size}\n- Total deaths: {total_deaths}\n- Remaining living population: {remaining_alive}\n- Initial vaccinated population: {initial_vacc}\n- Final vaccinated population: {final_vacc}\n- Total number of unique infections: {total_unique_infections}\n- Total number of times a vaccine prevented infection: {total_vaccine_saves}\n- Overall sim runtime: {sim_time_string} seconds')
        outfile.close()

