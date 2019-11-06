from CreateMap.__init__ import createMap
from CreateMap.__init__ import createWorkPlaces

from CreateMap import saveMaps

NUMBERS_OF_PRODUCTS = 20
NUMBERS_OF_WORKPLACE = 5

#Create Diagrams of process
MaxNodos = 0;
MaxWP = 0
print("starting")
for j in range(200):
    proMaps=[]
    tempNodos = 0
    if(j%10 == 0):
        print(str(j/10))
    
    for i in range(NUMBERS_OF_PRODUCTS):
        temp = createMap(str(i))
        proMaps.append(temp)
        tempNodos += len(temp.nodes)
    #Create Workplace
    MaxNodos = max(tempNodos,MaxNodos)
    
    workPMap = createWorkPlaces(NUMBERS_OF_WORKPLACE)
    MaxWP = max(len(workPMap),MaxWP)
    #guardar y cargar datos
    
    saveMaps(workPMap,'workp'+str(j))
    saveMaps(proMaps,'nodos'+str(j))



COLOURS = {}
colorValues = {0:"ef",1:"aa",2:"05",3:"10"}
colorCount = 0;
for a in range(4):
    for b in range(4):
        for c in range(4):
            COLOURS[str(colorCount)]= "#"+colorValues[a]+colorValues[b]+colorValues[c]
            colorCount+=1

saveMaps(COLOURS,'colores')

print("end")
print (MaxNodos)
print(MaxWP)
