>python jgtml/mlfcli.py -i SPX500 -t D1 -fr --full -pn peaks
INFO::Columns List from Higher TF to prep laggings using MLF: ['price_peak_above', 'price_peak_bellow', 'ao_peak_above', 'ao_peak_bellow']

>python jgtml/mlfcli.py -i SPX500 -t D1 -fr --full -pn  peaksmfi

>python jgtml/mlfcli.py -i $i -t $t -fr --full -pn mfizone

```

INFO::Columns List from Higher TF to prep laggings using MLF: ['mfi_sig', 'zone_sig']


INFO::Columns List from Higher TF to prep laggings using MLF: ['ao', 'ac']
------------------------------------------------- Not Implemented Yet:: aoac

INFO::Columns List from Higher TF to prep laggings using MLF: ['price_peak_above', 'price_peak_bellow', 'ao_peak_above', 'ao_peak_bellow']
------------------------------------------------- Not Implemented Yet:: peaks

```


# Did the read comes from input pattern ??


```

INFO::Columns List from Higher TF to prep laggings using MLF: ['mfi_sig', 'zone_sig']
------------------------------------------------- Not Implemented Yet:: mfizone
   Read TTF:  /var/lib/jgt/full/data/ttf/SPX500_D1_mfizone.csv
Index(['BidOpen', 'BidHigh', 'BidLow', 'BidClose', 'AskOpen', 'AskHigh',
       'AskLow', 'AskClose', 'Volume', 'Open', 'High', 'Low', 'Close',
       'Median', 'ao', 'ac', 'jaw', 'teeth', 'lips', 'bjaw', 'bteeth', 'blips',
       'tjaw', 'tteeth', 'tlips', 'fh', 'fl', 'fh3', 'fl3', 'fh5', 'fl5',
       'fh8', 'fl8', 'fh13', 'fl13', 'fh21', 'fl21', 'fh34', 'fl34', 'fh55',
       'fl55', 'fh89', 'fl89', 'mfi', 'fdbb', 'fdbs', 'fdb', 'aoaz', 'aobz',
       'zlc', 'zlcb', 'zlcs', 'zcol', 'zone_sig', 'sz', 'bz', 'acs', 'acb',
       'ss', 'sb', 'price_peak_above', 'price_peak_bellow', 'ao_peak_above',
       'ao_peak_bellow', 'mfi_sq', 'mfi_green', 'mfi_fade', 'mfi_fake',
       'mfi_sig', 'mfi_str', 'mfi_sig_M1', 'zone_sig_M1', 'mfi_sig_W1',
       'zone_sig_W1'],
      dtype='object')

```

> SOUNDS GREAT

----

```

INFO::Columns List from Higher TF to prep laggings using MLF: ['price_peak_above', 'price_peak_bellow', 'ao_peak_above', 'ao_peak_bellow']
------------------------------------------------- Not Implemented Yet:: peaks
   Read TTF:  /var/lib/jgt/full/data/ttf/SPX500_D1_peaks.csv
Index(['BidOpen', 'BidHigh', 'BidLow', 'BidClose', 'AskOpen', 'AskHigh',
       'AskLow', 'AskClose', 'Volume', 'Open', 'High', 'Low', 'Close',
       'Median', 'ao', 'ac', 'jaw', 'teeth', 'lips', 'bjaw', 'bteeth', 'blips',
       'tjaw', 'tteeth', 'tlips', 'fh', 'fl', 'fh3', 'fl3', 'fh5', 'fl5',
       'fh8', 'fl8', 'fh13', 'fl13', 'fh21', 'fl21', 'fh34', 'fl34', 'fh55',
       'fl55', 'fh89', 'fl89', 'mfi', 'fdbb', 'fdbs', 'fdb', 'aoaz', 'aobz',
       'zlc', 'zlcb', 'zlcs', 'zcol', 'zone_sig', 'sz', 'bz', 'acs', 'acb',
       'ss', 'sb', 'price_peak_above', 'price_peak_bellow', 'ao_peak_above',
       'ao_peak_bellow', 'mfi_sq', 'mfi_green', 'mfi_fade', 'mfi_fake',
       'mfi_sig', 'mfi_str', 'price_peak_above_M1', 'price_peak_bellow_M1',
       'ao_peak_above_M1', 'ao_peak_bellow_M1', 'price_peak_above_W1',
       'price_peak_bellow_W1', 'ao_peak_above_W1', 'ao_peak_bellow_W1'],
      dtype='object')
```

> YEAH

----
# jgtmlcli

## Did we read the appropriate data ?

