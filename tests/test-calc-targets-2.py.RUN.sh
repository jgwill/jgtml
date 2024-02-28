
TCONDA_ENV=jgtml-tests

CURR_CONDA_ENV=$(conda info | awk '/active environment/{print $4}')
if [ "$CURR_CONDA_ENV" != "$TCONDA_ENV" ];then conda activate $TCONDA_ENV;echo "Conda env $TCONDA_ENV Activated";fi


export I="XAU/USD"
export I="GBP/USD"
export I="SPX500,GBP/USD,EUR/USD,USD/CAD,AUD/USD"
export I="SPX500,XAU/USD,EUR/USD,USD/CAD,AUD/USD,GBP/USD"
export I="SPX500"

export T="D1"
export T="D1,H4,H1"
export T="W1,H1"
export T="D1,H4,W1,H1"
export T="W1,D1,H4"
export T="H2,H1"
export T="D1,H4"
export T="D1"

#export T="D1,H4,W1,H1"

#export T="H1"

# Path: calculate_target_variable_mx_as_cli-transforming.py


python test-calc-targets-2.py
