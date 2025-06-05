#!/bin/bash
# This file is used to define functions that are used in the JGTML (Jean Guillaume's Trading Machine Learning) project.  It assist now in wrapping the various command line tools in workflows.

# This file is meant to be sourced in the shell, so that the functions are available in the shell.  It is not meant to be executed directly.


#ttf_patterns=$(jgtset|jq '.ttf2run[]'||echo "ttf mfi")


if [ -e "/opt/anaconda3/bin/conda" ];then

	__conda_setup="$('/opt/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
	if [ $? -eq 0 ]; then
			eval "$__conda_setup"
	else
			if [ -f "/opt/anaconda3/etc/profile.d/conda.sh" ]; then
					# shellcheck disable=SC1091
					. "/opt/anaconda3/etc/profile.d/conda.sh"&>/dev/null
			else
					export PATH="/opt/anaconda3/bin:$PATH"
			fi
	fi
	unset __conda_setup
fi

# WATCH OUT BELLOW BECAUSE IT WILL ACTIVATE ENV that are not with the latest codebase.
#TODO : Think of making a new script like that one that we can run within the repository during development.
conda activate i||conda activate hfsp_basjupyterlab2406&>/dev/null || conda activate "$CONDA_ENV_PROD"&>/dev/null || conda activate i || echo "Assuming Conda Environment is already set"
#conda activate jgtml
ttf_patterns=$(jgtset|jq '.ttf2run[]'||echo "ttf mfi")



__functionusage__=' 
# Refresh the CDS for an instrument and timeframe
	jgtml_prep_cds_05 <instrument> <timeframe> 
# Refresh the TTF for an instrument and timeframe
	jgtml_prep_ttf_10_all_patterns_for_instrument_timeframe <instrument> <timeframe>
# Refresh the MX
	jgtml_post_mx_15 <instrument> <timeframe>     
# Refresh TTF preparation for an instrument
	jgtml_wf_ttf_prep_by_instrument_19 instrument <instrument> 
# Calculate the MX for an instrument
	jgtml_wf_mx_by_instrument_20 <instrument>
# Run for all instruments in I variable
	jgtml_wf_mx_all_20    
#run the unified alligator CLI (replaces legacy pto tidealligator)
	jgtml_ptojgtmltidealligator_by_instrument_tf_21 <instrument> <timeframe> <buysell>
	# RECOMMENDED: python -m jgtml.alligator_cli -i <instrument> -t <timeframe> -d <direction> --type <tide|big|regular|all>
# Run the jgtmlfcli for an instrument and timeframe
	jgtmlf_exec_by_instrument_tf_22 <instrument> <timeframe> 
	'

__usage()
{
	echo "Usage: $0 [all|instrument]"
	echo "  all: Run for all instruments"
	echo "  instrument: Run for a specific instrument"
	echo " OR Functions gets loaded and can be called directly"
	echo "$__functionusage__"
}


jgtml_setup_00_user()
{
	conda activate baseprod || conda activate base || echo "Conda env baseprod or base not found.  We will try anyway...."
	pip install --user -U jgtfxcon jgtfx2console jgtutils
}

jgtml_setup_00_current()
{
	conda activate baseprod || conda activate base || echo "Conda env baseprod or base not found.  We will try anyway...."
	pip install -U jgtfxcon jgtfx2console jgtutils
}

_jgtfxcli_execute_by_instrument_and_timeframe()
{
	local _i=$1
	if [ "$_i" == "" ];then echo "Instrument is required jgtfxcli";return;fi
	local _t=$2
	if [ "$_t" == "" ];then echo "Timeframe is required jgtfxcli";return;fi
	local _xarg4="--full" #@STCGoal Futur support for notfull for normal inferences
	jgtfxcli -i $_i -t $_t $_xarg4

}

# 01 Refresh the PDS full for an instrument and timeframe
jgtml_prep_pds_01()
{
	local _i=$1
	if [ "$_i" == "" ];then echo "Instrument is required jgtml_prep_pds_01";return;fi
	local _t=$2
	if [ "$_t" == "" ];then echo "Timeframe is required" jgtml_prep_pds_01;return;fi

	_jgtfxcli_execute_by_instrument_and_timeframe $_i $_t

}

_jgtcli_execute_by_instrument_and_timeframe()
{
	local _i=$1
	if [ "$_i" == "" ];then echo "Instrument is required";return;fi
	local _t=$2
	if [ "$_t" == "" ];then echo "Timeframe is required";return;fi
	local _fresh="$3"
	local _xarg3="" 
	if [ "$_fresh" == "fresh" ];then 
		_xarg3="--fresh"
		echo "Freshening the dependent data for CDS $_i $_t, hopefully"
	fi
	local _xarg4="--full" #@STCGoal Futur support for notfull for normal inferences

	jgtcli -i $_i -t $_t  $_xarg3 $_xarg4

}


