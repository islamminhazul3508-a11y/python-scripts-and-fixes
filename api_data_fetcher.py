import json
import urllib.request

def fetch_crypto_rates():
    """
    Fetches real-time market data from a public API, handles network errors,
    and parses structured JSON responses safely.
    """
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                usd_rate = data['bpi']['USD']['rate']
                print(f"Current Bitcoin Rate: ${usd_rate} USD")
                return data
    except urllib.error.URLError as err:
        print(f"Network error encountered: {err.reason}")
    except KeyError:
        print("Data parsing error: Key not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    fetch_crypto_rates()
