from experta import *
from .facts import Animal, UserPreferences

class PetAdvisor(KnowledgeEngine):
    @DefFacts()
    def load_default_facts(self):
        # Fatos básicos sobre os pets
        yield Animal(nome="cachorro", espaco="grande", custo="alto", energia="alta", afeto="alto", alergia_pelo=False, tipo_casa=["Apartamento", "Casa", "Condomínio"], tempo_disponivel=["muito", "medio", "pouco"], interacao_desejada=True, animal_exotico=False, ambiente_rural=False, nojo_roedor=False)
        yield Animal(nome="gato", espaco="pequeno", custo="medio", energia="medio", afeto="alto", alergia_pelo=False, tipo_casa=["Apartamento", "Casa", "Condomínio"], tempo_disponivel=["muito", "medio", "pouco"], interacao_desejada=True, animal_exotico=False, ambiente_rural=False, nojo_roedor=False)
        yield Animal(nome="coelho", espaco="medio", custo="medio", energia="medio", afeto="alto", alergia_pelo=False, tipo_casa=["Apartamento", "Casa", "Condomínio"], tempo_disponivel=["muito", "medio", "pouco"], interacao_desejada=True, animal_exotico=False)
        yield Animal(nome="peixe_pequeno", espaco="pequeno", custo="baixo", energia="baixa", afeto="baixo", alergia_pelo=True, interacao_desejada=False)
        yield Animal(nome="peixe_grande", espaco="grande", custo="baixo", energia="baixa", afeto="baixo", alergia_pelo=True, interacao_desejada=False)
        yield Animal(nome="jabuti", espaco="grande", custo="medio", energia="baixa", afeto="baixo", alergia_pelo=True, interacao_desejada=False)
        yield Animal(nome="papagaio", espaco="medio", custo="alto", energia="alta", afeto="alto", alergia_pelo=False, interacao_desejada=True)
        yield Animal(nome="canario", espaco="medio", custo="baixo", energia="media", afeto="baixo", alergia_pelo=False, interacao_desejada=True)
        yield Animal(nome="periquito", espaco="pequeno", custo="baixo", energia="media", afeto="baixo", alergia_pelo=False, interacao_desejada=True)
        yield Animal(nome="porquinho_india", espaco="medio", custo="medio", energia="medio", afeto="alto", alergia_pelo=False, interacao_desejada=True, nojo_roedor=False)
        yield Animal(nome="rato_domestico", espaco="pequeno", custo="baixo", energia="alto", afeto="medio", alergia_pelo=False, interacao_desejada=True, nojo_roedor=True)
        yield Animal(nome="hamster", espaco="pequeno", custo="baixo", energia="medio", afeto="medio", alergia_pelo=False, interacao_desejada=True, nojo_roedor=False)
        yield Animal(nome="tartaruga_aquatica", espaco="medio", custo="medio", energia="baixa", afeto="baixo", alergia_pelo=False, interacao_desejada=False)
        yield Animal(nome="gecko", espaco="medio", custo="medio", energia="baixa", afeto="baixo", alergia_pelo=False, interacao_desejada=False, animal_exotico=True)
        yield Animal(nome="caranguejeira", espaco="pequeno", custo="medio", energia="media", afeto="baixo", alergia_pelo=False, interacao_desejada=False, animal_exotico=True)
        yield Animal(nome="camaleao", espaco="pequeno", custo="alto", energia="media", afeto="baixo", alergia_pelo=False, interacao_desejada=True, animal_exotico=True)
        yield Animal(nome="cacatua", espaco="grande", custo="alto", energia="alta", afeto="alto", alergia_pelo=False, interacao_desejada=True, animal_exotico=True)
        yield Animal(nome="arara", espaco="grande", custo="alto", energia="media", afeto="alto", alergia_pelo=False, interacao_desejada=True, animal_exotico=True)
        yield Animal(nome="galinha", espaco="grande", custo="baixo", energia="baixa", afeto="baixo", alergia_pelo=False, interacao_desejada=False, ambiente_rural=True)
        yield Animal(nome="iguana", espaco="grande", custo="medio", energia="media", afeto="baixo", alergia_pelo=False, interacao_desejada=False, animal_exotico=True)
        yield Animal(nome="mini_porco", espaco="medio", custo="alto", energia="alta", afeto="alto", alergia_pelo=False, interacao_desejada=True, animal_exotico=True, ambiente_rural=True)
        yield Animal(nome="mini_vaca", espaco="grande", custo="alto", energia="alta", afeto="alto", alergia_pelo=False, interacao_desejada=True, animal_exotico=True, ambiente_rural=True)
        yield Animal(nome="mini_cabra", espaco="grande", custo="alto", energia="alta", afeto="alto", alergia_pelo=False, interacao_desejada=True, animal_exotico=False, ambiente_rural=True)

    # Regras baseadas nas preferências declaradas pelo usuário
    @Rule(
        AND(
            UserPreferences(tipo_casa=MATCH.tipo_casa),
            UserPreferences(alergia_pelo=MATCH.alergia_pelo),
            UserPreferences(espaco=MATCH.espaco),
            UserPreferences(tempo_disponivel=MATCH.tempo),
            UserPreferences(interacao_desejada=MATCH.interacao),
            UserPreferences(animal_exotico=MATCH.exotico),
            UserPreferences(nojo_roedor=MATCH.nojo),
            UserPreferences(ambiente_rural=MATCH.rural)
        )
    )
    def recomendar_pet_ideal(self, tipo_casa, alergia_pelo, espaco, tempo, interacao, exotico, nojo, rural):
        # Filtra os fatos de Animal que atendam exatamente às preferências
        possiveis = [f for f in self.facts.values() if isinstance(f, Animal)]
        for pet in possiveis:
            match_tipo = (tipo_casa in pet.get('tipo_casa', [tipo_casa]))
            match_alergia = (pet['alergia_pelo'] == alergia_pelo)
            match_espaco = (pet['espaco'] == espaco)
            match_tempo = (tempo in (pet.get('tempo_disponivel', [tempo])))
            match_inter = (pet['interacao_desejada'] == interacao)
            match_exot = (pet.get('animal_exotico', False) == exotico)
            match_nojo = not (nojo and pet.get('nojo_roedor', False))
            match_rural = (pet.get('ambiente_rural', False) == rural)
            if all([match_tipo, match_alergia, match_espaco, match_tempo, match_inter, match_exot, match_nojo, match_rural]):
                self.declare(Animal(recomendado=pet['nome']))
                return

    # Caso nenhuma regra gere recomendação, não declara pet
    @Rule(NOT(Animal(recomendado=W())))
    def sem_recomendacao(self):
        pass  # Não declara fallback
