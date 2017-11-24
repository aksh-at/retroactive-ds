class DS: # partial
    """
    Template for data structures.
    """

    def __init__(self):
        self.ops = {}

    # add_op and remove_op can be replaced by an OFM structure later instead of our hash of fraction times
    def add_op(self, time, op):
        self.ops[time] = op

    def pop_op(self, time):
        store = self.ops[time]
        del self.ops[time]
        return store

    def Insert(self, time, op_name, *args):
        pass

    def Delete(self, time):
        pass

    # for partial ds time will be ignored
    def Query(self, time, *args): 
        pass
