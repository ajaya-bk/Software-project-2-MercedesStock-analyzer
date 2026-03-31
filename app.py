from flask import Flask, render_template
import requests
import json
from dotenv import load_dotenv
import os
from config import COMDAILY_API_URL, COMDAILY_AUTH, SYMBOL

load_dotenv()

app = Flask(__name__)


# helper to call the API - reusing this for both income and metrics
def fetch_data(endpoint):
    url = f"{COMDAILY_API_URL}/{endpoint}/{SYMBOL}"
    print("calling:", url)  # useful for debugging during dev

    try:
        res = requests.get(url, auth=COMDAILY_AUTH)
        res.raise_for_status()
        data = res.json()

        # both endpoints return data under a "message" key
        return data.get("message", [])

    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
    except Exception as e:
        print("something went wrong:", e)

    return []


# compares the oldest vs newest year to show if things went up or down
def compare_historical_to_latest(income_data):
    if not income_data or len(income_data) < 2:
        return None

    oldest = income_data[-1]
    latest = income_data[0]

    try:
        result = {
            "start_year": oldest["date"][:4],
            "end_year": latest["date"][:4],
            "revenue":   "↑" if float(latest["revenue"]) > float(oldest["revenue"]) else "↓",
            "netIncome": "↑" if float(latest["netIncome"]) > float(oldest["netIncome"]) else "↓",
            "eps":       "↑" if float(latest.get("eps", 0)) > float(oldest.get("eps", 0)) else "↓",
        }
        return result
    except (KeyError, ValueError):
        # just return nothing if something is missing in the data
        return None


# prepares data for the Chart.js charts in the frontend
# revenue and net income are converted to billions so the numbers aren't huge
def build_chart_data(income_data):
    if not income_data:
        return None

    # API returns newest first, so I reverse it for the chart to go left to right
    ordered = list(reversed(income_data[:8]))

    labels = []
    revenue = []
    net_income = []
    eps_values = []

    for row in ordered:
        try:
            labels.append(row["date"][:4])
            revenue.append(round(float(row.get("revenue", 0)) / 1e9, 2))
            net_income.append(round(float(row.get("netIncome", 0)) / 1e9, 2))
            eps_values.append(round(float(row.get("eps", 0)), 2))
        except (ValueError, TypeError):
            # skip any rows with bad/missing values
            continue

    return {
        "labels": labels,
        "revenue": revenue,
        "net_income": net_income,
        "eps": eps_values,
    }


@app.route("/")
def index():
    income = fetch_data("income-statement")
    metrics = fetch_data("key-metrics")

    trend_comparison = compare_historical_to_latest(income) if income else None
    chart_data = build_chart_data(income) if income else None

    return render_template(
        "index.html",
        income=income,
        metrics=metrics,
        trend_comparison=trend_comparison,
        chart_data=chart_data,
    )


if __name__ == "__main__":
    app.run(debug=True)