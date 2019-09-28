"""
Class that holds a genetic algorithm for evolving a network.

Inspiration:

    http://lethain.com/genetic-algorithms-cool-name-damn-simple/
"""
from __future__ import print_function

import random
import logging
import copy

from functools  import reduce
from operator   import add
from .genome     import Genome
from .idgen      import IDgen
from .allgenomes import AllGenomes


class Evolver():
    """Class that implements genetic algorithm."""
    def __init__(self, retain=0.15, random_select=0.1, mutate_chance=0.3):
        """Create an optimizer.

        Args:
            retain (float): Percentage of population to retain after
                each generation
            random_select (float): Probability of a rejected genome
                remaining in the population
            mutate_chance (float): Probability a genome will be
                randomly mutated

        """
        self.retain             = retain
        self.random_select      = random_select
        self.mutate_chance      = mutate_chance

        #set the ID gen
        self.ids = IDgen()
        
    def create_population(self, mould, count):
        """Create a population of random networks.

        Args:
            count (int): Number of networks to generate, aka the
                size of the population

        Returns:
            (list): Population of network objects

        """
        self.master = AllGenomes()
        pop = []

        for i in range(count):
            genome = Genome( mould.clone(), self.ids.get_next_ID(), 0, 0, self.ids.get_Gen() )
            genome.set_genes_random()
            self.register_new_genome(genome)
            pop.append(genome)
        return pop

    @staticmethod
    def fitness(genome):
        """Return the accuracy, which is our fitness function."""
        return genome.accuracy

    def grade(self, pop):
        """Find average fitness for a population.

        Args:
            pop (list): The population of networks/genome

        Returns:
            (float): The average accuracy of the population

        """
        summed = reduce(add, (self.fitness(genome) for genome in pop))
        return summed / float((len(pop)))

    def breed(self, mom, dad):
        """Make two children from parental genes.

        Args:
            mother (dict): genome parameters
            father (dict): genome parameters

        Returns:
            (tuple): Two network objects

        """

        #where do we recombine? 0, 1, 2, 3, 4... N?
        #with four genes, there are three choices for the recombination
        # ___ * ___ * ___ * ___ 
        #0 -> no recombination, and N == length of dictionary -> no recombination
        #0 and 4 just (re)create more copies of the parents
        #so the range is always 1 to len(all_possible_genes) - 1

        child1 = mom.genes.clone()
        child2 = dad.genes.clone()
        child1_genes = tuple(child1.all_genes())
        child2_genes = tuple(child2.all_genes())
        pcl = len(child1_genes)
        
        assert len(child1_genes) == len(child2_genes), "incompatible genome!"
        assert pcl>=2, "insufficient genes to recombinate"

        recomb_loc = random.randint(1, pcl - 1) 

        #*** CORE RECOMBINATION CODE ****
        for i in range(0, pcl):
            if i < recomb_loc:
                child1_genes[i].transfer(child2_genes[i].value)
            else:
                child2_genes[i].transfer(child1_genes[i].value)

        # Initialize a new genome
        # Set its parameters to those just determined
        # they both have the same mom and dad
        genome1 = Genome(child1, self.ids.get_next_ID(), mom.u_ID, dad.u_ID, self.ids.get_Gen() )
        genome2 = Genome(child2, self.ids.get_next_ID(), mom.u_ID, dad.u_ID, self.ids.get_Gen() )

        #at this point, there is zero guarantee that the genome is actually unique

        # Randomly mutate one gene
        if self.mutate_chance > random.random(): 
        	genome1.mutate_one_gene()

        if self.mutate_chance > random.random(): 
        	genome2.mutate_one_gene()

        #do we have a unique child or are we just retraining one we already have anyway?
        self.register_new_genome(genome1)
        self.register_new_genome(genome2)
        
        return genome1, genome2
    
    def register_new_genome(self, genome):
        while self.master.is_duplicate(genome):
            logging.debug("collision: mutate one gene...")
            genome.mutate_one_gene()
        self.master.add_genome(genome)

    def evolve(self, pop):
        """Evolve a population of genomes.

        Args:
            pop (list): A list of genome parameters

        Returns:
            (list): The evolved population of networks

        """
        assert len(pop)*self.retain>=2 , f"retain factor and population are too low"

        #increase generation 
        self.ids.increase_Gen()

        # Get scores for each genome
        graded = [(self.fitness(genome), genome) for genome in pop]

        # Sort on the scores.
        graded = [x[1] for x in sorted(graded, key=lambda x: x[0], reverse=True)]

        # Get the number we want to keep unchanged for the next cycle.
        retain_length = int(len(graded)*self.retain)
        logging.info(f"unchanged for the next cycle: {retain_length}")

        # In this first step, we keep the 'top' X percent (as defined in self.retain)
        # We will not change them, except we will update the generation
        new_generation = graded[:retain_length]

        # For the lower scoring ones, randomly keep some anyway.
        # This is wasteful, since we _know_ these are bad, so why keep rescoring them without modification?
        # At least we should mutate them
            
        mutated_length = 0
        for genome in graded[retain_length:]:
            if self.random_select > random.random(): 
                gtc = copy.deepcopy(genome)
                
                while self.master.is_duplicate(gtc):
                    gtc.mutate_one_gene()

                gtc.set_generation( self.ids.get_Gen() )
                new_generation.append(gtc)
                self.master.add_genome(gtc)
                mutated_length  += 1
        
        logging.info(f"mutated for the next cycle: {mutated_length}")


        # Now find out how many spots we have left to fill.
        ng_length = len(new_generation)
        desired_length = len(pop) - ng_length
        
        
        logging.info(f"babies for the next cycle: {desired_length}")

        
        # Add children, which are bred from pairs of remaining (i.e. very high or lower scoring) genomes.
        children = []
        while len(children) < desired_length:

            # Get a random mom and dad, but, need to make sure they are distinct
            parents  = random.sample(range(ng_length-1), k=2)
            
            i_male   = parents[0]
            i_female = parents[1]

            male   = new_generation[i_male]
            female = new_generation[i_female]

            # Recombine and mutate
            babies = self.breed(male, female)
            # the babies are guaranteed to be novel

            # Add the children one at a time.
            for baby in babies:
                # Don't grow larger than desired length.
                #if len(children) < desired_length:
                children.append(baby)

        new_generation.extend(children)

        return new_generation
