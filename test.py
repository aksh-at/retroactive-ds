from trivial_ds import Trivial_DS
from partial_to_full import Partial_To_Full

full_retro = Partial_To_Full(Trivial_DS)

full_retro.Insert(1, 'incr', 2)
full_retro.Insert(3, 'incr', 3)

print full_retro.Query(0)
print full_retro.Query(2)
print full_retro.Query(4)

print "Deleting first insert"
full_retro.Delete(1)

print full_retro.Query(0)
print full_retro.Query(2)
print full_retro.Query(4)

print "Deleting second insert"
full_retro.Delete(3)

print full_retro.Query(0)
print full_retro.Query(2)
print full_retro.Query(4)
