# Powered-Site Qualifier API

## Capability

- **One-line description:** Scores a powered site for Bitcoin-mining and AI/data-center readiness from initial qualification inputs.
- **Who it helps:** Infrastructure developers, site owners, power developers, and agents triaging early site opportunities.
- **Capability boundary:** Deterministic screening only. It does not replace engineering, utility, legal, permitting, environmental, financial, or investment diligence.

## Live API

- **API base URL:** Not public; local validation only.
- **Health-check URL:** `http://127.0.0.1:8787/health` during local validation.
- **Authentication:** None locally; public deployment authentication/rate limiting remains to be configured.
- **Rate limits / known limits:** No database or persistence; one request is scored synchronously. Public limits must be added before exposure.
- **API contract:** `source/API-SCHEMA.md` and the generated `/docs` endpoint.

## Source and reproducibility

- **Source repository:** Not yet created or published.
- **Review commit:** `REPLACE_WITH_CORE_REVIEW_COMMIT`
- **Source submitted in this preview:** `source/`
- **Run tests:** `.venv/bin/python -m unittest discover -s tests -v`
- **Run locally:** `XAGENT_REVIEW_COMMIT=<review-commit> .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8787`
- **Deploy:** Build `docker build -t powered-site-qualifier:<review-commit> .`; run with the documented loopback-only Compose profile.
- **Version binding:** `XAGENT_REVIEW_COMMIT` is returned by `/health` and `/.well-known/xagent-verification.json`.

The service must expose the exact reviewed commit in both proof responses before public submission.

## Verification

See `verification/README.md` for local health, proof, capability, and invalid-input calls.

## Security and data handling

- No confidential site or client data is included.
- No secrets, wallets, private keys, payment integrations, database, outbound scoring calls, shell execution, or remote downloads.
- See `source/SECURITY.md` for container and deployment restrictions.

## Support

- **Team / builder:** Tamer / Horse Lab
- **Contact:** To be supplied through the approved private review channel before submission.
- **License / rights:** To be finalized before external submission; all submitted source and examples must be authorized for review.
