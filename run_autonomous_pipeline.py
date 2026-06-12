import subprocess
import sys
import argparse
import os

def run_script(script_name, args=[]):
    print("\n" + "="*80, flush=True)
    print(f"   RUNNING: {script_name} {' '.join(args)}", flush=True)
    print("="*80, flush=True)
    
    cmd = [sys.executable, "-u", script_name] + args
    result = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    
    if result.returncode != 0:
        print(f"\n[Error] {script_name} failed with exit code {result.returncode}. Aborting pipeline.", flush=True)
        sys.exit(result.returncode)
    print(f"Finished {script_name} successfully.", flush=True)

def main():
    parser = argparse.ArgumentParser(description="Autonomous FPBV Trading Pipeline")
    parser.add_argument("--starting-cash", type=float, default=300.00, help="Starting capital for fresh bot state if state file doesn't exist (default: 300.00)")
    parser.add_argument("--reset-state", action="store_true", help="Reset bot state file before running")
    parser.add_argument("--skip-discovery", action="store_true", help="Skip Wikipedia scraping and solvency audits (run on existing watchlist)")
    args = parser.parse_args()
    
    print("\n" + "#"*100, flush=True)
    print("   FPBV MODEL V3.2: STARTING 100% AUTONOMOUS TRADING PIPELINE", flush=True)
    print("#"*100, flush=True)
    
    # 1. Update watchlist dynamically from S&P 500
    if not args.skip_discovery:
        run_script("watchlist_generator.py")
    else:
        print("\nSkipping universe discovery. Running on existing watchlist.", flush=True)
        
    # 2. Update upcoming earnings calendar catalysts
    run_script("earnings_scanner.py")
    
    # 3. Evaluate signals and execute trades
    bot_args = ["--starting-cash", str(args.starting_cash)]
    if args.reset_state:
        bot_args.append("--reset-state")
        
    run_script("ibkr_paper_trader.py", bot_args)
    
    print("\n" + "#"*100, flush=True)
    print("   AUTONOMOUS PIPELINE RUN COMPLETED SUCCESSFULLY.", flush=True)
    print("#"*100, flush=True)

if __name__ == '__main__':
    main()
