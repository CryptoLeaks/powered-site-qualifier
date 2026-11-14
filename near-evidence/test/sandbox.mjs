import {Worker} from 'near-workspaces';
import assert from 'node:assert/strict';
import {prepare,verify} from '../receipt.mjs';
const worker=await Worker.init();
try {
 const contract=await worker.rootAccount.devDeploy('build/contract.wasm');
 const attacker=await worker.rootAccount.createSubAccount('attacker');
 const {envelope,anchor}=prepare({available_mw:20,fictional:true},'41d099a75d1fca4962b5a5bab731e958125066d7');
 await assert.rejects(attacker.call(contract,'anchor',anchor));
 await contract.call(contract,'anchor',anchor);
 const stored=await contract.view('get_receipt',{id:anchor.id});
 assert.equal(verify(envelope,stored,contract.accountId,anchor.id).valid,true);
 assert.equal(verify({...envelope,report:{available_mw:99}},stored,contract.accountId,anchor.id).valid,false);
 await assert.rejects(contract.call(contract,'anchor',anchor));
 await assert.rejects(attacker.call(contract,'revoke',{id:anchor.id}));
 await contract.call(contract,'revoke',{id:anchor.id});
 const revoked=await contract.view('get_receipt',{id:anchor.id});
 assert.equal(verify(envelope,revoked,contract.accountId,anchor.id).valid,false);
 assert.equal(await contract.view('get_receipt',{id:'b'.repeat(64)}),null);
 console.log(JSON.stringify({network:'LOCAL NEAR SANDBOX, NOT TESTNET',contract:contract.accountId,stored,revoked,checks:['issuer-only anchoring','round-trip matching','tamper rejection','duplicate rejection','issuer-only revocation','revoked rejection','missing lookup']},null,2));
} finally {await worker.tearDown();}
