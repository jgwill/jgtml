"""
JGTML ML Model Training Service Components

This package provides the service architecture for automated ML model training
and feature engineering in the JGT ecosystem.

Main Components:
- ml_base: Core service configuration and management
- feature_processor: TTF → MLF → MX pipeline processing  
- model_trainer: ML model training and ensemble management
- model_server: Model serving and prediction API
- scheduler: Automated scheduling for daemon mode
- api: FastAPI web service endpoints

Architecture follows jgtpy.service patterns, adapted for ML workflows.
"""

from .ml_base import JGTMLServiceConfig, JGTMLServiceManager

__all__ = [
    'JGTMLServiceConfig',
    'JGTMLServiceManager'
]