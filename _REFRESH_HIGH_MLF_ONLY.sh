#(cd $JGTPY_DATA/cds;for f in *.csv;do droxul upload $f /dist/data/current/cds;done)
for t in W1 M1 D1 H4 ;do 
  for i in EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD;do 
	    for p in mfi mz zonesq;do 
		    ttfcli -i "$i" -t "$t" -pn "$p" --full -old && \
	    	mlfcli -i "$i" -t "$t" -pn "$p" --full -old && \
	    jgtmlcli -i "$i" -t "$t" -pn "$p" --full -old 
    done
  done
done

#(cd $JGTPY_DATA/cds;for f in *.csv;do droxul upload $f /dist/data/current/cds;done)
