import glob
import gzip
import os
import pickle
import sys
from collections import defaultdict
#todo replace with argparse


import argparse
import os
parser = argparse.ArgumentParser()

parser.add_argument('-t', '--threshold', type=int, default=25, help="Directory with scores files")  
parser.add_argument('-r', '--refset', type=str, default='newstest2020', help="Directory with scores files")  
parser.add_argument('-l', '--level', type=str, default='seg', help="Directory with scores files")  
parser.add_argument('--include_human', action='store_true', default = False, help='include human system')
parser.add_argument('-e', '--exclude', type=str, default="none", help="['outl', top1', 'top2', 'rand1', 'rand2']")  
parser.add_argument('-o', '--outputdir', type=str, default="out")  

args = parser.parse_args()
threshold=args.threshold
REFSET = args.refset
level = args.level 
exclude_sys = args.exclude

if args.include_human:
  human='incl'
else:
  human='excl'  

# this system is an outlier with extremely low human scores 
# and BLEU < 0.01 when others have BLEU > 0.3    
EXCL_YOLO_SYSTEM=False

 

# OUTPUTDIR=f'{level:3}-level/DArr-{level:3}-{REFSET}-{human}human-t{threshold}-excl{exclude_sys}'
OUTPUTDIR=args.outputdir
os.makedirs(OUTPUTDIR,  exist_ok=True)
print(OUTPUTDIR)

if exclude_sys == 'outl':
  exclude = pickle.load(open('../manual-evaluation/outlier-systems-dict.pk', 'rb'))
elif exclude_sys in ['top1', 'top2', 'rand1', 'rand2'] :
  exclude = pickle.load(open(f'../manual-evaluation/{exclude}-systems-dict.pk', 'rb'))
else:
  exclude = defaultdict(int)


print('excl', exclude)
print('all args',args)
# submissions = ["/home/nmathur/wmt20/baseline_metrics/newstest2020ref/*seg.score.gz",
# "/home/nmathur/wmt20/EVAL/metricsubmissions/seg/*seg.score.gz"]
# submissions = ["/home/nmathur/wmt20/baseline_metrics/newstest2020ref/*seg.score.gz"]

submissions = [f"../final-metric-scores/*/*{level[:3]}.score.gz"]
submissions = [f"../final-metric-scores/b*/*{level[:3]}.score.gz", f"../final-metric-scores/s*/*{level[:3]}.score.gz"]
# submissions = [f"../final-metric-scores/b*/b*{level[:3]}.score.gz", f"../final-metric-scores/b*/t*{level[:3]}.score.gz", f"../final-metric-scores/b*/chrf.{level[:3]}.score.gz"]
# submissions = [f"../final-metric-scores/*/BLEU.{level[:3]}.score.gz"]

f = f"../manual-evaluation/DArr-{level}level.csv" 

lines = [line.rstrip('\n') for line in open(f)]
lines.pop(0)
print('total lines in manual-evaluation file = ', len(lines))
manual = {}

for l in lines: 
  c = l.split()

  if len(c) < 5:
    print ("error in manual evaluation file")
    exit(1)

  # file format is LP DATA SID BETTER WORSE
  lp = c[0]
  data = c[1]
  sid = c[2] 
  better = c[3]
  worse = c[4]
  score_diff = c[5]
  if float(score_diff) < threshold:
    continue 
  # these are the language pairs with multiple references 
  if REFSET == 'newstestB2020' or  REFSET == 'newstestM2020':
    if lp not in ['en-de', 'de-en', 'zh-en','ru-en', 'en-zh']:
      continue
  if REFSET == 'newstestP2020' :
    if lp != 'en-de':
      continue

  # if exclude_sys != 'incl':
  #   # print(lp, 'excl', exclude[lp])
  #   if not exclude[lp] :
  #     continue

  #when we have scores available for the human reference, 
  #should we include the pairs with human translations
  if  human == 'excl' or REFSET == 'newstestM2020': 
    if better == 'Human-B.0' or worse == 'Human-B.0':
      continue
    if better == 'Human-A.0' or worse == 'Human-A.0':
      continue


  if REFSET == 'newstest2020': 
    if better == 'Human-A.0' or worse == 'Human-A.0':
      continue


  if REFSET == 'newstestB2020':
    if better == 'Human-B.0' or worse == 'Human-B.0':
      continue


  if  exclude_sys  in ['outl', 'top1', 'top2', 'rand1', 'rand2']:
    if (better  in exclude[lp]) or (worse in exclude[lp]):
      # print('outl', better, worse) 
      continue 
  # print(exclude, '---', (better  in exclude[lp]) , (worse in exclude[lp]))


  # if  lp == 'de-en' and EXCL_YOLO_SYSTEM:
  #   print('ol', better, worse)

  #   if better == 'yolo.1052' or worse == 'yolo.1052':
  #       continue
  # print(better, worse, exclude[lp])

  if lp not in manual:
    manual[lp] = {}
  if sid not in manual[lp]:
    manual[lp][sid] = {}
  if better not in manual[lp][sid]:
    manual[lp][sid][better] = {}
  if worse not in manual[lp][sid][better]:
    manual[lp][sid][better][worse] = 1
  
missing = 0

met_names = {}
metrics = {} 
print('reading metric scores...')

