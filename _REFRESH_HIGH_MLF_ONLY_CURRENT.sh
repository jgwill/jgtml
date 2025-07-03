#!/bin/bash
# Unset environment variables
unset JGTPY_DATA_FULL
unset JGTPY_DATA

# Source environment file
source .env 2>/dev/null || true

# Export variables
export JGTPY_DATA
export JGTPY_DATA_FULL



for t in W1 M1 D1 H4 ;do 
  for i in EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD;do 
	    for p in mfi mz zonesq;do 
		    ttfcli -i "$i" -t "$t" -pn "$p" -old && \
	    	mlfcli -i "$i" -t "$t" -pn "$p"  -old
	   
    done
  done
done

#(cd $JGTPY_DATA/cds;for f in *.csv;do droxul upload $f /dist/data/current/cds;done)
