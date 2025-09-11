#!/usr/bin/env python3
"""
JGTML Baseline ML Classifier

This module implements the first machine learning baseline for JGTML,
focusing on FDB signal classification using the existing data pipeline.

Key Features:
- Uses existing MX data for training targets
- Integrates with TTF/MLF feature engineering
- Simple scikit-learn implementation for quick deployment
- CLI integration with existing jgtml tools

Usage:
    python -m jgtml.experiments.baseline_classifier --train -i EUR/USD -t H4
    python -m jgtml.experiments.baseline_classifier --predict -i EUR/USD -t H4
    
Integration:
    # Use via jgtmlcli (future enhancement)
    jgtmlcli --ml-train -i EUR/USD -t H4
    jgtmlcli --ml-predict -i EUR/USD -t H4
"""

import argparse
import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import joblib
import logging
from datetime import datetime

# Standard ML imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JGTMLBaseline:
    """
    Baseline ML classifier for JGTML FDB signal prediction.
    
    This classifier uses the existing data pipeline:
    - CDS: Chaos Data Service (market data + indicators)
    - TTF: Transformed Trading Features (cross-timeframe features)  
    - MLF: Meta Lag Features (lagged versions)
    - MX: ML Targets (classification labels)
    """
    
    def __init__(self, model_dir: str = "./models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.target_column = 'target'  # Standard target column from MX data
        
        # Model metadata
        self.metadata = {
            'created_at': None,
            'trained_on': None,
            'accuracy': None,
            'feature_count': None,
            'training_samples': None
        }
    
    def create_demo_data(self, instrument: str, timeframe: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Create demo data for testing when real data is not available.
        
        This generates synthetic data that mimics the JGTML data structure.
        """
        logger.info(f"Creating demo data for {instrument} {timeframe}")
        
        # Generate synthetic features that might exist in JGTML
        n_samples = 1000
        np.random.seed(42)  # Reproducible results
        
        # Create features similar to what JGTML might generate
        features = {
            'mfi_sig': np.random.choice([-1, 0, 1], n_samples),
            'zone_sig': np.random.choice([-1, 0, 1], n_samples),
            'ao': np.random.randn(n_samples),
            'ac': np.random.randn(n_samples),
            'close': 1.0 + np.cumsum(np.random.randn(n_samples) * 0.01),
            'volume': np.random.lognormal(10, 1, n_samples),
            'rsi': np.random.uniform(20, 80, n_samples),
            'sma_20': 1.0 + np.cumsum(np.random.randn(n_samples) * 0.005),
            'sma_50': 1.0 + np.cumsum(np.random.randn(n_samples) * 0.003),
            'bb_upper': 1.0 + np.cumsum(np.random.randn(n_samples) * 0.005) + 0.02,
            'bb_lower': 1.0 + np.cumsum(np.random.randn(n_samples) * 0.005) - 0.02,
        }
        
        # Create lag features (MLF-style)
        for lag in [1, 2, 3, 5]:
            features[f'mfi_sig_lag_{lag}'] = np.roll(features['mfi_sig'], lag)
            features[f'close_lag_{lag}'] = np.roll(features['close'], lag)
            features[f'rsi_lag_{lag}'] = np.roll(features['rsi'], lag)
        
        # Create higher timeframe features (TTF-style)
        for tf in ['H4', 'D1']:
            features[f'mfi_sig_{tf}'] = np.random.choice([-1, 0, 1], n_samples)
            features[f'zone_sig_{tf}'] = np.random.choice([-1, 0, 1], n_samples)
            features[f'rsi_{tf}'] = np.random.uniform(20, 80, n_samples)
        
        feature_df = pd.DataFrame(features)
        
        # Create target variable (FDB signal)
        # Make it somewhat correlated with features for realistic training
        target_prob = (
            0.3 + 
            0.2 * (feature_df['mfi_sig'] > 0) +
            0.2 * (feature_df['zone_sig'] > 0) +
            0.1 * (feature_df['rsi'] < 30) +  # Oversold
            0.1 * (feature_df['close'] > feature_df['sma_20']) +
            0.1 * np.random.random(n_samples)
        )
        
        target = (target_prob > 0.5).astype(int)
        
        self.feature_columns = feature_df.columns.tolist()
        self.target_column = 'target'
        
        logger.info(f"Created demo data: {feature_df.shape} features, {len(target)} targets")
        logger.info(f"Target distribution: {pd.Series(target).value_counts().to_dict()}")
        
        return feature_df, pd.Series(target)
    
    def _find_data_files(self, instrument: str, timeframe: str) -> Dict[str, Optional[str]]:
        """
        Find available data files for the given instrument and timeframe.
        
        This method looks for data in the standard JGTML data structure:
        - MX files: contain target variables for training
        - TTF files: contain engineered features
        - MLF files: contain lag features
        """
        # Standard JGTML data paths (adjust based on actual structure)
        data_paths = {
            'mx': None,
            'ttf': None, 
            'mlf': None
        }
        
        # Common data directories to check
        possible_dirs = [
            Path("./data"),
            Path("../data"),
            Path(os.environ.get('JGTPY_DATA', './data')),
            Path(os.environ.get('JGTPY_DATA_FULL', './data'))
        ]
        
        for base_dir in possible_dirs:
            if base_dir.exists():
                # Look for MX files (most important - contains targets)
                mx_patterns = [
                    base_dir / f"mx/{instrument}_{timeframe}_mx.csv",
                    base_dir / f"current/mx/{instrument}_{timeframe}_mx.csv",
                    base_dir / f"full/mx/{instrument}_{timeframe}_mx.csv"
                ]
                
                for mx_path in mx_patterns:
                    if mx_path.exists():
                        data_paths['mx'] = str(mx_path)
                        break
                
                # Look for TTF files
                ttf_patterns = [
                    base_dir / f"ttf/{instrument}_{timeframe}_ttf.csv",
                    base_dir / f"current/ttf/{instrument}_{timeframe}_ttf.csv", 
                    base_dir / f"full/ttf/{instrument}_{timeframe}_ttf.csv"
                ]
                
                for ttf_path in ttf_patterns:
                    if ttf_path.exists():
                        data_paths['ttf'] = str(ttf_path)
                        break
                
                # Look for MLF files
                mlf_patterns = [
                    base_dir / f"mlf/{instrument}_{timeframe}_mlf.csv",
                    base_dir / f"current/mlf/{instrument}_{timeframe}_mlf.csv",
                    base_dir / f"full/mlf/{instrument}_{timeframe}_mlf.csv"
                ]
                
                for mlf_path in mlf_patterns:
                    if mlf_path.exists():
                        data_paths['mlf'] = str(mlf_path)
                        break
        
        return data_paths
    
    def load_training_data(self, instrument: str, timeframe: str, use_demo: bool = False) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load and prepare training data from the JGTML data pipeline.
        
        Returns:
            Tuple of (features_df, target_series)
        """
        if use_demo:
            return self.create_demo_data(instrument, timeframe)
        
        data_files = self._find_data_files(instrument, timeframe)
        
        if not data_files['mx']:
            logger.warning(f"No MX data found for {instrument} {timeframe}. Using demo data.")
            logger.warning(f"To generate real data, run: jgtmlcli -i {instrument} -t {timeframe} -pn mfi")
            return self.create_demo_data(instrument, timeframe)
        
        logger.info(f"Loading data for {instrument} {timeframe}")
        logger.info(f"Found files: {data_files}")
        
        # Load MX data (contains targets)
        mx_df = pd.read_csv(data_files['mx'])
        logger.info(f"Loaded MX data: {mx_df.shape}")
        
        # Start with MX data as base
        combined_df = mx_df.copy()
        
        # Add TTF data if available
        if data_files['ttf']:
            ttf_df = pd.read_csv(data_files['ttf'])
            # Merge on datetime/timestamp columns
            datetime_cols = [col for col in ttf_df.columns if 'datetime' in col.lower() or 'timestamp' in col.lower()]
            if datetime_cols and datetime_cols[0] in mx_df.columns:
                combined_df = combined_df.merge(ttf_df, on=datetime_cols[0], how='left', suffixes=('', '_ttf'))
                logger.info(f"Added TTF features: {ttf_df.shape}")
            else:
                # Simple concatenation if no datetime column
                combined_df = pd.concat([combined_df, ttf_df], axis=1)
                logger.info(f"Concatenated TTF features: {ttf_df.shape}")
        
        # Add MLF data if available  
        if data_files['mlf']:
            mlf_df = pd.read_csv(data_files['mlf'])
            datetime_cols = [col for col in mlf_df.columns if 'datetime' in col.lower() or 'timestamp' in col.lower()]
            if datetime_cols and datetime_cols[0] in combined_df.columns:
                combined_df = combined_df.merge(mlf_df, on=datetime_cols[0], how='left', suffixes=('', '_mlf'))
                logger.info(f"Added MLF features: {mlf_df.shape}")
            else:
                # Simple concatenation if no datetime column
                combined_df = pd.concat([combined_df, mlf_df], axis=1)
                logger.info(f"Concatenated MLF features: {mlf_df.shape}")
        
        # Identify target column
        target_columns = [col for col in combined_df.columns if 'target' in col.lower()]
        if not target_columns:
            # Look for common FDB signal columns
            signal_columns = [col for col in combined_df.columns if 'signal' in col.lower() or 'fdb' in col.lower()]
            if signal_columns:
                self.target_column = signal_columns[0]
            else:
                raise ValueError(f"No target column found in data. Available columns: {combined_df.columns.tolist()}")
        else:
            self.target_column = target_columns[0]
        
        logger.info(f"Using target column: {self.target_column}")
        
        # Prepare features and target
        target = combined_df[self.target_column]
        
        # Remove non-feature columns
        feature_df = combined_df.drop(columns=[
            col for col in combined_df.columns 
            if col.lower() in ['datetime', 'timestamp', 'date', self.target_column.lower()]
            or 'unnamed' in col.lower()
        ])
        
        # Store feature columns for later use
        self.feature_columns = feature_df.columns.tolist()
        
        logger.info(f"Features shape: {feature_df.shape}")
        logger.info(f"Target shape: {target.shape}")
        logger.info(f"Target distribution: {target.value_counts()}")
        
        return feature_df, target
    
    def train(self, instrument: str, timeframe: str, test_size: float = 0.2, use_demo: bool = False) -> Dict[str, float]:
        """
        Train the baseline classifier.
        
        Returns:
            Dictionary with training metrics
        """
        logger.info(f"Training model for {instrument} {timeframe}")
        
        # Load data
        X, y = self.load_training_data(instrument, timeframe, use_demo=use_demo)
        
        # Handle missing values
        imputer = SimpleImputer(strategy='median')
        X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_imputed, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        logger.info("Training Random Forest...")
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5)
        
        metrics = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_count': len(self.feature_columns),
            'training_samples': len(X_train)
        }
        
        # Update metadata
        self.metadata.update({
            'created_at': datetime.now().isoformat(),
            'trained_on': f"{instrument}_{timeframe}",
            'accuracy': accuracy,
            'feature_count': len(self.feature_columns),
            'training_samples': len(X_train)
        })
        
        logger.info(f"Training complete. Accuracy: {accuracy:.3f}")
        logger.info(f"CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        return metrics
    
    def predict(self, instrument: str, timeframe: str, use_demo: bool = False) -> Dict[str, Any]:
        """
        Make predictions for the given instrument and timeframe.
        
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first or load a trained model.")
        
        logger.info(f"Making predictions for {instrument} {timeframe}")
        
        # Load current data
        X, _ = self.load_training_data(instrument, timeframe, use_demo=use_demo)
        
        # Use only the last few rows for prediction (recent data)
        X_recent = X.tail(10)  # Last 10 bars
        
        # Handle missing values
        imputer = SimpleImputer(strategy='median')
        X_imputed = pd.DataFrame(imputer.fit_transform(X_recent), columns=X_recent.columns)
        
        # Scale features
        X_scaled = self.scaler.transform(X_imputed)
        
        # Make predictions
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        
        # Get latest prediction
        latest_prediction = predictions[-1]
        latest_probability = probabilities[-1].max()
        
        results = {
            'instrument': instrument,
            'timeframe': timeframe,
            'prediction': int(latest_prediction),
            'confidence': float(latest_probability),
            'predictions_history': predictions.tolist(),
            'probabilities_history': probabilities.tolist(),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Prediction: {latest_prediction}, Confidence: {latest_probability:.3f}")
        
        return results
    
    def save(self, model_name: str = None) -> str:
        """Save the trained model and metadata."""
        if model_name is None:
            model_name = f"jgtml_baseline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        model_path = self.model_dir / f"{model_name}.joblib"
        metadata_path = self.model_dir / f"{model_name}_metadata.json"
        
        # Save model
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'target_column': self.target_column
        }, model_path)
        
        # Save metadata
        import json
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        
        logger.info(f"Model saved: {model_path}")
        return str(model_path)
    
    def load(self, model_path: str):
        """Load a trained model."""
        data = joblib.load(model_path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_columns = data['feature_columns']
        self.target_column = data['target_column']
        
        # Load metadata if available
        model_path_obj = Path(model_path)
        metadata_path = model_path_obj.parent / (model_path_obj.stem + '_metadata.json')
        if metadata_path.exists():
            import json
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
        
        logger.info(f"Model loaded: {model_path}")


def main():
    """CLI interface for the baseline classifier."""
    parser = argparse.ArgumentParser(description="JGTML Baseline ML Classifier")
    parser.add_argument('--train', action='store_true', help='Train the model')
    parser.add_argument('--predict', action='store_true', help='Make predictions')
    parser.add_argument('-i', '--instrument', required=True, help='Instrument (e.g., EUR/USD)')
    parser.add_argument('-t', '--timeframe', required=True, help='Timeframe (e.g., H4)')
    parser.add_argument('--model-path', help='Path to load/save model')
    parser.add_argument('--model-dir', default='./models', help='Directory for models')
    parser.add_argument('--demo', action='store_true', help='Use demo data instead of real data')
    
    args = parser.parse_args()
    
    # Initialize classifier
    classifier = JGTMLBaseline(model_dir=args.model_dir)
    
    if args.train:
        try:
            metrics = classifier.train(args.instrument, args.timeframe, use_demo=args.demo)
            model_path = classifier.save()
            print(f"\n✅ Training complete!")
            print(f"📊 Accuracy: {metrics['accuracy']:.3f}")
            print(f"📈 Cross-validation: {metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}")
            print(f"🎯 Features used: {metrics['feature_count']}")
            print(f"📝 Training samples: {metrics['training_samples']}")
            print(f"💾 Model saved: {model_path}")
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            sys.exit(1)
    
    elif args.predict:
        try:
            if args.model_path:
                classifier.load(args.model_path)
            else:
                # Try to find latest model
                latest_model = None
                if Path(args.model_dir).exists():
                    model_files = list(Path(args.model_dir).glob("*.joblib"))
                    if model_files:
                        latest_model = max(model_files, key=lambda p: p.stat().st_mtime)
                
                if latest_model:
                    classifier.load(str(latest_model))
                else:
                    print("❌ No trained model found. Train first with --train")
                    sys.exit(1)
            
            results = classifier.predict(args.instrument, args.timeframe, use_demo=args.demo)
            print(f"\n🎯 Prediction for {results['instrument']} {results['timeframe']}:")
            print(f"📈 Signal: {results['prediction']} ({'BUY' if results['prediction'] == 1 else 'HOLD/SELL'})")
            print(f"🎲 Confidence: {results['confidence']:.3f}")
            print(f"🕒 Timestamp: {results['timestamp']}")
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()