import random, os
from manage import FileName

class MapLinker:
    
    #class initializer
    def __init__(self):
        self.mapdata = []
        self.mapfiles = FileName.mapfiles.value # get filenames
        self.before_get = None # all cases are available
        # read all files
        for mp in self.mapfiles:
            with open(os.path.join(FileName.map_sprites.value, mp), "r") as f: # open file
                data = str(f.read()).split("\n")
                assert len(data) >= 4
                self.mapdata.append(data)
                
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
    
    def get_next(self):
        ret_list = []
        for d in self.mapdata:
            if self.is_match(self.before_get, d):
                ret_list.append(d)
        idx = random.randint(0, len(ret_list) - 1)
        self.before_get = ret_list[idx]
        return ret_list[idx]
