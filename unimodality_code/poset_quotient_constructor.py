import boolean_quotients as bq
import numpy as np
import random
from itertools import *

class Poset:
    def __init(self):
        self.rank = 0
        self.vertices = []
        self.edges = []

def make_edge_mats(rank,vertices,edges,edge_counts):
    edge_mats = []
    for i in xrange(rank):
        rank_mat = np.zeros((len(vertices[i+1]),len(vertices[i])))
        for level_edge in edges[i]:
            (ct,b,a) = edge_counts[level_edge]
            rank_mat[b][a] = ct
        edge_mats.append(rank_mat)
    return edge_mats

def vert_dict(vertices):
    vert_dict = {}
    for i in range(len(vertices)):
        for j in range(len(vertices[i])):
            vert_dict[vertices[i][j]] = j
    return vert_dict

class Boolean_enlarge(Poset):
    def __init__(self,group):
        self.group = group
        self.rank = group.action_size
        self.vertices = []
        self.edges = []
        self.edge_counts = {}
        
        for i in xrange(self.rank+1):
            self.vertices.append(combinations(range(self.rank),i))

        ranked_orbits= []
        for i in xrange(self.rank+1):
            ranked_orbits.append(bq.set_vert_by_rank(group.generators,i))
        
        for i in xrange(self.rank):
            edge_i = []
            for a in ranked_orbits[i]:
                for b in ranked_orbits[i+1]:
                    if any(set(p).issubset(set(q)) for p in a for q in b):
                        for m in a:
                            for n in b:
                                edge_i.append((n,m))
            self.edges.append(edge_i)

    def edgify(self):
        edge_poset = Boolean_enlarge(self.group)
        edge_poset.rank = self.rank - 1
        edge_poset.vertices = self.edges
        edge_poset.edges = []
        edge_poset.edge_counts = {}
        edge_poset.edge_mats = []
        vert_d = vert_dict(edge_poset.vertices)

        for i in xrange(edge_poset.rank):
            edge_i = []
            for (y,x) in edge_poset.vertices[i]:
                for (b,a) in edge_poset.vertices[i+1]:
                    if set(y).issubset(set(b)) and set(x).issubset(set(a)):
                        edge_i.append(((b,a),(y,x)))
                        edge_poset.edge_counts[((b,a),(y,x))] = (1,vert_d[(b,a)],vert_d[(y,x)])
            edge_poset.edges.append(edge_i)
    
        edge_poset.edge_mats = make_edge_mats(edge_poset.rank,edge_poset.vertices,edge_poset.edges,edge_poset.edge_counts)

        return edge_poset

class Poset_edge_quot(Poset):
    def __init__(self,group):
        self.group = group
        self.rank = group.action_size
        self.vertices = []
        for i in range(self.rank):
            self.vertices.append(bq.pair_orbits(group.generators,self.rank,i+1,1))

class Poset_quot(Poset):
    def __init__(self,group):
        self.group = group
        self.rank = group.action_size

        self.vertices = []
        self.edges = []
        self.edge_counts = {}
        self.edge_mats = []

        for i in xrange(self.rank+1):
            self.vertices.append(bq.vert_by_rank(group.generators,i))

        for i in xrange(self.rank):
            (edge_lst,count_dict)=bq.edge_by_vert_counted(group.generators,self.vertices[i],self.vertices[i+1])
            self.edges.append(edge_lst)
            for level_edge in count_dict:
                self.edge_counts[level_edge] = count_dict[level_edge]
        self.edge_mats = make_edge_mats(self.rank,self.vertices,self.edges,self.edge_counts)

