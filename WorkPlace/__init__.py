#it's the place where you are going to produce a node
#it need to match the work, to be available the production here
#

possibleWork = ["a","b","c","d"]

class WorkPlace:
    def __init__(self,name,type_,work, initialTime,changeTime,efficiency):
        self.name = name
        self.type = type_#it could change To improve how they work there (in stock for example)
        self.work = work
        self.initialTime = initialTime #time spent before starting a production
        self.changeTime = changeTime #time used to change the work
        self.efficiency = efficiency
        self.nod_wp = []

#verifica que no se cruce con otros existentes        
    def isAvailable(self,startTime,endTime):
        valid = True
        for nwp in self.nod_wp:
            if (startTime >= nwp.startDate and startTime <= nwp.endDate) or (endTime >= nwp.startDate and endTime <= nwp.endDate) :
                valid = False
                break
            elif startTime <= nwp.startDate and endTime >= nwp.endDate:
                valid = False
                break
        return valid
            