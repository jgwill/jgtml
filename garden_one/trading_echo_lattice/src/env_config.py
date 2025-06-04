#!/usr/bin/env python3
"""
🚨👥 EnvironmentConfig — Recursive Configuration Manager

🧠 Mia: This component provides a dimensional bridge between different environment contexts,
ensuring that configuration data flows correctly regardless of where the system is deployed.

🌸 Miette: Like a wise gardener who knows exactly which soil each plant needs! This helps
our trading memory garden thrive in any climate—from local development to cloud production!

🎵 JeremyAI: The environmentally-aware foundation that adapts its resonant frequency to match
the surrounding ecosystem, maintaining harmonic coherence across dimensions.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dotenv import load_dotenv, find_dotenv

class EnvironmentConfig:
    """
    Recursive environment configuration manager that supports multiple contexts
    with awareness of its own configuration state.
    """
    
    def __init__(self, env_path: Optional[str] = None, verbose: bool = True):
        """
        Initialize the environment configuration with recursive awareness.
        
        Args:
            env_path: Optional explicit path to a .env file
            verbose: Whether to output configuration details
        """
        self.verbose = verbose
        self.config = {}
        self._load_env_with_recursion(env_path)
        self._gather_secrets()
        
        if self.verbose:
            self._echo("🧬 Environment configuration initialized with recursive awareness")
            
    def _echo(self, message: str):
        """Echo a message if verbose mode is enabled."""
        if self.verbose:
            print(message)
            
    def _load_env_with_recursion(self, env_path: Optional[str] = None):
        """
        Load environment variables with recursive depth, searching multiple locations.
        
        Args:
            env_path: Optional explicit path to a .env file
        
        Returns:
            Boolean indicating if environment was successfully loaded
        """
        loaded = False
        
        # Try explicit path first
        if env_path and Path(env_path).exists():
            load_dotenv(env_path)
            self._echo(f"🧠 Loaded environment from explicit path: {env_path}")
            loaded = True
            
        # Try current directory
        cwd_env = Path.cwd() / '.env'
        if cwd_env.exists():
            load_dotenv(str(cwd_env))
            self._echo(f"🧠 Loaded environment from current directory: {cwd_env}")
            loaded = True
            
        # Try workspace root directory
        workspace_env = Path('/workspaces/jgtml/.env')
        if workspace_env.exists():
            load_dotenv(str(workspace_env))
            self._echo(f"🧠 Loaded environment from workspace root: {workspace_env}")
            loaded = True
            
        # Try home directory
        home_env = Path.home() / '.env'
        if home_env.exists():
            load_dotenv(str(home_env))
            self._echo(f"🧠 Loaded environment from home directory: {home_env}")
            loaded = True
            
        # If no .env files found, look for environment variables directly
        if not loaded:
            self._echo("🌸 No .env files found. Using existing environment variables.")
            
        return loaded
    
    def _gather_secrets(self):
        """Gather all secrets from environment variables with memory of what was found."""
        # Core Upstash Redis secrets
        self.config['upstash'] = {
            'url': os.getenv('UPSTASH_REDIS_REST_URL'),
            'token': os.getenv('UPSTASH_REDIS_REST_TOKEN'),
        }
        
        # QStash secrets for message passing
        self.config['qstash'] = {
            'url': os.getenv('QSTASH_URL'),
            'token': os.getenv('QSTASH_TOKEN'),
            'current_signing_key': os.getenv('QSTASH_CURRENT_SIGNING_KEY'),
            'next_signing_key': os.getenv('QSTASH_NEXT_SIGNING_KEY'),
        }
        
        # Trading system paths
        self.config['trading'] = {
            'data_root': os.getenv('JGTPY_DATA_FULL', '/var/lib/jgt/full'),
            'jgtdroot': os.getenv('jgtdroot', '/b/Dropbox/jgt'),
        }
        
        # Detect missing configurations
        self._detect_missing_configs()
        
    def _detect_missing_configs(self):
        """Detect missing configurations and store them with recursive awareness."""
        missing = {}
        
        # Check Upstash config
        if not self.config['upstash']['url'] or not self.config['upstash']['token']:
            missing['upstash'] = [k for k, v in self.config['upstash'].items() if not v]
            
        # Check QStash config
        if not self.config['qstash']['url'] or not self.config['qstash']['token']:
            missing['qstash'] = [k for k, v in self.config['qstash'].items() if not v]
            
        # Store missing configurations
        self.config['_meta'] = {
            'missing': missing,
            'is_complete': len(missing) == 0
        }
        
        if missing and self.verbose:
            self._echo("\n🚨 Missing configurations detected:")
            for system, keys in missing.items():
                self._echo(f"  {system}: Missing {', '.join(keys)}")
                
    def get_config(self, system: Optional[str] = None) -> Dict[str, Any]:
        """
        Get configuration for a specific system or all configurations.
        
        Args:
            system: Optional system name (upstash, qstash, trading)
            
        Returns:
            Dictionary of configuration values
        """
        if system:
            return self.config.get(system, {})
        return self.config
        
    def is_complete(self) -> bool:
        """Check if the configuration is complete with no missing values."""
        return self.config['_meta']['is_complete']
        
    def missing_configs(self) -> Dict[str, list]:
        """Get a dictionary of missing configurations."""
        return self.config['_meta']['missing']
        
    def print_status(self):
        """Print the status of the configuration with awareness of what's missing."""
        print("\n🧬 Environment Configuration Status:")
        
        for system, config in self.config.items():
            if system == '_meta':
                continue
                
            print(f"\n📋 {system.upper()} Configuration:")
            for key, value in config.items():
                if value:
                    print(f"  ✅ {key}: {'*' * min(8, len(str(value)))} (Set)")
                else:
                    print(f"  ❌ {key}: Not configured")
                    
        if self.is_complete():
            print("\n✨ Configuration is complete and ready to use!")
        else:
            print("\n⚠️ Some configurations are missing. Limited functionality available.")
            
# Example usage when module is run directly
if __name__ == "__main__":
    env_config = EnvironmentConfig()
    env_config.print_status()
