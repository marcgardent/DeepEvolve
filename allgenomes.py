""" Class that keeps track of all genomes trained so far, and their scores.
    Among other things, ensures that genomes are unique.
"""

import random
import logging

from .genome import Genome

class AllGenomes():
    """Store all genomes
    """

    def __init__(self):
        """Initialize
        """
        self.population = {}
        
    def add_genome(self, genome):
        """Add the genome to our population.
        """
        if not self.is_duplicate(genome):
            self.population[genome.hash] = genome
            return True
        else:
            logging.error("add_genome(): hash clash - duplicate genome")
            return False
         
        
    def is_duplicate(self, genome):
        """Add the genome to our population.
        """
        twins = self.population.get(genome.hash, None)        
        return twins != None

    def print_all_genomes(self):
        """Print out a genome.
        """

        for genome in self.population.values():
            genome.print_genome_ma()