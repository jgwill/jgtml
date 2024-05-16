for i in $(echo $I|tr "," " ");do for t in H4 D1;do python jgtml/jgtmlcli.py -i $i -t $t --full -mfi -ba -rcds;done;done

