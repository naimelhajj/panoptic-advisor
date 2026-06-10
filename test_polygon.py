import os
from dotenv import load_dotenv
from polygon import RESTClient

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")

def test_polygon():
    if not API_KEY:
        print("Error: POLYGON_API_KEY not found in .env file.")
        return

    print("Authenticating with Polygon.io...")
    client = RESTClient(api_key=API_KEY)
    
    print("\n1. Testing basic stock data connection (CASY)...")
    try:
        # Get one day of CASY stock data just to verify the key works
        aggs = client.get_aggs(
            ticker="CASY",
            multiplier=1,
            timespan="day",
            from_="2026-06-01",
            to="2026-06-05"
        )
        print("Success! Downloaded CASY stock data.")
    except Exception as e:
        print(f"Failed: {e}")
        # Continue to test options anyway

    print("\n2. Testing Options Basic data tier (Pulling SPY Call Contracts)...")
    try:
        contracts = []
        # Pull up to 5 Call option contracts for SPY to verify the Options tier works
        for c in client.list_options_contracts(underlying_ticker="SPY", contract_type="call", limit=5):
            contracts.append(c)
            if len(contracts) >= 5:
                break
                
        print(f"Success! Found {len(contracts)} options contracts.")
        for c in contracts:
            print(f" -> Contract ID: {c.ticker} | Strike: ${c.strike_price} | Expiry: {c.expiration_date}")
            
        print("\n3. Testing Options Daily Pricing (Pulling price history for the first contract)...")
        if len(contracts) > 0:
            opt_ticker = contracts[0].ticker
            opt_aggs = client.get_aggs(
                ticker=opt_ticker,
                multiplier=1,
                timespan="day",
                from_="2026-06-01",
                to="2026-06-05"
            )
            print(f"Success! Downloaded daily price history for {opt_ticker}.")
            for a in opt_aggs:
                print(f"  -> Date: {a.timestamp}, Close: ${a.close}, Vol: {a.volume}")
            
    except Exception as e:
        print(f"Failed to fetch options data: {e}")

if __name__ == "__main__":
    test_polygon()
