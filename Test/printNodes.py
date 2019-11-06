'''
Created on 5/11/2019

@author: Guest
'''
from graphviz import Digraph

def printPDFNodes(workPMap):
    
    COLOURS = {}
    colorValues = {0:"ef",1:"aa",2:"05",3:"10"}
    colorCount = 0;
    for a in range(4):
        for b in range(4):
            for c in range(4):
                COLOURS[str(colorCount)]= "#"+colorValues[a]+colorValues[b]+colorValues[c]
                colorCount+=1
    
    
#Print:
    g = Digraph('G', engine="neato", filename='test.gv',format='pdf')
    g.attr(size='7')
    #workPMap
    cont = 0
    maximo = 0;
    NodeMaps={}
    
    for wp in workPMap:
        g.node(wp.name,pos='-1,'+str(cont)+'!', color="#ff0000",shape="box",width="1")
        for nd in wp.nod_wp:
            if maximo <nd.endDate:
                maximo = nd.endDate
            largo = nd.endDate-nd.startDate
            posi = str(nd.startDate+largo/2)+','+str(cont)+'!'   
            nombre = nd.node.mapper.name+"  "+nd.node.name
            g.node(nombre,pos=posi, color=COLOURS[str(nd.node.mapper.name)],shape="box",width=str(largo))        
            NodeMaps[nd.node.mapper.name]=nd.node.mapper.endDate
        cont+=1
    
    for k,endDate in NodeMaps.items():
        posi = str(int(endDate))+',-2!'
        g.node("last" + str(endDate),pos=posi, color=COLOURS[str(k)],shape="box")        
    
    for i in range(0,int(maximo),10):
        posi = str(i)+',-1!'
        g.node(str(i),pos=posi, color="black",)        
    
    #for wp in workPMap:
    #    for nd in wp.nod_wp:
    #        for k,nx in nd.node.next.items() :
    #            g.edge(nd.node.mapper.name+"  "+nd.node.name,nx.mapper.name+"  "+nx.name)
             
             
             
             
             
    print("render...")
    g.render()
    print("render done, starting view")
    g.view()
    print("view end")



