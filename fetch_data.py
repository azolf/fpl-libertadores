import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

LEAGUE_ID = 970015
BASE_URL = "https://fantasy.premierleague.com/api"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def fetch_standings():
    entries = []
    page = 1
    while True:
        url = f"{BASE_URL}/leagues-classic/{LEAGUE_ID}/standings/?page_standings={page}"
        data = fetch(url)
        results = data["standings"]["results"]
        entries.extend(results)
        if not data["standings"]["has_next"]:
            break
        page += 1
        time.sleep(0.5)
    return entries


def fetch_history(entry_id):
    url = f"{BASE_URL}/entry/{entry_id}/history/"
    return fetch(url)


def main():
    print("Fetching league standings...")
    standings = fetch_standings()

    print(f"Fetching history for {len(standings)} entries...")
    for entry in standings:
        time.sleep(0.8)
        history = fetch_history(entry["entry"])
        current = history.get("current", [])
        chips = history.get("chips", [])

        entry["history"] = current
        entry["chips"] = chips

        # Attach last GW data for convenience
        if current:
            last = current[-1]
            entry["event_total"] = last["points"]
            entry["event_transfers"] = last["event_transfers"]
            entry["event_transfers_cost"] = last["event_transfers_cost"]
            entry["points_on_bench"] = last["points_on_bench"]
        else:
            entry["event_total"] = entry.get("event_total", 0)
            entry["event_transfers"] = 0
            entry["event_transfers_cost"] = 0
            entry["points_on_bench"] = 0

        print(f"  {entry['player_name']} ({entry['entry_name']}) done")

    out = Path("data/data.json")
    out.parent.mkdir(exist_ok=True)
    payload = {"updated_at": datetime.now(timezone.utc).isoformat(), "standings": standings}
    out.write_text(json.dumps(payload, indent=2))
    print(f"Saved {len(standings)} entries to {out}")


if __name__ == "__main__":
    main()
