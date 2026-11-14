# Powered-Site Evidence Receipts on NEAR

New hackathon extension to the existing Powered-Site Qualifier. A powered-land or hosting report changes as capacity, tariff and supporting evidence change. Counterparties need to establish whether the report in front of them is the same report the issuer committed to, and whether the issuer withdrew it.

This extension commits a salted SHA-256 digest to an issuer-controlled NEAR contract. It does **not** prove the facts true, customer demand, ownership, deliverability, engineering readiness or availability. NEAR supplies an independently readable timestamped commitment and revocation state, not a diligence oracle.

## Status

- Contract compiles to NEAR WASM.
- Seven JavaScript receipt/contract-host tests and seven original Python qualification tests pass.
- Local demo combines actual qualifier output with receipt generation and tamper detection.
- Full sandbox test written; this environment cannot start NEAR Sandbox because the OS caps file descriptors at 16384 and NEAR requires 65535. No security settings were changed.
- Live NEAR TESTNET contract: `cl-evidence-1794509534759.testnet`. Verified deployment, anchoring and final-RPC readback. Actual qualifier-output integration also passed duplicate rejection and revocation checks. Public synthetic-only proofs are under `evidence/`. Run `node --use-env-proxy verify-live.mjs` for a fresh final read.
- No mainnet deployment, production API modification, X publication or hackathon submission is implied.

## Reproduce

From this directory, with Node 22+ and Python 3.12+:

```sh
npm ci
npm test
npm run build
node demo.mjs
node test/sandbox.mjs
```

`demo.mjs` explicitly labels its simulated receipt. The sandbox test deploys real WASM to a local NEAR chain and checks authorization, immutable receipt IDs, round-trip verification and revocation. It requires the host to support NEAR Sandbox resource limits.

`deploy-testnet.mjs` is an operator-only deployment utility. It creates a dedicated disposable testnet account via the official helper and uses only testnet tokens, then deploys/anchors/reads back. It stores its key outside the extension in ignored `.secrets`, never logs it and never handles a mainnet account. Do not rerun it blindly after partial success; first inspect the transaction/account and existing receipt to avoid duplicate writes.

## Contract

- `anchor({id,digest})`: only contract account itself; random 32-byte ID, SHA-256 digest, append-only.
- `revoke({id})`: issuer only; irreversible revocation flag.
- `get_receipt({id})`: read-only; finality-aware client retrieves it through NEAR RPC.

No transfer/token purchase functionality. Issuer funds storage from its testnet account. Contract ownership is the account key, not a claim of CryptoLeaks identity by itself. Verifiers must obtain the expected issuer account and random receipt ID through their trusted workflow, not accept values supplied by an adversarial report.

The full salted envelope stays off-chain. A 256-bit random salt mitigates brute-force guessing of predictable report fields. An opaque ID prevents publishing a site name/contact. Hashing is not encryption: anyone given the envelope can read it. Never publish private reports, salts, customer documents or contact details into a demo.

## Hackathon provenance

Baseline: `41d099a75d1fca4962b5a5bab731e958125066d7`, repository `CryptoLeaks/powered-site-qualifier`.
Existing Python scoring, FastAPI site, and Hedera x402 implementation predate this extension. Only `near-evidence/` is the new NEAR work. Suggested tracks: realworld, business. No second independent project or prior submission is asserted.

Dependencies: official `near-sdk-js` 2.0.0 (contract toolchain), `near-workspaces` 5.0.0 (sandbox); Node built-in cryptography. Existing project is MIT; dependency licenses remain their own. AI-assisted code. Package-lock pins resolved dependencies. Patched overrides tar 7.5.23 and decode-uri-component 0.5.1 remove high/critical npm audit findings; 16 low findings remain. Build passes with a source-map resolution warning. No claim of production security audit.

## Before submission

Re-read official https://nearhackathon.com/HACKATHON.md. Current development deadline: 2026-11-14 23:59 UTC. Existing projects and testnet implementations qualify under the published rules, but acceptance is the organizers' decision. Public repo must include baseline diff and reproducible demo; local-only demo needs video. User must publish the X demonstration and supply its URL, verify their mainnet prize payout address, contact details/team size/project name and contact consent. Present the exact submission payload for confirmation before POST. Do not invent any user fields or submit twice.
