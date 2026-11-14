import {test} from 'node:test';
import assert from 'node:assert/strict';
import {canonical,prepare,verify,digest,readReceipt} from '../receipt.mjs';
const source='41d099a75d1fca4962b5a5bab731e958125066d7';
test('canonical JSON key order',()=>assert.equal(canonical({b:2,a:1}),canonical({a:1,b:2})));
test('nonfinite and undefined rejected',()=>{assert.throws(()=>canonical(NaN)); assert.throws(()=>canonical({a:undefined}));});
test('same report salted independently',()=>assert.notEqual(prepare({available_mw:20},source).anchor.digest,prepare({available_mw:20},source).anchor.digest));
test('valid, tampered, revoked, missing, wrong issuer/id',()=>{
const {envelope,anchor}=prepare({available_mw:20},source);const receipt={...anchor,issuer:'demo.testnet',revoked:false};
assert.equal(verify(envelope,receipt,'demo.testnet',anchor.id).valid,true);
assert.equal(verify({...envelope,report:{available_mw:21}},receipt,'demo.testnet',anchor.id).valid,false);
assert.equal(verify(envelope,{...receipt,revoked:true},'demo.testnet',anchor.id).valid,false);
assert.equal(verify(envelope,null,'demo.testnet',anchor.id).valid,false);
assert.equal(verify(envelope,receipt,'evil.testnet',anchor.id).valid,false);
assert.equal(verify(envelope,receipt,'demo.testnet','bad').valid,false);
});
test('testnet-only RPC protection',async()=>await assert.rejects(readReceipt({contract:'test.near',id:'a'.repeat(64)})));
test('source revision required',()=>assert.throws(()=>prepare({},'main')));
