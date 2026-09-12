# Verification evidence

This preview is local-only. Replace placeholders after an approved public deployment.

## Prerequisites

- Review commit: `f70b48d862d1d78b9f3e25346c44409e5b687a44`
- API base URL: `http://127.0.0.1:8787/v1` for local validation
- Authentication: none locally; public review access must be chosen before deployment

## Health check

```bash
curl --fail --silent --show-error http://127.0.0.1:8787/health
```

Expected response:

```json
{"status":"ok","commit":"<40-character review commit>"}
```

## Deployment proof

```bash
curl --fail --silent --show-error http://127.0.0.1:8787/.well-known/xagent-verification.json
```

Expected response:

```json
{"schemaVersion":1,"slug":"tamer-powered-site-qualifier","commit":"<40-character review commit>"}
```

## Capability call

```bash
curl --fail --silent --show-error \
  --request POST http://127.0.0.1:8787/v1/qualify \
  --header 'content-type: application/json' \
  --data @source/examples/site-ready.json
```

Expected result: HTTP 200 with both readiness scores, positives, missing information, blockers, next questions, and a classification. Unknown fields or negative numeric values return HTTP 422.
