# Software-project-2-MercedesStock-analyzer

A web app built with Flask that pulls financial data for **Mercedes-Benz Group AG (MBG.DE)** from the Comdaily API and displays it in a clean dashboard with charts.
 
This was built as a university project to practice working with REST APIs, Flask templating, and data visualization.
 
---
 
## What it does
 
- Fetches the income statement and key metrics for MBG.DE from the Comdaily API
- Shows a historical trend comparison (revenue, net income, EPS going up or down over time)
- Displays a bar chart comparing revenue vs net income over the years
- Shows an EPS trend line chart
- Includes a table with the last 5 years of income data
- Shows key metrics: P/E ratio, P/B ratio, and ROE
 
---

## Project structure
 
```
MBG.de/
│
├── mercedes/
│   ├── app.py          # main Flask app, fetches data and passes it to the template
│   ├── config.py       # API URL, auth credentials, and stock symbol
│   ├── .env            # your API credentials (not committed to git)
│   └── templates/
│       └── index.html  # the frontend template with Chart.js charts
│
└── README.md
```
 
---
 
## Requirements
 
- Python 3.8+
- A Comdaily API account (for the financial data)
 
Install dependencies:
 
```bash
pip install flask requests python-dotenv
```
 
---
## How it works
 
`app.py` has three main functions:
 
- **`fetch_data(endpoint)`** — makes a GET request to the Comdaily API and returns the data under the `message` key
- **`compare_historical_to_latest(income_data)`** — looks at the oldest and newest year in the data and returns arrows (↑ or ↓) to show the direction of change
- **`build_chart_data(income_data)`** — formats the income data into arrays that Chart.js can use directly; revenue and net income are converted to billions so the chart numbers are readable
 
The Flask route at `/` calls all three, then passes the results to `index.html` via `render_template`.
 
The frontend uses **Chart.js** (loaded from CDN) to render the charts. The chart data is passed from Flask into the template using Jinja2's `tojson` filter.
 
---
 
## API endpoints used
 
| Endpoint | What it returns |
|---|---|
| `/income-statement/MBG.DE` | Yearly revenue, net income, EPS |
| `/key-metrics/MBG.DE` | P/E ratio, P/B ratio, ROE |
 
Base URL is set in `config.py` as `COMDAILY_API_URL`.
 
---
 
## Notes
 
- If the API returns no data, the dashboard shows error messages instead of crashing
- The income table shows the 5 most recent years; the charts use up to 8 years
- Charts are only rendered if data is actually available (controlled by the `{% if chart_data %}` check in the template)
 
---
 
