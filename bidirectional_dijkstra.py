def bidirectional_dijkstra(Adj, w, s, t):
    """
    Return a list of vertices forming a shortest path from s to t 
    Vertices are all integers in range(len(Adj))
    Input:  Adj: undirected graph, Adj[v] is list of vertices adjacent to v
              w: weight dictionary, w[(u,v)] is integer weight of edge (u,v)
              s: source vertex
              t: target vertex
    """
    path = []
    ##################
    # YOUR CODE HERE #
    ##################
    n=len(Adj)
    ps=[None for _ in range(len(Adj))]
    pt=[None for _ in range(n)]
    ds=[float('inf') for _ in range(n)]
    dt=[float('inf') for _ in range(n)]
    ds[s], ps[s] = 0,s
    dt[t], pt[t] = 0,t
    Qs= PriorityQueue()
    Qt= PriorityQueue()
    for v in range(n):
        Qs.insert(v,ds[v])
    for v in range(n):
        Qt.insert(v,dt[v])
    vm=s
    D=ds[vm]+dt[vm]
    for _ in range(n):
        u=0
        flag=0
        if Qs.find_min()< Qt.find_min():
            u=Qs.extract_min()
            flag=1
        else:
            u=Qt.extract_min()
        if (ds[u] > D//2 ) and (dt[u] > D//2):
            break
        if (flag):
            for v in Adj[u]:
                relax(Adj,w,ds,ps,u,v)
                Qs.decrease_key(v,ds[v])
                if( ds[v] + dt[v] < D):
                    D=ds[v] + dt[v]
                    vm=v
        else:
            for v in Adj[u]:
                relax(Adj,w,dt,pt,u,v)
                Qt.decrease_key(v,dt[v])
                if( ds[v] + dt[v] < D):
                    D=ds[v] + dt[v]
                    vm=v
    i=vm
    p1=[]
    p2=[]
    while(ps[i]!=i):
        p1.append(ps[i])
        i=ps[i]
    p1.reverse()
    i=vm
    while(pt[i]!=i):
        p2.append(pt[i])
        i=pt[i]
    path=p1+[vm]+p2
    return path

def relax(A, w, d, parent, u, v):
    if d[v] > d[u] + w[(u, v)]:
        d[v] = d[u] + w[(u, v)]
        parent[v] = u

class Item:
    def __init__(self, label, key):
        self.label, self.key = label, key

class PriorityQueue:                      # Binary Heap Implementation
    def __init__(self):                   # stores keys with unique labels
        self.A = []
        self.label2idx = {}

    def min_heapify_up(self, c):            
        if c == 0: return
        p = (c - 1) // 2
        if self.A[p].key > self.A[c].key:   
            self.A[c], self.A[p] = self.A[p], self.A[c]         
            self.label2idx[self.A[c].label] = c
            self.label2idx[self.A[p].label] = p
            self.min_heapify_up(p)         

    def min_heapify_down(self, p):          
        if p >= len(self.A): return
        l = 2 * p + 1
        r = 2 * p + 2
        if l >= len(self.A): l = p
        if r >= len(self.A): r = p
        c = l if self.A[r].key > self.A[l].key else r 
        if self.A[p].key > self.A[c].key:             
            self.A[c], self.A[p] = self.A[p], self.A[c]         
            self.label2idx[self.A[c].label] = c
            self.label2idx[self.A[p].label] = p
            self.min_heapify_down(c)       

    def insert(self, label, key):         # insert labeled key
        self.A.append(Item(label, key))
        idx = len(self.A) - 1
        self.label2idx[self.A[idx].label] = idx
        self.min_heapify_up(idx)

    def find_min(self):                   # return minimum key
        return self.A[0].key

    def extract_min(self):                # remove a label with minimum key
        self.A[0], self.A[-1] = self.A[-1], self.A[0]
        self.label2idx[self.A[0].label] = 0
        del self.label2idx[self.A[-1].label]
        min_label = self.A.pop().label
        self.min_heapify_down(0)
        return min_label

    def decrease_key(self, label, key):   # decrease key of a given label
        if label in self.label2idx:
            idx = self.label2idx[label]
            if key < self.A[idx].key:
                self.A[idx].key = key
                self.min_heapify_up(idx)
