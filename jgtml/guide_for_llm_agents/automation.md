# Automation Overview

The dataset automation flow generates TTF and MLF pattern files using existing
CDS data. It is useful when you cannot connect to the broker API but still want
to refresh machine learning datasets.

1. Ensure `data/full/cds` contains CSVs produced by `jgtpy` or prior runs.
2. Invoke `ttfcli` and `mlfcli` to process D1 data for the instruments you care
   about. Run jobs in parallel to speed up generation.
3. Resulting pattern files appear under `data/full/ttf` and `data/full/mlf`.

Set `JGTPY_DATA_FULL` to the root of your dataset directory if it differs from
`data/full`. A helper script, `scripts/generate_ttf_mlf_d1.sh`, invokes `ttfcli`
and `mlfcli` for common instruments. It runs jobs in parallel, focusing on the
D1 timeframe so you can rebuild patterns offline.

> **Note**: A helper script exists to orchestrate these calls, but automation is
> still evolving. This section will expand once the workflow stabilizes.
