import itertools
Ori_graph = r"D:\Diffusion\soc-Pokec.mtx"
sampled_graph = r"D:\Diffusion\pokec_sample_10k.csv"
full_degree = r"D:\Diffusion\full_degrees.csv"
cur_rand=534
a = 1103515245
b = 12345
m = 2147483648
degree=[0]*2000000
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
            if degree[int(now[0])]==1:
                unique+=1
                maxi=max(maxi,int(now[0]))
print(unique)
limit=unique//10
count=0
final_sample=[[]]
for i in range(maxi+1):
    if degree[i]==0:continue
    if len(final_sample[-1])<10000:
        final_sample[-1].append(i)
    else:
        nex=(a*cur_rand +b)%m
        cur_rand=nex
        if nex%count<10000:
            degree[final_sample[-1][nex%count]]=0
            final_sample[-1][nex%count]=i
        else:
            degree[i]=0
    count+=1
    if count==limit:
        count=0
        final_sample.append([])

with open(full_degree,'w') as nodes:
    nodes.write("Node_ID,Full_degree\n")
    for box in final_sample:
        for node in box:
            nodes.write(f"{node},{degree[node]}\n")
s="unique"
edge=[]
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
            if degree[int(now[0])]==0 or degree[int(now[1])]==0:
                continue
            output.write(f"{int(now[0])},{int(now[1])}\n")
    output.write(f"{s},{unique}\n")