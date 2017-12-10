class Retroactive_DS: 
    """
    Template for retroactive data structures.      
    """
    def Insert(self, time, op_name, *args):
        pass

    def Delete(self, time):
        pass

    # for partial ds time will be ignored
    def Query(self, time, *args): 
        pass

#TODO: make inheritance relation from the above class to this. 
# Maybe subsume version in *args for insert and delete?
class Fully_Persistent_Retroactive_DS: 
    """
    Template for fully persistent, partially retro data structures.  
    Assume initial version is 0
    """

    # returns new version_no
    def Persistent_Insert(self, version, time, op_name, *args):
        pass

    # returns new version_no
    def Persistent_Delete(self, version, time):
        pass

    # for partial ds time will be ignored
    def Query(self, time, *args): 
        pass
