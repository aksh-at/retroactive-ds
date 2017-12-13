from ds import *
import math
import bintrees

class Partial_To_Full(Retroactive_DS):
    """ 
    We maintain the log of operations, which is used by the transformation 
    from partial to full retr.  
    Note: to omit the need for a fully persistent OFM structure (or something similar), 
    we instead only keep one global map from time -> query across all versions. 
    This requires the assertion that if we insert a query at a certain time 
    and then delete it, that particular timestamp can never be used again.  

    TODO: add checks to make sure this assertion is upheld
    """
    
    # underlying_ds is an instance of Fully_Persistent_Retroactive_DS
    def __init__(self, underlying_ds):
        self.underlying_ds = underlying_ds
        self.ds_instance = underlying_ds()
        self.m = 0 #number of ops
        self.ops_since_rebalance = 0
        self.ops = bintrees.AVLTree()
        self.ops.insert(0, ('init', 0)) # init op

        # Store (timestamp, persistent_version) fo each checkpoint
        # Time 0 corresponds to Initial state of persistent structure
        self.checkpoints = [(0, 0)] 

    # Get the greatest checkpoint strictly lower than 'time'
    def get_prev_checkpoint(self, time):
        ret = 0

        while (ret + 1) < len(self.checkpoints) and self.checkpoints[ret+1][0] < time:
            ret += 1

        return ret

    def check_for_remake(self):
        self.m = len(self.ops)
        self.ops_since_rebalance += 1

        thresh = math.sqrt(self.m) / 2

        if (self.ops_since_rebalance > thresh):
            self.ops_since_rebalance = 0
            self.Remake()

    def Remake(self):
        B = int(math.ceil(math.sqrt(self.m)))

        self.checkpoints = [(0,0)]
        self.ds_instance = self.underlying_ds()

        cur_version = 0 #persistent version of underlying data structure
        i = 0
        for (time, op) in self.ops.items():
            op_name, args = op

            if op_name == 'init':
                continue
            
            cur_version = self.ds_instance.Persistent_Insert(cur_version, time, op_name, *args)
            i += 1
            if (i % B) == 0:
                self.checkpoints.append((time, cur_version))

    def Query(self, time, *args):
        target_checkpoint = self.get_prev_checkpoint(time)

        # This is the last operation that has been applied to our version already.
        cur_time, cur_version = self.checkpoints[target_checkpoint] # Start rollback at this checkpoint version
        cur_time = self.ops.ceiling_key(cur_time) # In case we deleted the op corresponding to checkpoint

        if self.ops.max_key() != cur_time:
            next_time, next_op = self.ops.succ_item(cur_time)

            while next_time <= time:
                op_name, args =  next_op
                cur_version = self.ds_instance.Persistent_Insert(cur_version, time, op_name, *args)
                if next_time == self.ops.max_key():
                    break
                next_time, next_op = self.ops.succ_item(next_time)

        # At this point, state at time has been reconstructed.
        return self.ds_instance.Query(cur_version, time, *args)

    def Insert(self, time, op_name, *args):
        target_checkpoint = self.get_prev_checkpoint(time) + 1

        while target_checkpoint < len(self.checkpoints):
            cur_time, cur_version = self.checkpoints[target_checkpoint]
            new_version = self.ds_instance.Persistent_Insert(cur_version, time, op_name, *args)
            self.checkpoints[target_checkpoint] = (cur_time, new_version)
            target_checkpoint += 1
        
        # Insert (key, value)
        self.ops.insert(time, (op_name, args))
        self.check_for_remake()

    def Delete(self, time):
        target_checkpoint = self.get_prev_checkpoint(time) + 1

        while target_checkpoint < len(self.checkpoints):
            cur_time, cur_version = self.checkpoints[target_checkpoint]
            new_version = self.ds_instance.Persistent_Delete(cur_version, time)
            self.checkpoints[target_checkpoint] = (cur_time, new_version)
            target_checkpoint += 1
        
        self.ops.remove(time)
        self.check_for_remake()

