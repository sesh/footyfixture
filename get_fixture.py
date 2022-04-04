import time
import json
import sys
from thttp import request

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Account": "afl",
}

matches = []

for r in range(1, 24):
    print(f"Fetching Round {r}")
    response = request(
        f"https://aflapi.afl.com.au/afl/v2/matches?competitionId=1&compSeasonId=43&pageSize=50&roundNumber={r}"
    )

    try:
        matches.extend(response.json["matches"])
    except:
        print(response)
        sys.exit(1)

    print(f"{len(matches)} matches retrieved so far")
    time.sleep(5)

with open("matches.json", "w") as f:
    f.write(json.dumps(matches))
