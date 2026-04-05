import itertools
from collections import deque
import csv
Ori_graph = r"D:\Diffusion\soc-Pokec.mtx"
sampled_graph = r"D:\Diffusion\pokec_forest_fire_10k.csv"
full_degree = r"D:\Diffusion\full_forest_fire_degrees.csv"
profiles_file = r"D:\Diffusion\soc-pokec-profiles.txt" 
pref_csv = r"D:\Diffusion\pokec_forest_fire_preferences.csv"
pcount=0
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
print(maxi)
seen={maxi}
count=1
q=deque([maxi])
limit=1000
while count<limit:
    i=q.popleft()
    for j in adj[i]:
        if j in seen:continue
        cur_rand=(a*cur_rand +b)%m
        if (cur_rand/m)>0.5:continue
        seen.add(j)
        count+=1
        q.append(j)
    if len(q)==0:
        q.append(seen.pop())
        seen.add(q[0])
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

with open(profiles_file,'r',encoding='utf-8',errors='ignore') as f, open(pref_csv,'w',newline='',encoding='utf-8') as out:
    writer=csv.writer(out)
    writer.writerow(["Node_ID","Music","Movies","Politics"])
    while 1:
        cur=list(itertools.islice(f,100000))
        if not cur:
            break
        for row in cur:
            first_tab = row.find('\t')
            if first_tab==-1:continue
            try:
                user_id=int(row[:first_tab])
            except ValueError:
                continue
            if user_id not in seen:continue
            now=row.split('\t')
            mu=min(0.99, max(0.01, len(now[13])/50.0)) if len(now)>13 else 0.01
            mo=min(0.99, max(0.01, len(now[14])/50.0)) if len(now)>14 else 0.01
            po=min(0.99, max(0.01, len(now[47])/20.0)) if len(now)>47 else 0.01
            writer.writerow([user_id,round(mu,3),round(mo,3),round(po,3)])
            pcount+=1
            if pcount==len(seen):break
        if pcount==len(seen):break
print("Preferences saved:",pcount)