from itertools import *
from sets import Set
import math
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction

def prime_fact(n):
    if n <= 2:
        return [n]
    lst = []
    while n > 2:
        for i in range(2,n):
            if n % i == 0:
                n = n/i
                lst.append(i)
                if n <= 2:
                    lst.append(2)
                    return lst
                break
            if i == n-1:
                lst.append(n)
                return lst

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

def orbit_cycles(n,(y,x)):
    all_cycles = []
    for i in xrange(n):
        all_cycles.append((tuple(sorted(map(lambda t: (t+i)%n,y))),tuple(sorted(map(lambda t: (t+i)%n,x)))))
    return all_cycles

#print all_cycles(4,((1,2),(1,)))

def cyclic_p_i(n,i,r):
    pairs_set = pairs(n,i,r)
    reduced_pairs = []
    while len(pairs_set) > 0:
        elt = pairs_set.pop()
        reduced_pairs.append(elt)
        cycles = edge_cycles(n,elt)
        for i in cycles:
            if i in pairs_set:
                pairs_set.remove(i)
    return reduced_pairs

def cyclic_p_i(n,i,r):
    pairs_set = pairs(n,i,r)
    reduced_pairs = []
    while len(pairs_set) > 0:
        elt = pairs_set.pop()
        reduced_pairs.append(elt)
        cycles = edge_cycles(n,elt)
        for i in cycles:
            if i in pairs_set:
                pairs_set.remove(i)
    return reduced_pairs

def cyclic_q_i(n,i,r):
    pairs_set = pairs(n,i,r)
    reduced_pairs = []
    while len(pairs_set) > 0:
        elt = pairs_set.pop()
        reduced_pairs.append(elt)
        cycles = orbit_cycles(n,elt)
        for i in cycles:
            if i in pairs_set:
                pairs_set.remove(i)
    return reduced_pairs



#print cyclic_p_i(3,2,1)

def nCk(n,k): 
    return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

def calculate_p_i(n,i):
    return nCk(n-1,i-1)


for n in range (3,8):
    for i in range(1,n+1):
        print (n,i,len(cyclic_q_i(n,i,1)))
    print 'finished ' + str(n)


'''
for n in range (3,15):
    for i in range(2,n+1):
        print (n,i,prime_fact(len(cyclic_q_i(n,i,2))))
#        print (n,i,len(cyclic_q_i(n,i,2)))
    print 'finished ' + str(n)
'''
'''
for n in range (13,17):
    for i in range(7,n+1):
        print (n,i,len(cyclic_p_i(n,i,7)))
    print 'finished ' + str(n)
'''



'''for n in range (18,19):
    for i in range(8,9):
#        print cyclic_q_i(n,i,1)
#        print cyclic_p_i(n,i,1)
        print (n,i,set(cyclic_q_i(n,i,1)).difference(set(cyclic_p_i(n,i,1))))
    print 'finished ' + str(i)
'''
