. /opt/binscripts/load.sh

LOG_FILE=/var/log/jgt/fdbscan.log
LOG_ENABLED=y

#v=$2
#if [ -z $v ]; then
#	v=0
#fi
v=""
n="-N"

# That one RUNS EVERY Input Timeframe which later runs every sub timeframes.
if [ "$1" != "" ]; then
    log_info "Running FDB Scan for $1"
    #fdbscan -t $1 $v  && log_info "FDB Scan completed for $1" || log_error "FDB Scan failed for $1"
else
	echo "No Timeframe supplied, assuming you just want to load functions"
	echo "Here are the functions you can use:"
	echo "------------------"
	echo "fdbscan_m5"
	echo "fdbscan_m15"
	echo "fdbscan_H1"
	echo "fdbscan_H4"
	echo "------------------"
	echo "wtf_m5x"
	echo "wtf_m15x"
	echo "wtf_H1x"
	echo "wtf_H4x"
	echo "------------------"
	echo "__m15_m5_wtf_seq"
	echo "__H1_m15_m5_seq"
	echo "__H4_H1_m15_m5_seq"
	echo "------------------"

fi

fdbscan_m5()
{
	LOG_FILE=/var/log/jgt/fdbscan.log
	if [ "$NOm5" == "" ];then
		fdbscan -t m5 $v  && log_info "FDB Scan completed for m5" || log_error "FDB Scan failed for m5 $@"
	else
		log_info "Skipping m5"
	fi
}
fdbscan_m15()
{
	LOG_FILE=/var/log/jgt/fdbscan.log
	if [ "$NOm15" == "" ];then
		fdbscan -t m15 $v  && log_info "FDB Scan completed for m15" || log_error "FDB Scan failed for m15 $@"
	else
		log_info "Skipping m15"
	fi
}
fdbscan_H1()
{
	LOG_FILE=/var/log/jgt/fdbscan.log
	if [ "$NOH1" == "" ];then
		fdbscan -t H1 $v && log_info "FDB Scan completed for H1" || log_error "FDB Scan failed for H1 $@"
	else
		log_info "Skipping H1"
	fi
}
fdbscan_H4()
{
	LOG_FILE=/var/log/jgt/fdbscan.log
	fdbscan -t H4 $v && log_info "FDB Scan completed for H4" || log_error "FDB Scan failed for H4 $@"
}

_wtf_m5x()
{
	LOG_FILE=/var/log/jgt/wtf.log
	wtf -t m5 -X $n  && log_info "WTF m5 arrived. Clean exit." || log_error "WTF failed for m5"
}
_wtf_m15x()
{
	LOG_FILE=/var/log/jgt/wtf.log
	wtf -t m15 -X $n  && log_info "WTF m15 arrived. Clean exit." || log_error "WTF failed for m15"
}
_wtf_H1x()
{
	LOG_FILE=/var/log/jgt/wtf.log
	wtf -t H1 -X $n  && log_info "WTF H1 arrived. Clean exit." || log_error "WTF failed for H1"
}
_wtf_H4x()
{
	LOG_FILE=/var/log/jgt/wtf.log
	wtf -t H4 -X $n  && log_info "WTF H4 arrived. Clean exit." || log_error "WTF failed for H4"
}

__m15_m5_wtf_seq() #wtf -t m15 -N -S fdbscan_m15_m5.sh
{
	LOG_FILE=/var/log/jgt/fdbscan.log
	log_info "Starting m15_m5_wtf_seq"
	# Scan m15 when this is called
	fdbscan_m15 $@ 
        # happens at :00,:15,:30,:45
        fdbscan_m5 $@ 
	
        #waits for :05,:20,:35,:50
        _wtf_m5x $@ 
        fdbscan_m5 $@ 
        #waits for :10,:25,:40,:55
        _wtf_m5x $@ 
        fdbscan_m5 $@ 
        #Then we are back to the wtf -t m15
	# Its 0:10 of the hour by then when we exit here
}

__H1_m15_m5_seq()
{
	LOG_FILE=/var/log/jgt/fdbscan.log
        log_info "Starting H1_m15_m5_seq"
	# Scan H1 when this is called
	fdbscan_H1 $@ 
	
	# m15,m5 sequence which scan now and wait loop to scan each of their periods until we are at 0:10
	__m15_m5_wtf_seq $@  #:10
	_wtf_m15x $@  # we should exit this at :15
	#Scan m15,m5 at :15 and m5 at :20,:25
	__m15_m5_wtf_seq $@  # we should be at 0:25 after this and scan m15,m5 

	_wtf_m15x $@  # we should exit this at :30
	#Scan m15,m5 at :30 and m5 at :35,:40
	__m15_m5_wtf_seq $@  # we should be at 0:40 after this and scan m15,m5

}

__H4_H1_m15_m5_seq()
{
	LOG_FILE=/var/log/jgt/fdbscan.log
        log_info "Starting H4_H1_m15_m5_seq"
	# Scan H4 when this is called
	fdbscan_H4 $@

	__H1_m15_m5_seq $@  #hopefully we go to next hour after this
	_wtf_H1x $@  # we should exit this at :00
	#Scan H1 at :00 and m15,m5 at :05,:10
	__H1_m15_m5_seq $@  # we should be an hour later
	_wtf_H1x $@  # we should exit this at :15
	#Scan H1 at :15 and m15,m5 at :20,:25
	__H1_m15_m5_seq $@  # we should be an hour later
}



if [ "$1" == "m15" ]; then
	LOG_FILE=/var/log/jgt/fdbscan.log
        log_info "Running FDB Scan Sequence for m15"
	#shift args
	shift 1
	__m15_m5_wtf_seq $@ 

fi

if [ "$1" == "H1" ]; then
	LOG_FILE=/var/log/jgt/fdbscan.log
        log_info "Running FDB Scan Sequence for H1"
	#shift args, we are not using the first arg
	shift 1
	__H1_m15_m5_seq $@ 
fi

if [ "$1" == "H4" ]; then
	LOG_FILE=/var/log/jgt/fdbscan.log
	log_info "Running FDB Scan Sequence for H4"
	#shift args, we are not using the first arg
	shift 1
	__H4_H1_m15_m5_seq $@ 
fi



 

