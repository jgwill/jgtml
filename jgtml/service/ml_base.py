"""
Base service classes for JGTML ML Model Training Service

This module provides the core service management and configuration classes
for the JGTML ML pipeline: CDS → TTF → MLF → MX → Model Training → Model Serving

Based on jgtpy/service/base.py architecture, adapted for ML workflows.
"""

import sys
import os
import signal
import threading
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import from parent jgtml package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from jgtutils import jgtcommon
from jgtutils.jgtclihelper import print_jsonl_message

# Try to import python-dotenv if available
try:
    from dotenv import load_dotenv
    _has_dotenv = True
except ImportError:
    _has_dotenv = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def load_env_files():
    """Load .env files from multiple locations"""
    if not _has_dotenv:
        logger.warning("python-dotenv not available, .env files will not be loaded")
        return
    
    # Load .env files in order of precedence (last one wins)
    env_locations = [
        Path.home() / ".env",  # $HOME/.env
        Path.home() / ".jgt" / ".env",  # $HOME/.jgt/.env
        Path.cwd() / ".env"  # CWD/.env (highest precedence)
    ]
    
    loaded_files = []
    for env_file in env_locations:
        if env_file.exists():
            logger.info(f"Loading environment from: {env_file}")
            load_dotenv(env_file)
            loaded_files.append(str(env_file))
    
    if loaded_files:
        logger.info(f"Loaded {len(loaded_files)} .env files")
    else:
        logger.warning("No .env files found")

def load_jgt_config() -> Dict[str, Any]:
    """Load configuration from $HOME/.jgt/config.json"""
    config_file = Path.home() / ".jgt" / "config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load {config_file}: {e}")
    return {}

def _get_default_instruments() -> List[str]:
    """Get default instruments from environment variables or fallback to hardcoded list"""
    # Try various environment variable names
    instruments_env = os.getenv("JGTML_SERVICE_INSTRUMENTS", 
                               os.getenv("JCTPY_INSTRUMENTS",
                                        os.getenv("instruments")))
    
    if instruments_env:
        instruments = [i.strip() for i in instruments_env.split(",")]
        logger.debug(f"Default instruments from environment: {instruments}")
        return instruments
    
    # Fallback to SANDBOX tested instruments
    fallback = ["EUR/USD", "SPX500", "XAU/USD"]
    logger.debug(f"Using fallback default instruments: {fallback}")
    return fallback

def _get_default_timeframes() -> List[str]:
    """Get default timeframes from environment variables or fallback"""
    timeframes_env = os.getenv("JGTML_SERVICE_TIMEFRAMES",
                              os.getenv("JGTML_TIMEFRAMES"))
    
    if timeframes_env:
        timeframes = [t.strip() for t in timeframes_env.split(",")]
        logger.debug(f"Default timeframes from environment: {timeframes}")
        return timeframes
    
    # Fallback to SANDBOX tested timeframes  
    fallback = ["D1", "H4"]
    logger.debug(f"Using fallback default timeframes: {fallback}")
    return fallback

def _get_default_patterns() -> List[str]:
    """Get default patterns from environment variables or fallback"""
    patterns_env = os.getenv("JGTML_SERVICE_PATTERNS",
                            os.getenv("JGTML_PATTERNS"))
    
    if patterns_env:
        patterns = [p.strip() for p in patterns_env.split(",")]
        logger.debug(f"Default patterns from environment: {patterns}")
        return patterns
    
    # Fallback to SANDBOX tested patterns (including aoac)
    fallback = ["mfi", "mz", "zonesq", "aoac"]
    logger.debug(f"Using fallback default patterns: {fallback}")
    return fallback

