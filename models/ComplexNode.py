

class ComplexNode(object):
    def __init__(self, genes):
        self.genes= genes
        self.set_genes_random();

    def set_genes_random(self):
        for g in self.genes.values():
            g.set_genes_random();

    def __getitem__(self,key):
        return self.genes[key]

    def toString(self):
        return "{" + ','.join([f"{k}:{v.toString()}" for k,v in self.genes.items()]) + "}"
    

    def all_mutables(self):
        for g in self.genes.values():
            for m in g.all_mutables():
                yield m
    
    def all_genes(self):
        for g in self.genes.values():
            for m in g.all_genes():
                yield m
    def clone(self):
        data ={};
        for k,v in self.genes.items():
            data[k] = v.clone()
        return ComplexNode(data)

     