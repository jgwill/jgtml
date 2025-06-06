# TTFCLI Patterns Investigation

This report documents attempts to generate TTF pattern CSVs using `jgtml/ttfcli.py` for instrument **SPX500** and timeframe **H4**. Patterns were determined from `$HOME/.jgt/settings.json`.

## Patterns Tested
- mfi
- zonesq
- aoabz
- aoac
- ttf

## Command Template
```
python jgtml/ttfcli.py -i SPX500 -t H4 -pn <pattern> --json
```

## Observations
All commands failed with repeated `ORA-499` login errors from **ForexConnect**. The CLI attempted to read or generate CDS data and then aborted with `TypeError: object of type 'NoneType' has no len()`. No CSV output was created.

Example snippet from `ttfcli_mfi.log`:
```
TTF Columns : ['mfi_sq', 'mfi_green', 'mfi_fade', 'mfi_fake']
ERROR:root:Exception: ORA-499: Unable to obtain station descriptor. HTTP request failed object='/Hosts.jsp?ID=1749246897482&PN=Real&SN=ForexConnect&MV=5&LN=6700006491&AT=PLAIN' errorCode=60
Traceback (most recent call last):
  File "/root/.pyenv/versions/3.10.17/lib/python3.10/site-packages/jgtfxcon/jgtfxc.py", line 94, in login_forexconnect
    fx.login(user_id=user_id,password=password,url=url,connection=connection, pin="", session_id="", session_status_callback=jgtfxcommon.session_status_changed)
```

## Recommendations
1. **Provide Offline Sample Data**
   - Include pre-generated CDS/TTF files under `samples/` so CLI can be exercised without live credentials.
2. **Mock or Stub ForexConnect**
   - Implement a mock login layer or fallback mode to avoid `ORA-499` when network credentials are unavailable.
3. **Feature Exploration**
   - Once data is generated, clustering algorithms (e.g., K-Means, DBSCAN) could group TTF patterns by similarity. Results may feed supervised models for predictive trading decisions.

Further ML experiments depend on obtaining valid TTF output. The next step is to ensure offline execution paths.
