#for i in  EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD;do for t in D1 H4;do ttfcli -i $i -t $t -uf -pn mz;done;done

(droxul mkdir /dist/data/full/ttf&>/dev/null;cd $JGTPY_DATA_FULL/ttf && echo -n "UPloading ttf to /dist/data/full/ttf ";  for f in *csv;do droxul upload $f /dist/data/full/ttf/$f&>/dev/null;echo -n ".";done)  && echo " done."

