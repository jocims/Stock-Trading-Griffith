# implementation of the one max problem using ga accroding to the DEAP documentation

import random

from deap import base
from deap import creator
from deap import tools

# constants that define the likely hood of two individuals having crossover performed
# and the probability that a child will be mutated
CXPB = 0.5
MUTPB = 0.2

# the evaulation function that will be used to evaluate fitness. simply adds up all
# of the ones in the list
def evalOneMax(individual):
    return sum(individual),

# the first step in DEAPs process is to figure out a fitness. The below line
# maps a fitness function to the DEAP library that extends the base fitness class
# it adds a weights attribute that states that we have one parameter that we want
# to maximise. Note that we need an evaluation function to go with this that we
# will define later
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# next we state how to generate an individual, here we are stating that we will use
# a python list to represent a solution and will use the fitness function defined in
# the previous line to evaluate the fitness of an individual.
creator.create("Individual", list, fitness=creator.FitnessMax)

# we need an instance for the toolbox as this will contain everything for generating
# a population and doing the mating and generation stuff
toolbox = base.Toolbox()

# here we will register a function that we will use to initialise an individual
# the initialisation will be a random integer either 0 and 1
toolbox.register("attr_bool", random.randint, 0, 1)

# we tell the toolbox how to generate an individual. in this case we will get it
# to populate the an instance of creator.Individual and to generate the data we
# will repeatedly call the toolbox.attr_bool method 100 and store all 100 results
# in the collection that represents an individual
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)

# similarly we tell the toolbox how to generate a population. in that case we
# are telling the toolbox to call the individual method repeatedly and store the
# individuals in a list
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# register the evaluation function with the toolbox
toolbox.register("evaluate", evalOneMax)

# the mating function for producing children in this case we will use a two point
# crossover, this is already set to work with teh collection classes
toolbox.register("mate", tools.cxTwoPoint)

# the mutation function the mutFlipBit will take each item in the sequence and will
# apply the not operator to it in order to flip it. we state that there is a 5% chance
# that a mutation will occur for each bit
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

# also figure out how to select the parents by using a selection tournament faclity
# provided by the DEAP library
toolbox.register("select", tools.selTournament, tournsize=3)

# here we will generate a population of 300 members using our toolbox and we
# evalulate the fitness of that initial population by maping the evaluation function
# we defined earlier in our toolbox to each member of the population
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
while max(fits) < 1000 and generation < 1000:
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
