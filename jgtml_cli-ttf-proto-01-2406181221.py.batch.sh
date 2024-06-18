for i in $(echo $I|tr "," " ");do 
  for t in D1;do 
    python jgtml_cli-ttf-proto-01-2406181221.py -i $i -t $t --full --fresh
  done
done