# functionalized the following code, not sure how to do triple quotes comment in a class
#        for i in xrange(self.rank):
 #           rank_mat = np.zeros((len(self.vertices[i+1]),len(self.vertices[i])))
  #          for (ct,b,a) in self.edge_counts[i]:
   #             rank_mat[b][a] = ct
    #        self.edge_mats.append(rank_mat)         

    def edgify(self):
        edge_poset = Poset_quot(self.group)
        edge_poset.rank = self.rank - 1
        edge_poset.vertices = self.edges
        edge_poset.edges = []
        edge_poset.edge_counts = {}
        edge_poset.edge_mats = [] 
        
        vert_d = vert_dict(self.vertices)

        for i in xrange(edge_poset.rank):
            edge_lst = []
            for l_index in xrange(len(edge_poset.vertices[i])):
                for u_index in xrange(len(edge_poset.vertices[i+1])):
                    (l_top,l_bot) = edge_poset.vertices[i][l_index]
                    (u_top,u_bot) = edge_poset.vertices[i+1][u_index]
                    lower_count = self.edge_mats[i][vert_d[u_bot]][vert_d[l_bot]]
                    upper_count = self.edge_mats[i+1][vert_d[u_top]][vert_d[l_top]]
                    if lower_count * upper_count != 0:
                        edge_lst.append(((l_bot,l_top),(u_bot,u_top)))
                        edge_poset.edge_counts[((l_bot,l_top),(u_bot,u_top))]=(lower_count * upper_count,u_index,l_index)
            edge_poset.edges.append(edge_lst)

        edge_poset.edge_mats = make_edge_mats(edge_poset.rank,edge_poset.vertices,edge_poset.edges,edge_poset.edge_counts)
        return edge_poset

def matrix_compositions(mat_lst):
    n = len(mat_lst)+1
    bot = (n-2)/2
    top = (n-1)/2
#    print 'bot '+ str(bot)
#    print 'top ' +str(top)
    compositions_lst = []
    shifted_compositions = []
    if n % 2 == 0:
        running_mat = mat_lst[bot]
    else:
#        print 'mat_lst_top_shape ' + str(mat_lst[top].shape)
#        print 'mat_lst_bot_shape ' + str(mat_lst[bot].shape)
        shifted_compositions.append(mat_lst[bot])
        running_mat = np.dot(mat_lst[top],mat_lst[bot])
#    print 'shape ' + str(running_mat.shape)
    compositions_lst.append(running_mat)
    bot -= 1
    top += 1
    while bot >= 0:
#        print bot
#        print 'running_mat_shape ' + str(running_mat.shape)
#        print 'mat_lst_bot_shape ' + str(mat_lst[bot].shape)
        running_mat = np.dot(running_mat,mat_lst[bot])
        shifted_compositions.append(running_mat)
#        print 'running_mat_shape ' + str(running_mat.shape)
#        print 'mat_lst_top_shape ' + str(mat_lst[top].shape)
        running_mat = np.dot(mat_lst[top],running_mat)
        compositions_lst.append(running_mat)
        bot -= 1
        top += 1
    return (compositions_lst,shifted_compositions)
    
def gen_p_lst(grp):
    poset = Poset_quot(grp)
#    vertex_orbits = map(lambda x: map(lambda z:bq.orbit(grp.generators,z),x),poset.vertices)
    edge_poset = Poset_quot.edgify(Poset_quot(grp))
#    edge_orbits = map(lambda x: map(lambda z: bq.edge_orbit(grp.generators,z),x) ,poset.vertices)
    return map(len,edge_poset.vertices),poset.vertices,edge_poset.vertices
    
def gen_q_lst(grp):
    poset = Poset_edge_quot(grp)
    return map(len,map(list,poset.vertices))

def print_stats(poset):
#    print poset.vertices
#    print poset.edges
#    print poset.edge_counts
    print 'edge counts'
    for i in xrange(poset.rank+1):
        print len(poset.vertices[i])
    print 'map ranks'
    for i in xrange(poset.rank):
        print np.linalg.matrix_rank(poset.edge_mats[i])
    print 'composition_ranks'
    mc,mc_shifted = matrix_compositions(poset.edge_mats)
    print 'shifted_compositions '+ str(map(np.linalg.matrix_rank,mc_shifted))
#    print 'normal_compositions ' +str(map(np.linalg.matrix_rank,mc))
#    for i in mc:
#        for j in i:
#            for t in j:
#                print int(t),
#            print ''
#    print 'shifted ' + str(map(np.linalg.matrix_rank,mc_shifted))

