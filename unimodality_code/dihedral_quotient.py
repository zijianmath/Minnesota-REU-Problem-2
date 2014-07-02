from itertools import *
from sets import Set
import math
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction

def pairs(n,i,r):
    lst = range(n)
    size_i_sets = combinations(lst,i)
    pair_sets = Set([])
    for t in size_i_sets:
        t = t
        x = combinations(t,i-r)
        for s in x:
            pair_sets.add((t,s))
    return pair_sets

#print pairs(4,2,1)


def edge_cycles(n,(y,x)):
    all_cycles = []
    x_cycles = map(lambda i: map(lambda t: (t+i)%n,x),range(n))
    y_cycles = map(lambda i: map(lambda t: (t+i)%n,y),range(n))
    for i in x_cycles:
        for j in y_cycles:
            if set(i).issubset(set(j)):
                all_cycles.append((tuple(sorted(j)),tuple(sorted(i))))
    return all_cycles

def dihedral_involution(n,x):
    return map(lambda t: (n-t)%n,x)

def cyclic_single_orbit(n,x):
    return map(lambda i: map(lambda t: (t+i)%n,x),range(n))

def dihedral_single_orbit(n,x):
    reverse_x = dihedral_involution(n,x)
    return cyclic_single_orbit(n,x) + cyclic_single_orbit(n,reverse_x)

def dihedral_edges(n,(x,y)):
    all_cycles = []
    x_cycles = dihedral_single_orbit(n,x)
    y_cycles = dihedral_single_orbit(n,y)
    for i in x_cycles:
        for j in y_cycles:
            if set(i).issubset(set(j)):
                all_cycles.append((tuple(sorted(j)),tuple(sorted(i))))
    return all_cycles

def cyclic_double_orbit(n,(x,y)):
    cyclic_orbits = []
    for i in xrange(n):
        cyclic_orbits.append((tuple(sorted(map(lambda t: (t+i)%n,x))),tuple(sorted(map(lambda t: (t+i)%n,y)))))
    return cyclic_orbits

def dihedral_double_orbit(n,(x,y)):
    reverse_xy = (dihedral_involution(n,x),dihedral_involution(n,y))
    return cyclic_double_orbit(n,(x,y)) + cyclic_double_orbit(n,reverse_xy)

#print all_cycles(4,((1,2),(1,)))

def dihedral_p_i(n,i,r):
    pairs_set = pairs(n,i,r)
    reduced_pairs = []
    while len(pairs_set) > 0:
        elt = pairs_set.pop()
        reduced_pairs.append(elt)
        cycles = dihedral_edges(n,elt)
        for i in cycles:
            if i in pairs_set:
                pairs_set.remove(i)
    return reduced_pairs

def dihedral_q_i(n,i,r):
    pairs_set = pairs(n,i,r)
    reduced_pairs = []
    while len(pairs_set) > 0:
        elt = pairs_set.pop()
        reduced_pairs.append(elt)
        cycles = dihedral_double_orbit(n,elt)
        for i in cycles:
            if i in pairs_set:
                pairs_set.remove(i)
    return reduced_pairs


#print cyclic_p_i(3,2,1)


for n in range (3,17):
    for i in range(2,n):
        print (n,i,len(dihedral_q_i(n,i,1)))
    print 'finished ' + str(n)


'''
for n in range (3,15):
    for i in range(2,n+1):
        print (n,i,prime_fact(len(cyclic_q_i(n,i,2))))
#        print (n,i,len(cyclic_q_i(n,i,2)))
    print 'finished ' + str(n)
'''
'''
for n in range (2,13):
    for i in range(1,n+1):
        print (n,i,len(dihedral_q_i(n,i,1)))
    print 'finished ' + str(n)
'''
'''for n in range (2,7):
    for i in range(1,n+1):
        print (n,i,len(dihedral_q_i(n,i,1)))
    print 'finished ' + str(n)
'''



'''for n in range (18,19):
    for i in range(8,9):
#        print cyclic_q_i(n,i,1)
#        print cyclic_p_i(n,i,1)
        print (n,i,set(cyclic_q_i(n,i,1)).difference(set(cyclic_p_i(n,i,1))))
    print 'finished ' + str(i)
'''
