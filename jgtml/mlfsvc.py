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