# 05 Refresh the   CDS
jgtml_prep_cds_05()
{
	local _i=$1
	if [ "$_i" == "" ];then echo "Instrument is required jgtml_prep_cds_05";return;fi
	local _t=$2
	if [ "$_t" == "" ];then echo "Timeframe is required jgtml_prep_cds_05";return;fi

	local _fresh="$3"
	# if [ "$_fresh" == "fresh" ];then
	# 	echo "Freshening the dependent data for CDS $_i $_t, hopefully"
	#   jgtml_prep_pds_01 $_i $_t
	# fi

	_jgtcli_execute_by_instrument_and_timeframe $_i $_t $_fresh

}

# 06 Refresh the   CDS from old PDS
jgtml_prep_cds_06_old()
{
	jgtcli -i $1 -t $2 --full -mfi -ba -ta -old

}

# 10 Refresh the TTF for an instrument and timeframe
jgtml_prep_ttf_10_all_patterns_for_instrument_timeframe()
{
	local _i=$1
	if [ "$_i" == "" ];then echo "Instrument is required";return;fi
	local _t=$2
	if [ "$_t" == "" ];then echo "Timeframe is required";return;fi
	local _refresh="$3"
	if [ "$_refresh" == "" ];then _refresh="norefresh";fi

	if [ "$_refresh" == "fresh" ];then
		echo "Freshening the dependent data for TTF (using prep_cds fresh): $_i $_t, hopefully"
		jgtml_prep_cds_05 "$_i" "$_t" fresh
	fi
	local _xarg3="-old"  #Data should be fresh so we can use old
	local _xarg4="--full" #@STCGoal Futur support for notfull for normal inferences
	for pn in $ttf_patterns;do 
		jgtmlttfcli -i $_i -t $_t  $_xarg3 $_xarg4 -pn $pn|| echo "jgtmlttfcli failed for pattern $pn"
	done

	#jgtmlttfcli -i $_i -t $_t  $_xarg3 $_xarg4  -pn mfi || echo "jgtmlttfcli failed for pattern mfi"
	#jgtmlttfcli -i $_i -t $_t  $_xarg3 $_xarg4 -pn 
	#jgtmlttfcli -i $_i -t $_t  $_xarg3 $_xarg4 -clh price_peak_above price_peak_bellow ao_peak_above ao_peak_bellow mfi_sig -pn peaksmfi
	#jgtmlttfcli -i $_i -t $_t  $_xarg3 $_xarg4 -clh price_peak_above price_peak_bellow ao_peak_above ao_peak_bellow -pn peaks
	#jgtmlttfcli -i $_i -t $_t  $_xarg3 $_xarg4 -clh ao ac -pn aoac
}

# 15 Refresh the MX (using the TTF) for an instrument and timeframe
jgtml_post_mx_15()
{
	if [ "$1" == "" ];then echo "Instrument is required";return;fi
	if [ "$2" == "" ];then echo "Timeframe is required";return;fi
	
	for pn in $ttf_patterns;do 
		jgtmlcli -i $1 -t $2  -old -pn $pn || echo "jgtmlcli failed for pattern ttf"
	done
	#jgtmlcli -i $1 -t $2  -old -pn mfi || echo "jgtmlcli failed for pattern mfi"
	# jgtmlcli -i $1 -t $2 -ba -ta -old -pn peaks
	# jgtmlcli -i $1 -t $2 -ba -ta -old -pn peaksmfi
	# jgtmlcli -i $1 -t $2 -ba -ta -old -pn aoac

}

# 19 Refresh TTF preparation for an instrument (timeframes are predefined)
jgtml_wf_ttf_prep_by_instrument_19()
{
	local _i=$1

	local _refresh="$2"
	if [ "$_refresh" == "" ];then _refresh="norefresh";fi

	local _timeframes="D1"
	local _higher_tf="M1 W1 "

	if [ "$3" != "" ];then _timeframes="$3";fi
	if [ "$4" != "" ];then _higher_tf="$4";fi



	if [ "$_i" == "" ];then echo "Instrument is required jgtml_wf_ttf_prep_by_instrument_19";echo "Usage:jgtml_wf_ttf_prep_by_instrument_19 <instrument> <refresh> <timeframes>";return;fi
	
	echo "TTF for:$_i... $_refresh...$_higher_tf$_timeframes..."
	for _t in $_higher_tf$_timeframes;do
					if [ "$NOUP" != "1" ];then 
					  echo "jgtml_wf_ttf_prep_by_instrument_19 is callingjgtml_prep_cds_05 with  -> i:$_i, t:$_t"
						jgtml_prep_cds_05 "$_i" "$_t" "$_refresh"
					fi

	done
	echo " ## We have created all required CDS for $_i $2"
	
	echo " ## Creating TTF and them MX for desired TF $2"
	for _t in $_timeframes;do
					echo "jgtml_wf_ttf_prep_by_instrument_19::Preping TTf for: $_i  $_t"
					jgtml_prep_ttf_10_all_patterns_for_instrument_timeframe "$_i" "$_t"
	done
	echo "------TTF------------------$_i------$_refresh------done"
}

