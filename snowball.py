import itertools
from collections import deque
Ori_graph = r"D:\Diffusion\soc-Pokec.mtx"
sampled_graph = r"D:\Diffusion\pokec_snowball_10k.csv"
full_degree = r"D:\Diffusion\full_snowball_degrees.csv"
cur_rand=534
a = 1103515245
b = 12345
m = 2147483648
degree=[0]*2000000
adj=[[] for _ in range(len(degree))]
unique=0
maxi=0
with open(Ori_graph,'r') as f:
    while 1:
        cur=list(itertools.islice(f,100000))
        if not cur:
            break

        for row in cur:
            if row.startswith('%') or not row.strip():
                continue
            now=row.split()
            if len(now)<2:continue
            degree[int(now[0])]+=1
            adj[int(now[0])].append(int(now[1]))
            if len(adj[int(now[0])])>len(adj[maxi]):
                maxi=int(now[0])
seen={maxi}
count=1
q=deque([maxi])
limit=100000
while count<limit and q:
    i=q.popleft()
    for j in adj[i]:
        if j in seen:continue
        seen.add(j)
        count+=1
        q.append(j)
with open(full_degree,'w') as nodes:
    nodes.write("Node_ID,Full_degree\n")
    for node in seen:
        nodes.write(f"{node},{degree[node]}\n")
s="unique"
count=0
with open(Ori_graph,'r') as f,open(sampled_graph,'w') as output:
    while 1:
        cur=list(itertools.islice(f,100000))
        if not cur:
            break

        for row in cur:
            if row.startswith('%') or not row.strip():
                continue
            now=row.split()
            if len(now)<2:continue
            if int(now[0]) not in seen or int(now[1]) not in seen:
                continue
            output.write(f"{int(now[0])},{int(now[1])}\n")
            count+=1
    output.write(f"{s},{count}\n")