import random
import hashlib
import logging

class Genome(object):
    """
    Represents one genome and all relevant utility functions (add, mutate, etc.).
    """

    def __init__(self, genes, u_ID = 0, mom_ID = 0, dad_ID = 0, gen = 0):
        self.genes= genes
        self.accuracy = 0
        self.u_ID = u_ID
        self.parents = [mom_ID, dad_ID]
        self.generation = gen
        self.__update_hash()

    def set_genes_random(self):
        self.genes.set_genes_random()
        self.__update_hash()

    def mutate_one_gene(self):
        all = tuple(self.genes.all_mutables())
        gene = random.choice(all)
        gene.mutate()
        self.__update_hash()

    def clone(self):
        return Genome(self.genes.clone())

    def train(self, train_and_score_callback):
        """Train the genome and record the accuracy.

        Args:
            train_and_score_callback (func): (geneparam) -> accuracy:

        """
        if self.accuracy == 0.0: #don't bother retraining ones we already trained 
            self.accuracy = train_and_score_callback(self.genes)

    def set_generation(self, generation):
        """needed when a genome is passed on from one generation to the next.
        the id stays the same, but the generation is increased"""
        self.generation = generation

        
    def print_genome(self):
        """Print out a genome."""
        self.print_geneparam()
        logging.info("Acc: %.2f%%" % (self.accuracy * 100))
        logging.info("UniID: %d" % self.u_ID)
        logging.info("Mom and Dad: %d %d" % (self.parents[0], self.parents[1]))
        logging.info("Gen: %d" % self.generation)
        logging.info("Hash: %s" % self.hash)

    def print_genome_ma(self):
        """Print out a genome."""
        self.print_geneparam()
        logging.info("Acc: %.2f%% UniID: %d Mom and Dad: %d %d Gen: %d" % (self.accuracy * 100, self.u_ID, self.parents[0], self.parents[1], self.generation))
        logging.info("Hash: %s" % self.hash)

    # print nb_neurons as single list
    def print_geneparam(self):
        logging.info(self.genes.toString())
        
    def __update_hash(self):
         self.hash = hashlib.md5(self.genes.toString().encode("UTF-8")).hexdigest()