# 20 Calculate the MX for instruments defined in I
jgtml_wf_ttf_prep_all_19()
{
	for _i in $(echo "$I"|tr "," " ");do 
		jgtml_wf_ttf_prep_by_instrument_19 $_i $2
	done
}

# 20 Calculate the MX for an instrument (timeframes are predefined)
jgtml_wf_mx_by_instrument_20()
{
	local _i="$1"
	local _refresh="$2"
	if [ "$_refresh" == "" ];then _refresh="norefresh";fi

	local _timeframes="D1"
	local _higher_tf="M1 W1 "
	if [ "$3" != "" ];then _timeframes="$3";fi
	if [ "$4" != "" ];then _higher_tf="$4";fi
	if [ "$_i" == "" ];then echo "Instrument is required";echo "USage:jgtml_wf_mx_by_instrument_20 <instrument> <timeframes> <refresh> ";return;fi

	echo "jgtml_wf_mx_by_instrument_20 for i:$_i"
	jgtml_wf_ttf_prep_by_instrument_19 "$_i" "$_refresh" "$_higher_tf$_timeframes"
	# for t in M1 W1 D1 H4;do

	#         if [ "$NOUP" != "1" ];then 
	# 					jgtml_prep_cds_05 $_i $t $2
	# 				fi

	# done
	# echo " ## We have created all required CDS for $_i"
	
	echo " ##  Creating MX for desired TF of instrument:$_i"
	for _t in $_timeframes;do
					echo "  $_t"
					#jgtml_prep_ttf_10_all_patterns_for_instrument_timeframe $_i $t
					#
					jgtml_post_mx_15 "$_i" "$_t"
	done
	echo "---------$_i----jgtml_wf_mx_by_instrument_20--------done"
}


# 20 Calculate the MX for all instruments defined in I

# shellcheck disable=SC2120
jgtml_wf_mx_all_20()
{
	local _refresh="$2"
	if [ "$_refresh" == "" ];then _refresh="norefresh";fi

	local _timeframes="D1 H4"
	for _i in $(echo "$I"|tr "," " ");do 
		jgtml_wf_mx_by_instrument_20 "$_i" "$_refresh" "$_timeframes"
	done
}

ttfmxwf()
{
	(for _i in $(echo "$I"|tr "," " ");do echo "$_i";jgtapp ttfmxwf -i "$_i";done)&
}

# 21 Run the unified alligator CLI for an instrument, timeframe and buysell (DEPRECATED - Use python -m jgtml.alligator_cli)
jgtml_ptojgtmltidealligator_by_instrument_tf_21()
{
	echo "⚠️  DEPRECATED: jgtml_ptojgtmltidealligator_by_instrument_tf_21"
	echo "    Use: python -m jgtml.alligator_cli -i $1 -t $2 -d $3 --type tide"
	python -m jgtml.alligator_cli -i $1 -t $2 -d $3 --type tide --quiet
}

jgtmlf_exec_by_instrument_tf_22()
{
	local _i=$1
	local _t=$2
	#@STCIssue THAT IS WHERE WE ARE IN NEED TO UPGRADE THE CLI
	if [ "$_i" == "" ];then echo "Instrument is required";return;fi
	if [ "$_t" == "" ];then echo "Timeframe is required";return;fi
	local _fresh="$3"
	local _xarg3="--fresh"
	if [ "$_fresh" == "" ];then 
		_fresh="norefresh"
		_xarg3=""
		echo "MLF not refreshing, assuming its fresh already"
	fi
	local _xarg4="--full" #@STCGoal Futur support for notfull for normal inferences
	for pn in $ttf_patterns;do 
		jgtmlfcli -i $_i -t $_t $_xarg4 $_xarg3  -pn "$pn"
	done


}

