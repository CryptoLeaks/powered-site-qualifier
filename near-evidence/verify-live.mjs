import fs from 'node:fs';
import {readReceipt,verify} from './receipt.mjs';
const path=process.argv[2]||'evidence/demo-envelope.json';
const {envelope,anchor}=JSON.parse(fs.readFileSync(path));
const contract='cl-evidence-1794509534759.testnet';
const result=await readReceipt({contract,id:anchor.id});
console.log(JSON.stringify({...result,verification:verify(envelope,result.receipt,contract,anchor.id)},null,2));
