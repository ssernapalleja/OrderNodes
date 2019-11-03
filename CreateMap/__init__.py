from Node.__init__ import Node
from NodeMap.__init__ import NodeMap
from graphviz import Digraph
from WorkPlace import possibleWork
from WorkPlace.__init__ import WorkPlace

import random
import math

def expRandom(max_):
    val = random.uniform(0, math.log(max_))
    return math.floor(math.exp(val)) 
def createName(level,num):
    return str(level)+"-"+str(num)


#
#create Randoms Node Map, with conexion between them
def createMap(nameMap):
    MIN_LEVEL_NODOS = 5
    MAX_LEVEL_NODOS = 20
    
    MIN_NODES_NUMBER = 25
    MAX_NODES_NUMBER = 100
    
    MAX_NUMBER_WORKERS = 3
    MAX_TIME=20
    MAX_PREV_CONEXIONS=3
    
    
    #create Random Nodes.
    
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
    
    nodes = {}
    for k,group in mapaNodos.items():
        for k2,n in group.items():
            nodes[k2]=n
    map_ = NodeMap(nameMap,random.randrange(1, 3,1),random.randrange(500, 10000,10),nodes)
    return map_





#create random WorkPlaces for the production Line
def createWorkPlaces():
    MAX_NUMBERS_WP = 50
    MAX_TIME_INITIAL_TIME = 0.5
    MAX_TIME_CHANGE_TIME = 0.5
    MIN_EFFICIENCI = 0.5
    MAX_EFFICIENCI = 0.8
    
    workPlacesMap = []
    for wp in possibleWork:
        NumberOfWP = random.randrange(1,MAX_NUMBERS_WP,1)        
        for a in range(NumberOfWP):
            possibleChanges=random.randrange(0,2,1)
            wps = [wp]
            for i in range(possibleChanges):
                new = random.choice(possibleWork)
                if not(new in wps):
                    wps.append(new)
            itime = round(random.uniform(0,MAX_TIME_INITIAL_TIME),2)
            ctime = round(random.uniform(0,MAX_TIME_CHANGE_TIME),2)
            ef = round(random.uniform(MIN_EFFICIENCI,MAX_EFFICIENCI),2)
            workPlacesMap.append(WorkPlace( wp+"-"+str(a),"NA",wps,itime,ctime,ef))
    return  workPlacesMap  