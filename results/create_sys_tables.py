 


outputformat = 'latex' 
significance = False
correlation_type = 'Pearson'

scores_dir = './output/system-level/'
outdir= './tables'

 


import pickle
import os
import numpy as np
 

 
scores_files = f'{scores_dir}/*scores.csv' 
outliers_dict  = pickle.load(open('../manual-evaluation/outlier-systems-dict.pk', 'rb'))
def is_outlier(df, syscolname = 'SYSTEM'): 
    lp = df.LP[0][:5]
    outliers = [True if sys in outliers_dict[lp] else False for sys in df[syscolname]]
    return np.array(outliers)
exclude_outliers = lambda scores: scores[~is_outlier(scores)]

 
qe_metrics = ['COMET-QE', 'OpenKiwi-Bert', 'OpenKiwi-XLMR', 'YiSi-2']
human_systems = ['Human-A.0','Human-B.0', 'Human-P.0']

langs=['cs', 'de', 'ja','pl','ru','ta','zh']    

ENTO_LPS = [f'en-{l}' for l in langs]
ENTO_LPS.extend( ['en-iu_full','en-iu_news'])

TOEN_LPS = [f'{l}-en' for l in langs]
TOEN_LPS.extend( ['iu-en','km-en','ps-en'])

ALL_LPS = TOEN_LPS + ENTO_LPS

MULTIREF_TOEN_LPS = ['de-en','de-en_B','de-en_M',  'ru-en', 'ru-en_B', 'ru-en_M', 'zh-en','zh-en_B','zh-en_M', ]
MULTIREF_ENTO_LPS = [ 'en-de','en-de_B','en-de_P','en-de_M', 'en-zh', 'en-zh_B', 'en-zh_M']


EVALHUMAN_LPS = ['de-en', 'ru-en', 'zh-en', 'en-de',   'en-zh']
 
os.makedirs(outdir, exist_ok = True)
 

 

import pandas as pd
import glob 
            
from metric_williams import metric_williams
from utils import output_tables, output_combined_tables

class DACorrelation:
    """ stores and returns information related to Pearson/Kendall Tau correlation
    and (optionally) significance values for each language pair """
    
    def __init__(self, scores_dir = None, correlation = 'Pearson', williams = False, include_lps = None, exclude_outliers = None, 
                 exclude_systems = None, include_metrics = None): 
        self.correlation = correlation
        self.ss = williams  
        self.lps = []  
        self.scores = {}
        self.include_metrics = include_metrics
        self.exclude_outliers = exclude_outliers 
        self.correlations = {}  
        self.pvals = {}   
        if scores_dir:
            scores_files = f'{scores_dir}/*scores.csv'
            print(f'importing scores from dir: {scores_dir}')
            for file in sorted(glob.glob(scores_files)): 
                self.add_scores_file(file, include_lps = include_lps, exclude_systems = exclude_systems)
        
    def add_scores_file(self, file, include_lps = None, exclude_systems = None):  
            scores = pd.read_csv(file, delimiter = '\s', engine='python') 
    
            lp = scores['LP'].values[0] 
            if include_lps:
                if lp not in include_lps:
                    return
                
            if self.include_metrics:  
                temp=scores[['LP','SYSTEM','HUMAN']].copy()
                for metric in self.include_metrics:
                    if metric in scores:
                        temp[metric] = scores[metric]
                if len(temp.columns) == 3:
                    print(f'skipping {lp}: None of {include_metrics} are available') 
                    display(scores)
                    return
                scores = temp
            
            if exclude_systems:                
                scores = scores[~scores.SYSTEM.isin(exclude_systems)]  
                
            scores_nonans = scores.dropna(axis = 1) 
            metricsna = set(scores.columns) - set(scores_nonans.columns)

            if len(metricsna) != 0:
                print(f' NaNs for lp {lp} for metrics {metricsna}') 
                if len(scores_nonans.columns) == 3:
                    print(f'skipping {lp}: No metrics without NaNs for lp') 
                    return
                    
            scores = scores.dropna(axis = 1) 
            
            if self.exclude_outliers: 
                temp = self.exclude_outliers(scores)  
#                 print(f'{lp}:  {len(scores) - len(temp)} outliers')
                scores = temp          
