class folder :
    def __init__(self):
        self.name = ""
        self.path = ""
        self.haveFiles = False
        self.type = ""
    
    def getName (self):
        return self.name
    def getPath (self):
        return self.path
    def haveFiles (self):
        return self.haveFiles
    def haveFiles(self, val):
        self.haveFiles = val
    def setType(self, val):
        self.type = val
    def getType(self):
        return self.type