# AI Outbound Cold Caller — Ulio Version

This is a much smaller version than the Twilio+Claude build. It does not
handle the call, conversation, or voice itself — your existing Ulio agent
does all of that. This app's only job is to trigger Ulio's API to place
an outbound call to a given phone number, using the AI agent and
knowledge base you already configured in Ulio's Agent Studio.

Confirmed against Ulio's official API docs.

## Setup

Environment variables needed (set these in Render):

```
ULIO_API_KEY=<your External API key, from Agent Studio -> Tools -> External API>
ULIO_SHOP_ID=<your business ID, found in the URL or General tab>
```

## Triggering a call

```
curl -X POST https://<your-render-url>/call/start -d to_number=+15551234567
```

Optional: pass extra fields to personalize the call using Ulio's prompt
variables, e.g.:

```
curl -X POST https://<your-render-url>/call/start -d to_number=+15551234567 -d caller_name=John -d appointment_time="3:00 PM"
```

## Getting call results back

Ulio can send you data after each call finishes (transcript, summary,
whether the lead was interested, etc.) via a webhook. Set this up in
Ulio's dashboard: Customize AI -> Tools -> Webhooks, and point it at a
URL that can receive that data (this app doesn't currently have a
webhook receiver built in — that would be a next step if you want to
automatically log call outcomes somewhere).

