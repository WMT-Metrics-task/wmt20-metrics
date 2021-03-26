# mv summary* ~/trash
echo "LP DATA SID BETTER WORSE" > ../DArr-seglevel.csv
python seglevel-ken-rr.py cs en newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py de en newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py iu en newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py ja en newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py pl en newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py ru en newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py ta en newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py zh en newstest2020 seg >> ../DArr-seglevel.csv
 
python seglevel-ken-rr.py km en newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py ps en newstest2020 seg >> ../DArr-seglevel.csv


python seglevel-ken-rr.py en cs newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py en de newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py en iu newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py en ja newstest2020 seg   >> ../DArr-seglevel.csv
python seglevel-ken-rr.py en pl newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py en ru newstest2020 seg >> ../DArr-seglevel.csv
python seglevel-ken-rr.py en ta newstest2020 seg   >> ../DArr-seglevel.csv
python seglevel-ken-rr.py en zh newstest2020 seg >> ../DArr-seglevel.csv

mkdir seg-summary

mv summary* seg-summary

echo "LP DATA SID BETTER WORSE" > ../DArr-doclevel.csv
python seglevel-ken-rr.py cs en newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py de en newstest2020 doc >> ../DArr-documentlevel.csv
# iuen was not doc level python seglevel-ken-rr.py iu en newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py ja en newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py pl en newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py ru en newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py ta en newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py zh en newstest2020 doc >> ../DArr-documentlevel.csv
 
python seglevel-ken-rr.py km en newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py ps en newstest2020 doc >> ../DArr-documentlevel.csv


python seglevel-ken-rr.py en cs newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py en de newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py en iu newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py en ja newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py en pl newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py en ru newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py en ta newstest2020 doc >> ../DArr-documentlevel.csv
python seglevel-ken-rr.py en zh newstest2020 doc >> ../DArr-documentlevel.csv

cp ../DArr-documentlevel.csv ../DArr-doclevel.csv

mkdir -p doc-summary

mv summary* doc-summary
# echo "LP DATA SID BETTER WORSE" > ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py cs en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py de en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py iu en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py ja en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py pl en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py ru en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py ta en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py zh en newstest2020 >> ../DArr-seglevel-random.csv

# python seglevel-ken-rr.py de cs newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py de fr newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py fr de newstest2020 >> ../DArr-seglevel.csv


# python seglevel-ken-rr.py en cs newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en de newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en fi newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en gu newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en kk newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en lt newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en ru newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en zh newstest2020 >> ../DArr-seglevel.csv


# echo "LP DATA SID BETTER WORSE" > ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py cs en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py de en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py iu en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py ja en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py pl en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py ru en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py ta en newstest2020 >> ../DArr-seglevel-random.csv
# python seglevel-ken-rr.py zh en newstest2020 >> ../DArr-seglevel-random.csv

# python seglevel-ken-rr.py de cs newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py de fr newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py fr de newstest2020 >> ../DArr-seglevel.csv


# python seglevel-ken-rr.py en cs newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en de newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en fi newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en gu newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en kk newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en lt newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en ru newstest2020 >> ../DArr-seglevel.csv
# python seglevel-ken-rr.py en zh newstest2020 >> ../DArr-seglevel.csv