jgtmlf_wf_by_instrument_tf_22()
{
	local _i="$1"
	local _refresh="$2"
	if [ "$_refresh" == "" ];then _refresh="norefresh";fi

	local _timeframes="D1"
	if [ "$3" != "" ];then _timeframes="$3";fi


	if [ "$_i" == "" ];then echo "Instrument is required";echo "Usage:jgtmlf_wf_by_instrument_tf_22 <instrument> <refresh> <timeframes> <pattern>";return;fi

	#@STCIssue Incoherence to run MX before MLF (we would need to run MLF before MX and various pattern in MX could be used with the actual MLF Pattern)
	for _t in $_timeframes;do
		jgtmlf_exec_by_instrument_tf_22 "$_i" "$_t" 
	done

	jgtml_wf_mx_by_instrument_20 "$_i" "$_refresh" "$_timeframes"
}


jgtmlf_exec_all_22()
{
	local _refresh="$1"
	if [ "$_refresh" == "" ];then _refresh="norefresh";fi

	local _timeframes="D1"
	if [ "$2" != "" ];then _timeframes="$2";fi

	for _i in $(echo "$I"|tr "," " ");do 
		jgtmlf_wf_by_instrument_tf_22 "$_i" "$_refresh" "$_timeframes"
	done

}

# Relative to JGT file manipulation
i2fn()
{
        local _i="$1"
        local ifn=${_i//\//-}
        echo $_ifn
}

topovfn()
{
        local _i="$1"
        local _t="$2"
        local ifn=${_i//\//-}
        local sep="_"
        if [ "$2" == "" ];then sep="";fi

        echo $ifn"$sep"$_t$3
}

# tojgtpy_data_path()
# {
# 				local _i="$1"
# 				local _t="$2"
# 				local ifn=${_i//\//-}
# 				local sep="_"
# 				if [ "$2" == "" ];then sep="";fi
# 				local data_path=$JGTPY_DATA_FULL

# 				echo $_data_path/$_ifn"$sep"$_t$3

# }

# SOME UTILITIES such as tail the full PDS/CDS/TTF/MX data for an instrument and its timeframe
jgtml_hail_pds_99()
{
	local _pov=$(topovfn $1 $2)
	local data_path=$JGTPY_DATA_FULL
	if [ "$3" != "" ];then data_path=$3;fi
	local _fp=$data_path'/pds/'$_pov'.csv'
	echo "$_fp"
	if [ -e $_fp ];then
	  head -n 1 $_fp
		tail -n 1 $_fp
	fi
}

jgtml_hail_cds_99()
{
	local _pov=$(topovfn $1 $2)
	local data_path=$JGTPY_DATA_FULL
	if [ "$3" != "" ];then data_path=$3;fi
	local _fp=$data_path'/cds/'$_pov'.csv'
	echo "$_fp"
	if [ -e $_fp ];then
	  head -n 1 $_fp
		tail -n 1 $_fp
	fi
}

jgtml_hail_ttf_99()
{
	local _pov=$(topovfn $1 $2)
	local data_path=$JGTPY_DATA_FULL
	if [ "$3" != "" ];then data_path=$3;fi
	local _fp=$data_path'/ttf/'$_pov'_ttf.csv'
	echo "$_fp"
	if [ -e $_fp ];then
	  head -n 1 $_fp
		tail -n 1 $_fp
	fi

}

jgtml_hail_mx_99()
{
	local _pov=$(topovfn $1 $2)
	local data_path=$JGTPY_DATA_FULL
	if [ "$3" != "" ];then data_path=$3;fi
	local _fp=$data_path'/targets/mx/'$_pov'.csv'
	echo "$_fp"
	if [ -e $_fp ];then
	  head -n 1 $_fp
		tail -n 1 $_fp
	fi
}

jgtml_hail_all()
{
	local _pov=$(topovfn $1 $2)
	echo "pov:$_pov"
	local data_path=$JGTPY_DATA_FULL
	if [ "$3" != "" ];then data_path=$3;fi
	echo "PDS"
	jgtml_hail_pds_99 $1 $2 $data_path
	echo "CDS"
	jgtml_hail_cds_99 $1 $2 $data_path
	echo "TTF"
	jgtml_hail_ttf_99 $1 $2 $data_path
	echo "MX"
	jgtml_hail_mx_99 $1 $2 $data_path

}







# Usage with --help or -h
if [ "$1" == "--help" ] || [ "$1" == "-h" ];then
	__usage
else 

	if [ "$1" == "all" ];then
		jgtml_wf_mx_all_20
	else
		# if $1 is not all and has a value, we assume it is an instrument
		if [ "$1" != "" ];then
			echo "Running for $1"
			jgtml_wf_mx_by_instrument_20 $1

		fi
	fi
fi



echo "jgtml.sh sourced"
