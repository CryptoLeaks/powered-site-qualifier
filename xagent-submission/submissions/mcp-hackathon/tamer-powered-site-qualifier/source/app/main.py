from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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
