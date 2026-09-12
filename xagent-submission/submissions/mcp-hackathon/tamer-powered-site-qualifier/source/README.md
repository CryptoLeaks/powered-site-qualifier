# Powered-Site Qualifier API

Production-style deterministic API for an initial powered-site qualification. It returns separate Bitcoin Mining and AI/Data Center readiness scores, evidence gaps, blockers, next questions, and a classification.

This project uses general infrastructure qualification heuristics informed by Tamer's domain expertise. It contains no confidential client/site data.

## Endpoints

* `GET /health` — X-Agent health/version binding.
* `GET /.well-known/xagent-verification.json` — X-Agent deployment proof.
* `POST /v1/qualify` — score a site.
* `GET /docs` — FastAPI OpenAPI UI.

The supplied Compose file binds to loopback only. No public port is opened.

## Run locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export XAGENT_REVIEW_COMMIT=local-development
uvicorn app.main:app --host 127.0.0.1 --port 8787
```

The placeholder commit must be replaced by the exact 40-character reviewed Git commit before any X-Agent submission or public deployment.

```bash
curl -sS http://127.0.0.1:8787/v1/qualify \
  -H 'content-type: application/json' \
  -d @examples/site-ready.json
```

The scoring engine is pure, deterministic, explainable, and has no database or outbound calls. Unknown fields are not guessed: they become missing information and may create blockers.

## Docker

```bash
docker compose up --build
```

The Compose file publishes `127.0.0.1:8787:8787`, with no host networking, privileged mode, Docker socket, host filesystem mount, or secret.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

This project is local preparation only. It is not an X-Agent submission, public deployment, GitHub PR, or externally registered service.
