from .DiscretGene import DiscretGene

class ArrayNode(object):
    def __init__(self, genes, counter):
        self.count = counter
        self.genes = genes
    
    @classmethod
    def Duplicate(cls, gene, min, max):
        genes = [gene.clone() for l in range(max)]
        return cls(genes, DiscretGene(range(min, max)))

    def set_genes_random(self):
        self.count.set_genes_random()
        for g in self.genes:
            g.set_genes_random();

    def all_mutables(self):
        yield self.count 
        for g in self.__enabled():
            for m in g.all_mutables():
                yield m
    
    def all_genes(self):
        for g in self.genes:
            for m in g.all_genes():
                yield m

    def __enabled(self):
        return self.genes[:self.count.value]

    def toString(self):
        return "[" +','.join([v.toString() for v in self.__enabled()]) + "]"

    def __getitem__(self,index):
        return self.genes[index]
    def clone(self):
        ret = ArrayNode([g.clone() for g in self.genes], self.count.clone())
        return ret