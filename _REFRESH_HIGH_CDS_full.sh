for t in W1 M1 D1;do for i in EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD;do jgtapp cds -i $i -t $t --fresh --full;done;done
(cd $JGTPY_DATA_FULL/cds;for f in *.csv;do droxul upload $f /dist/data/full/cds;done)