@dataclass
class JGTMLServiceConfig:
    """Configuration class for JGTML ML Model Training Service"""
    
    # Core ML settings
    instruments: List[str] = field(default_factory=lambda: _get_default_instruments())
    timeframes: List[str] = field(default_factory=lambda: _get_default_timeframes())
    patterns: List[str] = field(default_factory=lambda: _get_default_patterns())
    model_types: List[str] = field(default_factory=lambda: ["logistic", "random_forest", "xgboost"])
    
    # Service settings
    refresh_interval: int = 3600  # 1 hour for ML models
    max_workers: int = 4
    
    # Data paths (follow SANDBOX architecture)
    data_path: str = "/tmp/jgtml/data/current"  # TTF/MLF current data
    data_full_path: str = "/tmp/jgtml/data/full"  # TTF/MLF/MX full historical
    models_path: str = "/tmp/jgtml/models"  # Trained models storage
    
    # Service modes
    daemon_mode: bool = False
    web_mode: bool = False
    web_port: int = 8080
    refresh_features: bool = False
    train_models: bool = False
    serve_models: bool = False
    
    # ML-specific settings
    ensemble_mode: str = "consensus"  # consensus, voting, stacking
    validation_split: float = 0.2
    auto_retrain: bool = False
    
    # Processing modes (like SANDBOX)
    production_mode: bool = True   # TTF+MLF only (~400 rows)
    discovery_mode: bool = False   # TTF+MLF+MX (full historical)
    
    # Upload settings (for model distribution)
    enable_upload: bool = True
    model_registry_url: Optional[str] = None
    
    # Processing settings
    use_fresh: bool = True
    quiet: bool = False
    verbose_level: int = 1
    
    # Error handling
    retry_attempts: int = 3
    retry_delay: int = 30  # seconds
    continue_on_error: bool = True
    
    @classmethod
    def from_env(cls) -> "JGTMLServiceConfig":
        """Create configuration from environment variables and config files"""
        # Load .env files first
        load_env_files()
        
        # Load JGT config file
        jgt_config = load_jgt_config()
        
        config = cls()
        
        # Parse instruments from env
        instruments_env = os.getenv("JGTML_SERVICE_INSTRUMENTS", 
                                   os.getenv("JGTML_INSTRUMENTS"))
        if instruments_env:
            config.instruments = [i.strip() for i in instruments_env.split(",")]
        elif "instruments" in jgt_config:
            config.instruments = jgt_config["instruments"]
        
        # Parse timeframes from env  
        timeframes_env = os.getenv("JGTML_SERVICE_TIMEFRAMES",
                                  os.getenv("JGTML_TIMEFRAMES"))
        if timeframes_env:
            if ',' in timeframes_env:
                config.timeframes = [t.strip() for t in timeframes_env.split(",")]
            else:
                config.timeframes = [t.strip() for t in timeframes_env.split()]
            logger.info(f"Loaded timeframes from environment: {config.timeframes}")
        elif "timeframes" in jgt_config:
            config.timeframes = jgt_config["timeframes"]
            logger.info(f"Loaded timeframes from config file: {config.timeframes}")
        else:
            logger.info(f"Using default timeframes: {config.timeframes}")
        
        # Parse patterns from env
        patterns_env = os.getenv("JGTML_SERVICE_PATTERNS",
                                os.getenv("JGTML_PATTERNS"))
        if patterns_env:
            config.patterns = [p.strip() for p in patterns_env.split(",")]
            logger.info(f"Loaded patterns from environment: {config.patterns}")
        elif "patterns" in jgt_config:
            # Extract pattern names from jgt_config patterns structure
            if isinstance(jgt_config["patterns"], dict):
                config.patterns = list(jgt_config["patterns"].keys())
            else:
                config.patterns = jgt_config["patterns"]
            logger.info(f"Loaded patterns from config file: {config.patterns}")
        else:
            logger.info(f"Using default patterns: {config.patterns}")
        
        # ML model types
        models_env = os.getenv("JGTML_SERVICE_MODEL_TYPES")
        if models_env:
            config.model_types = [m.strip() for m in models_env.split(",")]
        
        # Data paths (use SANDBOX-compatible paths by default)
        config.data_path = os.getenv("JGTML_DATA", 
                                    os.getenv("JGTPY_DATA", 
                                             config.data_path))
        config.data_full_path = os.getenv("JGTML_DATA_FULL", 
                                         os.getenv("JGTPY_DATA_FULL", 
                                                  config.data_full_path))
        config.models_path = os.getenv("JGTML_MODELS_PATH", config.models_path)
        
        # Model registry
        config.model_registry_url = os.getenv("JGTML_MODEL_REGISTRY_URL")
        
        # Numeric settings
        if os.getenv("JGTML_SERVICE_PARALLEL_WORKERS"):
            config.max_workers = int(os.getenv("JGTML_SERVICE_PARALLEL_WORKERS"))
        if os.getenv("JGTML_SERVICE_REFRESH_INTERVAL"):
            config.refresh_interval = int(os.getenv("JGTML_SERVICE_REFRESH_INTERVAL"))
        if os.getenv("JGTML_SERVICE_WEB_PORT"):
            config.web_port = int(os.getenv("JGTML_SERVICE_WEB_PORT"))
        if os.getenv("JGTML_VALIDATION_SPLIT"):
            config.validation_split = float(os.getenv("JGTML_VALIDATION_SPLIT"))
        
        # Boolean settings
        config.enable_upload = os.getenv("JGTML_SERVICE_ENABLE_UPLOAD", "true").lower() == "true"
        config.use_fresh = os.getenv("JGTML_SERVICE_USE_FRESH", "true").lower() == "true"
        config.quiet = os.getenv("JGTML_SERVICE_QUIET", "false").lower() == "true"
        config.auto_retrain = os.getenv("JGTML_AUTO_RETRAIN", "false").lower() == "true"
        
        # String settings
        if os.getenv("JGTML_ENSEMBLE_MODE"):
            config.ensemble_mode = os.getenv("JGTML_ENSEMBLE_MODE")
        
        return config
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        if not self.instruments:
            errors.append("No instruments configured")
        if not self.timeframes:
            errors.append("No timeframes configured")
        if not self.patterns:
            errors.append("No patterns configured")
        if not self.model_types:
            errors.append("No model types configured")
        if self.max_workers < 1:
            errors.append("max_workers must be >= 1")
        if self.refresh_interval < 1:
            errors.append("refresh_interval must be >= 1")
        if not (0.0 < self.validation_split < 1.0):
            errors.append("validation_split must be between 0.0 and 1.0")
        if self.ensemble_mode not in ["consensus", "voting", "stacking"]:
            errors.append("ensemble_mode must be one of: consensus, voting, stacking")
            
        return errors


