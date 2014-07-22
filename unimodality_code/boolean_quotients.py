from itertools import *
from sets import Set
import math
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction

#computes the product first doing b and then a
def perm_mult(a,b):
    return tuple(map(lambda i: a[i],b))

def compute_group(generators):
    temp_set = set(generators)
    full_set = Set([])
    while len(temp_set) != 0:
        g = temp_set.pop()
        for elt in generators:
            prod = perm_mult(elt,g)
            if prod not in full_set:
                full_set.add(prod)
                temp_set.add(prod)
    return full_set

class Grp:
#lst should be nonempty
    def __init__(self,tpl_lst):
        self.generators = tpl_lst
        self.action_size = len(tpl_lst[0])
        self.group_set = compute_group(self.generators)

#grp = Grp([(1,0,2,3,4,5,6),(0,2,1,3,4,5,6),(0,1,3,2,4,5,6),(0,1,2,4,3,5,6),(0,1,2,3,5,4,6),(0,1,2,3,4,6,5)])
#print len(grp.group_set)

#computes all pairs in the boolean algebra
def pairs(n,i,r):
    lst = range(n)
    if r == 0:
        return set(combinations(lst,i))
    else:
        size_i_sets = combinations(lst,i)
        pair_sets = Set([])
        for t in size_i_sets:
            t = t
            x = combinations(t,i-r)
            for s in x:
                pair_sets.add((t,s))
        return pair_sets

#print pairs(4,2,1)

def act(elt,x):
    return tuple(sorted(map(lambda i: elt[i],x)))

#print act([0,2,1],(0,1))

#returns the set of all elements in the orbit of x
def orbit(g_lst,x):
    orbit_set = Set([])
    temp_set = Set([x])
    while len(temp_set)!=0:
        t = temp_set.pop()
        orbit_set.add(t)
        for elt in g_lst:
            gt = act(elt,t)
            if gt not in orbit_set:
                temp_set.add(gt)
    return orbit_set

#print orbit([[1,2,3,0],[1,0,2,3]],(2,3))

#returns the set of all elements in the orbit of (y,x)
def pair_orbit(g_lst,(y,x)):
    orbit_set = Set([])
    temp_set = Set([(y,x)])
    while len(temp_set)!=0:
        (t,r) = temp_set.pop()
        orbit_set.add((t,r))
        for elt in g_lst:
            (gt,gr) = (act(elt,t),act(elt,r))
            if (gt,gr) not in orbit_set:
                temp_set.add((gt,gr))
    return orbit_set

#print pair_orbit([[1,2,3,0]],((2,3),(3,)))

#returns the set of all edges in the G\times G orbit of y,x
def edge_orbit(g_lst,(y,x)):
    whole_orbit = []
    x_cycles = orbit(g_lst,x)
    y_cycles = orbit(g_lst,y)
    for i in x_cycles:
        for j in y_cycles:
            if set(i).issubset(set(j)):
                whole_orbit.append((sorted(j),sorted(i)))
    return whole_orbit

#print edge_orbit([[1,2,3,0]],((2,3),(3,)))

#returns a list of representatives of the level i orbits
def vert_by_rank(g_lst,i):
    n = len(g_lst[0])
    level_i_set = map(tuple,pairs(n,i,0))
    reduced_verts = []
    while len(level_i_set) > 0:
        elt = level_i_set.pop()
        reduced_verts.append(elt)
        orb = orbit(g_lst,elt)
        for i in orb:
            if i in level_i_set:
                level_i_set.remove(i)
    return reduced_verts

#returns a list of the sets of orbits of all level i elements
def set_vert_by_rank(g_lst,i):
    n = len(g_lst[0])
    level_i_set = map(tuple,pairs(n,i,0))
    reduced_verts = []
    while len(level_i_set) > 0:
        elt = level_i_set.pop()
        orb = orbit(g_lst,elt)
        reduced_verts.append(orb)
        for i in orb:
            if i in level_i_set:
                level_i_set.remove(i)
    return reduced_verts

#print set_vert_by_rank([[1,2,3,4,5,6,0]],2)

#returns a list of edges, given by representatives
def edge_by_vert_counted(g_lst,vert_bot,vert_top):
    edge_lst = []
    count_dict = {}
    orb_bot_lst = map(lambda t: orbit(g_lst,t),vert_bot)
    orb_top_lst = map(lambda t: orbit(g_lst,t),vert_top)
    for a in xrange(len(vert_bot)):
        for b in xrange(len(vert_top)):
            count = 0
            for i in orb_bot_lst[a]:
                for j in orb_top_lst[b]:
                    if set(i).issubset(set(j)):
                        count += 1
            if count > 0:
                edge_lst.append((vert_top[b],vert_bot[a]))
                count_dict[(vert_top[b],vert_bot[a])]=(count,b,a)
    return edge_lst,count_dict

