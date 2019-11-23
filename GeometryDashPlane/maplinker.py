import random
from manage import FileName

class MapLinker:
    
    #class initializer
    def __init__(self):
        self.mapdata = []
        self.mapfiles = FileName.mapfiles # get filenames
        self.before_get = None # all cases are available
        
        # read all files
        for mp in self.mapfiles:
            with open(mp, "r") as f: # open file
                data = str(f.read()).split("\n")
                assert len(data) >= 4
                mp.append(data)
                
    #extract UML type
    def is_match(self, data1, data2):
        if data1 == None:
            return True
        a = data1[1].split(" ")[1]
        b = data2[1].split(" ")[0]
        for i in a:
            for j in b:
                if i == j:
                    return True
        return False
    
    def get_next():
        ret_list = []
        for d in self.mapdata:
            if is_match(self.before_get, d):
                ret_list.append(d)
        idx = random.Random.randint(0,len(ret_list))
        self.before_get = ret_list[idx]
        return ret_list[idx]
