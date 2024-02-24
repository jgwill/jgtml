# %% Imports
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from jgtpy import JGTPDSP as pds
import tlid


from jgtutils.jgtos import get_data_path


# %% Functions


def _crop_dataframe(df, crop_last_dt: str = None, crop_start_dt: str = None):
    if crop_last_dt is not None:
        df = df[df.index <= crop_last_dt]
    if crop_start_dt is not None:
        df = df[df.index >= crop_start_dt]
    return df


def calculate_target_variable_min_max(
    dfsrc,
    crop_last_dt=None,
    crop_start_dt=None,
    WINDOW_MIN=1,
    WINDOW_MAX=150,
    set_index=True,
    rounder=2,
    pipsize=-1,
):
    df = dfsrc.copy()

    df = _crop_dataframe(df, crop_last_dt, crop_start_dt)

    # reset index before we iterate
    try:
        df.reset_index(drop=False, inplace=True)
    except:
        pass

    # Initialize the tmax and tmin columns with NaN values
    df["tmax"] = float("nan")
    df["tmin"] = float("nan")
    df["p"] = float("nan")
    df["l"] = float("nan")
    df["target"] = float("nan")

    # Calculate the maximum and minimum Close value in the window range for each row
    for i in range(WINDOW_MIN, len(df) - WINDOW_MAX):
        # FDBS
        if df.loc[i, "fdbs"] == 1.0:
            df.loc[i, "tmax"] = df.loc[i : i + WINDOW_MAX, "Close"].min()
            df.loc[i, "tmin"] = df.loc[i : i + WINDOW_MAX, "Close"].max()

            if df.loc[i, "High"] < df.loc[i, "tmin"]:
                df.loc[i, "l"] = round(df.loc[i, "High"] - df.loc[i, "Low"], rounder)
                df.loc[i, "target"] = round(
                    -1 * (df.loc[i, "High"] - df.loc[i, "Low"]), rounder
                )
            else:
                df.loc[i, "p"] = round(df.loc[i, "Low"] - df.loc[i, "tmax"], rounder)
                df.loc[i, "target"] = round(
                    df.loc[i, "Low"] - df.loc[i, "tmax"], rounder
                )
        # FDBB
        if df.loc[i, "fdbb"] == 1.0:
            df.loc[i, "tmax"] = df.loc[i : i + WINDOW_MAX, "Close"].max()
            df.loc[i, "tmin"] = df.loc[i : i + WINDOW_MAX, "Close"].min()

            if df.loc[i, "Low"] > df.loc[i, "tmin"]:
                df.loc[i, "l"] = round(df.loc[i, "High"] - df.loc[i, "Low"], rounder)
                df.loc[i, "target"] = round(
                    -1 * (df.loc[i, "High"] - df.loc[i, "Low"]), rounder
                )
            else:
                df.loc[i, "p"] = round(df.loc[i, "tmax"] - df.loc[i, "High"], rounder)
                df.loc[i, "target"] = round(
                    df.loc[i, "tmax"] - df.loc[i, "High"], rounder
                )

    # Fill NaN with zero for columns tmax and tmin
    df["tmax"] = df["tmax"].fillna(0)
    df["tmin"] = df["tmin"].fillna(0)
    df["p"] = df["p"].fillna(0)
    df["l"] = df["l"].fillna(0)
    df["target"] = df["target"].fillna(0)
    # After calculating the 'target' column
    if pipsize != -1:
        df["target"] = df["target"] / pipsize

    # @q Maybe set backnthe index !??
    if set_index:
        df.set_index("Date", inplace=True)
    return df


def pto_target_calculation(
    i, t, crop_start_dt=None, crop_end_dt=None, tlid_tag=None, output_report_dir=None
):
    """
    Calculate the PTO target based on the given POV parameters and output to file with report.

    Args:
        i (int): The value of i.
        t (int): The value of t.
        crop_start_dt (datetime, optional): The start date for cropping. Defaults to None.
        crop_end_dt (datetime, optional): The end date for cropping. Defaults to None.
        tlid_tag (str, optional): The TLID tag. Defaults to None.
        output_report_dir (str, optional): The output report directory. Defaults to None.

    Returns:
        None
    """
    if tlid_tag is None:
        tlid_tag = tlid.get_minutes()

    default_jgtpy_data_full = "full/data"
    default_jgtpy_data_full = "/var/lib/jgt/full/data"
    data_dir_full = os.getenv("JGTPY_DATA_FULL", default_jgtpy_data_full)
    indir_cds = os.path.join(data_dir_full, "cds")
    outdir_tmx = os.path.join(
        data_dir_full, "targets", "mx"
    )  # @STCIssue Hardcoded path future JGTPY_DATA_FULL/.../mx
    _pov_target_calculation_n_output240223(
        indir_cds,
        outdir_tmx,
        crop_start_dt,
        crop_end_dt,
        i,
        t,
        tlid_tag,
        output_report_dir=output_report_dir,
    )