for s in submissions:
  files = glob.glob(s)
  for f in files:
    print('    ',f)
    lines = [line.decode('utf8') for line in gzip.open(f,'r')]
    lines = [line.rstrip('\n') for line in lines]

    for l in lines: 

        c = l.split() 
        # cols = ['metric', 'lp', 'testset','refset','system', 'docid','segid', 'score']
        if level=='seg' and len(c) != 8 :
          print('len != 8', c)
          missing = missing + 1
          continue

        # cols = ['metric', 'lp', 'testset','refset','system', 'docid', 'score']
        elif level=='document' and len(c) != 7 :
          print('len != 8', c)
          missing = missing + 1
          continue

        else:  
          metric = c[0].replace('+','_PLUS_').replace('-','_DASH_') 
          lp = c[1]
          data = c[2]
          refset = c[3]
          system = c[4]
          if level=='seg' :
            # sid of seg human scores file is in the form of docid::segid 
            sid = c[5] + '::' +c[6]
            score = float(c[7])          
          if level=='document' or level=='doc' : 
            sid = c[5] 
            score = float(c[6])   

          if refset != REFSET: 
            continue


          if lp not in metrics:
            metrics[lp] = {}
          if metric not in metrics[lp]:
            metrics[lp][metric] = {}
          if sid not in metrics[lp][metric]:
            metrics[lp][metric][sid] = {}
          if system not in metrics[lp][metric][sid]:
            metrics[lp][metric][sid][system] = score
    
print('metrics scores stored in memory for lps = ', sorted(list(metrics.keys())))
print('manual scores stored in memory for lps = ', sorted(list(manual.keys())))

for lp in manual:
  print('processing',lp)
# check which metrics have scores for all segs    
  if lp not in metrics:
    print (lp+" not in metrics")
    exit(1)
  
  for metric in metrics[lp]:

    allthere = True

    # check if all manual segments are present for this metric
    for sid in manual[lp]: #[sid][better][worse]
       if not sid in metrics[lp][metric]:
         allthere = False
         print ("A) Missing "+lp+" "+metric+" "+sid+" no scores at all for this metric and sid")
         exit(1)
       else:  # if that metric does have at least one score for this sid - check system
         for s1 in manual[lp][sid]:
           if not s1 in metrics[lp][metric][sid]:
             allthere = False
             print ("B) Missing "+lp+" "+metric+" "+sid+" "+s1+" no scores for this metric for sid and first  system")
             exit(1)
           for s2 in manual[lp][sid][s1]:
             if not s2 in metrics[lp][metric][sid]:
               allthere = False
               print ("C) Missing "+lp+" "+metric+" "+sid+" "+s1+" "+s2+" no scores for this metric for sid and second system")
               exit(1)

    if allthere:
      if lp not in met_names:
        met_names[lp] = {}
      if metric not in met_names[lp]:
        met_names[lp][metric] = 1

    else:
     print ("segment mismatch "+lp+" "+metric) 

 
for lp in manual:

  s = ""
  l = lp.replace("-","")

  f = f"{OUTPUTDIR}/RR-newstest2020-"+l+"-seg-nohy-cor.csv"
  F = open(f,'w')

  for metric in sorted(met_names[lp]):

    conc = 0
    disc = 0

    for sid in manual[lp]:
      
      for better in manual[lp][sid]:
        for worse in manual[lp][sid][better]:

          if better not in metrics[lp][metric][sid]:
            print ("error "+lp+" "+metric+" "+better)

          score1 = metrics[lp][metric][sid][better]
          score2 = metrics[lp][metric][sid][worse]
  
          if score1 > score2:
            conc = conc + 1
          else:
            disc = disc + 1
          
    conc =  (conc)
    disc =  (disc)
    #result = abs((conc-disc)/(conc+disc))
    result = (conc - disc)/(conc+disc)
    # s = s + metric+" "+f'{result:.4}'+" "+str(int(conc))+" "+str(disc)+" "+str(conc+disc)+"\n"
    s = s + f'{metric} {result:.4} {conc+disc}\n'

  F.write(s)
  F.close() 




print('done printing correlations')
for lp in manual:

  l = lp.replace("-","")

  f = f"{OUTPUTDIR}/RR-newstest2020-"+l+"-seg-nohy-agree.csv"
  # print(f)
  # if os.path.isfile(f):
  #   print('already exists')
  #   continue
  F = open(f,'w')

  s = "SID BETTER WORSE" 

  for metric in sorted(met_names[lp]):
    s = s + " "+metric
  s = s + "\n"
  F.write(s)
  
  print ("starting "+lp  )

  for sid in manual[lp]:
    for better in manual[lp][sid]:
      for worse in manual[lp][sid][better]:
        #print better, worse
        s = sid+" "+better+" "+worse
 
        for metric in met_names[lp]:

          if better not in metrics[lp][metric][sid]:
            print ("error "+lp+" "+metric+" "+better)
            exit(1)

          score1 = metrics[lp][metric][sid][better]
          score2 = metrics[lp][metric][sid][worse]

          answer = "0"
  
          if score1 > score2:
            answer = "1"


          s = s + " "+answer  

        s = s +"\n"
        F.write(s) 
  # F.write(s)
  F.close()
  print ("finished "+lp)

print ("finished creating relative scores")


 