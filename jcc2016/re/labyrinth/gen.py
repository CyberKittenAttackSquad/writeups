import base64
import random
import subprocess

chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+-={}|[]\\;\':",./<>?'

def mutate (s) :
    for i in range(random.randint(1, 5)) :
        position = random.randint(0, len(s) - 1)
        t = list(s)
        t[position] = chars[random.randint(0, len(chars) - 1)]#chr(random.randint(0, 255))
        s = t
    return ''.join(s)


def getScore (s) :
    proc = subprocess.Popen('./lab-solve', stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    stdout, stderr = proc.communicate(s)

    r = 0
    for i in range(6) :
        if len(stdout) <= i :
            break
        if stdout[i] == 'BASE64'[i] :
            r += 1
        else :
            break
    return r


class Gene :
    def __init__ (self, s) :
        self.s = s
        self._score = None

    def score (self) :
        if self._score == None :
            self._score = getScore(self.s)
        return self._score


class Pool :
    def __init__ (self) :
        self.genes = []

    def add_gene (self, gene) :
        self.genes.append(gene)

    def score_genes (self) :
        for gene in self.genes :
            gene.score()

    def sort (self) :
        def cmp (x, y) :
            return x.score() - y.score()
        self.genes = sorted(self.genes, cmp)
        self.genes.reverse()

    def mutate_all (self) :
        for i in range(len(self.genes)) :
            self.genes[i] = Gene(mutate(self.genes[i].s))

    def kill_and_reproduce (self) :
        self.genes = self.genes[:100]
        new_genes = []
        for gene in self.genes :
            for i in range(10) :
                new_genes.append(Gene(mutate(gene.s)))
        self.genes += new_genes

pool = Pool()
for i in range(1000) :
    pool.add_gene(Gene('aaaaaaaaaaaaaaaaaaa'))

for i in range(1000) :
    random.shuffle(pool.genes)
    pool.score_genes()
    pool.sort()
    pool.kill_and_reproduce()

    print 'done with family', i
    for i in range(10) :
        gene = pool.genes[i]
        print gene.score(), gene.s