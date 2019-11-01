from Node.__init__ import Node
from NodeMap.__init__ import NodeMap
from CreateMap.__init__ import createMap
from CreateMap.__init__ import createWorkPlaces
from WorkPlace.__init__ import WorkPlace
from graphviz import Digraph
from WorkPlace.__init__ import possibleWork


import random
import math
from _operator import not_

NUMBERS_OF_PRODUCTS = 30



#Create Diagrams of process
proMaps=[]
for i in range(NUMBERS_OF_PRODUCTS):
    proMaps.append(createMap())

#Create Workplace
workPMap = createWorkPlaces()

#Select Posible Initial nodes
posibleInitial = []
for pro in proMaps:
    for key in pro:
        for keyNode in pro[key]:
            if len(pro[key][keyNode].prev) == 0:
                posibleInitial.append(pro[key][keyNode])
            
print(len(posibleInitial))
print(len(proMaps))
print(len(workPMap))

#crear un dictionary con los workplaces
dictWP = {};
for i in workPMap:
    for a in i.work:
        dictWP[a].append(i)



while(len(posibleInitial)>0):
    node = posibleInitial[0]
    posibleWP = dictWP[node.work]
    date = input("ingresa hora")
    wp = input("ingresa en cual puesto de trabajo")

#add to the time places
    #check if it available
    #update new initial nodes