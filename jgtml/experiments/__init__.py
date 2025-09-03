# JGTML Machine Learning Experiments
"""
This module contains machine learning experiments and model implementations
for the JGTML trading system.

Key Components:
- baseline_classifier.py: Initial ML model for FDB signal classification
- model_utils.py: Utilities for model training, evaluation, and persistence
- data_loader.py: Data loading and preprocessing utilities

Usage:
    python -m jgtml.experiments.baseline_classifier --train
    python -m jgtml.experiments.baseline_classifier --predict -i EUR/USD -t H4
"""

__version__ = "0.1.0"

# Import key functions for easy access
try:
    from .baseline_classifier import train_model, predict_signal, load_model
    from .model_utils import evaluate_model, save_model, load_model_metadata
    __all__ = ['train_model', 'predict_signal', 'load_model', 'evaluate_model', 'save_model', 'load_model_metadata']
except ImportError:
    # Modules not yet implemented
    __all__ = []