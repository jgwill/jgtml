. $HOME/.bashrc &>/dev/null
#. data/scripts/_fnml.sh

# Detect available tools
if command -v conda >/dev/null 2>&1; then
    HAVE_CONDA=1
else
    HAVE_CONDA=0
fi

TIMEFRAMES="D1 H4"
if [ "$1" != "" ];then
    TIMEFRAMES="$1"
fi

INSTRUMENTS="SPX500 EUR/USD"
if [ "$2" != "" ];then
    INSTRUMENTS="$2"
fi

PATTERNS_BEING_EXPLORED="mfi zonesq aoac" #see:  $HOME/.jgt/settings.json for the property "patterns"
# #Ex. settings.json
#  "patterns": {
#     "mfi": {
#       "columns": [
#         "mfi_sq",
#         "mfi_green",
#         "mfi_fade",
#         "mfi_fake"
#       ]
#     },
#     "zonesq": {
#       "columns": [
#         "zone_sig",
#         "mfi_sq"
#       ]
#     },
#     "aoabz": {
#       "columns": [
#         "aoaz",
#         "aobz"
#       ]
#     },
#     "aoac": {
#       "columns": [
#         "ao",
#         "ac"
#       ]
#     },
#     "ttf": {
#       "columns": [
#         "mfi_sig",
#         "zone_sig"
#       ]
#     }
#   },
#   ...
#. /workspace/i/_fnml.sh

COMMIT_ACTIVATE=0
ENVIRONMENT_NAME=lab

#That would make this script runnable into the production environment.
if [ "$ENVIRONMENT_NAME" == "prod" ] ;then
    export RUN_DIRECTORY=.
    if [ $HAVE_CONDA -eq 1 ]; then
        conda activate i || echo "warning: can't activate env i"
    else
        echo "conda not found; using system Python"
    fi
    export JGTPY_DATA=/workspace/data/current
    export JGTPY_DATA_FULL=/workspace/data/full
    export mlfcli_command="mlfcli"
    export jgtmlcli_command="jgtmlcli"
fi

#Insure we run current code into our repository sources.  Agents should understand that this is a way to run and learn about these commands into current codebase
if [ "$ENVIRONMENT_NAME" == "lab" ] ;then
    if [ $HAVE_CONDA -eq 1 ]; then
        conda activate jgtml || echo "warning: can't activate env jgtml"
    else
        echo "conda not found; using system Python"
    fi
    if [ -d /src/jgtml ]; then
        export RUN_DIRECTORY=/src/jgtml
    else
        export RUN_DIRECTORY="$(git rev-parse --show-toplevel)"
    fi
    export JGTPY_DATA="$RUN_DIRECTORY/data/current"
    export JGTPY_DATA_FULL="$RUN_DIRECTORY/data/full"
    export mlfcli_command="python jgtml/mlfcli.py"
    export jgtmlcli_command="python jgtml/jgtmlcli.py"
fi

LOG_DIR="$RUN_DIRECTORY/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y%m%d%H%M%S)_batch.log"

#fdbscan > _fdbscan.sh &
USE_FULL=0
EXTRA_ARG=""
if [ "$USE_FULL" -eq 1 ];then
    EXTRA_ARG="--full"
fi

cd $RUN_DIRECTORY #so we run this where we are in prod and in the codebase in lab environment.
for p in $PATTERNS_BEING_EXPLORED;do
    echo "# Pattern: $p" | tee -a $LOG_FILE
    
    for t in $TIMEFRAMES;do 
        for i in $INSTRUMENTS;do 
            echo "# $i $t" | tee -a $LOG_FILE
            echo "$mlfcli_command -i $i -t $t -pn $p  $EXTRA_ARG" | tee -a $LOG_FILE
            $mlfcli_command -i $i -t $t -pn $p  $EXTRA_ARG  |tee -a $LOG_FILE

            echo "$jgtmlcli_command -i $i -t $t -pn $p $EXTRA_ARG" | tee -a $LOG_FILE
            $jgtmlcli_command -i $i -t $t -pn $p $EXTRA_ARG |tee -a $LOG_FILE


            
        if [ $COMMIT_ACTIVATE -eq 0 ];then
            continue
        fi
        #git add batch.log &>/dev/null
            #git commit batch.log -m "done $i $t"&>/dev/null
            #git push &>/dev/null
        done
    done
done

