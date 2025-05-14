# SignalGenerator_MouthWaterInterpreter
# Extracted from: xpto231125v4fix.lua, xptoDSPrep231124v5.lua, x220929_240422b.lua
# Format: Engine description for Alligator-based metaphor signal logic

signal_engine = {
    "description": "Interprets Alligator indicator mouth state and price position to derive metaphor states (e.g., waterState). Used to qualify signal entry logic.",
    "indicators": ["ALLIGATOR", "AO", "Fractals"],
    "mouth_components": ["Jaw", "Teeth", "Lips"],
    "states": {
        "mouthState": ["open", "closed", "transitioning"],
        "waterState": ["eating", "splashing", "drowning", "floating"],
        "pricePosition": ["inside_mouth", "above_mouth", "below_mouth"]
    },
    "logic_clusters": {
        "FDB": {
            "signal_type": "Fractal Divergent Bar",
            "condition": "price diverges from Alligator direction while AO confirms",
            "entry_rule": "only valid if waterState = 'eating' and pricePosition = 'outside_mouth'"
        },
        "ZLC": {
            "signal_type": "Zero Line Cross",
            "condition": "AO crosses zero with confirmation",
            "dependency": "must not contradict mouthState"
        },
        "MSIG": {
            "signal_type": "Mouth Signal",
            "description": "Triggered when Alligator mouth transitions from closed to open or vice versa",
            "tracked": ["lastMouthSignalTriggered", "lastMouthSignalJaw"]
        }
    },
    "output": ["signal_label", "mouth_state", "water_state", "price_position"],
    "dependency_chain": {
        "mouth_state": "from Alligator structure (Lips, Teeth, Jaw)",
        "price_position": "from close vs. Alligator bounds",
        "water_state": "inferred from mouth_state + price_position dynamics"
    },
    "notes": [
        "Derived from older strategy Lua files by William (~2 years old)",
        "Matches labeled dataset: _mouth_signal_state_analysis.csv",
        "Used as pre-processor for ML or signal generation agents"
    ]
}

# This engine spec can be translated to Python or used by another LLM to re-implement runtime signal generation.
