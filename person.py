import random
from virus import Virus


class Person(object):
    # Define a person. 
    def __init__(self, _id, is_vaccinated, infection = None):
        # A person has an id, is_vaccinated and possibly an infection
        self._id = _id  # int
        self.is_vaccinated = is_vaccinated
        self.infection = infection
        self.is_alive = True

    def did_survive_infection(self):
        if self.infection:
            random_number = random.random()
            return (random_number > self.infection.mortality_rate)    
        # This method checks if a person survived an infection. 

if __name__ == "__main__":
   
    # This section is incomplete finish it and use it to test your Person class
    vaccinated_person = Person(1, True)
    assert vaccinated_person._id == 1
    assert vaccinated_person.is_alive is True
    assert vaccinated_person.is_vaccinated is True
    assert vaccinated_person.infection is None

    # Create an unvaccinated person and test their attributes

    unvaccinated_person = Person(2, False)

    # TODO Test unvaccinated_person's attributes here...
    assert unvaccinated_person._id == 2
    assert unvaccinated_person.is_alive is True
    assert unvaccinated_person.is_vaccinated is False
    assert unvaccinated_person.infection is None

    # Test an infected person. An infected person has an infection/virus
    # Create a Virus object to give a Person object an infection
    
    virus = Virus("Dysentery", 0.7, 0.2)
    
    # Create a Person object and give them the virus infection
    
    infected_person = Person(3, False, virus)
    
    # print (infected_person.infection.name)
    
    assert infected_person._id == 3
    assert infected_person.is_alive is True
    assert infected_person.is_vaccinated is False
    assert infected_person.infection == virus
    
    # You need to check the survival of an infected person. Since the chance
    # of survival is random you need to check a group of people. 
    # Create a list to hold 100 people. Use the loop below to make 100 people
    
    people = []
    for i in range(1, 101):
        people.append(Person(i, False, virus))

    # Now that you have a list of 100 people. Resolve whether the Person 
    # survives the infection or not by looping over the people list. 

    did_survive = 0
    did_not_survive = 0

    # NOTE: ADDITIONAL TESTS FOR person.py HERE

    # set random.seed() for tests
    random.seed(42)
    
    for person in people:
        # For each person call that person's did_survive_infection method
        survived = person.did_survive_infection()

    # Count the people that survived and did not survive: 
       
        if survived:
            did_survive += 1
        else:
            did_not_survive += 1       

    # NOTE: ADDITIONAL TEST 1 - test person.did_survive_infection() method with virus:
    # virus = Virus("Dysentery", 0.7, 0.2)
    # mortality rate of 20%
    # repro rate of 70%

    assert did_survive == 81
    assert did_not_survive == 19        

    # this is approximately 20% mortality!

    # Stretch challenge! 
    # Check the infection rate of the virus by making a group of 
    # unifected people. Loop over all of your people. 
    # Generate a random number. If that number is less than the 
    # infection rate of the virus that person is now infected. 
    # Assign the virus to that person's infection attribute. 

    uninfected_people = []
    new_infection = 0
    for i in range(1, 101):
        uninfected_people.append(Person(i, False))
    
    for person in uninfected_people:
        random_infection = random.random()
        if random_infection < virus.repro_rate:
            person.infection = virus
            new_infection += 1
    
    #NOTE: ADDITIONAL TEST 2 - test infection rate of virus:

    assert new_infection == 71

    # This is approximately 70% infection!

    #NOTE: ADDITIONAL TEST 3 - test infection and mortality of new virus:

    # - virus name: Ebola
    # - virus reproductive rate: 25%
    # - virus mortality rate: 70%

    virus2 = Virus('Ebola', 0.25, 0.7)
    people = []

    # create new population

    for i in range(1, 101):
        people.append(Person(i, False, virus2))

    # Now that you have a list of 100 people. Resolve whether the Person 
    # survives the infection or not by looping over the people list. 

    did_survive = 0
    did_not_survive = 0

    # Count the people that survived and did not survive: 
    for person in people:
        survived = person.did_survive_infection()
       
        if survived:
            did_survive += 1
        else:
            did_not_survive += 1
    
    # new uninfected population
    uninfected_people = []
    new_infection = 0
    for i in range(1, 101):
        uninfected_people.append(Person(i, False))
    
    for person in uninfected_people:
        random_infection = random.random()
        if random_infection < virus2.repro_rate:
            person.infection = virus2
            new_infection += 1      

    # checks on mortality
    assert did_survive == 32
    assert did_not_survive == 68

    # This is approx 70% mortality!

    # checks on infection

    assert new_infection == 19

    # ...sorta close to 25, this seed just has an off roll here.