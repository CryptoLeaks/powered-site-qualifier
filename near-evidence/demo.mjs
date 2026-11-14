import {spawnSync} from 'node:child_process';
import {prepare,verify} from './receipt.mjs';
const p=spawnSync('python3',['-c',`import json,sys;sys.path.insert(0,'..');from app.scoring import qualify;print(json.dumps(qualify({'available_mw':20,'power_ready':True,'power_price':0.055,'intended_use':'both'})))`],{encoding:'utf8'});
if(p.status!==0) throw new Error(p.stderr);
const prepared=prepare(JSON.parse(p.stdout),'41d099a75d1fca4962b5a5bab731e958125066d7');
const simulated={...prepared.anchor,issuer:'demo.testnet',revoked:false};
console.log(JSON.stringify({mode:'LOCAL SIMULATION ONLY; NOT ON-CHAIN',qualification:prepared.envelope.report,anchor:prepared.anchor,original:verify(prepared.envelope,simulated,'demo.testnet',prepared.anchor.id),tampered:verify({...prepared.envelope,report:{...prepared.envelope.report,classification:'ALTERED'}},simulated,'demo.testnet',prepared.anchor.id)},null,2));
