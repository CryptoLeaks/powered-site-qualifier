# 90-second demonstration

1. Problem (10s): Powered-site reports get copied and edited. A buyer needs to know whether this is the exact report the issuer committed to, without publishing deal details on a blockchain.
2. Run `node demo.mjs` (20s): show real deterministic qualifier output for fictional inputs, missing data and recommended questions. This step is labelled local simulation.
3. Run `node --use-env-proxy verify-live.mjs` (20s): show final NEAR testnet block hash, issuer, digest and verification result from live RPC. It is a TESTNET receipt for a fictional demonstration, not a claim about live site availability.
4. Show the tampered-envelope unit test (15s): changing one report field makes the check fail.
5. Show the testnet integration proof (15s): append-only receipts reject duplicates; issuer can revoke; latest final state marks revoked reports invalid.
6. Limitation (10s): It proves report integrity and issuer commitment, not truth of capacity, price, ownership or customer demand. Private files stay off-chain.

Do not include credential files, keys, customer documents, contact names or non-public locations in recordings.

Draft X text, for human review/publication only after final demo:

Built at NEAR HACKATHON: Powered-Site Evidence Receipts. We help counterparties check whether a mining / data-center qualification report is unchanged and still valid, without putting deal details on-chain. NEAR testnet records the issuer's salted hash and revocation status. Integrity is not proof of site readiness. Demo + source: [add verified links]. @NEARProtocol #NEARHackathon
