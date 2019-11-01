from Node.__init__ import Node
from NodeMap.__init__ import NodeMap
from graphviz import Digraph

import random
import math

def expRandom(max_):
    val = random.uniform(0, math.log(max_))
    return math.floor(math.exp(val)) 
def createName(level,num):
    return str(level)+"-"+str(num)

def createMap():
    MIN_LEVEL_NODOS = 5
    MAX_LEVEL_NODOS = 20
    
    MIN_NODES_NUMBER = 25
    MAX_NODES_NUMBER = 100
    
    MAX_NUMBER_WORKERS = 3
    MAX_TIME=20
    MAX_PREV_CONEXIONS=3
    
    
    #create Random Nodes.
    possibleWork = ["a","b","c","d"]
    numberNodes = random.randrange(MIN_NODES_NUMBER, MAX_NODES_NUMBER, 1);
    maxNumberLevels = random.randrange(MIN_LEVEL_NODOS, MAX_LEVEL_NODOS, 1);
    # print ("Nodos:" + str(numberNodes))
    mapaNodos = {}
    level = 0
    while numberNodes > 0:
        level += 1
        totNodes = random.randrange(1, maxNumberLevels, 1);#numero total de nodos
        levelNodos={}#nodos en el nivel   
        for x in range(totNodes):
            #crea nodo
            name = createName(level,x)
            levelNodos[name] = Node(name,random.randrange(1, MAX_TIME),random.randrange(1, MAX_NUMBER_WORKERS,1),random.choice(possibleWork),1,"-")
            if level > 1:
                #crea conexiones
                totalConexions = expRandom(MAX_PREV_CONEXIONS+1) 
                for n in range(totalConexions):
                    levelConx = level-expRandom(level)
                    prevName = createName(levelConx, random.randrange(0,len(mapaNodos[levelConx]),1))
                    levelNodos[name].setPrev(mapaNodos[levelConx][prevName])
        #agrega los nodos
        mapaNodos[level] = levelNodos
        numberNodes -= len(levelNodos)    
    
    #agregamos un nodo final para todos los que no tienen un next:
    level +=1
    name = createName(level,x)
    lastNode = {}
    lastNode[name] = Node(name,random.randrange(1, MAX_TIME),random.randrange(1, MAX_NUMBER_WORKERS,1),random.choice(possibleWork),1,"-")
    for key in mapaNodos:
        for key2 in  mapaNodos[key] :
            if len(mapaNodos[key][key2].next) == 0: 
                mapaNodos[key][key2].setNext(lastNode[name])
    mapaNodos[level] = lastNode   
    #imprimimos 
    ''''g = Digraph('G', filename='hello.gv')       
    for key in mapaNodos:
        print(str(key)+"--------")
        for key2 in  mapaNodos[key] :
            print("  "+key2)
            for key3 in mapaNodos[key][key2].next: 
                g.edge(key2, key3)
                print("    "+key3)       
          
    print("+++++++++++++")      
    for key in mapaNodos:
        print(str(key)+"--------")
        for key2 in  mapaNodos[key] :
            print("  "+key2)
            for key3 in mapaNodos[key][key2].prev: 
                print("    "+key3)     
    
    g.view()'''
    return mapaNodos