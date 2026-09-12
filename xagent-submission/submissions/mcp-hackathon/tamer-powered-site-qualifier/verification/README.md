# Verification evidence

## Public prerequisites

- API base URL: `https://qualifier.cryptoleaks.agency/v1`
- Review commit: `f70b48d862d1d78b9f3e25346c44409e5b687a44`
- No API key is required for the health, proof, or unpaid capability checks.

## Health check

```bash
curl --fail --silent --show-error \
  https://qualifier.cryptoleaks.agency/health
```

Expected:

```json
{"status":"ok","commit":"f70b48d862d1d78b9f3e25346c44409e5b687a44"}
```

## Deployment proof

```bash
curl --fail --silent --show-error \
  https://qualifier.cryptoleaks.agency/.well-known/xagent-verification.json
```

Expected:

```json
{"schemaVersion":1,"slug":"tamer-powered-site-qualifier","commit":"f70b48d862d1d78b9f3e25346c44409e5b687a44"}
```

## Unpaid capability

```bash
curl --fail --silent --show-error \
  --request POST https://qualifier.cryptoleaks.agency/v1/qualify \
  --header 'content-type: application/json' \
  --data @source/examples/site-ready.json
```

Expected result: HTTP 200, both readiness scores, and classification `READY`.

## Paid boundary without payment

```bash
curl --silent --show-error --include \
  --request POST https://qualifier.cryptoleaks.agency/v1/paid/qualify \
  --header 'content-type: application/json' \
  --data @source/examples/site-ready.json
```

Expected result: HTTP 402 with x402 v2 `exact`, `hedera:testnet`, native HBAR asset `0.0.0`, and the configured amount/pay-to/fee-payer fields. Do not attach a payment header during this check.
