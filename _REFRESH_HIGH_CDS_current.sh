#for t in W1 M1 D1 H4 H1;do for i in EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD;do jgtapp cds -i $i -t $t --fresh ;done;done
#(cd $JGTPY_DATA/cds;for f in *.csv;do droxul upload $f /dist/data/current/cds;done)
unset JGTPY_DATA_FULL
unset JGTPY_DATA
. .env|| true
export JGTPY_DATA
export JGTPY_DATA_FULL



for t in W1 M1 D1 H4 H1 m15 m5;do 
  for i in XAU/USD EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD;do 
    (jgtcli -i $i -t $t --fresh && (p=$(jgtcli -i $i -t $t --fresh -vp);droxul upload $p /dist/data/current/cds&))
  done
done

#(cd $JGTPY_DATA/cds;for f in *.csv;do droxul upload $f /dist/data/current/cds;done)