#returns a list of edges, with their full orbits
def set_edge_by_vert(g_lst,orb_bot_lst,orb_top_lst):
    edge_lst = []
    for a in orb_bot_lst:
        for b in orb_top_lst:
            edge_orbit = Set([])
            for i in a:
                for j in b:
                    if set(i).issubset(set(j)):
                        edge_orbit.add((j,i))
            if len(edge_orbit)>0:
                edge_lst.append(edge_orbit)
    return edge_lst

def edge_by_vert(g_lst,vert_bot,vert_top):
    edge_lst = []
    orb_bot_lst = map(lambda t: orbit(g_lst,t),vert_bot)
    orb_top_lst = map(lambda t: orbit(g_lst,t),vert_top)
    for a in xrange(len(vert_bot)):
        for b in xrange(len(vert_top)):
            if any(set(i).issubset(set(j)) for i in orb_bot_lst[a] for j in orb_top_lst[b]):
                edge_lst.append((vert_top[b],vert_bot[a]))
    return edge_lst

def grp_i_edges_from_vert(g_lst,i):
    vert_bot = vert_by_rank(g_lst,i)
    vert_top = vert_by_rank(g_lst,i+1)
    return edge_by_vert(g_lst,vert_by_rank(g_lst,i),vert_by_rank(g_lst,i+1))


def edges_above_vert(g_lst,v):
    edge_lst = []
    i = len(v)
    orbit_bot = orbit(g_lst,v)
    vert_top = vert_by_rank(g_lst,i+1)
    orb_top_lst = map(lambda t: orbit(g_lst,t),vert_top)
    for b in xrange(len(vert_top)):
        if any(set(i).issubset(set(j)) for i in orbit_bot for j in orb_top_lst[b]):
            edge_lst.append((vert_top[b],v))
    return edge_lst

def edges_below_vert(g_lst,v):
    edge_lst = []
    i = len(v)
    orbit_top = orbit(g_lst,v)
    vert_bot = vert_by_rank(g_lst,i-1)
    orb_bot_lst = map(lambda t: orbit(g_lst,t),vert_bot)
    for a in xrange(len(vert_bot)):
        if any(set(i).issubset(set(j)) for j in orbit_top for i in orb_bot_lst[a]):
            edge_lst.append((v,vert_bot[a]))
    return edge_lst

#print edges_above_vert([[1,2,3,4,5,0]],(0,1))

def cyclic_g_lst(n):
    a = range(1,n)
    a.append(0)
    return [tuple(a)]

def dihedral_g_lst(n):
    a = range(1,n)
    a.append(0)
    b = list(reversed(range(1,n)))
    b = [0]+b
    return [tuple(a),tuple(b)]

def symmetric_g_lst(n):
    lst = []
    for i in xrange(n-1):
        t = range(n)
        t[i] = i+1
        t[i+1] = i
        lst.append(tuple(t))
    return lst


'''
k = 5
gl = cyclic_g_lst(k)

for i in range(k):
    print set_edge_by_vert(gl,set_vert_by_rank(gl,i),set_vert_by_rank(gl,i+1))
'''
'''
n = 9
gl = [[1,2,0,3,4,5,6,7,8],[0,1,3,4,5,2,6,7,8],[0,1,2,3,4,6,5,7,8],[0,1,2,3,4,5,6,8,7]]

for i in range(1,(n+1)/2):
    print 'here is level ' + str(i)
    for j in vert_by_rank(gl,i):
        print len(edges_above_vert(gl,j)) - len(edges_below_vert(gl,j))
        if len(edges_above_vert(gl,j)) - len(edges_below_vert(gl,j)) <0:
            print edges_above_vert(gl,j)
            print edges_below_vert(gl,j)
gl = map(tuple,gl)

for i in range(1,(n+1)/2):
    print 'here is level ' + str(i)
    for j in vert_by_rank(gl,i):
        print len(edges_above_vert(gl,j)) - len(edges_below_vert(gl,j))
        if len(edges_above_vert(gl,j)) - len(edges_below_vert(gl,j)) <0:
            print edges_above_vert(gl,j)
            print edges_below_vert(gl,j)
'''
