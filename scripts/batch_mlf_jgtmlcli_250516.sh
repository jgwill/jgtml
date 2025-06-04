. $HOME/.bashrc &>/dev/null
#. data/scripts/_fnml.sh

conda activate i

. /workspace/i/_fnml.sh
export JGTPY_DATA=/workspace/data/current
export JGTPY_DATA_FULL=/workspace/data/full

COMMIT_ACTIVATE=0

#fdbscan > _fdbscan.sh &


for t in H4 H1 m15;do 
    for i in $II;do 
        echo "# $i $t" | tee -a batch.log
        mlfcli -i $i -t $t --full -pn mfi |tee -a batch.log
        jgtmlcli -i $i -t $t --full -pn mfi|tee -a batch.log
        
	if [ $COMMIT_ACTIVATE -eq 0 ];then
	    continue
	fi
	#git add batch.log &>/dev/null
        #git commit batch.log -m "done $i $t"&>/dev/null
        #git push &>/dev/null
    done
done
