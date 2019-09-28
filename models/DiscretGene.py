import random

class DiscretGene(object):
    def __init__(self, possible_values, value=None):
        self.possible_values = possible_values
        self.value = value

    def set_genes_random(self):
        self.value = random.choice(self.possible_values)

    def mutate(self):
        choices = list(self.possible_values)
        choices.remove(self.value)
        self.value = random.choice(choices)
    
    def transfer(self, value):
        assert value in self.possible_values ,"incompatible transfert"
        self.value = value


    def all_mutables(self):
        yield self

    def all_genes(self):
        yield self

    def toString(self):
        return "'" + str(self.value) + "'"

    def clone(self):
        return DiscretGene(self.possible_values, self.value)

