from ds import DS

class Trivial_DS(DS):

    def __init__(self, size):
        DS.__init__(self)
        self.A = [0] * size

    def incr(self, idx, val):
        self.A[idx] += val

    def undo_incr(self, idx, val):
        self.A[idx] -= val

    def Insert(self, time, op_name, *args):
        self.add_op(time, (op_name, args))
        getattr(self, op_name)(*args)

    def Delete(self, time):
        (op_name, args) = self.pop_op(time)
        getattr(self, "undo_"+op_name)(*args)

    def Query(self, time, *args):
        idx = args[0]
        return self.A[idx]

def shit_test():
    trivial_DS = Trivial_DS(5)
    trivial_DS.Insert(0.0, "incr", 1, 2)
    print trivial_DS.Query(5.0, 1)
    print trivial_DS.Query(5.0, 0)
    trivial_DS.Insert(0.3, "incr", 1, 3)
    print trivial_DS.Query(5.0, 1)
    print trivial_DS.Query(5.0, 0)
    trivial_DS.Delete(0.0)
    print trivial_DS.Query(5.0, 1)
    print trivial_DS.Query(5.0, 0)