```

-------JTC Processing : SPX500_D1
                                 jgtml is using ttf....
   Read TTF:  /var/lib/jgt/full/data/ttf/SPX500_D1_peaks.csv
INFO::Columns list from higher TF: ['price_peak_above', 'price_peak_bellow', 'ao_peak_above', 'ao_peak_bellow']
>   We would use that to filter the columns and get our training data out of this refactored module (JTC.py)  -or shall I say from prototype to production/new module.  -> OUTPUT:  Training Data and Reality Data with which we would predict using our model.
Does these columns read from the source we would use to create the MXTarget data align with the input pattern peaks: Index(['BidOpen', 'BidHigh', 'BidLow', 'BidClose', 'AskOpen', 'AskHigh',
       'AskLow', 'AskClose', 'Volume', 'Open', 'High', 'Low', 'Close',
       'Median', 'ao', 'ac', 'jaw', 'teeth', 'lips', 'bjaw', 'bteeth', 'blips',
       'tjaw', 'tteeth', 'tlips', 'fh', 'fl', 'fh3', 'fl3', 'fh5', 'fl5',
       'fh8', 'fl8', 'fh13', 'fl13', 'fh21', 'fl21', 'fh34', 'fl34', 'fh55',
       'fl55', 'fh89', 'fl89', 'mfi', 'fdbb', 'fdbs', 'fdb', 'aoaz', 'aobz',
       'zlc', 'zlcb', 'zlcs', 'zcol', 'zone_sig', 'sz', 'bz', 'acs', 'acb',
       'ss', 'sb', 'price_peak_above', 'price_peak_bellow', 'ao_peak_above',
       'ao_peak_bellow', 'mfi_sq', 'mfi_green', 'mfi_fade', 'mfi_fake',
       'mfi_sig', 'mfi_str', 'price_peak_above_M1', 'price_peak_bellow_M1',
       'ao_peak_above_M1', 'ao_peak_bellow_M1', 'price_peak_above_W1',
       'price_peak_bellow_W1', 'ao_peak_above_W1', 'ao_peak_bellow_W1'],
      dtype='object')

```

> YEAH :) 

## Does the targets/mx created is by input patterns ??

```

-------JTC Processing : SPX500_D1
                                 jgtml is using ttf....
   Read TTF:  /var/lib/jgt/full/data/ttf/SPX500_D1_peaks.csv
INFO::Columns list from higher TF: ['price_peak_above', 'price_peak_bellow', 'ao_peak_above', 'ao_peak_bellow']
>   We would use that to filter the columns and get our training data out of this refactored module (JTC.py)  -or shall I say from prototype to production/new module.  -> OUTPUT:  Training Data and Reality Data with which we would predict using our model.
Does these columns read from the source we would use to create the MXTarget data align with the input pattern peaks: Index(['BidOpen', 'BidHigh', 'BidLow', 'BidClose', 'AskOpen', 'AskHigh',
       'AskLow', 'AskClose', 'Volume', 'Open', 'High', 'Low', 'Close',
       'Median', 'ao', 'ac', 'jaw', 'teeth', 'lips', 'bjaw', 'bteeth', 'blips',
       'tjaw', 'tteeth', 'tlips', 'fh', 'fl', 'fh3', 'fl3', 'fh5', 'fl5',
       'fh8', 'fl8', 'fh13', 'fl13', 'fh21', 'fl21', 'fh34', 'fl34', 'fh55',
       'fl55', 'fh89', 'fl89', 'mfi', 'fdbb', 'fdbs', 'fdb', 'aoaz', 'aobz',
       'zlc', 'zlcb', 'zlcs', 'zcol', 'zone_sig', 'sz', 'bz', 'acs', 'acb',
       'ss', 'sb', 'price_peak_above', 'price_peak_bellow', 'ao_peak_above',
       'ao_peak_bellow', 'mfi_sq', 'mfi_green', 'mfi_fade', 'mfi_fake',
       'mfi_sig', 'mfi_str', 'price_peak_above_M1', 'price_peak_bellow_M1',
       'ao_peak_above_M1', 'ao_peak_bellow_M1', 'price_peak_above_W1',
       'price_peak_bellow_W1', 'ao_peak_above_W1', 'ao_peak_bellow_W1'],
      dtype='object')
INFO::Saving MX Target data to file...
Saved to /var/lib/jgt/full/data/targets/mx/SPX500_D1_peaks_sel.csv
INFO::Saved to /var/lib/jgt/full/data/targets/mx/SPX500_D1_peaks_tnd.csv
INFO::Saved to /var/lib/jgt/full/data/targets/mx/SPX500_D1_peaks.csv

```
> yeah: /var/lib/jgt/full/data/targets/mx/SPX500_D1_peaks.csv

