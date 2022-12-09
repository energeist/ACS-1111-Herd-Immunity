# ACS-1111-HERD-IMMUNITY

- Parses parameters from terminal using `argparse`
- Terminal parameters required are `pop_size | vacc_percentage | virus_name | mortality_rate repro_rate | initial_infected`
- Sample output has been generated with the following terminal command: `python3 simulation.py 100000 0.90 Ebola 0.70 0.25 10`
- Test log file found in `test_log_class.md`
- Extra tests included in `virus.py`, `person.py`, `logger.py` and `simulation_test.py`
- Simulation output will appear in `simulation_log.md`
- Data for `answers.txt` contained in `simulation_log_snapshot.md`
- plots generated with matplotlib