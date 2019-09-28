from .evolver import Evolver
import logging

class Producter:
    """Produce a tournament and find best NN"""

    def __init__(self, train_and_score_callback, mould, count):
        self.evolver = Evolver(retain=0.15, random_select=0.1, mutate_chance=0.3)
        self.genomes = self.evolver.create_population(mould, count)
        self.train_and_score_callback =train_and_score_callback

    def evolve(self):
        logging.info(f"***Now in generation {self.evolver.ids.get_Gen()}***")
        #self.print_genomes(self.genomes);

        for genome in self.genomes:
            genome.train(self.train_and_score_callback)

        self.genomes = self.evolver.evolve(self.genomes)

    def tournament(self, count):
        for i in range(0, count):
            self.evolve()
        
        # Sort our final population according to performance.
        self.genomes = sorted(self.genomes, key=lambda x: x.accuracy, reverse=True)
        logging.info(f"***Top 5***")
        # Print out the top 5 networks/genomes.
        self.print_genomes(self.genomes[:5])

    def print_genomes(self, genomes):
        logging.info('-'*80)
        for genome in genomes:
            genome.print_genome()


