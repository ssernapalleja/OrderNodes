'''
Created on 5/11/2019

@author: Guest
'''


from Node.__init__ import Node
from NodeMap.__init__ import NodeMap
from CreateMap.__init__ import createMap
from CreateMap.__init__ import createWorkPlaces
from WorkPlace.__init__ import WorkPlace
from Node_WorkPlace.__init__ import Node_WorkPlace
import graphviz
from graphviz import Digraph
from WorkPlace.__init__ import possibleWork

import random
import math
from CreateMap import saveMaps, loadMaps

COLOURS = {}
colorValues = {0:"ef",1:"aa",2:"05",3:"10"}
colorCount = 0;
for a in range(4):
    for b in range(4):
        for c in range(4):
            COLOURS[str(colorCount)]= "#"+colorValues[a]+colorValues[b]+colorValues[c]
            colorCount+=1

#Create Diagrams of process
proMaps = loadMaps('nodos')

#Create Workplace
workPMap = loadMaps('workp')

#Select Posible Initial nodes

total = 0
posibleInitial = []
for pro in proMaps:
    for key,node in pro.nodes.items():
        total +=1
        if len(node.prev) == 0:
            posibleInitial.append(node)
            
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


contador = 0
while(len(posibleInitial)>0):
    print(str(len(posibleInitial)) + "  "+str(contador)+" de "+str(total))
    node = posibleInitial[random.randrange(len(posibleInitial))]
    posibleWP = dictWP[node.work]
    #date = int(input("ingresa hora"))
    #wp = int(input("ingresa en cual puesto de trabajo de "+str(len(posibleWP))))
    wp = random.randrange(len(posibleWP))
    listaFechas = [x.endDate for x in posibleWP[wp].nod_wp]
    date = 0
    if len(listaFechas)>0:
        date = max( listaFechas   )+0.1 #encontrar el mas grande de todos
    for k, prevN in node.prev.items():
        date = max([prevN.nod_wp.endDate+0.1, date])
        
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
            contador +=1
        else :
            print("valores no permitidos")  
            wp = int(input("xxxxxxx "+str(len(posibleWP))))
    except:     
        print("error 420")   
        wp = int(input("xxxxxxx "+str(len(posibleWP))))   





#for wp in workPMap:
#    for nd in wp.nod_wp:
#        for k,nx in nd.node.next.items() :
#            g.edge(nd.node.mapper.name+"  "+nd.node.name,nx.mapper.name+"  "+nx.name)
         
         
         
         
         
print("render...")
g.render()
print("render done, starting view")
g.view()
print("view end")



