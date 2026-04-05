import networkx as nx
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
cur=534
a = 1103515245
c = 12345
N = 2147483648
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
#third probability
p3=1-p2-p1

def dot_prod(a,b):
    res=0.0
    for i in range(len(a)):
        res+=a[i]*b[i]
    return res
def get_preprocessed_network(random_type,S_percent=0.05):
    cur=534
    a = 1103515245
    b = 12345
    m = 2147483648
    G=nx.DiGraph()
    N=0
    if random_type=="reservoir":
        sample=r"D:\Diffusion\pokec_sample_10k.csv"
        full_degree=r"D:\Diffusion\full_degrees.csv"
        preference=r"D:\Diffusion\pokec_reservoir_preferences.csv"
    elif random_type=='snowball':
        sample=r"D:\Diffusion\pokec_snowball_10k.csv"
        full_degree=r"D:\Diffusion\full_snowball_degrees.csv"
        preference=r"D:\Diffusion\pokec_snowball_preferences.csv"
    else:
        sample=r"D:\Diffusion\pokec_forest_fire_10k.csv"
        full_degree=r"D:\Diffusion\full_forest_fire_degrees.csv"
        preference=r"D:\Diffusion\pokec_forest_fire_preferences.csv"
    with open(sample,"r") as f:
        reader=csv.reader(f)
        for row in reader:
            if not row:continue
            if row[0]=='unique':
                N=int(row[1])
                continue
            G.add_edge(int(row[0]),int(row[1]))
    with open(preference,'r') as f:
        reader=csv.reader(f)
        next(reader)
        for node,music,movies,politics in reader:
            if int(node) in G:
                G.nodes[int(node)]["prob_array"]=[float(music),float(movies),float(politics)]
    degree={}
    with open(full_degree,'r') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            if not row:continue
            degree[int(row[0])]=int(row[1])
    for node in G.nodes():
        G.nodes[node]['degree']=degree[node]
        G.nodes[node]['state']='U'
        G.nodes[node]["threshold"]=(degree[node]/(N-1))
        if "prob_array" not in G.nodes[node]:
            G.nodes[node]["prob_array"]=[0.01,0.01,0.01]
    arr=list(G.nodes())
    print("no of nodes",len(arr))
    spreader=set()
    for i in range(int(S_percent*len(arr))):
        cur= a*cur +b
        cur%=len(arr)
        cur=i+(cur%(len(arr)-i))
        arr[i],arr[cur]=arr[cur],arr[i]
        G.nodes[arr[i]]['state']='S'
        spreader.add(arr[i])
    return G,spreader,N

def diffusion(G,spreader,N,info):
    m=2147483648
    cur=546
    history = []
    history.append({node: G.nodes[node]["state"] for node in G.nodes()})
    while spreader:
        level=set()
        print("no of current spreader node:",len(spreader))
        for u in spreader:
            for v in G[u]:
                prod=dot_prod(info,G.nodes[v]["prob_array"])
                cur=(a*cur+c)%m
                if G.nodes[v]["state"]=='U' and (cur/m)<(G.nodes[v]['threshold']**prod):
                    G.nodes[v]["state"]='K'
                elif G.nodes[v]["state"]=='U':
                    cur=(a*cur+c)%m
                    if (cur/m)<p1*(1-(G.nodes[v]['threshold']**prod)):
                        G.nodes[v]["state"]="S"
                        level.add(v)
                    else:
                        G.nodes[v]["state"]="H"
                elif G.nodes[v]["state"]=='H':
                    cur=(a*cur+c)%m
                    if (cur/m)<p2:
                        G.nodes[v]["state"]="S"
                        level.add(v)
                    else:
                        G.nodes[v]["state"]='K'
            cur=(a*cur+c)%m
            if (cur/m)<p3:
                G.nodes[u]["state"]='K'
            else:
                level.add(u)
        spreader=level
        history.append({node: G.nodes[node]["state"] for node in G.nodes()})
    count=0
    for node in G.nodes:
        count+=int(G.nodes[node]["state"] in ("K","S"))
    print(count)
    return history
def visualize_network(G, history):
    pos = nx.spring_layout(G, seed=42)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    color_map={'U':'green','S':'red','H':'yellow','K':'black'}
    
    def update(frame):
        ax.clear()
        current_states=history[frame]
        node_colors=[color_map[current_states[node]] for node in G.nodes()]
        
        nx.draw(G, pos, 
                node_color=node_colors, 
                node_size=10, 
                with_labels=False, 
                width=0.05, 
                ax=ax)
        
        ax.set_title(f"Diffusion Step {frame} | U:Gray S:Red H:Yellow K:Black") 
    ani=animation.FuncAnimation(fig,update,frames=len(history),interval=10000,repeat=False)
    plt.show()
type1="reservoir"
type2="snowball"
type3="forest_fire"
G,spreader,N=get_preprocessed_network(type1,0.5)
history=diffusion(G,spreader,N,[0,0,1])
print(N)
if N<=10000:
    visualize_network(G, history)