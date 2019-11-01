class WorkPlace:
    def __init__(self,name,type_,work, initialTime,changeTime,efficiency):
        self.name = name
        self.type = type_
        self.work = work
        self.initialTime = initialTime #time spent before starting a production
        self.changeTime = changeTime #time used to change the work
        self.efficiency = efficiency