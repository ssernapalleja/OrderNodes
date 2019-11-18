import numpy as np
from CreateMap import loadMaps
from WorkPlace import possibleWork
from Node_WorkPlace import Node_WorkPlace


class environment:
    def __init__(self):
        self.totalMapas = 200;
        self.maxNodos = 200*5;
        self.maxWP = 15
        self.aCargar = -1;
        
        self.states_nodos = (self.maxNodos+1)*10
        self.states_wp = 6*self.maxWP
        
    
    def cargarMapaAleatorio(self, nuevo = False):
        if nuevo or self.cargar == -1:
            self.aCargar = np.random.randint(0,self.totalMapas-1)
        self.nodMaps = loadMaps('nodos'+str(self.aCargar))
        self.workPMap = loadMaps('workp'+str(self.aCargar))
        
        #normalizar valores
        self.norm_time = max([a.endDate for a in self.nodMaps], )
        self._start_posibles()
        self._mapToArray()
       
    def reiniciar(self):
        self.cargarMapaAleatorio(True)
        return self.arregloNodos, self.arregloWP
        
    def _mapToArray(self):
        
        self.arregloWP = [0] * self.states_wp 
        self.arregloNodos = [0] * self.states_nodos
        contador = 0

        max_id = 0
        
        
        for _map in self.nodMaps:
            for _key,nod in _map.nodes.items():
                
                if not hasattr(nod,'id'):
                    contador += 1
                    nod.id = contador
                    #max_id = max(contador,max_id )
                elif nod.id == 0:
                    contador += 1
                    nod.id = contador
                    #max_id = max(contador,max_id )
                self.arregloNodos[nod.id*10]=(nod.id) #0 nombre
                if nod in self.posibles :    
                    self.arregloNodos[nod.id*10+1]=(1) #1 si es posible
                else :
                    self.arregloNodos[nod.id*10+1]=(0)
                self.arregloNodos[nod.id*10+2]=(nod.time*1000/self.norm_time) #2 tiempo de produccion
                self.arregloNodos[nod.id*10+3]=(_map.endDate) #3 fecha final
                self.arregloNodos[nod.id*10+4]=(_map.importance) #4 importancia
                self.arregloNodos[nod.id*10+5]=(possibleWork.index(nod.work)) #5 donde puede ir
                self.arregloNodos[nod.id*10+6]=(0) #6 endDate
                cont = 0
                for pr in nod.prev.values(): #7 8 9 previos
                    cont += 1
                    if not hasattr(pr,'id'):
                        contador += 1
                        pr.id = contador
                    elif pr.id == 0:
                        contador += 1
                        pr.id = contador
                        #max_id = max(pr.id,max_id )
                    self.arregloNodos[nod.id*10+6+cont]=(pr.id)
                    if(cont == 3):
                        break
                if cont < 3:
                    for _r in range(cont,3):
                        self.arregloNodos[nod.id*10+6+_r+1]=(-1)
                
        
        id_wp = -1 
        for wp in self.workPMap: #previos
            id_wp +=1
            wp.id = id_wp
            cont = 0
            self.arregloWP[wp.id*6]=0
            for i in wp.work:
                cont += 1
                self.arregloWP[wp.id*6 + cont] = possibleWork.index(i)
            if cont < 5:
                for _k in range(cont,5):
                    self.arregloWP[wp.id*6 + _k + 1] = -1
                    
                
    def select_random(self) : #selecciona un nodo aleatorio, y una ubicacion posible de forma aleatoria, con una probabilidad del 50 % que no sea correcta
        a = np.random.choice(self.posibles) 
        
        b = np.random.randint(len(self.workPMap)-1)
        while not ( a.work in  self.workPMap[b].work):
            b = (b+1)%len(self.workPMap)
        return a.id, b
                

        
    def step(self,action_node,action_workPlace):
       
       #node_id = self.posibles.index( )
        
        
        workplace_id = action_workPlace
        node = next(filter(lambda x: x.id == action_node,  self.posibles))
        workplace = self.workPMap[workplace_id]


        listaFechas = [x.endDate for x in workplace.nod_wp]
        date = 0
        
        poner_espacio=False
        if len(listaFechas)>0:
            date = max(listaFechas)+0.01 #encontrar el mas grande de todos
        for _, prevN in node.prev.items():
            if date < prevN.nod_wp.endDate:
                date = prevN.nod_wp.endDate
                #poner_espacio = True revisar.. cual es la mejor opcion
                
        if not poner_espacio:    
            new = Node_WorkPlace(workplace,node,date) 
            try:
                if new.available:
                    #update new initial nodes
                    for __,next_ in node.next.items():
                        addNew = True;
                        if not( next_ in self.posibles): # don't have already added to the initial
                            for ___,prev in next_.prev.items():
                                if(prev.isPlaced == False):
                                    addNew = False
                                    break
                            if addNew:
                                self.posibles.append(next_)
                                self.arregloNodos[next_.id*10+1] = 1 #agrega de los posibles
                        #remove new one
                    self.posibles.remove(node)
                    self.arregloNodos[node.id*10+1] = 0 #sale de los posibles
                    self.arregloNodos[next_.id*10+6] = new.endDate*1000/self.norm_time #fecha final
                    self.arregloWP[workplace_id*6] = new.endDate*1000/self.norm_time #fecha final
                else :
                    return self.arregloNodos,self.arregloWP,-1000.0,False
            except:   
                return self.arregloNodos,self.arregloWP,-1000.0,False  
                print("error 420")   
            


        terminado = len(self.posibles) == 0
        
        
        return self.arregloNodos,self.arregloWP,self.calcularGanancia(),terminado 

    
    def calcularGanancia(self):
        total = 0.0
        for map in self.nodMaps:
            nodes_val = list(map.nodes.values())
            if all(x.isPlaced for x in nodes_val):
                lastProduccion = max(x.nod_wp.endDate for x in nodes_val)
                total += (min( x.npd_wp.StartDate for x in nodes_val)-lastProduccion)/self.norm_time
                if(lastProduccion < map.endDate):
                    total += 100 - ((map.endDate - lastProduccion)/8*15 )
                else:                              
                    total += - ((map.endDate - lastProduccion)/8*50*(map.importance+1))
        #print(total)
        #if total != 0:
        #    print(total)
        return max([-500,total])
    
    def _start_posibles(self):
        self.posibles = []
        for pro in self.nodMaps:
            for key,node in pro.nodes.items():
                if len(node.prev) == 0:
                    self.posibles.append(node)
     
     
            
    