#for t in W1 M1 D1 H4 H1;do for i in EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD;do jgtapp cds -i $i -t $t --fresh ;done;done
#(cd $JGTPY_DATA/cds;for f in *.csv;do droxul upload $f /dist/data/current/cds;done)

unset JGTPY_DATA_FULL
unset JGTPY_DATA
. .env|| true
export JGTPY_DATA
export JGTPY_DATA_FULL

#Ensure the folders where we drop our files are there
(droxul mkdir /dist/data&>/dev/null;for d in cds ttf mlf targets;do droxul mkdir /dist/data/full/$d &>/dev/null;done;droxul mkdir /dist/data/full/targets/mx&>/dev/null)&
patterns="mfi mz zonesq"

for t in W1 M1 D1 H4 ;do 
	for i in EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD;do 
    (jgtcli -i $i -t $t --fresh --full && \
	    (fp=$(jgtcli -i $i -t $t --fresh --full -vp);droxul upload $fp /dist/data/full/cds/)&) && \
	    if [ "$t" != "M1" ];then 
		    ( 
		    for p in $patterns;do 
			ttfcli -i "$i" -t "$t" -pn "$p" --full -old && \
	    		mlfcli -i "$i" -t "$t" -pn "$p" --full -old && \
	    		jgtmlcli -i "$i" -t "$t" -pn "$p" --full -old  
    			done
			)
	    fi
  	done #all instrucments just done for the timeframe
	# we upload in background each patterns we calculated for the timeframe
	(for p in $patterns;do 
		(cd $JGTPY_DATA_FULL && \
			for d in ttf mlf targets/mx;do 
				(cd $d && \
					droxul upload *$t*$p*.csv /dist/data/full/$d/
				) 
			done \
		)&>/dev/null && \
				echo "----$t UPLOADED OK-------------------------------------------------------------------------------------------------------------------------------------------------") &


done

#(cd $JGTPY_DATA/cds;for f in *.csv;do droxul upload $f /dist/data/current/cds;done)
#