```
Date,BidOpen,BidHigh,BidLow,BidClose,AskOpen,AskHigh,AskLow,AskClose,Volume,Open,High,Low,Close,Median,ao,ac,jaw,teeth,lips,bjaw,bteeth,blips,tjaw,tteeth,tlips,fh,fl,fh3,fl3,fh5,fl5,fh8,fl8,fh13,fl13,fh21,fl21,fh34,fl34,fh55,fl55,fh89,fl89,mfi,fdbb,fdbs,fdb,aoaz,aobz,zlc,zlcb,zlcs,zcol,zone_sig,sz,bz,acs,acb,ss,sb,price_peak_above,price_peak_bellow,ao_peak_above,ao_peak_bellow,mfi_sq,mfi_green,mfi_fade,mfi_fake,mfi_sig,mfi_str,price_peak_above_M1,price_peak_bellow_M1,ao_peak_above_M1,ao_peak_bellow_M1,price_peak_above_W1,price_peak_bellow_W1,ao_peak_above_W1,ao_peak_bellow_W1,target,vaosc,vaobc,vaoc
```

```
-------JTC Processing : SPX500_D1
                                 jgtml is using ttf....
   Read TTF:  /var/lib/jgt/full/data/ttf/SPX500_D1_mfizone.csv
INFO::Columns list from higher TF: ['mfi_sig', 'zone_sig']
>   We would use that to filter the columns and get our training data out of this refactored module (JTC.py)  -or shall I say from prototype to production/new module.  -> OUTPUT:  Training Data and Reality Data with which we would predict using our model.
Does these columns read from the source we would use to create the MXTarget data align with the input pattern mfizone: Index(['BidOpen', 'BidHigh', 'BidLow', 'BidClose', 'AskOpen', 'AskHigh',
       'AskLow', 'AskClose', 'Volume', 'Open', 'High', 'Low', 'Close',
       'Median', 'ao', 'ac', 'jaw', 'teeth', 'lips', 'bjaw', 'bteeth', 'blips',
       'tjaw', 'tteeth', 'tlips', 'fh', 'fl', 'fh3', 'fl3', 'fh5', 'fl5',
       'fh8', 'fl8', 'fh13', 'fl13', 'fh21', 'fl21', 'fh34', 'fl34', 'fh55',
       'fl55', 'fh89', 'fl89', 'mfi', 'fdbb', 'fdbs', 'fdb', 'aoaz', 'aobz',
       'zlc', 'zlcb', 'zlcs', 'zcol', 'zone_sig', 'sz', 'bz', 'acs', 'acb',
       'ss', 'sb', 'price_peak_above', 'price_peak_bellow', 'ao_peak_above',
       'ao_peak_bellow', 'mfi_sq', 'mfi_green', 'mfi_fade', 'mfi_fake',
       'mfi_sig', 'mfi_str', 'mfi_sig_M1', 'zone_sig_M1', 'mfi_sig_W1',
       'zone_sig_W1'],
      dtype='object')
INFO::Saving MX Target data to file...
Saved to /var/lib/jgt/full/data/targets/mx/SPX500_D1_mfizone_sel.csv
INFO::Saved to /var/lib/jgt/full/data/targets/mx/SPX500_D1_mfizone_tnd.csv
INFO::Saved to /var/lib/jgt/full/data/targets/mx/SPX500_D1_mfizone.csv

```
> # We sounds great !

```
Date,BidOpen,BidHigh,BidLow,BidClose,AskOpen,AskHigh,AskLow,AskClose,Volume,Open,High,Low,Close,Median,ao,ac,jaw,teeth,lips,bjaw,bteeth,blips,tjaw,tteeth,tlips,fh,fl,fh3,fl3,fh5,fl5,fh8,fl8,fh13,fl13,fh21,fl21,fh34,fl34,fh55,fl55,fh89,fl89,mfi,fdbb,fdbs,fdb,aoaz,aobz,zlc,zlcb,zlcs,zcol,zone_sig,sz,bz,acs,acb,ss,sb,price_peak_above,price_peak_bellow,ao_peak_above,ao_peak_bellow,mfi_sq,mfi_green,mfi_fade,mfi_fake,mfi_sig,mfi_str,mfi_sig_M1,zone_sig_M1,mfi_sig_W1,zone_sig_W1,target,vaosc,vaobc,vaoc
```
----

# What is the next step ??

>python jgtml/mlfcli.py -i $i -t $t -fr --full -pn  >> /a/src/_jgt/jgtml/mlfcli-pattern-test.md

```sh
i=SPX500;t=D1
python jgtml/ptojgtmlttfprotocli.py -i $i -t $t --full -fr -clh fh fl fh3 fl3 fh5 fl5 fh8 fl8 fh13 fl13 -pn frac013
```

# Refactorization of the JTC.py toward receiving an input Dataset with lags and all that is required to create the FDB_TARGETS

```



```

