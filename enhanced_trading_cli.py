import subprocess
import argparse
from jgtml.automated_fdb_trading_system import AutomatedFDBTradingSystem

def run_auto_trade(instruments, timeframes, demo=True, quality_threshold=8.0):
    """Run automated FDB trading with higher timeframe bias analysis"""
    print(f"\n🤖 AUTOMATED FDB TRADING - Enhanced Mode")
    print("=" * 60)
    print(f"Instruments: {instruments}")
    print(f"Mode: {'DEMO' if demo else 'REAL'}")
    print(f"Quality Threshold: {quality_threshold}")
    print("=" * 60)
    
    # Create automated trading system
    trading_system = AutomatedFDBTradingSystem(demo_mode=demo)
    trading_system.quality_threshold = quality_threshold
    
    all_results = {}
    campaigns_created = []
    
    for instrument in instruments:
        try:
            result = trading_system.analyze_instrument_for_trading(instrument)
            all_results[instrument] = result
            
            if result.get("campaign_created"):
                campaigns_created.append({
                    "instrument": instrument,
                    "campaign_id": result.get("campaign_id"),
                    "action": result.get("recommended_action"),
                    "quality": result.get("quality_score")
                })
                
        except Exception as e:
            print(f"❌ Error processing {instrument}: {e}")
            all_results[instrument] = {"error": str(e)}
    
    # Summary
    print("\n🎯 AUTOMATED TRADING RESULTS")
    print("=" * 50)
    
    for instrument, result in all_results.items():
        if "error" in result:
            print(f"❌ {instrument}: Error - {result['error']}")
        else:
            action = result.get("recommended_action", "NONE")
            quality = result.get("quality_score", 0)
            campaign_status = "✅ CAMPAIGN CREATED" if result.get("campaign_created") else "📋 MANUAL REVIEW"
            
            print(f"📈 {instrument}: {action} (Q: {quality:.1f}) - {campaign_status}")
    
    if campaigns_created:
        print(f"\n🚀 CAMPAIGNS CREATED: {len(campaigns_created)}")
        for campaign in campaigns_created:
            print(f"  ✅ {campaign['instrument']}: {campaign['action']} (Q: {campaign['quality']:.1f})")
            print(f"     Campaign ID: {campaign['campaign_id']}")
        
        print(f"\n📁 Campaign files: ./campaigns/")
        print("📋 Review and execute campaigns using entry.sh scripts")
    else:
        print("\n📋 No high-quality signals found for automated campaigns")
    
    return all_results

# Command handlers
def handle_auto_trade(args):
    """Handle auto-trade command"""
    instruments = [i.strip() for i in args.instruments.split(',')]
    demo_mode = not args.real  # Real overrides demo
    
    try:
        run_auto_trade(
            instruments=instruments,
            timeframes=["H4", "H1", "m15"],  # Fixed trading timeframes
            demo=demo_mode,
            quality_threshold=args.quality_threshold
        )
    except Exception as e:
        print(f"❌ Error in automated trading: {e}")
        return 1
    
    return 0

def handle_auto(args):
    """Handle auto command - alias for auto-trade"""
    return handle_auto_trade(args)

def handle_enhanced(args):
    """Handle enhanced command"""
    print("Enhanced trading mode - feature coming soon")
    return 0

def handle_production(args):
    """Handle production command"""
    print("Production trading mode - feature coming soon") 
    return 0

def handle_illusion(args):
    """Handle illusion detection command"""
    print("Alligator Illusion Detection - feature coming soon")
    return 0

def handle_status(args):
    """Handle status command"""
    print("Trading system status - feature coming soon")
    return 0

# Command definitions
def add_auto_trade_command(subparsers):
    """Add auto-trade command to CLI"""
    parser_auto = subparsers.add_parser(
        'auto-trade',
        help='Automated FDB trading with higher timeframe bias analysis'
    )
    parser_auto.add_argument(
        '-i', '--instruments',
        type=str,
        required=True,
        help='Comma-separated instruments (e.g., EUR-USD,GBP-USD)'
    )
    parser_auto.add_argument(
        '--demo',
        action='store_true',
        default=True,
        help='Use demo mode (default)'
    )
    parser_auto.add_argument(
        '--real',
        action='store_true',
        help='Use real trading mode'
    )
    parser_auto.add_argument(
        '--quality-threshold',
        type=float,
        default=8.0,
        help='Minimum quality threshold for campaign creation (default: 8.0)'
    )
    parser_auto.set_defaults(func=handle_auto_trade)

def add_auto_command(subparsers):
    """Add auto command to CLI (alias for auto-trade)"""
    parser_auto = subparsers.add_parser(
        'auto',
        help='Automated FDB trading (alias for auto-trade)'
    )
    parser_auto.add_argument(
        '-i', '--instruments',
        type=str,
        required=True,
        help='Comma-separated instruments (e.g., EUR-USD,GBP-USD)'
    )
    parser_auto.add_argument(
        '--demo',
        action='store_true',
        default=True,
        help='Use demo mode (default)'
    )
    parser_auto.add_argument(
        '--real',
        action='store_true',
        help='Use real trading mode'
    )
    parser_auto.add_argument(
        '--quality-threshold',
        type=float,
        default=8.0,
        help='Minimum quality threshold for campaign creation (default: 8.0)'
    )
    parser_auto.set_defaults(func=handle_auto)

def add_enhanced_command(subparsers):
    """Add enhanced command to CLI"""
    parser = subparsers.add_parser('enhanced', help='Enhanced trading mode')
    parser.set_defaults(func=handle_enhanced)

def add_production_command(subparsers):
    """Add production command to CLI"""
    parser = subparsers.add_parser('production', help='Production trading mode')
    parser.set_defaults(func=handle_production)

def add_illusion_command(subparsers):
    """Add illusion command to CLI"""
    parser = subparsers.add_parser('illusion', help='Alligator Illusion Detection')
    parser.set_defaults(func=handle_illusion)

def add_status_command(subparsers):
    """Add status command to CLI"""
    parser = subparsers.add_parser('status', help='Trading system status')
    parser.set_defaults(func=handle_status)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='enhancedtradingcli',
        description='Enhanced Trading CLI with FDB Signal Detection and Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add all commands
    add_enhanced_command(subparsers)
    add_production_command(subparsers) 
    add_auto_command(subparsers)
    add_auto_trade_command(subparsers)
    add_illusion_command(subparsers)
    add_status_command(subparsers)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)

if __name__ == "__main__":
    exit(main()) 