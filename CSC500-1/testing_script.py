import requests, urllib3, time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def refresh_watchlist(conids):
    base_url = "https://localhost:5000/v1/api/"
    url = f"{base_url}iserver/marketdata/snapshot"
    params = {
        "conids": ",".join(conids),
        "fields": "31,84,86"
    }

    while True:
        response = requests.get(url, params=params, verify=False)
        data = response.json()
        print("----- REFRESH -----")
        for quote in data:
            print(f"{quote['conid']}: Last={quote.get('31')} | Bid={quote.get('84')} | Ask={quote.get('86')}")
        time.sleep(15)

# Example: Watch AAPL (265598) and MSFT (272093)
refresh_watchlist(["265598", "272093"])
