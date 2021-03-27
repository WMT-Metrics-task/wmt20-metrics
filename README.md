
Repo to hold code for WMT Metrics Task evaluation

Requirements: Python >= 3.6, numpy and pandas

And optionally, if you'd like to get "winners" of a language pair, i.e. metrics not outperformed by any other based on the William's test for statistical significance, you'll need the r2py library in python, and the psych library in R.


Run results/get-all-results.sh to reproduce results





Intermediate tables with metric scores and correlations for each language pair  in results/output 

Final latex tables in results/tables 


The notebook results/p0-preprocess_scores_and_visualize.ipynb  contains code for preprocessing human and metric scores and visualising system level scores and identifying outliers. 
