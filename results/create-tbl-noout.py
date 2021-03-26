import sys
import glob 
import os.path

from collections import defaultdict
DATA = sys.argv[1]
HYBRID = sys.argv[2]
LEVEL = sys.argv[3]
outfn = sys.argv[4]
SIGNIFICANCE = 'NO'

nonensemble =defaultdict(int) 
print DATA, LEVEL ,outfn
 
f = 'output/' + LEVEL + "level_excloutl/*-"+DATA+"*en-*"+'seg'+"*"+HYBRID+"*cor.csv"
toen_noout = glob.glob(f)
f =  'output/' + LEVEL + "level_excloutl/*-"+DATA+"*-en*"+'seg'+"*"+HYBRID+"*cor.csv"
ento_noout = glob.glob(f)

f = 'output/' + LEVEL + "level_allsys/*-"+DATA+"*en-*"+'seg'+"*"+HYBRID+"*cor.csv"
toen = glob.glob(f)
f = 'output/' + LEVEL + "level_allsys/*-"+DATA+"*-en*"+'seg'+"*"+HYBRID+"*cor.csv"
ento = glob.glob(f)
# print(f) 

def printTable( files, files_noout, outfn):
  # print(files_noout)
  with open(outfn, 'a') as outf:

    r  = {}
    r_noout = {}
    names = {}
    systems = {}
    systems_noout = {}
    winners = {}
    winners_noout = {}
    numcols =   len(files)  

    outf.write('\n\n\n')
    outf.write('\\begin{{tabular}}{{l{0}}}\n\\toprule\n'.format('c'*numcols))

    for f , fo in zip(files, files_noout):

       
      outf.write("%% "+f + '\n')
      if f.find("en-")> -1:
        i = f.find("en-")-2
        lp = f[i:i+4]
      else:
        i = f.find("-en")+1
        lp = f[i:i+4]
      winnerf = f.replace("cor.csv","winners.csv")
      winnerf_noout = fo.replace("cor.csv","winners.csv")
      if SIGNIFICANCE=='YES' and   os.path.exists(winnerf): 
 
          lines = [line.rstrip('\n') for line in open(winnerf)]
          lines_noout = [line.rstrip('\n') for line in open(winnerf_noout)]

          for l in lines:
            c = l.split()
            metric = c[0]
            winner = c[1]
            if lp not in winners:
              winners[lp] = {}
            if metric not in winners[lp]: 
                winners[lp][metric] = winner  


          for l in lines_noout:
            c = l.split()
            metric = c[0]
            winner_noout = c[1]
            if lp not in winners_noout:
              winners_noout[lp] = {}
            if metric not in winners_noout[lp]: 
                winners_noout[lp][metric] = winner_noout  

      else: 
        winners_noout = {}
        winners ={}
      # print 'Winners' , lp, winners
      lines = [line.rstrip('\n') for line in open(f)]
      lines_noout = [line.rstrip('\n') for line in open(fo)]
      for l in lines:
        c = l.split()

        metric = c[0]
        # print(metric)
        cor = c[1]
        n = c[2]

        if metric not in names:
          names[metric] = 1
    
        if lp not in r:
          r[lp] = {}
        if metric not in r[lp]:
          r[lp][metric] = round(float(cor),3)
        if lp not in systems:
          systems[lp] = int(n)


      for l in lines_noout:
        c = l.split()

        metric = c[0]
        cor_noout = c[1]
        n = c[2]

        if metric not in names:
          names[metric] = 1
    
        if lp not in r_noout:
          r_noout[lp] = {}
        if metric not in r_noout[lp]:
          r_noout[lp][metric] = round(float(cor_noout),3) 

        if lp not in systems_noout:
          systems_noout[lp] = int(n)
      # print lp, r_noout[lp], r[lp]
    s = "                           "
    # print systems_noout, systems
    for lp in sorted(r):  
      l = lp[0:2]+"-"+lp[2:4]

      # s = s+" & \multicolumn{2}{c}{\\bf "+l+"}" 
      s = s+" & {\\bf "+l.replace("_","\\_")+"}" 
    s = s + " \\\\[1ex]\n"
    s = s+"                           "

    for lp in sorted(r): 
      if systems[lp] - systems_noout[lp] > 0:  
        s = s + " & all \quad all-out "
      else:
        s = s + " & all "

    s = s + " \\\\[1ex]\n"

    for lp in sorted(r): 
      n = str(systems[lp])
      n_o = str(systems_noout[lp])
      while len(n) < 10:
        n = " "+n 
        n_o = ' ' + n_o
      if systems[lp] - systems_noout[lp] > 0:  
        s = s+" & "+n+ " \quad "+n_o+" " 
      else:
        s = s+" & "+n+" "   

    s = s + " \\\\[1ex]\n"

    s = s + " \\midrule\n" 
  # print(names) 
    for metric in sorted(names, key=lambda s: s.lower()):
      m = metric
      m = m.replace('_PLUS_',"+")
      m = m.replace('_DASH_',"-")  
 
 
      m = m.replace("_","\\_")
      m = "\\metric{"+m+"} "
      while len(m) < 26:
        m = m+" "    

      s = s+m+" "
      for lp in sorted(r):
        if metric in r[lp]:
          correl = str(r[lp][metric])
          correl_noout =  str(r_noout[lp][metric])
          while len(correl) < 5:
            correl = correl+"0"
          while len(correl_noout) < 5:
            correl_noout = correl_noout+"0"

          if lp in winners and winners[lp][metric] == "YES":
            s = s + " & {  "+correl+"}"
          else:
            s = s + " &      "+correl+" "
          if systems[lp] - systems_noout[lp] > 0:  
            if lp in winners_noout and winners_noout[lp][metric] == "YES":
              s = s + " / {  "+correl_noout+"}"
            else:
              s = s + " /      "+correl_noout+" "
        else:
          s = s + " &         $-$ "

      s = s + " \\\\\n" 
    outf.write(s)    
    outf.write('\\bottomrule\n')
    outf.write('\\end{tabular}\n')
    # outf.write('\\end{sidewaystable}\n')


print outfn

printTable(toen, toen_noout,outfn)
printTable(ento, ento_noout,outfn)
