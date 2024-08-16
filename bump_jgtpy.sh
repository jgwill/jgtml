


# This wont be run by post_dist rather its just a flag to run _bump_jgtpy function




oldjgtpyversion=$(cat pyproject.toml|grep "jgtpy"|tr '>' ' '|tr "'" " "|tr "=" " "|tr "," " "|awk '{print $2}')
. .env 
(conda activate $WS_CONDA_ENV_NAME&>/dev/null;pip install -U jgtpy|tr '(' ' '|tr ')' ' '|grep "jgtpy in"|awk '/jgtpy/{print $7}')
newjgtpyversion=$(conda activate $WS_CONDA_ENV_NAME&>/dev/null;pip install -U jgtpy|tr '(' ' '|tr ')' ' '|grep "jgtpy in"|awk '/jgtpy/{print $7}')

# We want to replace jgtpy>=0.4.70 with jgtpy>=0.4.71
## run if they are different
if [ "$oldjgtpyversion" == "$newjgtpyversion" ]; then
    echo "No need to update jgtpy version in $WS_CONDA_ENV_NAME package/env"
else

	sed -i "s/jgtpy>=$oldjgtpyversion/jgtpy>=$newjgtpyversion/g" pyproject.toml
	git add pyproject.toml
	git commit -m "auto bump:jgtpy  $oldjgtpyversion to $newjgtpyversion"
fi

if [ "$1" == "dev" ]; then
	echo "dev mode"
	make dev-release-plus && \
		(sleep 25;conda activate jgtsd && pip install -U jgtml) &>/dev/null&
fi
#(conda activate jgtsd && pip install -U jgtpy) &>/dev/null
