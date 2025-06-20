#for t in W1 M1 D1 H4 H1;do for i in EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD;do jgtapp cds -i $i -t $t --fresh ;done;done
#(cd $JGTPY_DATA/cds;for f in *.csv;do droxul upload $f /dist/data/current/cds;done)
. .env||true

for t in W1 M1 D1 H4 ;do 
  for i in EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD;do 
    (jgtcli -i $i -t $t --fresh --full && \
	    (p=$(jgtcli -i $i -t $t --fresh --full -vp);droxul upload $p /dist/data/full/cds)&) && \
	    (for p in mfi mz zonesq;do ttfcli -i "$i" -t "$t" -pn "$p" --full -old && \
	    mlfcli -i "$i" -t "$t" -pn "$p" --full -old && \
	    jgtmlcli -i "$i" -t "$t" -pn "$p" --full -old ;done)
  done
done

#(cd $JGTPY_DATA/cds;for f in *.csv;do droxul upload $f /dist/data/current/cds;done)
