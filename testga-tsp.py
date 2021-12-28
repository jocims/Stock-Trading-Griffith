# will attempt to do the TSP problem but using GA to solve it instead of SA

# imports necessary for this to work
import random
from deap import base
from deap import creator
from deap import tools

# define a list of cities
city_names = ['Dublin', 'Belfast', 'Galway', 'Tralee', 'Athlone', 'Cork', 'Kilkenny']
distances = [
    [0, 168, 208, 299, 124, 264, 151], # dublin
    [168, 0, 369, 484, 242, 425, 300], # belfast
    [208, 369, 0, 207, 87, 262, 184], # galway
    [299, 484, 207, 0, 214, 113, 241], # tralee
    [124, 242, 87, 214, 0, 209, 140], # athlone
    [264, 425, 262, 113, 209, 0, 151], # cork
    [151, 300, 184, 241, 140, 151, 0] # kilkenny
]

# constants that define the likely hood of two individuals having crossover
# performed and the probability that a child will be mutated
CXPB = 0.5
MUTPB = 0.2

# container for the travelling salesman problem
class TravellingSalesman():
    # constructor that will take in a list of cities that will serve as the genetic code
    def __init__(self):
        self.cities = [0, 1, 2, 3, 4, 5, 6]

    # performs a randomised initilisation of our TSP problem
    def randomise(self):
        random.shuffle(self.cities)

# function that will generate a individual of travelling salesman
def initTSPIndividual(ind_class):
    ind = ind_class()
    ind.randomise()
    return ind

def crossoverTSP(ind1, ind2):
    # make two new individuals
    child1 = TravellingSalesman()
    child2 = TravellingSalesman()
    child1.cities.clear()
    child2.cities.clear()

    # child 1 should take the first half of ind1 and the second half of ind2 and
    # child 2 vice versa
    half = int(len(ind1.cities) / 2)
    for i in range(half):
        child1.cities.append(ind1.cities[i])
        child2.cities.append(ind2.cities[i])
    for i in range(half, len(ind1.cities)):
        child1.cities.append(ind2.cities[i])
        child2.cities.append(ind1.cities[i])

    # return the children
    return (child1, child2)

# takes an individual and will mutate them
def mutateTSP(individual, indpb):
    # for each city check to see if we will mutate it
    for i in range(len(individual.cities)):
        if random.random() < indpb:
            individual.cities[i] = random.randint(0, 7)


# function that will evaluate the distance that is produced by an instance of
# TSP
def evaluateDistance(individual):
    # create a copy of the cities without duplicates
    no_dup = list(set(individual.cities))
    no_dup.sort()

    # if the list is not exactly 7 elements long then return a bad distance
    if len(no_dup) != 7:
        return 10000,

    # make sure the elements 0 to 6 are in the list. if not return a bad distance
    for i in range(7):
        if i not in no_dup:
            return 10000,

    total = 0
    for i in range(len(individual.cities) - 1):
        total += distances[individual.cities[i]][individual.cities[i+1]]

    # this needs to be caluclated as we must end in the city we started in
    total += distances[individual.cities[0]][individual.cities[len(individual.cities) - 1]]
    #print('total energy:', total)
    return total,

# define a base fitness that will look to minimise rather than maximise.
creator.create("Fitness", base.Fitness, weights=(-1.0,))

# define the creation of an individual that will link to our TSP container class
creator.create("Individual", TravellingSalesman, fitness=creator.Fitness)

# get a toolbox
toolbox = base.Toolbox()

# tell the toolbox how to create an individual
toolbox.register("individual", initTSPIndividual, creator.Individual)

# tell the toolbox that we will store our population in a list
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# tell the toolbox what to use for evaluating the distance
toolbox.register("evaluate", evaluateDistance)

# register our custom crossover function
toolbox.register("mate", crossoverTSP)

# register our custom mutation function
toolbox.register("mutate", mutateTSP, indpb=0.05)

# use a selection tournament to select our parents
toolbox.register("select", tools.selTournament, tournsize=3)

# create a population of 300 and do an initial evaluation on them
pop = toolbox.population(n=300)
fitnesses = list(map(toolbox.evaluate, pop))

# here we join the fitnesses up with the relevant individuals for the purposes
# of running generations
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit

# create a list of all the fitness values that we have so far
fits = [ind.fitness.values[0] for ind in pop]

# we will run while we have less than 1000 generations and we have not hit a maximum of 100
# in one of our lists
generation = 0
while generation < 100:
    # we are making a new generation
    generation += 1
    print("==== Generation %i ====" % generation)

    # select the fittest parents for the next generation
    parents = toolbox.select(pop, len(pop))

    # take a full copy of the parents as we will use these instances to perform our crossover
    # and mutations
    offspring = list(map(toolbox.clone, parents))

    # choose the crossovers at random
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        # test to see if we will do a crossover between two parents
        if random.random() < CXPB:
            # do the crossover and delete the fitness values as they refer to the parent fitness
            # and not the children
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    # for each child in the offspring see if we will mutate it
    for mutant in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # go through each child in the offspring. if they have an invalid fitness then reevaluate
    # their fitness
    for individual in offspring:
        if not individual.fitness.valid:
            individual.fitness.values = toolbox.evaluate(individual)

    # replace the population with the offspring
    pop[:] = offspring

    # print out some stats about fitness of the population
    fits = [ind.fitness.values[0] for ind in pop]
    length = len(pop)
    mean = sum(fits) / length
    sum2 = sum(x*x for x in fits)
    std = abs(sum2 / length - mean ** 2)**0.5

    print(' Min:', min(fits))
    print(' Max:', max(fits))
    print(' Avg:', mean)
    print(' Std:', std)
