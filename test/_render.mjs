import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
import {spawn} from 'node:child_process'; import {createRequire} from 'node:module'; import {fileURLToPath} from 'node:url';
import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
const akar = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const json = r => JSON.parse(r.content[0].text);
const [f, keluar, ...jenis] = process.argv.slice(2);
const data = fs.mkdtempSync(path.join(os.tmpdir(), 'rr-'));
const app = spawn(require('electron'), [akar, f, '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'], {env: {...process.env, RANCANG_DATA_DIR: data}, stdio: 'ignore'});
const c = new Client({name: 'v', version: '1'});
await c.connect(new StdioClientTransport({command: process.execPath, args: [path.join(akar, 'build/mcp/server/index.mjs')], env: {...process.env, RANCANG_DATA_DIR: data}}));
let info; for (let i = 0; i < 120 && !(info && info.aplikasiBerjalan); i++) { await new Promise(r => setTimeout(r, 500)); try { info = json(await c.callTool({name: 'info_proyek', arguments: {}})); } catch { info = null; } }
for (const j of jenis) {
  const r = await c.callTool({name: 'gambar_2d', arguments: {jenis: j, format: 'png', kertas: 'A3'}});
  const img = r.content.find(x => x.type === 'image');
  if (img) fs.writeFileSync(path.join(keluar, j.replace(/[:@#+]/g, '_') + '.png'), Buffer.from(img.data, 'base64'));
  else console.log(j, JSON.stringify(r.content).slice(0, 300));
}
app.kill(); process.exit(0);
