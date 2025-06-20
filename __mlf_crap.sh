
unset JGTPY_DATA_FULL
unset JGTPY_DATA
. .env|| true
export JGTPY_DATA
export JGTPY_DATA_FULL

pattern=mz
for i in  EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD;do for t in D1;do mlfcli -i $i -t $t -pn $pattern -uf;done;done
