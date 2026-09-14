from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from .scoring import qualify
from .x402 import decode_payment_payload, encode_payment_required, payment_required_response, verify_and_settle

SLUG = "tamer-powered-site-qualifier"
COMMIT = os.getenv("XAGENT_REVIEW_COMMIT", "local-development")


class SiteQualificationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    country_state: str | None = None
    available_mw: float | None = Field(default=None, ge=0)
    power_ready_now: bool | None = None
    energization_rfs_date: str | None = None
    voltage: str | None = None
    utility_interconnection_status: str | None = None
    grid_or_gas_to_power: str | None = None
    power_price_usd_kwh: float | None = Field(default=None, ge=0)
    land_size_acres: float | None = Field(default=None, ge=0)
    lease_sale_jv: str | None = None
    fiber_availability: str | None = None
    water_availability: str | None = None
    gas_availability: str | None = None
    permitting_status: str | None = None
    expansion_capacity_mw: float | None = Field(default=None, ge=0)
    intended_use: str = "both"


app = FastAPI(title="Powered-Site Qualifier API", version="0.1.0", description="Deterministic powered-site qualification for Bitcoin mining and AI/data-center infrastructure.")


LANDING_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="AI-ready qualification for Bitcoin mining and data-center powered sites.">
  <title>Powered-Site Qualifier</title>
  <style>
    :root { color-scheme: dark; --bg: #08111f; --panel: #101d30; --line: #263b56; --text: #ecf4ff; --muted: #9eb1c9; --accent: #55d6be; --accent-2: #6aa8ff; }
    * { box-sizing: border-box; }
    body { margin: 0; background: radial-gradient(circle at 80% 0, #18375a 0, var(--bg) 42rem); color: var(--text); font: 16px/1.6 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    main { width: min(1080px, calc(100% - 2rem)); margin: 0 auto; padding: 3.5rem 0 4rem; }
    .hero { padding: 2.5rem 0 2rem; }
    .eyebrow { color: var(--accent); font-size: .78rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
    h1 { margin: .5rem 0 1rem; font-size: clamp(2.3rem, 7vw, 4.8rem); line-height: 1.03; letter-spacing: -.045em; }
    h2 { margin-top: 0; font-size: 1.15rem; }
    .subtitle { max-width: 700px; margin: 0; color: #d7e5f8; font-size: clamp(1.1rem, 2.2vw, 1.45rem); }
    .description { max-width: 700px; color: var(--muted); }
    .actions { display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 1.5rem; }
    a.button { border: 1px solid var(--accent); border-radius: 999px; color: #061b1a; background: var(--accent); padding: .65rem 1rem; font-weight: 750; text-decoration: none; }
    a.button.secondary { border-color: var(--line); color: var(--text); background: var(--panel); }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem; }
    .card { border: 1px solid var(--line); border-radius: 16px; background: color-mix(in srgb, var(--panel) 92%, transparent); padding: 1.25rem; }
    .card h2 { color: #dceaff; }
    ul { margin: 0; padding-left: 1.2rem; color: var(--muted); }
    li + li { margin-top: .25rem; }
    .status { color: var(--accent); font-weight: 700; }
    code { color: #c4d8ff; font: .92em ui-monospace, SFMono-Regular, Menlo, monospace; }
    .endpoint { display: flex; gap: .75rem; align-items: baseline; padding: .45rem 0; border-bottom: 1px solid #1b2d44; }
    .endpoint:last-child { border-bottom: 0; }
    .method { min-width: 3.4rem; color: var(--accent-2); font: 700 .78rem ui-monospace, SFMono-Regular, Menlo, monospace; }
    .flow { display: grid; justify-items: center; gap: .35rem; margin: .5rem auto 0; color: #cbd9eb; text-align: center; }
    .flow span { width: min(100%, 310px); border: 1px solid var(--line); border-radius: 10px; background: #0c192a; padding: .55rem .8rem; }
    .arrow { color: var(--accent); line-height: 1; }
    .note { margin-top: 1.5rem; border-left: 3px solid var(--accent-2); color: var(--muted); padding: .25rem 0 .25rem 1rem; }
    footer { margin-top: 2rem; color: #7187a3; font-size: .9rem; }
    @media (max-width: 520px) { main { padding-top: 2rem; } .hero { padding-top: 1rem; } }
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <div class="eyebrow">Live infrastructure qualification API</div>
      <h1>Powered-Site Qualifier</h1>
      <p class="subtitle">AI-ready qualification for Bitcoin mining and data-center powered sites.</p>
      <p class="description">Instantly score powered infrastructure opportunities for Bitcoin Mining Readiness, AI / Data Center Readiness, Blockers, Missing Information, and Next Qualification Questions.</p>
      <div class="actions"><a class="button" href="https://github.com/CryptoLeaks/powered-site-qualifier">GitHub Repository</a><a class="button secondary" href="/health">Health Check</a></div>
    </section>

    <section class="grid" aria-label="Service details">
      <article class="card"><h2>Service</h2><ul><li class="status">Live API</li><li>HTTPS enabled</li><li>Hedera x402 testnet payment support</li><li>Public source code</li><li>Current classification example: <span class="status">READY</span></li></ul></article>
      <article class="card"><h2>Main endpoints</h2><div class="endpoint"><span class="method">GET</span><code>/health</code></div><div class="endpoint"><span class="method">GET</span><code>/.well-known/xagent-verification.json</code></div><div class="endpoint"><span class="method">POST</span><code>/v1/qualify</code></div><div class="endpoint"><span class="method">POST</span><code>/v1/paid/qualify</code></div></article>
    </section>

    <section class="card" style="margin-top: 1rem"><h2>Qualification flow</h2><div class="flow"><span>Site Data</span><b class="arrow">↓</b><span>Readiness Analysis</span><b class="arrow">↓</b><span>Bitcoin / AI Scores</span><b class="arrow">↓</b><span>HTTP 402 if paid route</span><b class="arrow">↓</b><span>Hedera x402 Payment</span><b class="arrow">↓</b><span>HTTP 200 + Qualification Result</span></div></section>

    <section class="card" style="margin-top: 1rem"><h2>Hedera payment support</h2><div class="grid"><ul><li>Network: Hedera Testnet</li><li>Payment protocol: x402 v2 exact</li><li>Asset: Native HBAR</li><li>Amount: 0.001 HBAR</li></ul><ul><li>Buyer account: <code>0.0.10488940</code></li><li>Seller account: <code>0.0.10489770</code></li><li>Successful test transaction: <code>0.0.7162784@1789186391.831327025</code></li></ul></div></section>

    <p class="note">This is an initial qualification tool and does not replace engineering, utility, legal, or financial due diligence.</p>
    <footer>Built for fast, transparent qualification of powered infrastructure opportunities.</footer>
  </main>
</body>
</html>"""


def _site_dict(request: SiteQualificationRequest) -> dict[str, Any]:
    data = request.model_dump()
    return {
        "power_ready": data["power_ready_now"], "available_mw": data["available_mw"],
        "energization_rfs_date": data["energization_rfs_date"], "utility_status": data["utility_interconnection_status"],
        "grid_or_gas": data["grid_or_gas_to_power"], "power_price": data["power_price_usd_kwh"],
        "land_size": data["land_size_acres"], "lease_sale_jv": data["lease_sale_jv"],
        "fiber": data["fiber_availability"], "water": data["water_availability"],
        "permitting_status": data["permitting_status"], "expansion_capacity": data["expansion_capacity_mw"],
        "intended_use": data["intended_use"],
    }


@app.get("/", response_class=HTMLResponse)
def landing_page() -> HTMLResponse:
    return HTMLResponse(content=LANDING_PAGE)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "commit": COMMIT}


@app.get("/.well-known/xagent-verification.json")
def verification() -> dict[str, Any]:
    return {"schemaVersion": 1, "slug": SLUG, "commit": COMMIT}


@app.post("/v1/qualify")
def qualify_site(request: SiteQualificationRequest) -> dict[str, Any]:
    return qualify(_site_dict(request))


@app.post("/v1/paid/qualify")
def paid_qualify(raw_request: Request, request: SiteQualificationRequest) -> Any:
    """x402-gated version of the qualification capability."""
    required = payment_required_response()
    payment_header = raw_request.headers.get("PAYMENT-SIGNATURE") or raw_request.headers.get("X-PAYMENT")
    if not payment_header:
        return JSONResponse(
            status_code=402,
            content=required,
            headers={
                "PAYMENT-REQUIRED": encode_payment_required(required),
                "Access-Control-Expose-Headers": "PAYMENT-REQUIRED",
            },
        )
    try:
        payment = verify_and_settle(decode_payment_payload(payment_header))
    except (RuntimeError, ValueError) as exc:
        return JSONResponse(status_code=402, content={"error": "Payment not accepted", "reason": str(exc)})
    result = qualify(_site_dict(request))
    result["x402_payment"] = {
        "network": payment.network,
        "payer": payment.payer,
        "transaction": payment.transaction,
    }
    return JSONResponse(
        status_code=200,
        content=result,
        headers={"PAYMENT-RESPONSE": encode_payment_required(result["x402_payment"])},
    )
