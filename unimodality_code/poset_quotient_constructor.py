import boolean_quotients as bq
import numpy as np

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
#        print poset.edge_mats[i]

#grp = bq.Grp([(1,0,2,3,4,5,6),(0,2,1,3,4,5,6),(0,1,3,2,4,5,6),(0,1,2,4,3,5,6),(0,1,2,3,5,4,6),(0,1,2,3,4,6,5)])
#grp = bq.Grp([(1,2,3,4,5,6,7,8,9,0),(9,8,7,6,5,4,3,2,1,0)])

#grp = bq.Grp([(1,2,3,4,5,6,7,8,0),(0,8,7,6,5,4,3,2,1)])
#poset = Poset_quot(grp)
grp = bq.Grp([(1,2,0,3,4,5,6,7,8),(0,1,3,4,5,2,6,7,8),(0,1,2,3,4,6,5,7,8),(0,1,2,3,4,5,6,8,7)])
poset = Poset_quot.edgify(Poset_quot(grp))
print_stats(poset)

'''
for i in range(9):
    grp = bq.Grp(bq.dihedral_g_lst(i))
    poset = Poset_quot.edgify(Poset_quot(grp))
    print_stats(poset)
'''

