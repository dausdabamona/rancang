import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
import {spawn} from 'node:child_process'; import {createRequire} from 'node:module'; import {fileURLToPath} from 'node:url';
import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
const akar = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const json = r => JSON.parse(r.content[0].text);
const dir = process.argv[2], files = fs.readdirSync(dir).filter(f => f.endsWith('.rancang'));
const data = fs.mkdtempSync(path.join(os.tmpdir(), 'cb-'));
const app = spawn(require('electron'), [akar, path.join(dir, files[0]), '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'], {env: {...process.env, RANCANG_DATA_DIR: data}, stdio: 'ignore'});
const c = new Client({name: 'v', version: '1'});
await c.connect(new StdioClientTransport({command: process.execPath, args: [path.join(akar, 'build/mcp/server/index.mjs')], env: {...process.env, RANCANG_DATA_DIR: data}}));
let info; for (let i = 0; i < 120 && !(info && info.aplikasiBerjalan); i++) { await new Promise(r => setTimeout(r, 500)); try { info = json(await c.callTool({name: 'info_proyek', arguments: {}})); } catch { info = null; } }
const hasil = {};
for (const f of files) {
  await c.callTool({name: 'buka_proyek', arguments: {jalur: path.join(dir, f)}});
  await new Promise(r => setTimeout(r, 1500));
  const rab = json(await c.callTool({name: 'volume_rab', arguments: {}}));
  const db = json(await c.callTool({name: 'daftar_besi', arguments: {}}));
  hasil[f] = {rab: Object.fromEntries(rab.flatMap(dv => dv.baris).filter(b => /^Pembesian/.test(b.uraian)).map(b => [b.uraian.split(' ')[1], b.vol])),
    daftar: Object.fromEntries((db.perDiameter || []).map(x => [x.besi, x.beratDenganSisaKg])), baris: db.baris ? db.baris.length : db.jumlahBaris, tipe: (db.tipe || []).map(t => t.kode).join(' '), catatan: db.catatan};
}
console.log(JSON.stringify(hasil));
app.kill(); process.exit(0);
