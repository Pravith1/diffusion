import itertools
import csv
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
seen=set()
with open(full_degree,'w') as nodes:
    nodes.write("Node_ID,Full_degree\n")
    for box in final_sample:
        for node in box:
            nodes.write(f"{node},{degree[node]}\n")
            seen.add(node)
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
            if degree[int(now[0])]==0 or degree[int(now[1])]==0:
                continue
            output.write(f"{int(now[0])},{int(now[1])}\n")
            count+=1
    output.write(f"{s},{count}\n")

profiles_user = r"D:\Diffusion\soc-Pokec_user_id.mtx"
profiles_music = r"D:\Diffusion\soc-Pokec_I_like_music.txt"
profiles_movies = r"D:\Diffusion\soc-Pokec_I_like_movies.txt"
profiles_politics = r"D:\Diffusion\soc-Pokec_politics.txt"
pref_csv = r"D:\Diffusion\pokec_reservoir_preferences.csv"

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