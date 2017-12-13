from ds import *
from bintrees import AVLTree

# This is a really dumb persistent DS in which we don't even keep the version tree, since there is only one value
class Trivial_DS(Fully_Persistent_Retroactive_DS):
    def __init__(self):
        self.last_version = 0
        self.version_to_val = {}
        self.version_to_val[0] = 0
        self.ops = {}

    def init(self, version, val):
        self.last_version += 1
        self.version_to_val[self.last_version] = self.version_to_val[version] + val
        return self.last_version

    def incr(self, version, val):
        self.last_version += 1
        self.version_to_val[self.last_version] = self.version_to_val[version] + val
        return self.last_version

    def undo_incr(self, version, val):
        self.last_version += 1
        self.version_to_val[self.last_version] = self.version_to_val[version] - val
        return self.last_version

    def Persistent_Insert(self, version, time, op_name, *args):
        self.ops[time] = (op_name, args)
        return getattr(self, op_name)(version, *args)

    def Persistent_Delete(self, version, time):
        (op_name, args) = self.ops[time]
        return getattr(self, "undo_"+op_name)(version, *args)

    #ignore time since partially retroactive
    def Query(self, version, time, *args):
        return self.version_to_val[version]

def shit_test():
    trivial_DS = Trivial_DS()
    v0 = 0

    v1 = trivial_DS.Persistent_Insert(v0, 1, 'incr', 2)
    v2 = trivial_DS.Persistent_Insert(v0, 1.5, 'incr', 3)
    print trivial_DS.Query(v1, 100)
    print trivial_DS.Query(v2, 100)

    v3 = trivial_DS.Persistent_Insert(v1, 2, 'incr', 5)
    print trivial_DS.Query(v3, 100)

    v4 = trivial_DS.Persistent_Delete(v3, 1)
    print trivial_DS.Query(v4, 100)
