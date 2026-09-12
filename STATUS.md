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

The x402 implementation commit is `306a8b2c0828eb65e7e51e4f2725057b00ef536d`. The repository remains local and clean.

## Real Hedera testnet proof gate

Read-only Blocky402 check completed on 2026-09-12:

* Endpoint: `https://api.testnet.blocky402.com/supported`
* Result: Hedera testnet advertised.
* Result: x402 v2 `exact` advertised.
* Result: facilitator fee payer `0.0.7162784` advertised.
* Result: no testnet API key required according to the current Blocky402 documentation.
* Native HBAR route: selected using asset `0.0.0`, which is documented by the official Hedera x402 mechanism.

Stopped before account creation because the official Hedera Portal requires an authenticated interactive session that is not available in this workspace. No buyer/seller keys, accounts, `.secrets` file, faucet request, facilitator call, transaction, or real evidence were created. No assumptions were substituted for the missing portal access.

## Local verification

Scoring, API, container, x402 mock-flow, and example-contract verification completed with:

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

The same qualification endpoint now has a local x402 wrapper. Minimum additional work is:

1. Use the real Hedera testnet and Blocky402 facilitator/testnet flow.
2. Run the consuming agent with a dedicated testnet identity and payment proof.
4. Create only the minimum testnet identity/funding after explicit approval; no wallet or secret exists in this project now.
5. Demonstrate at least one successful paid request and settlement, with redacted evidence.
6. Add the public GitHub/demo links and any exact ETHGlobal submission artifacts required by the live bounty page.

Official references checked: [X-Agent repository](https://github.com/xagentAI/xagt-plugin), [X-Agent submission guide](https://github.com/xagentAI/xagt-plugin/blob/main/docs/agent-submission-guide.md), [ETHOnline 2026 Hedera bounty page](https://ethglobal.com/events/ethonline2026/prizes/hedera), [Hedera x402 overview](https://hedera.com/blog/hedera-and-the-x402-payment-standard/), and [Blocky402 API reference](https://blocky402.com/docs/api-reference/).

## Not done and explicitly stopped

* No Hedera account, wallet, or private key created.
* No public port or firewall rule opened.
* No real/testnet payment or facilitator call made.
* No Blocky402 registration or external account created.
* No GitHub fork, branch, push, PR, or X-Agent submission.
* No public deployment or HTTPS endpoint.
* No real paid-request evidence or demo video.

## Before submission

1. Obtain approval for two dedicated Hedera testnet accounts and protected runtime secret handling.
2. Confirm Blocky402 `/supported` and testnet faucet availability immediately before testing.
3. Run one real paid request and capture redacted evidence.
4. Deploy only after explicit approval, with HTTPS and a fixed public API URL.
5. Set the exact deployed commit in `/health` and proof verification.
6. Prepare public GitHub/demo artifacts and submit only after explicit authorization.

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

Current estimated ETHOnline/Hedera readiness: 45%. Local implementation and mock evidence are ready; the mandatory real testnet payment, public service, public repository, and demo remain outstanding.
