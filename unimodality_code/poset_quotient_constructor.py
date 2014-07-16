import boolean_quotients as bq
import numpy as np
import random

class Poset:
    def __init(self):
        self.rank = 0
        self.vertices = []
        self.edges = []
        self.edge_counts = []
        self.edge_mats = []

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
    n = len(mat_lst)
    bot = (n-1)/2
    compositions_lst = []
    shifted_compositions = []
    if n % 2 == 0:
        running_mat = np.dot(mat_lst[n-bot-1],mat_lst[bot])
    else:
        running_mat = mat_lst[bot]
    compositions_lst.append(running_mat)
    bot -= 1
    while bot >= 0:
        running_mat = np.dot(running_mat,mat_lst[bot])
        shifted_compositions.append(running_mat)
        running_mat = np.dot(mat_lst[n-bot-1],running_mat)
        compositions_lst.append(running_mat)
        bot -= 1
    return (compositions_lst,shifted_compositions)

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
    print map(np.linalg.matrix_rank,mc)
    for i in mc:
        for j in i:
            for t in j:
                print int(t),
            print ''
#    print 'shifted ' + str(map(np.linalg.matrix_rank,mc_shifted))


#num_gens > 0
def rand_grp(n,num_gens):
    lst = range(n)
    gens = []
    temp_lst = [6,7,0,1,2,3,4,5]
    temp_lst.reverse()
    gens.append(tuple(temp_lst))
    for i in range(num_gens):
        random.shuffle(lst)
        gens.append(tuple(lst))
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

boolean_matrix(5,)1

'''
for i in range(4,5):
    grp = bq.Grp([tuple(range(i))])
    print_stats(Poset_quot.edgify(Poset_quot(grp)))
'''

'''for i in range(20):
    grp = rand_grp(8,1)
    print "Group is " + str(grp.generators)
    print_stats(Poset_quot.edgify(Poset_quot(grp)))
'''

#grp = bq.Grp([(4,0,1,2,3)])
#print_stats(Poset_quot.edgify(Poset_quot(grp)))

#grp = bq.Grp([(8, 7, 6, 5, 4, 3, 2, 1, 0), (8, 1, 6, 5, 4, 7, 2, 3, 0)])
#print_stats(Poset_quot.edgify(Poset_quot(grp)))