#             print(f'{lp}: {len(scores)} systems')
            self.lps.append(lp) 
                
            self.scores[lp] = scores    
            self.compute_corrs(scores)
        

    def compute_corrs(self, scores):  
        lp = scores['LP'].values[0]  
        
        corrs = pd.DataFrame(scores.corr(self.correlation.lower()).HUMAN[1:].rename(self.correlation))    
        corrs = corrs.sort_values(self.correlation, ascending=False)
        corrs['N'] = len(scores)  
        
        if self.ss:
            self.pvals[lp], winners = metric_williams(scores)  
            corrs['Winner'] =  winners 
            
        self.correlations[lp] = corrs 
        self.write_corr_files(lp)
        
        
    def get_tables(self, lps, formatter):   
        corrs = [] 
        for lp in lps: 
            corr = self.correlations[lp]
            if 'Winner' not in corr.columns:
                corr['Winner'] = [False for _ in corr.index]
            formattedscores = [formatter(c, w) for c,w in zip(corr[self.correlation], corr.Winner)]    
            corrs.append(pd.DataFrame(index = corr.index, data = {(lp, corr.N[0]): formattedscores }))
            
        res = pd.DataFrame().join(corrs, how='outer', sort=False).fillna('-')
        
        if self.include_metrics:
            ordered_metrics = [m for m in  self.include_metrics if m in res.index ]
            return res.reindex(ordered_metrics)
        else:
            return res.reindex(sorted(res.index.values,key = lambda x: x.upper()))
    

    def write_corr_files(self, lp):
        if self.exclude_outliers:
            suffix = '-excloutl'
        else:
            suffix = ''
        """writes correlations and significance results to file for each language pair"""
        lp_ = "".join(lp.split('-'))  
        self.correlations[lp].to_csv( f"{scores_dir}/DA-{lp_}-cor{suffix}.csv", sep= '\t')
        if self.ss:
            self.pvals[lp].to_csv(f"{scores_dir}/DA-{lp_}-sig{suffix}.csv", sep= '\t')
            
                  

 



da_allsys = DACorrelation(scores_dir=scores_dir, williams = True, correlation='Pearson',  
                            include_lps = ENTO_LPS + TOEN_LPS, 
                            exclude_outliers = None, 
                            exclude_systems = human_systems, include_metrics = None)   
output_tables(da_allsys, outputformat=outputformat, output_dir=outdir, 
              lp_groups = {'MTall-exclhuman-ento': ENTO_LPS, 'MTall-exclhuman-toen': TOEN_LPS});

 


da_excloutl = DACorrelation(scores_dir=scores_dir, williams = True, correlation='Pearson', 
                           include_lps = None, 
                           exclude_outliers = exclude_outliers, 
                           exclude_systems = human_systems, include_metrics =  None)    


output_tables(da_excloutl, outputformat=outputformat, output_dir=outdir, 
             lp_groups = {'MTexcloutl-exclhuman-ento': ENTO_LPS, 'MTexcloutl-exclhuman-toen': TOEN_LPS});

 


output_combined_tables(da_allsys, da_excloutl, outputformat=outputformat, output_dir=outdir, 
             lp_groups = {'MTcombined-exclhuman-ento': ENTO_LPS, 'MTcombined-exclhuman-toen': TOEN_LPS}) ;

 

kt_allsys = DACorrelation(scores_dir=scores_dir, williams = False, correlation='Kendall', 
                            exclude_outliers = None, 
                            exclude_systems = human_systems, include_metrics = None,)   
output_tables(kt_allsys, outputformat=outputformat, output_dir=outdir, 
              lp_groups = {'MTall-exclhuman-ento': ENTO_LPS, 'MTall-exclhuman-toen': TOEN_LPS})

 


da_excloutl_mref = DACorrelation(scores_dir=scores_dir, williams = True, correlation='Pearson',  
                            include_lps = None,  
                            exclude_outliers = exclude_outliers, 
                            exclude_systems = human_systems, include_metrics = None)    

output_tables(da_excloutl_mref, outputformat=outputformat, output_dir=outdir, 
              lp_groups = {'MTexcloutl-exclhuman-alllp-mref': MULTIREF_ENTO_LPS + MULTIREF_TOEN_LPS});

 

