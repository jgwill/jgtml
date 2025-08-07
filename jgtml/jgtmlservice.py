#!/usr/bin/env python
"""
JGTML Data Refresh Service - Main CLI Entry Point

This script provides the main entry point for the JGTML ML model training and
feature engineering service with automated scheduling, parallel processing,
and model serving capabilities.

Based on jgtpy/jgtservice.py architecture, adapted for ML workflow:
CDS → TTF → MLF → MX → Model Training → Model Serving

Usage:
    jgtmlservice --daemon --patterns "mfi,mz,zonesq,aoac" --instruments "EUR/USD,XAU/USD"
    jgtmlservice --train-models --patterns "mfi,mz" --instruments "SPX500"
    jgtmlservice --web --port 8080
    jgtmlservice --refresh-features --all
    jgtmlservice --status
"""

import sys
import os
import argparse
import logging
from typing import List, Optional

# Add current directory to path for relative imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import from jgtutils for argument parsing and settings
from jgtutils import jgtcommon
from jgtutils.jgtclihelper import print_jsonl_message

# Import service components (to be implemented)
from service.ml_base import JGTMLServiceConfig, JGTMLServiceManager

logger = logging.getLogger(__name__)

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for the JGTML service"""
    
    parser = jgtcommon.new_parser(
        "JGTML ML Model Training and Feature Engineering Service",
        epilog="Automated ML pipeline: CDS → TTF → MLF → MX → Model Training → Model Serving",
        enable_specified_settings=True
    )
    
    # Service mode arguments
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--daemon', '-d',
        action='store_true',
        help='Run in daemon mode with continuous feature refresh and model training'
    )
    mode_group.add_argument(
        '--web', '-w', 
        action='store_true',
        help='Run web server mode with ML API endpoints'
    )
    mode_group.add_argument(
        '--refresh-features', '-r',
        action='store_true', 
        help='Run one-time feature generation (TTF → MLF → MX) and exit'
    )
    mode_group.add_argument(
        '--train-models', '-tm',
        action='store_true',
        help='Train ML models for specified patterns and exit'
    )
    mode_group.add_argument(
        '--serve-models', '-sm',
        action='store_true',
        help='Start model serving API without training'
    )
    mode_group.add_argument(
        '--status', '-s',
        action='store_true',
        help='Show service status, model coverage, and configuration'
    )
    
    # Configuration arguments
    parser.add_argument(
        '-i', '--instrument',
        type=str,
        action='append',  # Allow multiple -i arguments
        help='Instrument to process (e.g., EUR/USD, XAU/USD). Can be specified multiple times.'
    )
    parser.add_argument(
        '-t', '--timeframe', 
        type=str,
        action='append',  # Allow multiple -t arguments
        help='Timeframe to process (e.g., H1, H4, D1). Can be specified multiple times.'
    )
    
    # Pattern-specific arguments (core of JGTML)
    parser.add_argument(
        '-pn', '--pattern',
        type=str,
        action='append',
        help='Pattern to process (e.g., mfi, mz, zonesq, aoac). Can be specified multiple times.'
    )
    
    # Service-specific arguments
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Process all configured instruments, timeframes, and patterns'
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=8080,
        help='Port for web server mode (default: 8080)'
    )
    
    parser.add_argument(
        '--workers', '-j',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )
    
    # ML-specific arguments
    parser.add_argument(
        '--model-types',
        nargs='+',
        default=['logistic', 'random_forest', 'xgboost'],
        help='ML model types to train (default: logistic random_forest xgboost)'
    )
    
    parser.add_argument(
        '--ensemble-mode',
        choices=['consensus', 'voting', 'stacking'],
        default='consensus',
        help='Ensemble method for multi-model predictions (default: consensus)'
    )
    
    # Data processing modes
    parser.add_argument(
        '--production-mode',
        action='store_true',
        help='Production mode: TTF+MLF only (~400 rows) for real-time decisions'
    )
    
    parser.add_argument(
        '--discovery-mode',
        action='store_true', 
        help='Discovery mode: TTF+MLF+MX (full historical) for ML training'
    )
    
    # Upload/distribution
    parser.add_argument(
        '--no-upload',
        action='store_true',
        help='Disable model upload to cloud storage'
    )
    
    parser.add_argument(
        '--model-registry',
        type=str,
        help='Model registry URL for deployment'
    )
    
    # Processing options
    jgtcommon.add_use_fresh_argument(parser)
    jgtcommon.add_verbose_argument(parser)
    
    # Advanced ML options
    parser.add_argument(
        '--auto-retrain',
        action='store_true',
        help='Enable automatic model retraining based on data freshness'
    )
    
    parser.add_argument(
        '--validation-split',
        type=float,
        default=0.2,
        help='Validation split ratio for model training (default: 0.2)'
    )
    
    return jgtcommon.parse_args(parser)


def create_config_from_args(args: argparse.Namespace) -> JGTMLServiceConfig:
    """Create service configuration from parsed arguments"""
    
    # Start with environment-based config
    config = JGTMLServiceConfig.from_env()
    
    # Override with command line arguments
    if hasattr(args, 'instrument') and args.instrument:
        if args.all:
            # Use all configured instruments
            pass  # Keep config.instruments from env/settings
        else:
            config.instruments = args.instrument
    
    if hasattr(args, 'timeframe') and args.timeframe:
        if args.all:
            # Use all configured timeframes  
            pass  # Keep config.timeframes from env/settings
        else:
            config.timeframes = args.timeframe
            
    if hasattr(args, 'pattern') and args.pattern:
        if args.all:
            # Use all configured patterns
            pass  # Keep config.patterns from env/settings
        else:
            config.patterns = args.pattern
    
    # Service mode settings
    config.daemon_mode = getattr(args, 'daemon', False)
    config.web_mode = getattr(args, 'web', False)  
    config.refresh_features = getattr(args, 'refresh_features', False)
    config.train_models = getattr(args, 'train_models', False)
    config.serve_models = getattr(args, 'serve_models', False)
    
    # ML-specific settings
    if hasattr(args, 'model_types'):
        config.model_types = args.model_types
    if hasattr(args, 'ensemble_mode'):
        config.ensemble_mode = args.ensemble_mode
    if hasattr(args, 'validation_split'):
        config.validation_split = args.validation_split
    
    # Processing modes
    config.production_mode = getattr(args, 'production_mode', False)
    config.discovery_mode = getattr(args, 'discovery_mode', False)
    
    # Set default mode if none specified
    if not (config.production_mode or config.discovery_mode):
        config.production_mode = True  # Default to production mode
    
    # Other settings
    if hasattr(args, 'port'):
        config.web_port = args.port
    if hasattr(args, 'workers'):
        config.max_workers = args.workers
    if hasattr(args, 'no_upload'):
        config.enable_upload = not args.no_upload
    if hasattr(args, 'model_registry'):
        config.model_registry_url = args.model_registry
    if hasattr(args, 'fresh'):
        config.use_fresh = args.fresh
    if hasattr(args, 'verbose'):
        config.verbose_level = args.verbose
        config.quiet = args.verbose == 0
    if hasattr(args, 'auto_retrain'):
        config.auto_retrain = args.auto_retrain
    
    return config


def show_status(config: JGTMLServiceConfig):
    """Show current service configuration and ML model status"""
    print("JGTML ML Model Training Service - Configuration Status")
    print("=" * 60)
    print(f"Instruments: {', '.join(config.instruments)}")
    print(f"Timeframes: {', '.join(config.timeframes)}")
    print(f"Patterns: {', '.join(config.patterns)}")
    print(f"Model Types: {', '.join(config.model_types)}")
    print(f"Ensemble Mode: {config.ensemble_mode}")
    print(f"Max Workers: {config.max_workers}")
    print(f"Data Path: {config.data_path}")
    print(f"Data Full Path: {config.data_full_path}")
    print(f"Models Path: {config.models_path}")
    print(f"Production Mode: {config.production_mode}")
    print(f"Discovery Mode: {config.discovery_mode}")
    print(f"Auto Retrain: {config.auto_retrain}")
    print(f"Upload Enabled: {config.enable_upload}")
    if config.model_registry_url:
        print(f"Model Registry: {config.model_registry_url}")
    print(f"Use Fresh: {config.use_fresh}")
    print(f"Verbose Level: {config.verbose_level}")
    
    # Show model coverage status
    print(f"\nML Model Coverage Status:")
    print("=" * 40)
    
    total_combinations = len(config.instruments) * len(config.timeframes) * len(config.patterns)
    print(f"Total Combinations: {total_combinations}")
    
    # Calculate expected model files
    expected_models = total_combinations * len(config.model_types)
    print(f"Expected Models: {expected_models}")
    
    # Check existing models (placeholder - will be implemented)
    print(f"Trained Models: [TO BE IMPLEMENTED]")
    print(f"Coverage: [TO BE CALCULATED]")
    
    # Feature pipeline status
    print(f"\nFeature Pipeline Status:")
    print("=" * 40)
    print(f"TTF Files: [TO BE IMPLEMENTED]")
    print(f"MLF Files: [TO BE IMPLEMENTED]") 
    print(f"MX Files: [TO BE IMPLEMENTED]")
    
    # Validate configuration
    errors = config.validate()
    if errors:
        print("\nConfiguration Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\nConfiguration: VALID")


def main():
    """Main entry point for the JGTML service"""
    
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Create configuration
        config = create_config_from_args(args)
        
        # Handle status request
        if getattr(args, 'status', False):
            show_status(config)
            return
        
        # Set default mode if none specified
        if not any([config.daemon_mode, config.web_mode, config.refresh_features, 
                   config.train_models, config.serve_models]):
            config.refresh_features = True
        
        # Create and start service
        service_manager = JGTMLServiceManager(config)
        
        logger.info("Starting JGTML ML Model Training Service...")
        print_jsonl_message(
            "JGTML Service starting",
            extra_dict={
                "mode": ("daemon" if config.daemon_mode else 
                        "web" if config.web_mode else
                        "train" if config.train_models else
                        "serve" if config.serve_models else
                        "features"),
                "instruments": config.instruments,
                "timeframes": config.timeframes,
                "patterns": config.patterns,
                "model_types": config.model_types
            },
            scope="jgtmlservice",
            state="starting"
        )
        
        service_manager.start()
        
    except KeyboardInterrupt:
        logger.info("Service interrupted by user")
        print_jsonl_message(
            "JGTML Service interrupted by user",
            scope="jgtmlservice", 
            state="interrupted"
        )
    except Exception as e:
        logger.error(f"Service failed: {e}")
        print_jsonl_message(
            f"JGTML Service failed: {e}",
            scope="jgtmlservice",
            state="error"
        )
        sys.exit(1)


if __name__ == '__main__':
    main()