def _pov_target_calculation_n_output240223(
    indir_cds,
    outdir_tmx,
    crop_start_dt,
    crop_end_dt,
    i,
    t,
    tlid_tag,
    output_report_dir=None,
):
    if tlid_tag is None:
        tlid_tag = tlid.get_minutes()

    ifn = i.replace("/", "-")
    # read instrument prop
    iprop = pds.get_instrument_properties(i)
    pipsize = iprop["pipsize"]
    nb_decimal = (
        len(str(pipsize).split(".")[1]) if "." in str(pipsize) else len(str(pipsize))
    )
    rounder = nb_decimal

    # Possible crop of the dataframe to a specific date range

    # Read the source data of already calculated CDS
    df_cds_source = pd.read_csv(
        f"{indir_cds}/{ifn}_{t}.csv", index_col=0, parse_dates=True
    )

    df_result_tmx = calculate_target_variable_min_max(
        df_cds_source, crop_end_dt, crop_start_dt, rounder=rounder, pipsize=pipsize
    )

    # Save the result to a csv file
    output_all_cols_fn = f"{outdir_tmx}/{ifn}_{t}.csv"
    try:
        df_result_tmx.to_csv(output_all_cols_fn, index=True)
        print(f"Saved to {output_all_cols_fn}")
    except Exception as e:
        print(f"Error occurred while saving to {output_all_cols_fn}: {str(e)}")

    keeping_columns = ["Low", "fdbs", "fdbb", "tmax", "tmin", "p", "l", "target"]
    sel = df_result_tmx[keeping_columns].copy()
    sel = sel[(sel["p"] != 0) | (sel["l"] != 0)]

    output_sel_cols_fn = f"{outdir_tmx}/{ifn}_{t}_sel.csv"
    try:
        sel.to_csv(output_sel_cols_fn, index=True)
        print(f"Saved to {output_sel_cols_fn}")
    except Exception as e:
        print(f"Error occurred while saving to {output_sel_cols_fn}: {str(e)}")

    keeping_columns_sel2 = ["Open", "High", "Low", "Close", "fdbs", "fdbb", "target"]
    df_selection2 = df_result_tmx[keeping_columns_sel2].copy()
    df_selection2["target"] = df_selection2["target"].round(rounder)
    df_selection2 = df_selection2[(df_selection2["target"] != 0)]

    output_tnd_targetNdata_fn = f"{outdir_tmx}/{ifn}_{t}_tnd.csv"
    try:
        df_selection2.to_csv(output_tnd_targetNdata_fn, index=True)
        print(f"Saved to {output_tnd_targetNdata_fn}")
    except Exception as e:
        print(f"Error occurred while saving to {output_tnd_targetNdata_fn}: {str(e)}")

    _reporting(
        df_selection2, ifn, t, pipsize, tlid_tag, output_report_dir=output_report_dir
    )


def _reporting(df_selection2, ifn, t, pipsize, tlid_tag, output_report_dir=None):

    if output_report_dir is None:
        output_report_dir = os.getenv("JGTPY_DATA_FULL")

    report_file = f"{output_report_dir}/report-calc-{tlid_tag}.txt"
    print("Reporting to:", report_file)
    print(" tail -f ", report_file)

    with open(report_file, "a") as f:
        f.write(f"--- {ifn}_{t} --pipsize:{pipsize}---\n")
        f.write(f"Sum of target: {df_selection2['target'].sum()}\n\n")
        # f.write(f" (rounded): {(df_selection2['target'].sum()).round(2)}\n\n")


def readMXFile(
    instrument,
    timeframe,
    columns_to_remove=None,
    quiet=True,
    use_full=True,
    dt_crop_last=None,
    quote_count=None,
):
    """
    Read a MX Target file and return a pandas DataFrame.

    Parameters:
    instrument (str): The instrument name.
    timeframe (str): The timeframe of the data.
    columns_to_remove (list, optional): List of column names to remove from the DataFrame. Default is None.
    quiet (bool, optional): If True, suppresses the output messages. Default is True.
    use_full (bool, optional): If True, reads the full MX file. Default is True (there wont be MX in current data I think)).
    dt_crop_last (str, optional): The last date to crop the data. Default is None.
    quote_count (int, optional): The number of quotes to keep. Default is None.

    Returns:
    pandas.DataFrame: The DataFrame containing the MX Target data.
    """
    # Define the file path based on the environment variable or local path
    data_path_cds = get_data_path("targets/mx", use_full=use_full)
    fpath = pds.mk_fullpath(instrument, timeframe, "csv", data_path_cds)
    mdf = pd.read_csv(fpath)

    # Set 'Date' as the index and convert it to datetime
    mdf["Date"] = pd.to_datetime(mdf["Date"])
    mdf.set_index("Date", inplace=True)
    # Remove the specified columns
    if columns_to_remove is not None:
        mdf = mdf.drop(columns=columns_to_remove, errors="ignore")

    if dt_crop_last is not None:
        mdf = mdf[mdf.index < dt_crop_last]
    if quote_count is not None:
        mdf = mdf[-quote_count:]
    return mdf
