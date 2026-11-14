import { near } from 'near-sdk-js';

// Single issuer: only this contract account may mutate its evidence registry.
// No documents, prices, contacts, or site addresses are accepted on-chain.
function args() { return JSON.parse(near.input() || '{}'); }
function validId(id) { if (!/^[a-f0-9]{64}$/.test(id)) throw new Error('Expected 32-byte random receipt ID'); }
function owner() { if (near.predecessorAccountId() !== near.currentAccountId()) throw new Error('Issuer only'); }
function key(id) { validId(id); return 'receipt:' + id; }
function load(id) { const v = near.storageRead(key(id)); return v ? JSON.parse(v) : null; }
function output(v) { near.valueReturn(JSON.stringify(v)); }
export function anchor() {
  owner();
  const {id, digest} = args();
  validId(id);
  if (!/^[a-f0-9]{64}$/.test(digest)) throw new Error('Invalid SHA-256 digest');
  if (load(id)) throw new Error('Receipt already exists');
  const receipt = {id, digest, issuer: near.currentAccountId(), anchored_at_ns: near.blockTimestamp().toString(), revoked: false};
  near.storageWrite(key(id), JSON.stringify(receipt));
  output(receipt);
}
export function revoke() {
  owner();
  const {id} = args();
  const receipt = load(id);
  if (!receipt) throw new Error('Receipt not found');
  receipt.revoked = true;
  near.storageWrite(key(id), JSON.stringify(receipt));
  output(receipt);
}
export function get_receipt() { output(load(args().id)); }
