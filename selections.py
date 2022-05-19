import copy
import functools
import math
import random
from typing import Callable, List


class ClonesSelection:
    def __init__(self, evaluate: Callable, random: Callable, mutate: Callable) -> None:
        self.population = []
        self.evaluations = []
        self.evaluate = evaluate
        self.random = random
        self.mutate = mutate

    def init_population(self, length):
        self.population = [self.random() for _ in range(length)]

    def sort_by_affinity(self, items: List):
        items_copy = copy.deepcopy(items)
        items_copy.sort(key=self.evaluate, reverse=True)
        evaluations = list(map(self.evaluate, items_copy))
        return (items_copy, evaluations)

    def eval(self, items: List):
        return list(map(self.evaluate, items))

    def epoc(self):
        target_length = len(self.population)
        eval = self.eval(self.population)

        # clone
        clones = []
        total_eval = functools.reduce(lambda res, a: res+a, eval, 0)
        for (i, item) in enumerate(self.population):
            num_clones = math.ceil((eval[i]/total_eval)*target_length+3)
            for _ in range(num_clones):
                clones.append(copy.deepcopy(item))

        # mutate
        mutations = []
        clones_length = len(clones)
        for (i, clone) in enumerate(clones):
            j = random.randint(0, clones_length-1)
            while j == i:
                j = random.randint(0, clones_length-1)
            mutations.append(self.mutate(clone, clones[j]))

        # randoms
        randoms = []
        for _ in range(math.ceil(target_length*1.5)):
            randoms.append(self.random())

        (all_sorted, all_eva) = self.sort_by_affinity(
            self.population + mutations + randoms)
            
        self.population = all_sorted[:target_length]
        self.evaluations = all_eva[:target_length]
