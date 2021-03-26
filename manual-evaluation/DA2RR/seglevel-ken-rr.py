import sys

SRC=sys.argv[1]
TRG=sys.argv[2]
DATA=sys.argv[3]
LEVEL=sys.argv[4]
if len(sys.argv) == 5:
  f = f"../DA/metrics-ad-{LEVEL}-scores-"+SRC+"-"+TRG+".csv"
else:
  f=sys.argv[5] +SRC+"-"+TRG+".csv"

THRESHOLD=25
# f = "../DA/metrics-ad-seg-scores-"+SRC+"-"+TRG+".csv"
   

lines = [line.rstrip('\n') for line in open(f)]
lines.pop(0)

scores = {}
              

for l in lines:
  c = l.split()

  system = c[0] 
  if system.startswith('Human'):
    continue
  sid = c[1]
  score = float(c[2])
  zscore = float(c[3])

  if LEVEL=='doc':
    nannot = float(c[4])
    if nannot < 2:
      continue
  if sid not in scores:
    scores[sid] = {}

  if system not in scores[sid]:
    scores[sid][system] = (score, zscore)

cnt = 0
sid_cnt = 0
margin = 0
tot = 0
count_opp = 0
count_opp_threshold = 0
for sid in scores:
  if len(scores[sid]) > 1:
    for s1 in scores[sid]:
      for s2 in scores[sid]:
        if s1 > s2:
          sid_cnt = sid_cnt + 1

          scr1, scr1z = scores[sid][s1]
          scr2,scr2z = scores[sid][s2]
          if abs(scr1-scr2) >= THRESHOLD:
            margin = margin + 1  
          if (scr1 - scr2) * (scr1z - scr2z) < 0:
            if abs(scr1-scr2) >= THRESHOLD:
               # print(scr1 ,scr2, scr1z ,scr2z)
               count_opp_threshold +=1
               
            else:
              count_opp += 1
                    

          if scr1 > scr2:
            print (SRC+"-"+TRG+" "+DATA+" "+sid+" "+s1+" "+s2 + " " + str(abs(scr1-scr2)))
          else:
            print (SRC+"-"+TRG+" "+DATA+" "+sid+" "+s2+" "+s1 + " " + str(abs(scr1-scr2)))

for sid in scores:
  if len(scores[sid])>1:
    cnt = cnt + 1
    tot = tot + len(scores[sid])
#len(scores[sid])
  
f = "summary."+SRC+TRG
F = open(f,'w')  
F.write(SRC+"-"+TRG+" DA judgments "+str(cnt)+"\n")  
F.write(SRC+"-"+TRG+" ave DA judgments "+str(float(tot)/cnt)+"\n")  
F.write(SRC+"-"+TRG+" DA combos "+str(sid_cnt)+"\n")  
F.write(SRC+"-"+TRG+" > 25 dist "+str(margin)+"\n")  
F.write(SRC+"-"+TRG+" opp raw and z "+str(count_opp)+"  %" +str(count_opp*100/sid_cnt)+"\n")  
F.write(SRC+"-"+TRG+" opp raw and z with raw threshold"+str(count_opp_threshold)+"  %" +str(count_opp_threshold*100/margin)+"\n")  
F.close()

f = "summary-tbl" 
F = open(f,'a')  
avgcnt=(tot/cnt)
F.write('{\\bf ' + SRC+"-" + TRG + '}' + f"& {cnt} & {avgcnt:.1f} & {sid_cnt} & {margin} \\\\")
F.write('\n')
F.close()
