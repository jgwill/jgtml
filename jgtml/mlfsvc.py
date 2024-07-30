"""
@STCGoal Wrap what MLF does as Services

- Create MLF
- Read MLF (and create if doesn't exist and if we have a corresponding TTF PatternsData in the DB, we can also create the TTF)
- Update MLF
- Create TTF Patterns (data:  PatternName, PatternsColumns) 

Dependencies:
- MLFRequest
- TTF

Target Usage:
- mlfcli
- mlfapi
"""


import MLFRequest
import realityhelper


class MLFService:
    def generate_features(self, request: MLFRequest):
        try:
            return realityhelper.generate_mlf_feature_pattern(
                request.instrument,
                request.timeframe,
                use_full=request.use_full,
                force_refresh=request.force_refresh,
                lag_period=request.lag_period,
                total_lagging_periods=request.total_lagging_periods,
                dropna=request.dropna,
                columns_to_keep=request.columns_to_keep,
                columns_to_drop=request.columns_to_drop,
                drop_bid_ask=request.drop_bid_ask,
                pn=request.patternname
            )
        except Exception as e:
            print(f"Error in generate_mlf_feature_pattern: {e}")
            print(f"patternname: {request.patternname} might just not have its prerequisite TTF/Pattern data. We would be running: jgtmlttfcli -i {request.instrument} -t {request.timeframe} -new")