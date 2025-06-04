

BDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# the fdbscan_wtf.sh would scan twice the m5 then we would come back here after 
##  First scan the m15
## Immediate scan of m5 after m15
## Internal run of wtf -t m5 -N -X -> another fdbscan -t m5 -v 2
#fdbscan_m15_m5.sh
t=H4
log_info "Scanning $t once now then WTF Proto starts for tf=$t"
sleep 1
. $BDIR/fdbscan_WTF_240902.sh $t 

#log_info "First FDBSCAN of $t done, now WTF Proto starts for tf=$t"
wtf -t $t -N -S fdbscan_WTF_240902.sh
