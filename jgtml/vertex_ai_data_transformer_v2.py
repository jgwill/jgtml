import pandas as pd
import numpy as np
import os
import argparse
import json

# Assuming jgtutils is in the python path
from jgtutils import jgtcommon

def transform_for_regression(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares the DataFrame for a regression task.
    Keeps only the selected pattern columns and the numerical target.
    """
    if 'target' not in df.columns:
        raise ValueError("Target column 'target' not found in the DataFrame.")
    return df

def transform_for_classification(df: pd.DataFrame, target_col='target', new_col_name='target_class') -> pd.DataFrame:
    """
    Prepares the DataFrame for a classification task by converting the numerical
    target into categorical classes ('up', 'down', 'flat').
    """
    df_classification = df.copy()

    if target_col not in df_classification.columns:
        raise ValueError(f"Target column '{target_col}' not found in the DataFrame.")

    conditions = [
        df_classification[target_col] > 0,
        df_classification[target_col] < 0
    ]
    choices = ['up', 'down']
    df_classification[new_col_name] = np.select(conditions, choices, default='flat')
    
    df_classification = df_classification.drop(columns=[target_col])
    
    return df_classification

def transform_for_forecasting(df: pd.DataFrame, series_id: str, target_col='target', timestamp_col='Date') -> pd.DataFrame:
    """
    Prepares the DataFrame for a forecasting task, conforming to Vertex AI's
    expected format (time_series_identifier, timestamp, target_value, [features...]).
    """
    df_forecasting = df.copy()

    if target_col not in df_forecasting.columns:
        raise ValueError(f"Target column '{target_col}' not found.")
    if timestamp_col not in df_forecasting.columns:
        if df_forecasting.index.name == timestamp_col:
            df_forecasting.reset_index(inplace=True)
        else:
            raise ValueError(f"Timestamp column '{timestamp_col}' not found.")

    df_forecasting['time_series_identifier'] = series_id
    
    feature_cols = [col for col in df_forecasting.columns if col not in [timestamp_col, 'time_series_identifier', target_col]]
    final_cols = [timestamp_col, 'time_series_identifier', target_col] + feature_cols
    df_forecasting = df_forecasting[final_cols]

    return df_forecasting

def main():
    """Main function to drive the pattern-based data transformation."""
    parser = argparse.ArgumentParser(description="Transform pattern-based datasets for Vertex AI training.")
    parser.add_argument('-i', '--instrument', required=True, type=str, help='Instrument symbol (e.g., SPX500, EUR/USD).')
    parser.add_argument('-t', '--timeframe', required=True, type=str, help='Timeframe (e.g., D1, H4).')
    parser.add_argument('-pn', '--pattern', required=True, type=str, help='Pattern name to use for feature selection (e.g., mz, mfi).')
    parser.add_argument('-o', '--output-dir', type=str, default='data/vertex_ai', help='Output directory for transformed files.')
    
    args = parser.parse_args()
    
    print(f"Starting data transformation for pattern: {args.pattern}...")
    print(f"Instrument: {args.instrument}, Timeframe: {args.timeframe}")

    try:
        # Load settings using jgtcommon
        settings = jgtcommon.get_settings()
        patterns_config = settings.get('patterns', {})
        
        if args.pattern not in patterns_config:
            raise ValueError(f"Pattern '{args.pattern}' not found in settings.")
            
        pattern_columns = patterns_config[args.pattern].get('columns', [])
        if not pattern_columns:
            raise ValueError(f"No columns defined for pattern '{args.pattern}'.")

        # Construct input file path
        instrument_fn = args.instrument.replace('/', '-')
        # Assuming the pattern in the filename is just the pattern name itself.
        input_filename = f"{instrument_fn}_{args.timeframe}_{args.pattern}.csv"
        
        # Using the path structure you described
        data_dir_full = os.getenv("JGTPY_DATA_FULL", "data/full")
        input_filepath = os.path.join(data_dir_full, 'targets', 'mx', input_filename)
        
        print(f"Loading data from: {input_filepath}")
        
        # Load and filter data
        df = pd.read_csv(input_filepath)
        
        # Define columns to keep: Date, target, and the pattern's columns
        columns_to_keep = ['Date', 'target'] + pattern_columns
        
        # Ensure all desired columns exist in the dataframe before selection
        existing_columns_to_keep = [col for col in columns_to_keep if col in df.columns]
        missing_cols = set(columns_to_keep) - set(existing_columns_to_keep)
        if missing_cols:
            print(f"Warning: The following columns were not found in the dataset and will be skipped: {list(missing_cols)}")

        filtered_df = df[existing_columns_to_keep]
        
        if 'Date' in filtered_df.columns:
            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

        # Create output directory
        os.makedirs(args.output_dir, exist_ok=True)

        # --- Regression ---
        df_regression = transform_for_regression(filtered_df.copy())
        regression_output_path = os.path.join(args.output_dir, f'data_regression_{args.pattern}.csv')
        df_regression.to_csv(regression_output_path, index=False)
        print(f"✅ Regression data for '{args.pattern}' pattern saved to {regression_output_path}")

        # --- Classification ---
        df_classification = transform_for_classification(filtered_df.copy())
        classification_output_path = os.path.join(args.output_dir, f'data_classification_{args.pattern}.csv')
        df_classification.to_csv(classification_output_path, index=False)
        print(f"✅ Classification data for '{args.pattern}' pattern saved to {classification_output_path}")

        # --- Forecasting ---
        df_forecasting = transform_for_forecasting(filtered_df.copy(), args.instrument)
        forecasting_output_path = os.path.join(args.output_dir, f'data_forecasting_{args.pattern}.csv')
        df_forecasting.to_csv(forecasting_output_path, index=False)
        print(f"✅ Forecasting data for '{args.pattern}' pattern saved to {forecasting_output_path}")

    except FileNotFoundError:
        print(f"❌ Error: Input file not found at '{input_filepath}'. Please ensure the file exists.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
