


from scipy.stats import pearsonr
import pandas as pd
import sys
import argparse
import glob 
import random 
import os 
import numpy as np
import pickle

 


# en-iu: for all submited metrics, compute metric sys scores for out of domain segs separately as avg seg scores """
# note that we denote the lp of out of domain en-iu as en-in as some scripts later 
# expect lp to have the format of two letter codes for src and tgt
 

cols = ['metric', 'lp', 'testset','refset','SYSTEM', 'docid','segid', 'score'] 
metricspath=f'../final-metric-scores/submissions/*.seg.*gz'  
output_dir=f'../final-metric-scores/subm_eniu_outofdomain/' 

os.makedirs(output_dir, exist_ok=True) 

for fn in sorted(glob.glob(metricspath)):
   basename = fn.split('/')[-1]
    
   sys_fn =basename.replace('seg.sc','sys.sc')   
   if os.path.isfile(os.path.join(output_dir, sys_fn)):
       continue
   metric_df = pd.read_csv(fn, sep='\t',header=None)    
   if len(metric_df.columns) != len(cols ): 
       print("!error with format of file",fn)
       continue

   metric_df.columns = cols   
   metric=metric_df.metric[0]
   
   news = metric_df[metric_df.testset  == 'newstest2020'] 
   eniu = news[news.lp == 'en-iu'].copy()
   outofdomain = eniu[~eniu.docid.str.startswith('Hansard')].copy()
   outofdomain['lp'] = 'en-in'
   if len(eniu) != 0: 
       sys  = outofdomain.groupby(['metric','lp','testset','refset', 'SYSTEM']).score.mean()
       sys.to_csv( os.path.join(output_dir, sys_fn),compression='gzip', header = False, index =True, sep='\t')

 


DAscorespath = '../manual-evaluation/DA' 
metricspath=f'../final-metric-scores/*/*.sys.*gz'   
scoresdir = '../results/output/system-level/' 
os.makedirs(scoresdir, exist_ok=True)  

 
langs=['cs', 'de','iu', 'ja','pl','ru','ta','zh']    
ALL_LPS = [f'{l}-en' for l in langs]
ALL_LPS.extend( ['km-en','ps-en'])
ALL_LPS.extend( [f'en-{l}' for l in langs])

refsets_available={}
for lp in ALL_LPS:
    refsets_available[lp] = [ 'newstest2020']

    
for lp in ['de-en',  'ru-en', 'zh-en', 'en-de', 'en-zh']:
    refsets_available[lp].extend([ 'newstestB2020', 'newstestM2020'])
refsets_available['en-de'].append('newstestP2020') 
    
refset_suffixes = {'newstest2020':'', 'newstestB2020':'_B', 'newstestM2020':'_M', 'newstestP2020':'_P'    }

QE_METRICS=  [  'COMET-QE',  'OpenKiwi-Bert', 'OpenKiwi-XLMR',
       'YiSi-2'] 

 



#read human scores

all_scores = {}
for lp in ALL_LPS:
    human_scores = pd.read_csv(f'{DAscorespath}/metrics-ad-sys-scores-{lp}.csv', sep=' ') 
    for refset in refsets_available[lp]:
        all_scores[(lp, refset)] = pd.DataFrame.from_dict({'LP':lp,
                                                 'SYSTEM': human_scores['SYS'], 
                                                 'HUMAN': human_scores['Z.SCR'],
                                                'HUMAN_RAW': human_scores['RAW.SCR']
                                                })
    
all_scores[('en-in', 'newstest2020')]     = all_scores[('en-iu', 'newstest2020')].copy()
all_scores[('en-in', 'newstest2020')].LP = 'en-in'

 
#read metrics

metricspath=f'../final-metric-scores/*/*.sys.*gz'  

cols= {'sys':['metric', 'lp', 'testset','refset', 'SYSTEM',  'score'] }
level='sys' 
  
for fn in sorted(glob.glob(metricspath)): 
    metric_df = pd.read_csv(fn, sep='\t',header=None)    
    if len(metric_df.columns) != len(cols[level]): 
        print('!! error in columns',fn)
        continue

    metric_df.columns = cols[level]   
    metric=metric_df.metric[0]
#     print(metric)
#     print('\t', metric_df.lp.unique())
#     print('\t', metric_df.refset.unique()) 

    if any(metric_df.score.isna()):
        print(f'!! NaNs in {metric} scores :( ') 
        continue
    for (lp, refset) in all_scores: 
        if metric in QE_METRICS:
            metriclp = metric_df[(metric_df.lp == lp) & (metric_df.refset == 'newstest2020')]
             
        else:
            metriclp = metric_df[(metric_df.lp == lp) & (metric_df.refset == refset)]

        if len(metriclp) == 0:
            continue 
        metriclp = metriclp[['SYSTEM','score']]
        metriclp.columns=['SYSTEM',metric] 

        if metric in all_scores[(lp, refset)].columns: 
            continue
            
        alp = all_scores[(lp, refset)].merge(metriclp, on=['SYSTEM'], how='left') 

        if len(alp) == len(all_scores[(lp, refset)]):
            all_scores[(lp, refset)] = alp
        else:
            print("!error reading scores:",metric, lp, refset) 
                        
        
 
# (our files use code en-in to represent  out of domain en-iu)
all_scores[('en-iu_news', 'newstest2020')] = all_scores.pop(('en-in', 'newstest2020'))
all_scores[('en-iu_full', 'newstest2020')] = all_scores.pop(('en-iu', 'newstest2020'))
all_scores[('en-iu_news', 'newstest2020')]['LP'] = 'en-iu_news'
all_scores[('en-iu_full', 'newstest2020')]['LP'] = 'en-iu_full'
 




# compute mref scores of MEE as max score of all testsets
for lp, refsets in refsets_available.items():
    print(lp)
    if 'newstestM2020' in refsets:
        m = {}
        for r in refsets:
            if r != 'newstestM2020':
                if 'MEE' in all_scores[lp, r].columns:
                    m[r] = all_scores[lp, r].MEE
            
        df = pd.DataFrame.from_dict(m)
        all_scores[lp, 'newstestM2020' ]['MEE'] = df.max(axis = 1, skipna=False)
 



#store scores
pickle.dump(all_scores, open(os.path.join(scoresdir, 'allsysscores.pk'), 'wb'))
 
for (lp, refset), scoresdf in all_scores.items(): 
    df = scoresdf.copy()
    lp1 = "".join(lp.split('-')) 
    df['LP'] = lp + refset_suffixes[refset] 
    df.to_csv(f'{scoresdir}/DA-{refset}-{lp1}-sys-scores.csv',sep=" ", index=False)
    
 

#eniu_news-vs-full
# corrs = pd.DataFrame.from_dict({'news':all_scores[('en-iu_news', 'newstest2020')].corr().HUMAN , 'full testset':all_scores[('en-iu_full', 'newstest2020')].corr().HUMAN})
# corrs.to_csv('output/system-level/eniu_news-vs-full', sep = '\t')