class JGTMLServiceManager:
    """Main service manager for JGTML ML Model Training Service"""
    
    def __init__(self, config: JGTMLServiceConfig):
        self.config = config
        self.running = False
        self.scheduler = None
        self.feature_processor = None
        self.model_trainer = None
        self.model_server = None
        self.web_server = None
        self.shutdown_event = threading.Event()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("JGTML Service Manager initialized")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, initiating shutdown...")
        self.stop()
    
    def start(self):
        """Start the service based on configuration"""
        logger.info("Starting JGTML ML Model Training Service...")
        
        # Validate configuration
        errors = self.config.validate()
        if errors:
            for error in errors:
                logger.error(f"Configuration error: {error}")
            raise ValueError(f"Configuration validation failed: {errors}")
        
        self.running = True
        
        try:
            # Initialize components
            self._initialize_components()
            
            if self.config.refresh_features:
                # One-time feature generation mode
                self._run_feature_refresh()
            elif self.config.train_models:
                # One-time model training mode
                self._run_model_training()
            elif self.config.serve_models:
                # Model serving mode
                self._run_model_serving()
            elif self.config.web_mode:
                # Web server mode
                self._run_web_server()
            elif self.config.daemon_mode:
                # Daemon mode with scheduler
                self._run_daemon()
            else:
                # Default: run feature refresh then exit
                self._run_feature_refresh()
                
        except Exception as e:
            logger.error(f"Service startup failed: {e}")
            self.stop()
            raise
    
    def stop(self):
        """Stop the service gracefully"""
        if not self.running:
            return
            
        logger.info("Stopping JGTML Service...")
        self.running = False
        self.shutdown_event.set()
        
        # Stop components
        if self.scheduler:
            self.scheduler.stop()
        if self.feature_processor:
            self.feature_processor.shutdown()
        if self.model_trainer:
            self.model_trainer.shutdown()
        
        logger.info("JGTML Service stopped")
    
    def _initialize_components(self):
        """Initialize service components"""
        logger.info("Initializing JGTML service components...")
        
        # Create necessary directories
        os.makedirs(self.config.data_path, exist_ok=True)
        os.makedirs(self.config.data_full_path, exist_ok=True)
        os.makedirs(self.config.models_path, exist_ok=True)
        
        logger.info(f"Initialized JGTML service with paths:")
        logger.info(f"  Data: {self.config.data_path}")
        logger.info(f"  Data Full: {self.config.data_full_path}")
        logger.info(f"  Models: {self.config.models_path}")
        
        # Components will be initialized as needed
        # (FeatureProcessor, ModelTrainer, ModelServer, etc.)
    
    def _run_feature_refresh(self):
        """Run one-time feature generation (TTF → MLF → MX)"""
        logger.info("Running one-time feature refresh...")
        logger.info("Feature generation not yet implemented - placeholder")
        
        # TODO: Implement feature processing pipeline
        # 1. Check CDS data availability
        # 2. Generate TTF features
        # 3. Generate MLF lag features
        # 4. Generate MX targets (if discovery mode)
        
        logger.info("Feature refresh completed (placeholder)")
    
    def _run_model_training(self):
        """Run one-time model training"""
        logger.info("Running one-time model training...")
        logger.info("Model training not yet implemented - placeholder")
        
        # TODO: Implement model training pipeline
        # 1. Load MLF + MX data
        # 2. Train ensemble models (logistic, rf, xgboost)
        # 3. Save trained models
        # 4. Generate model metadata
        
        logger.info("Model training completed (placeholder)")
    
    def _run_model_serving(self):
        """Run model serving mode"""
        logger.info("Starting model serving...")
        logger.info("Model serving not yet implemented - placeholder")
        
        # TODO: Implement model serving
        # 1. Load trained models
        # 2. Start prediction API
        # 3. Handle inference requests
        
        logger.info("Model serving started (placeholder)")
    
    def _run_daemon(self):
        """Run in daemon mode with scheduler"""
        logger.info("Starting daemon mode...")
        logger.info("Daemon mode not yet implemented - placeholder")
        
        # TODO: Implement daemon scheduler
        # 1. Schedule feature refresh
        # 2. Schedule model retraining
        # 3. Monitor data freshness
        
        logger.info("Daemon mode started (placeholder)")
    
    def _run_web_server(self):
        """Run web server mode"""
        logger.info(f"Starting web server on port {self.config.web_port}...")
        logger.info("Web server not yet implemented - placeholder")
        
        # TODO: Implement FastAPI web server
        # 1. Feature generation endpoints
        # 2. Model training endpoints
        # 3. Model serving endpoints
        # 4. Status and monitoring endpoints
        
        logger.info("Web server started (placeholder)")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current service status"""
        status = {
            "running": self.running,
            "config": {
                "instruments": self.config.instruments,
                "timeframes": self.config.timeframes,
                "patterns": self.config.patterns,
                "model_types": self.config.model_types,
                "max_workers": self.config.max_workers,
                "ensemble_mode": self.config.ensemble_mode,
                "production_mode": self.config.production_mode,
                "discovery_mode": self.config.discovery_mode
            }
        }
        
        return status