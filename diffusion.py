import networkx as nx
N=4000
a=1534
c=54424
cur=5
#first probability
cur=a*cur+c
cur%=N
p1=cur/N
nex=1-p1
#second probability 
cur=a*cur+c
cur%=N
p2=cur/N
p2=p2*nex
p3=1-p2-p1


def get_preprocessed_network(network_type="WS", N=4000, avg_k=22, S_percent=0.3):
    cur=5
    if network_type == "BA":
        m = avg_k // 2
        G = nx.barabasi_albert_graph(n=N, m=m)
    elif network_type == "WS":
        G = nx.watts_strogatz_graph(n=N, k=avg_k, p=0.6)
    for node in G.nodes():
        G.nodes[node]['degree'] = G.degree(node)
        G.nodes[node]['state'] = 'U'
        G.nodes[node]['threshold']=(G.degree(node)/(N-1))**(1/3)
    arr=list(G.nodes())
    
    spreader=set()
    for i in range(int(S_percent*len(arr))):
        cur= a*cur +c
        cur%=len(arr)
        cur=i+(cur%(len(arr)-i))
        arr[i],arr[cur]=arr[cur],arr[i]
        G.nodes[arr[i]]['state']='S'
        spreader.add(arr[i])
    return G,spreader

def diffusion(G,spreader,N):
    cur=5
    while spreader:
        level=set()
        for u in spreader:
            for v in G[u]:
                cur=(a*cur+c)%N
                if G.nodes[v]["state"]=='U' and (cur/N)<G.nodes[v]['threshold']:
                    G.nodes[v]["state"]='K'
                elif G.nodes[v]["state"]=='U':
                    cur=(a*cur+c)%N
                    if (cur/N)<p1*(1-G.nodes[v]['threshold']):
                        G.nodes[v]["state"]="S"
                        level.add(v)
                    else:
                        G.nodes[v]["state"]="H"
                elif G.nodes[v]["state"]=='H':
                    cur=(a*cur+c)%N
                    if (cur/N)<p2:
                        G.nodes[v]["state"]="S"
                        level.add(v)
                    else:
                        G.nodes[v]["state"]='K'
                cur=(a*cur+c)%N
                if (cur/N)<p3:
                    G.nodes[u]["state"]='K'
                else:
                    level.add(u)
        spreader=level
    
G,spreader=get_preprocessed_network()
diffusion(G,spreader,4000)