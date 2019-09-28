
class AllPossibleGenesBuilder:

    def __init__(self):
        self.data = {}
    
    def set(self, k, possible_values):
        self.data[k] =possible_values
        return self
    
    def duplicate(self, prefix, possible_values, count):
        for i in range(count):
            self.data[prefix + "#" + str(i)]=possible_values
        return self
    
    def toDict(self):
        return self.data

    
class GenomeReader:

    def __init__(self, geneparam):
        self.data=geneparam
     
    def scalar(self, key):
        return self.data[key]

    def array(self, prefix):
        i = 0;
        while True:
            key = prefix  + str(i)
            value = self.geneparam.get(key, None)
            if value !=None:
                yield key, value
                i+=1
            else:
                return