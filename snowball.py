import itertools
from collections import deque
import csv
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

profiles_user = r"D:\Diffusion\soc-Pokec_user_id.mtx"
profiles_music = r"D:\Diffusion\soc-Pokec_I_like_music.txt"
profiles_movies = r"D:\Diffusion\soc-Pokec_I_like_movies.txt"
profiles_politics = r"D:\Diffusion\soc-Pokec_politics.txt"
pref_csv = r"D:\Diffusion\pokec_snowball_preferences.csv"

pcount = 0

with open(profiles_user, 'r', encoding='utf-8') as f_u, \
     open(profiles_music, 'r', encoding='utf-8', errors='ignore') as f_mu, \
     open(profiles_movies, 'r', encoding='utf-8', errors='ignore') as f_mo, \
     open(profiles_politics, 'r', encoding='utf-8', errors='ignore') as f_po, \
     open(pref_csv, 'w', newline='', encoding='utf-8') as out:
         
    writer = csv.writer(out)
    writer.writerow(["Node_ID", "Music", "Movies", "Politics"])
    
    for line in f_u:
        if not line.startswith('%'):
            break 
            

    for line_u, line_mu, line_mo, line_po in zip(f_u, f_mu, f_mo, f_po):
        try:
            user_id = int(line_u.strip())
        except ValueError:
            continue
            
        if user_id not in seen:
            continue
            
        line_mu = line_mu.strip()
        line_mo = line_mo.strip()
        line_po = line_po.strip()
        

        len_mu = len(line_mu) if line_mu != "null" else 0
        len_mo = len(line_mo) if line_mo != "null" else 0
        len_po = len(line_po) if line_po != "null" else 0
        
        mu = min(0.99, max(0.01, len_mu / 50.0))
        mo = min(0.99, max(0.01, len_mo / 50.0))
        po = min(0.99, max(0.01, len_po / 20.0))
        
        writer.writerow([user_id, round(mu, 3), round(mo, 3), round(po, 3)])
        pcount += 1
        
        if pcount == len(seen):
            break

print("Preferences saved:", pcount)