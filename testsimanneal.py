import random # need a random number generator
import time
from simanneal import Annealer # import the annealler from the sim anneal library

class TravellingSalesmanProblem(Annealer):
    def __init__(self, cities, distances):
        self.cities = cities
        self.distances = distances
        super(TravellingSalesmanProblem, self).__init__(cities) # annealer needs the initial list of cities

    def move(self):
        # pick two cities that we will swap
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        temp = self.state[a]
        self.state[a] = self.state[b]
        self.state[b] = temp
        #self.state[a], self.state[a] = self.state[b], self.state[a]

        time.sleep(0.001)

    def energy(self):
        total = 0
        for i in range(0, len(self.state) - 1):
            total += self.distances[self.state[i]][self.state[i+1]]

        # this needs to be caluclated as we must end in the city we started in
        total += self.distances[self.state[0]][self.state[len(self.state) - 1]]
        #print('total energy:', total)
        return total

# define a list of cities
city_names = ['Dublin', 'Belfast', 'Galway', 'Tralee', 'Athlone', 'Cork', 'Kilkenny']
cities = [0, 1, 2, 3, 4, 5, 6]
distances = [
    [0, 168, 208, 299, 124, 264, 151], # dublin
    [168, 0, 369, 484, 242, 425, 300], # belfast
    [208, 369, 0, 207, 87, 262, 184], # galway
    [299, 484, 207, 0, 214, 113, 241], # tralee
    [124, 242, 87, 214, 0, 209, 140], # athlone
    [264, 425, 262, 113, 209, 0, 151], # cork
    [151, 300, 184, 241, 140, 151, 0] # kilkenny
]

# generate an instance of the TSP class with our information and shuffle the initial list of cities
random.shuffle(cities)
tsp = TravellingSalesmanProblem(cities, distances)

# state how may steps we wish to take in our schedule
tsp.steps = 100000

# run the annealer
state, e = tsp.anneal()

print('Best route is:')
for i in range(0, len(state)):
    print(city_names[state[i]])
print('Total distance of route:', e, 'Kilometres')
