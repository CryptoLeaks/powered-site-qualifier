# Powered-Site Qualifier API

## Capability

Powered-Site Qualifier gives AI agents and infrastructure teams a deterministic first screen for powered sites. It returns separate Bitcoin Mining Readiness and AI/Data Center Readiness scores, evidence gaps, blockers, next questions, and a classification.

It is a screening capability only; it does not replace engineering, utility, legal, permitting, environmental, financial, or investment diligence.

## Live API

- **Base URL:** https://qualifier.cryptoleaks.agency
- **Health:** https://qualifier.cryptoleaks.agency/health
- **Deployment proof:** https://qualifier.cryptoleaks.agency/.well-known/xagent-verification.json
- **Unpaid capability:** `POST https://qualifier.cryptoleaks.agency/v1/qualify`
- **Paid capability:** `POST https://qualifier.cryptoleaks.agency/v1/paid/qualify`
- **Authentication:** x402 payment is required only for the paid route; no buyer credential is accepted by the API.
- **Review commit:** `f70b48d862d1d78b9f3e25346c44409e5b687a44`

The public health and proof endpoints return the exact review commit. The API container is private to Docker; only the HTTPS reverse proxy is public.

## Payment proof

The paid route uses x402 v2 `exact` on Hedera TESTNET with native HBAR asset `0.0.0` and Blocky402 `/verify` and `/settle`. One real proof completed successfully:

- Buyer: `0.0.10488940`
- Seller/pay-to: `0.0.10489770`
- Amount: `100000` tinybars / `0.001` testnet HBAR
- Transaction: `0.0.7162784@1789186391.831327025`
- Blocky402 verify: success
- Blocky402 settle: success
- Final API response: HTTP 200, classification `READY`

Evidence is redacted and included under `source/evidence/hedera-real/`.

## Reproducibility

```bash
cd source
python3 -m unittest discover -s tests -v
docker compose up --build
```

The consuming agent is `source/agent/consume.mjs` and uses the official `@x402/hedera` client. The buyer private key must be provided only through a protected runtime environment when an approved testnet run is performed. It must never be committed, logged, or placed in the API container.

The production deployment configuration is in `source/deploy/`; it uses Caddy for automatic HTTPS, publishes only TCP 80/443, limits the API to one vCPU/one GB RAM, and runs the API non-root with a read-only filesystem and dropped capabilities.

## Source and rights

The complete reviewed source is under `source/`. The public repository name recommended for this package is `powered-site-qualifier`; the GitHub owner/repository URL is intentionally not invented before repository creation.
