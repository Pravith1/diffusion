import itertools
from collections import deque
import csv

music_pos=["pop", "rock", "rap", "metal", "hip", "hop", "house", "techno", "dance", "vsetko", "hudba", "vsetky"]
music_neg=["nepocuvam", "ziadna", "nic", "nie", "ziadne", "nezaujima"]

movies_pos=["komedie", "akcne", "horory", "romanticke", "sci-fi", "thrillery", "dokumentarne", "historicke", "vsetko", "filmy", "serialy", "zahadne", "mysteriozne", "vojnove"]
movies_neg=["nepozeram", "ziadne", "nic", "nie", "nezaujima"]


pol_pos=["zaujimam", "ano", "sledujem", "spravy", "pravica", "lavica", "politika", "velmi"]
pol_neg=["nezaujima", "nenavidim", "hnus", "nic", "nie", "kaslem", "neznasam", "nuda", "fuj"]
def score_text(text,pos,neg):
    text=text.lower()
    if len(text)<3 or text in ("nic","nie","ziadne","null"):
        return 0.01
    p = sum(text.count(w) for w in pos)
    n = sum(text.count(w) for w in neg)
    if n>p:
        return 0.01
    if p>0:
        return min(0.99,1.0-(0.5**p))
    return min(0.5,len(text)/100.0)
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
node_degree=[0]*2000000
adj=[[] for _ in range(len(node_degree))]
unique=0
max_node=0
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
            node_degree[int(now[0])]+=1
            adj[int(now[0])].append(int(now[1]))
            if len(adj[int(now[0])])>len(adj[max_node]):
                max_node=int(now[0])
print(max_node)
picked={max_node}
count=1
q=deque([max_node])
limit=100000
while count<limit:
    i=q.popleft()
    for j in adj[i]:
        if j in picked:continue
        cur_rand=(a*cur_rand +b)%m
        if (cur_rand/m)>0.5:continue
        picked.add(j)
        count+=1
        q.append(j)
    if len(q)==0:
        q.append(picked.pop())
        picked.add(q[0])
with open(full_degree,'w') as nodes:
    nodes.write("Node_ID,Full_degree\n")
    for node in picked:
        nodes.write(f"{node},{node_degree[node]}\n")
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
            if int(now[0]) not in picked or int(now[1]) not in picked:
                continue
            output.write(f"{int(now[0])},{int(now[1])}\n")
            count+=1
    output.write(f"{s},{count}\n")
profiles_user = r"D:\Diffusion\soc-Pokec_user_id.mtx"
profiles_music = r"D:\Diffusion\soc-Pokec_I_like_music.txt"
profiles_movies = r"D:\Diffusion\soc-Pokec_I_like_movies.txt"
profiles_politics = r"D:\Diffusion\soc-Pokec_politics.txt"
pref_csv = r"D:\Diffusion\pokec_forest_fire_preferences.csv"

pcount = 0

with open(profiles_user, 'r', encoding='utf-8') as f_u, open(profiles_music, 'r', encoding='utf-8', errors='ignore') as f_mu, open(profiles_movies, 'r', encoding='utf-8', errors='ignore') as f_mo, open(profiles_politics, 'r', encoding='utf-8', errors='ignore') as f_po, open(pref_csv, 'w', newline='', encoding='utf-8') as out:
    writer = csv.writer(out)
    writer.writerow(["Node_ID", "Music", "Movies", "Politics"])
    for line in f_u:
        if not line.startswith('%'):
            break 
    for line_u,line_mu,line_mo,line_po in zip(f_u,f_mu,f_mo,f_po):
        try:
            user_id=int(line_u.strip())
        except ValueError:
            continue
        if user_id not in picked:
            continue
        line_mu=line_mu.strip()
        line_mo=line_mo.strip()
        line_po=line_po.strip()
        mu=score_text(line_mu,music_pos,music_neg)
        mo=score_text(line_mo,movies_pos,movies_neg)
        po=score_text(line_po,pol_pos,pol_neg)
        writer.writerow([user_id,round(mu,3),round(mo,3),round(po,3)])
        pcount += 1
        if pcount==len(picked):
            break
print("Preferences saved:", pcount)