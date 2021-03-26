 
LEVEL=$1
THRESHOLD=25
REFSET=newstest2020

EXCLUDE=none

echo "python combine-scores-seg-RR.py -l ${LEVEL}  -e ${EXCLUDE}"
python combine-scores-seg-RR.py -l ${LEVEL}  -e ${EXCLUDE}
  

# python2 create-tbl-noout.py newstest2020 nohy ${LEVEL}  out/tbl-combined-${REFSET}-nohy-${LEVEL}-excl${EXCLUDE}.tex

outdir=output/${LEVEL}level_allsys 
mkdir -p $outdir 
mv out/* $outdir

 
EXCLUDE=outl 

echo "python combine-scores-seg-RR.py -l ${LEVEL}  -e ${EXCLUDE}"
python combine-scores-seg-RR.py -l ${LEVEL}  -e ${EXCLUDE}
 
# python2 create-tbl-noout.py newstest2020 nohy ${LEVEL}  out/tbl-combined-${REFSET}-nohy-${LEVEL}-excl${EXCLUDE}.tex

outdir=output/${LEVEL}level_excloutl  
mkdir -p $outdir 
mv out/* $outdir

 
REFSET=newstest2020
mkdir -p tables 

tbl_filename=tables/tbl-combined-${REFSET}-nohy-${LEVEL}.tex
python2 create-tbl-noout.py newstest2020 nohy ${LEVEL}  $tbl_filename NO
 