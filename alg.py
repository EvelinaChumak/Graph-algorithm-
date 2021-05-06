import numpy as np
import copy


def Read(file):
    n,m = [int(x) for x in next(file).split()]
    G = np.zeros((n,n))
    for line in file:
        first,second,w =[int(x) for x in line.split()]
        G[first-1][second-1] = w
    return int(n), G

def push(u,v,fl, ee, G):
  d = min(ee[u], G[u][v] - fl[u][v])
  ee[u] = ee[u] - d
  ee[v] = ee[v] + d
  fl[u][v] = fl[u][v] + d
  fl[v][u] = - fl[u][v]
  return fl,ee

def lift(u,h,fl,G,n):
  d = 10000
  for i in range(0,n):
    if G[u][i] - fl[u][i] > 0:
      d = min(d,h[i])
  h[u] = d + 1
  return h

def bfs(graf,n):        #global_relabing
  d = [10000 for i in range(n)]
  dist = 1
  visited = []
  for i in range(0,n):
    if graf[0][i] > 0:
      visited.append(i)
      d[i] = 1
  for item in visited:
    for i in range(n):
      if graf[item][i] > 0 and i not in visited and i!=0:
        visited.append(i)
        if d[i] > d[item] + 1:
          d[i] = d[item] + 1
  if n-1 not in visited:      #go from drain to source
    g = np.zeros((n,n))
    for i in range(0,n):
      for j in range(0,n):
        g[i][j] = graf[n-1-i][n-1-j]
    d = bfs(g,n)[::-1]
  for i in range(0,n):
    if d[i] == 10000:
      d[i] = 0
  return d[::-1]      #to get the distance of each vertex to the drain


def main(G,n):
      fl = np.zeros((n,n))      #flow
      fl[0] = G[0]

      for i in range(0,n):
        fl[i][0] = -G[0][i]

      h = np.zeros(n)
      h[0] = n
      e = np.zeros(n)
      queue = [] 

      for i in range(1,n):      #first pass to determine the queue
          if fl[0][i] > 0:
            if i != n-1:        #we exclude the drain so that we do not let everything back to the source
              queue.append(i)
            e[i] = fl[0][i]

      d = bfs(G,n)
      h = copy.deepcopy(d)
      h[0] = n
      m = 0
      while len(queue) > 0:
        m+=1
        if m%n == 0:
          d = bfs(G - fl,n)
          for i in range(0,n):
            if h[i] < d[i]:
              h[i] = d[i]
        i = queue[0]
        for j in range(0,n):
          if G[i][j] - fl[i][j] > 0 and h[i]==h[j]+1:
              if j != n-1 and j != 0 and j not in queue:
                  queue.append(j)
              j = j-1
              break
        j = j+1
        if j<n:
            fl,e = push(i,j,fl,e,G)
            c = queue.pop(0)
            if e[c] > 0:
                queue.append(i)
        else:
            h = lift(i,h,fl,G,n)
            c = queue.pop(0)
            queue.append(i)
      
      print(int(e[n-1]))





file = open(input(), 'r')
n ,G  = Read(file)
main(G,n)