def check_unimodality(lst):
    for i in range(len(lst)):
        if len(lst[i]) != len(lst[len(lst)-i-1]):
            print lst[i],lst[len(lst)-i-1]
            return False
    for i in range(len(lst)/2):
        if len(lst[i]) > len(lst[i+1]):
            print len(lst[i]),len(lst[i+1])
            return False
    return True

def gen_rand_period(n,period):
    lst = range(n)
    perm = [0]*n
    while len(lst) >= period:
        cycle = random.sample(lst,period)
#        print cycle
#        print sorted_cycle
        for i in xrange(period):
            perm[cycle[i]] = cycle[(i+1) % period]
#        print perm
        for x in cycle:
            lst.remove(x)
#        print perm
    for i in lst:
        perm[i] = i
    return perm
    

#print gen_rand_period(7,3)

#num_gens > 0
#gen_size_list is a list with the periods of the generators
def rand_grp(n,gen_size_lst):
    lst = range(n)
    gens = []
    for i in gen_size_lst:
        single_gen = gen_rand_period(n,i)
        gens.append(tuple(single_gen))
    return bq.Grp(gens)


def boolean_matrix(n,i):
    grp = bq.Grp([tuple(range(n))])
    poset=Poset_quot.edgify(Poset_quot(grp))
    mc,mc_shifted = matrix_compositions(poset.edge_mats)
    mc = mc[n-i-(n+3)/2]
    print poset.vertices[i]
#    print '{',
    for t in xrange(len(mc)):
        print poset.vertices[n-i-1][t],
#        print '{',
        for j in xrange(len(mc[0])):
            if j != len(mc[0])-1:
                print str(int(mc[t][j])),
            if j == len(mc[0])-1:
                print str(int(mc[t][j])),
        print ''
#        print '},'
#    print '}'

def full_size(grp):
    if len(list(set(grp.generators))) != len(grp.generators):
        return False
    for i in xrange(grp.action_size):
        if all(g[i]==i for g in grp.generators):
            return False
    return True

#boolean_matrix(5,1)

grp = bq.Grp([(1,0,2,3,4,5,6,7),(0,1,3,2,4,5,6,7),(0,1,2,3,5,4,6,7),(0,1,2,3,4,5,7,6),(2,3,0,1,4,5,6,7),(0,1,2,3,6,7,4,5),(4,5,6,7,0,1,2,3)])

poset  = Poset_quot(grp)
for i in xrange(poset.rank+1):
    print poset.vertices[i]
for i in xrange(poset.rank+1):
    print poset.edges[i]

'''
for i in range(3,10):
    grp = bq.Grp(bq.cyclic_g_lst(i))
    print gen_p_lst(grp)
    print gen_q_lst(grp)    
'''

'''
n = 9
for j in range(0,n):
    for k in range(2,n):
        for l in range(k,n):
            for i in range(5):
                grp = rand_grp(j,[k,l])
                if full_size(grp):
                    p_lst,vertex_reps,edge_reps = gen_p_lst(grp)
                    q_lst = gen_q_lst(grp)
                    if any(i != 1 for i in q_lst):
#                if any(i != 1 for i in q_lst) and p_lst == q_lst:
                        print "Group order is " + str(len(grp.group_set))
                        print "Group is " + str(grp.generators)
                        print 'k: '+ str(k)
                        print 'l: '+str(l)
                        print "p_lst: " + str(p_lst)
                        print "q_lst: " + str(q_lst)
                        print 'vertex_lengths: '+ str(map(len,vertex_reps))
                        print 'vertex_orbits: ' +str(vertex_reps)
                        print 'edge_orbits: '+ str(edge_reps)
                        print ''
                        print ''
                    
#                print str(i) + 'i done'
#            print str(l) + 'l done'
#        print str(k) + 'k done'
#    print str(j) + 'i done'
'''


'''
grp = bq.Grp([(5, 4, 0, 1, 3, 2, 7, 8, 6), (6, 4, 0, 7, 5, 1, 2, 8, 3)])
print_stats(Poset_quot.edgify(Poset_quot(grp)))
'''
#grp = bq.Grp([(8, 7, 6, 5, 4, 3, 2, 1, 0), (8, 1, 6, 5, 4, 7, 2, 3, 0)])
#print_stats(Poset_quot.edgify(Poset_quot(grp)))
