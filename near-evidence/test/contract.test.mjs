import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
test('contract issuer controls and append-only semantics (mock host)',async()=>{
 const state=new Map();let input='',out='',caller='issuer.testnet';
 globalThis.__nearTest={input:()=>input,currentAccountId:()=> 'issuer.testnet',predecessorAccountId:()=>caller,storageRead:k=>state.get(k)??null,storageWrite:(k,v)=>state.set(k,v),blockTimestamp:()=>123n,valueReturn:v=>out=v};
 const source=fs.readFileSync('contract.js','utf8').replace("import { near } from 'near-sdk-js';",'const near=globalThis.__nearTest;');
 const contract=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
 input=JSON.stringify({id:'a'.repeat(64),digest:'b'.repeat(64)});
 caller='attacker.testnet';assert.throws(()=>contract.anchor(),/Issuer only/);caller='issuer.testnet';
 contract.anchor();assert.equal(JSON.parse(out).digest,'b'.repeat(64));assert.throws(()=>contract.anchor(),/already exists/);
 caller='attacker.testnet';assert.throws(()=>contract.revoke(),/Issuer only/);caller='issuer.testnet';contract.revoke();assert.equal(JSON.parse(out).revoked,true);
 input=JSON.stringify({id:'x'});assert.throws(()=>contract.get_receipt());
 input=JSON.stringify({id:'c'.repeat(64)});contract.get_receipt();assert.equal(JSON.parse(out),null);
 delete globalThis.__nearTest;
});
