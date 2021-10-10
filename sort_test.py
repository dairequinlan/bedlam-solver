import functools
from operator import itemgetter, attrgetter

def compare(block1, block2):
            x1,y1,z1 = block1
            x2,y2,z2 = block2
            if z1 > z2: return 1
            elif z1 < z2: return -1
            elif x1 > x2: return 1
            elif x1 < x2: return -1
            elif y1 > y2: return 1
            elif y1 < y2: return -1
            else: return 0


blocks = [[0, 0, 0],[0, 0, 1],[0, 1, 0],[1, 1, 0],[1, 2, 0]]

print(blocks)
print(sorted(blocks, key=itemgetter(2,1,0)))
#blocks.sort(key=functools.cmp_to_key(compare))
blocks.sort(key=itemgetter(2,1,0))
print(blocks)