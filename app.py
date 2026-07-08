"""
AI Outbound Cold Caller — Ulio version
----------------------------------------
This version does NOT handle the call or conversation itself — Ulio does
that entirely, using the agent/knowledge base you already configured in
your Ulio dashboard. This app's only job is to trigger Ulio's API to
place a call to a given number.

Confirmed against Ulio's official API docs (External API section).
"""

import os
import requests
from flask import Flask, request

app = Flask(__name__)

ULIO_API_KEY = os.environ["ULIO_API_KEY"]     # from Agent Studio -> Tools -> External API
ULIO_SHOP_ID = os.environ["ULIO_SHOP_ID"]     # your business ID, found in the URL or General tab

ULIO_OUTBOUND_URL = "https://api.ulio.ai/v1/calls/outbound"


@app.route("/call/start", methods=["POST"])
def start_call():
    """Trigger Ulio to place an outbound call using your existing agent.
    Call this yourself, e.g.:
    curl -X POST <your-render-url>/call/start -d to_number=+15551234567
    Optional form fields to personalize the call, e.g. -d caller_name=John
    """
    to_number = request.form["to_number"]

    # Any extra form fields (besides to_number) get passed through as
    # variables the AI can use in its prompt, e.g. caller_name, company, etc.
    variables = {k: v for k, v in request.form.items() if k != "to_number"}

    response = requests.post(
        ULIO_OUTBOUND_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ULIO_API_KEY,
        },
        json={
            "phone_number": to_number,
            "shop_id": ULIO_SHOP_ID,
            "variables": variables,
        },
        timeout=15,
    )

    return {
        "status_code": response.status_code,
        "ulio_response": response.text,
        "debug_shop_id_used": ULIO_SHOP_ID,
        "debug_api_key_length": len(ULIO_API_KEY),
        "debug_api_key_last_4": ULIO_API_KEY[-4:] if len(ULIO_API_KEY) >= 4 else "TOO_SHORT",
    }


@app.route("/", methods=["GET"])
def health_check():
    return {"status": "ok", "service": "cold-caller-ulio"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
