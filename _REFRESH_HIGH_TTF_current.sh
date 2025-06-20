for i in  EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD;do for t in D1 H4;do ttfcli -i $i -t $t -pn mz;done;done

(droxul mkdir /dist/data/current/ttf&>/dev/null;cd $JGTPY_DATA/ttf && echo -n "UPloading ttf to /dist/data/current/ttf ";  for f in *csv;do droxul upload $f /dist/data/current/ttf/$f&>/dev/null;echo -n ".";done) && echo " done."

