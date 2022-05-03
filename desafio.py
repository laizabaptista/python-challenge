# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from copy import deepcopy

facts = [
  ('gabriel', 'endereço', 'av rio branco, 109', True),
  ('joão', 'endereço', 'rua alice, 10', True),
  ('joão', 'endereço', 'rua bob, 88', True),
  ('joão', 'telefone', '234-5678', True),
  ('joão', 'telefone', '91234-5555', True),
  ('joão', 'telefone', '234-5678', False),
  ('gabriel', 'telefone', '98888-1111', True),
  ('gabriel', 'telefone', '56789-1010', True),
  ('yago', 'endereço', 'rua errada, 10', True),
  ('yago', 'endereço', 'rua torta, 88', True),
  ('yago', 'telefone', '234-567344', True),
]


schema = [
    ('endereço', 'cardinality', 'one'),
    ('telefone', 'cardinality', 'many')
]
   
#remove o que contem falso
def removeFalse(facts):
    return list(filter(lambda x: False not in x,facts))

#remove elementos
def deleteElements(list, removed):
    for s in sorted(removed, reverse=True):
        list.pop(s)

    return list

# retorna uma lista com os nomes
def deleteCopies(elements):
    elements = list(dict.fromkeys(elements))
    return elements

#Remove todos os registros iguais e mais antigos do que o expirado
def deleteExpired(facts, expiredElement):
    expiredElementTrue = expiredElement[:-1] + (True,)

    expiredIndex = facts.index(expiredElement)

    newList = list(filter((expiredElementTrue).__ne__, facts[:expiredIndex]))
    return newList + facts[expiredIndex:]

#cria uma lista aninhada com os itens que não vão ser exibidos
def flatList(list):
    flat_list = [item for sublist in list for item in sublist]
    return flat_list

# "Pega" uma lista de atributos
def getAtributeList(schema, cardinality):
    atributes = list(filter(lambda x: cardinality in x, schema))
    return list(zip(*atributes))[0]

#Calcula o index de cada registro nos fatos e retorna todos menos o mais recente
def getOlder(original, elements):

    lastIndex = 0
    indexes = [original.index(element) for element in elements]
    #remove o endereço que tem o indice maior(mais antigo)
    indexes.remove(max(indexes))
    
    return indexes

#função principal
def getCurrentFacts(facts, schema):
    #copiando os dados 
    currentyFacts = deepcopy(facts)
    expireFacts = list(
        filter(
            lambda x: False in x, currentyFacts))
    #Remove os registros iguais e mais antigos do que o expirado
    for element in expireFacts:
        currentyFacts = deleteExpired(currentyFacts, element)
    #remove o que contem falso
    currentyFacts = removeFalse(currentyFacts)
    #atribui a essa variavel o atributo  que tem a cardinalidade 1:1 - no caso do exemplo é "endereço"
    atributesOneToOne = getAtributeList(schema, "one")
    toRemoved = []
    # "Pega" os nomes 
    name = list(zip(*currentyFacts))[0]
    name = deleteCopies(name)
    #consulta cada nome , e pega os dados no nome da pessoa
    for n in name:
        registersWithName = list(filter(lambda x: n in x, currentyFacts))
    #dos itens de cada nome, ele separa só os que tem cadinalidade 1:1
        for a in atributesOneToOne:
            selectedAtributes = list(filter(lambda x: a in x, registersWithName))
            if len(selectedAtributes) > 0:
                toRemoved.append(getOlder(currentyFacts, selectedAtributes))
    
    toRemoved = flatList(toRemoved)
    currentyFacts = deleteElements(currentyFacts, toRemoved)

    return print(currentyFacts)

getCurrentFacts(facts, schema)

