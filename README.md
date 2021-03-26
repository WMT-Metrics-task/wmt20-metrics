
Repo to hold code for WMT Metrics Task evaluation

Requirements: Python >= 3.6, numpy and pandas

And optionally, if you'd like to get "winners" of a language pair, i.e. metrics not outperformed by any other based on the William's test for statistical significance, you'll need the r2py library in python, and the psych library in R.



in the results folder, look at the three ipython nbs:
p1-process_scores_and_visualize.ipynb: this processes metric scores, updates human scores to be consistent with metrics inputs, computes doclevel human scores, and visualises sys-level human scores and computes outlier systems. 

p2-combine-sys-scores.ipynb: this is to generate csv files to store all sys-level human and metric scores for each lp

p3-maketables.ipynb: this creates systemlevel tables in latex, as well as display in the notebook. replace 'latex' with 'csv' to generate csvs instead.

Final tables in results/system-level/tables



For seg/doc level results, run
 
>>bash get-daRR-results-nosig.sh LEVEL
where LEVEL is seg or doc
 
Final tables in results/out



to compute signficance results as well,  run

>>bash get-daRR-results-sig.sh LEVEL
 


