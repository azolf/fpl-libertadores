# 🏆 Badfish Libertadores

Fantasy Premier League standings page for the Badfish Libertadores league, hosted on GitHub Pages.

## How it works

- `fetch_data.py` fetches standings and per-manager history from the FPL API and saves it to `data/data.json`
- `index.html` is a static page that loads `data/data.json` at runtime and renders the standings table
- A manual GitHub Actions workflow runs the script and commits the updated data

## Usage

**Trigger a data refresh:** go to Actions → Fetch FPL Data → Run workflow.

**Run locally:**
```bash
python fetch_data.py
python -m http.server 8000  # open http://localhost:8000
```
