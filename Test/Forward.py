'''
Created on 5/11/2019
the AI is going to SELECT the total
this is going to add each node in a linear way, it's going to make 
@author: Guest
'''
from Node_WorkPlace.__init__ import Node_WorkPlace
from Test.printNodes import printPDFNodes
import random
from CreateMap import loadMaps


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
    
    node = posibleInitial[random.randrange(len(posibleInitial))] #select node
    posibleWP = dictWP[node.work] #select wp
    wp = random.randrange(len(posibleWP))
    listaFechas = [x.endDate for x in posibleWP[wp].nod_wp]
    date = 0
    if len(listaFechas)>0:
        date = max( listaFechas   )+0.01 #encontrar el mas grande de todos
    for k, prevN in node.prev.items():
        date = max([prevN.nod_wp.endDate+0.01, date])
        
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


printPDFNodes(workPMap)