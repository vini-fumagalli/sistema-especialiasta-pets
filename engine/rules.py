from experta import *
from .facts import Animal, UserPreferences

class PetAdvisor(KnowledgeEngine):
    @DefFacts()
    def load_initial_facts(self):
        # Pode carregar de JSON ou deixar hardcoded
        yield Animal(nome="gato", espaco="pequeno", custo="baixo")

    @Rule(Animal(nome="gato"))
    def recommend_cat(self):
        self.declare(Animal(recomendado="gato"))