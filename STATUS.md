# Progress status

Date: 2026-09-12

## Current state

Local project prepared under `/opt/horse-lab/agents/xagent-powered-site`.

Implemented:

* FastAPI application with `POST /v1/qualify`.
* `GET /health` returning `{"status":"ok","commit":...}`.
* `GET /.well-known/xagent-verification.json` returning schema version, slug, and commit.
* Deterministic, explainable Bitcoin Mining and AI/Data Center scoring.
* Explicit missing-information, blocker, next-question, and classification output.
* Pydantic request validation with unknown-field rejection.
* Dockerfile and loopback-only Docker Compose configuration.
* Examples, API schema, README, and unit tests.

Build phase completed on 2026-09-12:

* Isolated `.venv` created with pinned `requirements.txt` and generated `requirements.lock.txt`.
* FastAPI/Uvicorn API smoke tests passed on `127.0.0.1:8787`.
* Docker image `powered-site-qualifier:local-review` built successfully.
* Container smoke tests passed on `127.0.0.1:8787` with 1 CPU, 1 GiB RAM, read-only rootfs, dropped capabilities, no privileged mode, no host networking, no host mounts, and no Docker socket.
* The service performs normal scoring without an external network dependency; scoring code uses local deterministic logic only.
* X-Agent preview package prepared under `xagent-submission/submissions/mcp-hackathon/tamer-powered-site-qualifier/`.

## Hedera x402 phase

Implemented locally, without accounts or payment execution:

* `POST /v1/paid/qualify` with x402 v2 `402` challenge and `PAYMENT-REQUIRED` header.
* Hedera testnet `exact` native-HBAR requirements (`hedera:testnet`, asset `0.0.0`, default `100000` tinybars).
* Remote facilitator adapter for Blocky402 `/verify` and `/settle`, fail-closed unless `X402_MODE=remote` and seller configuration are present.
* Explicit local mock mode and Python consuming client.
* Future real-testnet Node consuming client using official `@x402/hedera` and `@x402/fetch` packages.
* `.env.example`, evidence structure, architecture, wallet approval gate, and bounty checklist in `HEDERA-X402.md`.

Local mock flow passed: initial HTTP `402`, Hedera testnet payment requirement, consuming-agent retry, HTTP `200`, and `READY` qualification. No facilitator request or Hedera transaction was made.

## Local verification

Dependency-free scoring, API, container, and example-contract verification completed with:

```text
Ran 3 tests in 0.000s
OK
```

The ready example returned Bitcoin `100`, AI/data-center `100`, and `READY`. API and container checks also returned HTTP 422 for unknown fields and negative numeric input.

The project-local virtual environment contains only the pinned application dependency set. The host system Python was not modified.

## X-Agent rules verified

Official repository: `https://github.com/xagentAI/xagt-plugin`

Submission directory: `submissions/mcp-hackathon/<team-or-builder>-<project-slug>/`

Required artifacts: `SUBMISSION.md`, `submission.json`, `RIGHTS.md`, complete source under `source/`, and `verification/README.md`.

The public API must expose the exact reviewed 40-character commit at `/health`, plus same-origin `/.well-known/xagent-verification.json` with schema version, slug, and commit. A deployed API, pinned public commit, public source, reproducible instructions, and one real API call are required.

The official event page states the registration/build/submission period is September 2–19, 2026, with technical review September 20–October 1 and winners October 2–4.

## ETHOnline / Hedera x402 adaptation boundary

The same qualification endpoint can be wrapped later, but payment work is intentionally not implemented. Minimum additional work is:

1. Add an x402 HTTP 402 payment wrapper around a paid qualification route.
2. Use Hedera testnet and Blocky402’s facilitator/testnet flow.
3. Add a consuming agent that discovers/calls the endpoint and supplies payment proof.
4. Create only the minimum testnet identity/funding after explicit approval; no wallet or secret exists in this project now.
5. Demonstrate at least one successful paid request and settlement, with redacted evidence.
6. Add the public GitHub/demo links and any exact ETHGlobal submission artifacts required by the live bounty page.

Official references checked: [X-Agent repository](https://github.com/xagentAI/xagt-plugin), [X-Agent submission guide](https://github.com/xagentAI/xagt-plugin/blob/main/docs/agent-submission-guide.md), [ETHOnline 2026 Hedera bounty page](https://ethglobal.com/events/ethonline2026/prizes/hedera), [Hedera x402 overview](https://hedera.com/blog/hedera-and-the-x402-payment-standard/), and [Blocky402 API reference](https://blocky402.com/docs/api-reference/).

## Not done and explicitly stopped

* No dependencies installed, API server started, Docker image built, or container run.
* No public port or firewall rule opened.
* No wallet, key, payment integration, or external registration.
* No GitHub fork, branch, push, PR, or X-Agent submission.
* No public deployment or HTTPS endpoint.
* No testnet wallet, Hedera account, Blocky402 registration, real paid-request evidence, public deployment, or external submission.

## Before submission

1. Install/build dependencies in an approved isolated environment or build the Docker image.
2. Run unit tests and local API smoke tests.
3. Create a local Git commit and verify all source files.
4. Deploy only after explicit approval, with HTTPS and a fixed public API URL.
5. Set the exact deployed 40-character commit in `/health` and verification proof.
6. Prepare X-Agent submission artifacts and rights declaration.
7. Submit a PR only after explicit authorization.

## Local review binding

The exact core-service review commit is `f70b48d862d1d78b9f3e25346c44409e5b687a44`. It is inserted into the X-Agent preview metadata. The local runtime must receive it through `XAGENT_REVIEW_COMMIT`; the public deployment must expose the same 40-character value from both proof endpoints.

## Deployment proposal, not executed

* Application: container on internal `127.0.0.1:8787`.
* Reverse proxy: Caddy or Nginx on the VPS, terminating HTTPS on external TCP 443 and proxying to `127.0.0.1:8787`.
* Authentication: initially a short-lived review credential or API key, plus rate limiting; do not expose an unauthenticated production endpoint.
* Firewall: allow only 443 (and administrative access already approved); no firewall change has been made.

## Priority

1. ETHOnline/Hedera deadline: freeze the base API, decide the paid route, then implement and test the x402/Blocky402/Hedera testnet wrapper and consuming agent.
2. X-Agent deadline: deploy the same core service only after the payment branch is stable or keep the X-Agent submission on the unpaid core API; verify the exact reviewed commit and prepare the public submission package before September 19.
