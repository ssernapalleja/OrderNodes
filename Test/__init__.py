from Node.__init__ import Node
from NodeMap.__init__ import NodeMap
from CreateMap.__init__ import createMap
from CreateMap.__init__ import createWorkPlaces
from WorkPlace.__init__ import WorkPlace
from Node_WorkPlace.__init__ import Node_WorkPlace
from graphviz import Digraph
from WorkPlace.__init__ import possibleWork


import random
import math



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
        dictWP[a]=[]
for i in workPMap:
    for a in i.work:
        dictWP[a].append(i)



while(len(posibleInitial)>0):
    print(len(posibleInitial))
    node = posibleInitial[0]
    posibleWP = dictWP[node.work]
    date = int(input("ingresa hora"))
    wp = int(input("ingresa en cual puesto de trabajo de "+str(len(posibleWP))))
    new = Node_WorkPlace(posibleWP[wp],node,date)
    try:
        if new.available:
            #update new initial nodes
            for k,next_ in node.next.items():
                addNew = True;
                if not( next_ in posibleInitial): # don't have already added to the initial
                    for k2,prev in next_.prev.items():
                        if(prev.isPlaced == False):
                            addNew = False
                            break
                    if addNew:
                        posibleInitial.append(next_)
                #remove new one
            posibleInitial.remove(node)
        else :
            print("valores no permitidos")  
    except:     
        print("error 420")      

#add to the time places
    #check if it available
    #update new initial nodes
    
