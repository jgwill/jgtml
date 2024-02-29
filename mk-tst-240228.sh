
cversion="0.0.24"
i=SPX500
i="GBP/USD"
ifn="$(topovfn $i)"
t="D1,H4"
if [ "$1" == "update" ];then 
  echo "Updating Fresh price and generating indicators for $i $t"
  jgtfxcli -i "$i" -t "$t" --full;jgtcli -i "$i" -t "$t" --full

fi

make dist && (cd tests;conda activate jgtml-tests;pip uninstall jgtml -y;pip install /a/src/_jgt/jgtml/dist/jgtml-$cversion-py3-none-any.whl;./test-calc-targets-2.py.RUN.sh "$i" "$t";cp $JGTPY_DATA_FULL'/targets/mx/'$ifn'_D1'* /b/Dropbox/jgt/drop/build/;cp $JGTPY_DATA_FULL'/targets/mx/'$ifn'_H4'* /b/Dropbox/jgt/drop/build;mkdir -p /b/Dropbox/jgt/drop/build/pds;cp $JGTPY_DATA_FULL'/pds/'$ifn'_D1'* /b/Dropbox/jgt/drop/build/pds;cp /var/lib/jgt/full/data/pds/SPX500_H4* /b/Dropbox/jgt/drop/build/pds;mkdir -p /b/Dropbox/jgt/drop/build/cds;cp /var/lib/jgt/full/data/cds/SPX500_* /b/Dropbox/jgt/drop/build/cds;cp /var/lib/jgt/full/data/targets/mx/GBP-USD_D1* /b/Dropbox/jgt/drop/build/;cp /var/lib/jgt/full/data/targets/mx/GBP-USD_H4* /b/Dropbox/jgt/drop/build;mkdir -p /b/Dropbox/jgt/drop/build/pds;cp /var/lib/jgt/full/data/pds/GBP-USD_D1* /b/Dropbox/jgt/drop/build/pds;cp /var/lib/jgt/full/data/pds/GBP-USD_H4* /b/Dropbox/jgt/drop/build/pds;mkdir -p /b/Dropbox/jgt/drop/build/cds;cp /var/lib/jgt/full/data/cds/GBP-USD_* /b/Dropbox/jgt/drop/build/cds)
