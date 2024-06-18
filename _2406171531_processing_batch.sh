for i in SPX500 EUR/USD GBP/USD AUD/USD;do for d in S B;do for t in H4 D1;do 
  python jgtml_observe_dataset__240515_valid_TIDE_alligator_SIGNALS.py -i $i -t $t -nf -bs $d 
  done;done;done
