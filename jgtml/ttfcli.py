import argparse
import os
import sys
try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover - runtime dependency check
    missing = str(exc).split(':')[-1].strip()
    sys.stderr.write(
        f"[ttfcli] Missing dependency: {missing}. "
        "Install it with `pip install python-dateutil pandas`\n"
    )
    raise

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from mlclicommon import (add_patterns_arguments,
                         check_arguments) # -pn "<pattern> <pattern> <pattern> ..."

from mlcliconstants import TTFCLI_DESCRIPTION, TTFCLI_EPILOG, TTFCLI_PROG_NAME
from ptottf import create_ttf_csv # type: ignore
from jgtutils import jgtcommon

# Tracing integration with fail-safe design
try:
    from jgtcore import JGTTracer
    _has_tracing = True
except ImportError:
    _has_tracing = False

def _parse_args():
    parser:argparse.ArgumentParser=jgtcommon.new_parser(TTFCLI_DESCRIPTION,TTFCLI_EPILOG,TTFCLI_PROG_NAME)
    parser=jgtcommon.add_instrument_timeframe_arguments(parser)
    parser=jgtcommon.add_use_fresh_argument(parser)
    parser=jgtcommon.add_bars_amount_V2_arguments(parser)
    parser=jgtcommon.add_patterns_arguments(parser)
    
    #DEPRECATED
    #parser.add_argument("-fr", "--force_read", action="store_true", help="Force to read CDS (should increase speed but relies on existing data)")
  
    # #columns_list_from_higher_tf
    # pn_group=parser.add_argument_group("Patterns")
    # pn_group.add_argument("-clh", "--columns_list_from_higher_tf", nargs='+', help="List of columns to get from higher TF.  Default is mfi_sig,zone_sig,ao", default=None)
    # #@STCGoal Future Proto where Sub-Patterns are created from TTF with their corresponding Columns list and mayby Lags
    # #patternname
    # pn_group.add_argument("-pn", "--patternname", help="Pattern Name", default="ttf")
    

    args = jgtcommon.parse_args(parser)
    
    args =check_arguments(args)

    return args


def generate_ttf_for_pattern(instrument, timeframe, patternname="ttf", use_full=True, use_fresh=False, quotescount=-1, columns_list_from_higher_tf=None, args=None):
    """Programmatic helper mirroring CLI behavior for JTC integrations."""
    # Initialize tracing for programmatic TTF generation
    tracer = None
    if _has_tracing:
        try:
            tracer = JGTTracer("jgtml", "ttf_generation")
        except Exception:
            pass  # Graceful fallback
    
    if tracer:
        trace_metadata = {
            "instrument": instrument,
            "timeframe": timeframe,
            "pattern": patternname,
            "use_full": use_full,
            "use_fresh": use_fresh,
            "quotescount": quotescount,
            "programmatic_call": True
        }
        
        with tracer.trace_operation(f"TTF_prog_{instrument}_{timeframe}_{patternname}", trace_metadata) as trace_id:
            tracer.add_step("ttf_parameters", input_data=trace_metadata)
            
            # Core TTF processing
            pseudo_force_read_flag = True if not use_fresh else False
            result = create_ttf_csv(
                instrument,
                timeframe,
                use_full if use_full else False,
                True if use_fresh else False,
                quotescount,
                pseudo_force_read_flag,
                columns_list_from_higher_tf=columns_list_from_higher_tf,
                pn=patternname,
                args=args,
            )
            
            tracer.add_step("ttf_generation_complete", 
                          output_data={"success": True, "pattern": patternname, "call_type": "programmatic"})
            return result
    else:
        pseudo_force_read_flag = True if not use_fresh else False
        return create_ttf_csv(
            instrument,
            timeframe,
            use_full if use_full else False,
            True if use_fresh else False,
            quotescount,
            pseudo_force_read_flag,
            columns_list_from_higher_tf=columns_list_from_higher_tf,
            pn=patternname,
            args=args,
        )


def main():
    args = _parse_args()
    
    # Initialize tracing for TTF CLI processing
    tracer = None
    if _has_tracing:
        try:
            tracer = JGTTracer("jgtml", "ttf_cli")
        except Exception:
            pass  # Graceful fallback
    
    columns_list_from_higher_tf = args.columns_list_from_higher_tf if args.columns_list_from_higher_tf else None
    
    if tracer:
        trace_metadata = {
            "instrument": args.instrument,
            "timeframe": args.timeframe,
            "pattern": args.patternname,
            "use_full": args.full,
            "use_fresh": args.fresh,
            "quotescount": args.quotescount,
            "columns_from_higher_tf": columns_list_from_higher_tf,
            "cli_call": True
        }
        
        with tracer.trace_operation(f"TTF_CLI_{args.instrument}_{args.timeframe}_{args.patternname}", trace_metadata) as trace_id:
            tracer.add_step("cli_argument_parsing", input_data=vars(args))
            
            tracer.add_step("ttf_configuration", 
                          input_data={
                              "higher_tf_columns": columns_list_from_higher_tf,
                              "force_read_flag": not args.fresh
                          })
            
            # Core TTF processing with tracing
            pseudo_force_read_flag = True if not args.fresh else False
            try:
                create_ttf_csv(
                    args.instrument, 
                    args.timeframe, 
                    args.full if args.full else False, 
                    True if args.fresh else False, 
                    args.quotescount,
                    pseudo_force_read_flag, 
                    columns_list_from_higher_tf=columns_list_from_higher_tf, 
                    pn=args.patternname, 
                    args=args
                )
                
                tracer.add_step("ttf_processing_complete", 
                              output_data={
                                  "success": True, 
                                  "pattern": args.patternname,
                                  "instrument": args.instrument,
                                  "timeframe": args.timeframe,
                                  "call_type": "cli"
                              })
            except Exception as e:
                tracer.add_step("ttf_processing_error",
                              input_data={"error_type": type(e).__name__},
                              output_data={"error_message": str(e)})
                raise
    else:
        # Original processing without tracing
        pseudo_force_read_flag = True if not args.fresh else False
        create_ttf_csv(
            args.instrument, 
            args.timeframe, 
            args.full if args.full else False, 
            True if args.fresh else False, 
            args.quotescount,
            pseudo_force_read_flag, 
            columns_list_from_higher_tf=columns_list_from_higher_tf, 
            pn=args.patternname, 
            args=args
        )

if __name__ == "__main__":
  main()
  
