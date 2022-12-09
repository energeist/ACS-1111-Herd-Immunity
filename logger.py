from datetime import datetime
import matplotlib.pyplot as plt

class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.date_invoked = (datetime.now().astimezone().strftime("%b/%d/%Y %H:%M:%S"))

    def write_metadata(self, pop_size, vacc_percentage, initial_infected, virus_name, mortality_rate, basic_repro_num):
        outfile = open(self.file_name, 'w')
        outfile.write(f'# SIMULATION SUMMARY\nThis output file was generated {self.date_invoked}\n\n## Starting conditions\n- Initial population size: {pop_size}\n- Population vaccination rate: {vacc_percentage*100}%\n- Initial infected people: {initial_infected}\n- Virus name: {virus_name}\n- Virus mortality rate: {mortality_rate}\n- Virus reproduction number: {basic_repro_num}\n')
        outfile.close()

    def log_interactions(self, step_number, number_of_interactions, number_of_new_infections, number_new_dead, number_new_vaccinated, step_vaccine_saves, time_interval):
        outfile = open(self.file_name, 'a')
        outfile.write(f'\n## End of time step {step_number}\n- Number of interactions: {number_of_interactions}\n- Number of new infections: {number_of_new_infections}\n- Number of people that died on this timestep: {number_new_dead}\n- Number of people vaccinated on this timestep: {number_new_vaccinated}\n- Number of times a vaccine prevented infection on this timestep: {step_vaccine_saves} \n- Sim calculation time for this step: {time_interval} second(s)\n')
        outfile.close()

    def log_percent_change(self, pop_pct_change, deaths_pct_prev_step, vaccinations_pct_prev_step, vacc_saves_pct_prev_step):
        outfile = open(self.file_name, 'a')
        outfile.write(f'\n- Population lost on this step: {pop_pct_change:.3f}% as of end of step\n- Change in deaths/step: {deaths_pct_prev_step:.2f}% from previous step\n- Change in vaccinations/step: {vaccinations_pct_prev_step:.2f}% from previous step\n- Change in vaccination saves/step: {vacc_saves_pct_prev_step:.2f}% from previous step\n')
        outfile.close()

    def final_log(self, reason_for_ending, pop_size, total_deaths, pct_deaths_total, remaining_alive, initial_vacc, final_vacc, total_unique_infections, infect_pct_total, total_vaccine_saves, sim_time_string):
        outfile = open(self.file_name, 'a')
        outfile.write(f'\n## END OF SIMULATION SUMMARY:\n- Reason for simulation ending: {reason_for_ending}\n- Initial population: {pop_size}\n- Total deaths: {total_deaths}\n- Percentage of total population that died: {pct_deaths_total:.2f}%\n- Remaining living population: {remaining_alive}\n- Initial vaccinated population: {initial_vacc}\n- Final vaccinated population: {final_vacc}\n- Total number of unique infections: {total_unique_infections}\n- Percentage of total population infected: {infect_pct_total:.2f}%\n- Total number of times a vaccine prevented infection: {total_vaccine_saves}\n- Overall sim runtime: {sim_time_string} seconds')
        outfile.close()

    def end_plots(self, data_arrays):
        step = []

        for i in range(len(data_arrays['alive_array'])):
            step.append(i)

        max_pop = int(data_arrays['alive_array'][0])
        min_pop = int(round(data_arrays['alive_array'][int(len(data_arrays['alive_array'])-1)]))  
        
        fig, ax1 = plt.subplots()
        plt.xlabel("Timestep")
        ax1.plot(step, data_arrays['alive_array'], color ='blue')
        ax1.set_ylim([min_pop/1.025, max_pop*1.025])
        ax1.set_ylabel('Living population on timestep (#)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        

        ax2 = ax1.twinx()
        ax2.scatter(step, data_arrays['pop_pct_change_array'], color='red')
        ax2.set_ylabel('Population decrease per step (%)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.spines['left'].set_color('blue')
        ax2.spines['right'].set_color('red')
        plt.title("Change in Population Over Duration of Simulation")
        plt.savefig('popchange.png')
        plt.close()

        plt.scatter(step, data_arrays['dead_array'], label = "Deaths per timestep")
        plt.title("# of deaths on each simulation timestep")
        plt.xlabel("Timestep")
        plt.ylabel("Number of deaths per step")
        plt.savefig('deaths.png')
        plt.close()

        plt.scatter(step, data_arrays['vaccinated_array'], label = "New vaccinations per timestep")
        plt.title("# of New Vaccinations on Each Simulation Timestep")
        plt.xlabel("Timestep")
        plt.ylabel("Number of new vaccinations")
        plt.savefig('vaccinations.png')
        plt.close()

        plt.scatter(step, data_arrays['vacc_saves_array'], label = "Infection preventions per timestep")
        plt.title("# of Times a Vaccine Prevented Infection Per Timestep")
        plt.xlabel("Timestep")
        plt.ylabel("Number of prevented infections")
        plt.savefig('prevention.png')
        plt.close()



