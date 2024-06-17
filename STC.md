
## 2406171357

| sig_namespace | title | notes | refacto |
| --- | --- | --- | --- | 
| mouth_is_open | Regular Mouth is Open | | sig_mouth_is_open |
| not_in_lips_teeth | Signal not in Mouth | Signal not in regular Mouth (lips/teeth) | sig_not_in_mouth |
| sig_is_in_bteeth_sum | | | sig_is_in_bteeth_sum |
| sig_in_blips_bmouth_is_open | | | sig_bmopen_in_blips_sum |
| big_m_open_in_bteeth_sum | | | sig_bmopen_in_bteeth_sum |

### REVIEW
* All Big Alligator signals are based on the 'mouth_is_open'/'not_in_lips_teeth' which is ok but we might want a variation where the signal is not in the Mouth but the 'Mouth is Not open' (the marker oscillate on that timeframe).

### Desired result points
* mfi signals
* tide alligator filtering (reproduce experimentation of the big alligator) -> --@STCGoal Insights of Larger Timeframes 

### CDS Data Refresh
```sh
for t in H4 D1 W1 M1;do jgtcli -i SPX500 -t $t --full -ta -ba -mfi;done
```

#### Files

```sh
pip uninstall jgtpy -y ;pip install  /a/src/_jgt/ids/dist/jgtpy-0.4.53-py3-none-any.whl
```


