import {connect,keyStores,KeyPair} from 'near-api-js';
import fs from 'node:fs';
import {prepare,verify,readReceipt} from './receipt.mjs';
const secretFile='../.secrets/near-hackathon-testnet.json';
let secret;
if(fs.existsSync(secretFile)){secret=JSON.parse(fs.readFileSync(secretFile,'utf8'));}else{
 const key=KeyPair.fromRandom('ed25519');
 secret={accountId:'cl-evidence-'+Date.now()+'.testnet',privateKey:key.toString()};
 fs.writeFileSync(secretFile,JSON.stringify(secret),{mode:0o600});
}
const key=KeyPair.fromString(secret.privateKey);
const ks=new keyStores.InMemoryKeyStore();await ks.setKey('testnet',secret.accountId,key);
const near=await connect({networkId:'testnet',nodeUrl:'https://rpc.testnet.near.org',keyStore:ks});
const account=await near.account(secret.accountId);
try{await account.state();}catch(e){
 if(e.type!=='AccountDoesNotExist'&&!String(e).includes('UNKNOWN_ACCOUNT')) throw e;
 const response=await fetch('https://helper.testnet.near.org/account',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({newAccountId:secret.accountId,newAccountPublicKey:key.getPublicKey().toString()}),signal:AbortSignal.timeout(30000)});
 if(!response.ok)throw new Error('Official testnet helper: HTTP '+response.status+' '+(await response.text()).slice(0,300));
 await account.state();
}
console.log('Account ready:',secret.accountId);
const deploy=await account.deployContract(fs.readFileSync('build/contract.wasm'));
console.log('Deploy:',deploy.transaction.hash);
const proofFile='build/testnet-envelope.private.json';
const prepared=fs.existsSync(proofFile)?JSON.parse(fs.readFileSync(proofFile)):prepare({fictional:true,available_mw:20,qualification:'demo, not live site'},'41d099a75d1fca4962b5a5bab731e958125066d7');
fs.writeFileSync(proofFile,JSON.stringify(prepared),{mode:0o600});
const anchored=await account.functionCall({contractId:secret.accountId,methodName:'anchor',args:prepared.anchor,gas:30000000000000n,attachedDeposit:0n});
const chain=await readReceipt({contract:secret.accountId,id:prepared.anchor.id});
const result=verify(prepared.envelope,chain.receipt,secret.accountId,prepared.anchor.id);
if(!result.valid)throw new Error('Readback failed');
fs.writeFileSync('build/testnet-proof.json',JSON.stringify({network:'NEAR TESTNET',accountId:secret.accountId,deploymentTx:deploy.transaction.hash,anchorTx:anchored.transaction.hash,...chain,verification:result},null,2));
console.log(JSON.stringify(result));
