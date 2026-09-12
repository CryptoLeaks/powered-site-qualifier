# ETHOnline / X-Agent demo script (under five minutes)

1. **Problem (0:00–0:30):** Infrastructure developers and AI agents need a fast, explainable first screen for powered sites before expensive diligence.
2. **Product (0:30–1:00):** Powered-Site Qualifier accepts structured site facts and returns separate Bitcoin-mining and AI/data-center readiness scores, evidence gaps, blockers, next questions, and a classification.
3. **Unpaid API (1:00–1:40):** Open `https://qualifier.cryptoleaks.agency/health`, `https://qualifier.cryptoleaks.agency/.well-known/xagent-verification.json`, then call `POST https://qualifier.cryptoleaks.agency/v1/qualify` with `examples/site-ready.json`. Show the deterministic `READY` result and the exact reviewed commit.
4. **Paid boundary (1:40–2:20):** Call `POST https://qualifier.cryptoleaks.agency/v1/paid/qualify` without payment. Show HTTP 402 and the x402 v2 `exact` Hedera TESTNET requirement: native HBAR `0.0.0`, `100000` tinybars, seller account, and Blocky402 fee payer.
5. **Payment proof (2:20–3:20):** Explain that the official `@x402/hedera` consuming agent signed one TESTNET payment locally, Blocky402 verified and settled it, and Hedera Mirror Node confirmed the successful transaction. Show only the redacted proof file; never show the key or signed payload.
6. **Paid result (3:20–4:00):** Retry the request with the payment client and show HTTP 200 with classification `READY`, plus the two readiness scores and no blockers.
7. **Usefulness (4:00–4:40):** Agents can pay per qualification request, receive machine-readable diligence gaps, and route promising mining/data-center opportunities to human engineering, utility, legal, and financial review.
8. **Safety (4:40–5:00):** State that the deployed API uses HTTPS, loopback/private container networking, seller-only payment configuration, body limits, security headers, rotated logs, and no buyer key.

Do not repeat the real payment during the demo without explicit approval; use the recorded redacted proof or a controlled testnet run approved separately.
