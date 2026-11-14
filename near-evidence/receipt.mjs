import {createHash, randomBytes} from 'node:crypto';
// Canonicalize JSON without losing key order. Reject non-JSON values and floats
// that cannot be represented reproducibly. Input is parsed from JSON.
export function canonical(value) {
  if(value === null || typeof value === 'boolean' || typeof value === 'string') return JSON.stringify(value);
  if(typeof value === 'number' && Number.isFinite(value)) return JSON.stringify(value);
  if(Array.isArray(value)) return '['+value.map(canonical).join(',')+']';
  if(value && Object.getPrototypeOf(value) === Object.prototype) return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',')+'}';
  throw new Error('Unsupported non-JSON value');
}
export function digest(envelope) { return createHash('sha256').update(canonical(envelope)).digest('hex'); }
export function prepare(report, sourceCommit) {
  if(!/^[a-f0-9]{40}$/.test(sourceCommit)) throw new Error('Exact source commit required');
  const envelope={schema:'cryptoleaks.qualification.receipt.v1', salt:randomBytes(32).toString('hex'), sourceCommit, report};
  return {envelope, anchor:{id:randomBytes(32).toString('hex'), digest:digest(envelope)}};
}
export function verify(envelope, receipt, expectedIssuer, expectedId) {
  if(!receipt || receipt.id!==expectedId || receipt.issuer!==expectedIssuer) return {valid:false, reason:'Unknown receipt or wrong issuer'};
  if(receipt.revoked !== false) return {valid:false, reason:'Revoked or invalid status'};
  if(receipt.digest!==digest(envelope)) return {valid:false, reason:'Report changed'};
  return {valid:true, reason:'Exact report matches issuer commitment. Facts are NOT independently verified.'};
}
export async function readReceipt({contract,id,rpc='https://rpc.testnet.near.org'}) {
  if(!contract.endsWith('.testnet')) throw new Error('Testnet account required');
  if(!/^[a-f0-9]{64}$/.test(id)) throw new Error('Invalid receipt ID');
  const response=await fetch(rpc,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({jsonrpc:'2.0',id:'receipt',method:'query',params:{request_type:'call_function',finality:'final',account_id:contract,method_name:'get_receipt',args_base64:Buffer.from(JSON.stringify({id})).toString('base64')}})});
  if(!response.ok) throw new Error('RPC HTTP '+response.status);
  const data=await response.json();
  if(data.error || !Array.isArray(data.result?.result)) throw new Error('RPC returned no verified result');
  return {receipt:JSON.parse(Buffer.from(data.result.result).toString('utf8')),blockHash:data.result.block_hash,blockHeight:data.result.block_height};
}
