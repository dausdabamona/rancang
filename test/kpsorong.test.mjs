// Uji model Dermaga KP Sorong (v0.41): tiang miring, selimut tiang, timbunan causeway, profil dasar laut, dan gambar.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
import {modelKPSorong} from './model-kpsorong.mjs';

const akar = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const serverMcp = path.join(akar, 'build', 'mcp', 'server', 'index.mjs');
const require = createRequire(import.meta.url);
const json = r => JSON.parse(r.content[0].text);

test('dermaga KP Sorong: tiang miring, selimut, causeway', {skip: process.env.RANCANG_UJI_ELECTRON !== '1'}, async () => {
  const m = modelKPSorong();
  const data = fs.mkdtempSync(path.join(os.tmpdir(), 'rancang-kps-')), proyek = path.join(data, 'kps.rancang');
  fs.writeFileSync(proyek, JSON.stringify({format: 'rancang-proyek', versi: 1, aplikasi: 'RANCANG', setel: m.setel, elemen: {}, grup: m.grup, komponen: {}, kusen: {}}));
  const argv = [akar, proyek, '--use-angle=swiftshader', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'];
  if (process.platform === 'linux') argv.push('--no-sandbox');
  const app = spawn(require('electron'), argv, {env: {...process.env, RANCANG_DATA_DIR: data}, stdio: 'ignore'});
  const c = new Client({name: 'uji-kps', version: '1.0.0'});
  await c.connect(new StdioClientTransport({command: process.execPath, args: [serverMcp], env: {...process.env, RANCANG_DATA_DIR: data}, stderr: 'inherit'}));
  const keluar = process.env.RANCANG_UJI_KELUAR || os.tmpdir();
  try {
    let info = null;
    for (let i = 0; i < 120 && !(info && info.aplikasiBerjalan); i++) {
      await new Promise(r => setTimeout(r, 500));
      try { info = json(await c.callTool({name: 'info_proyek', arguments: {}})); } catch { info = null; }
    }
    assert.ok(info && info.aplikasiBerjalan, 'aplikasi tidak siap');
    const ubah = Object.entries(m.elemen).map(([id, d]) => ({id, data: d}));
    const r = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: ubah}}));
    assert.equal(r.ok, true, JSON.stringify(r).slice(0, 400));
    // penolakan: miring di luar 1..50, selimut atas < bawah, timbunan tanpa lebar
    for (const d of [
      {jenis: 'tiang', bahan: 'baja', x: 0, y: 0, dLuar: 406.4, tebal: 12, panjang: 10, zKepala: 2, miring: {n: 80, arah: 0}},
      {jenis: 'tiang', bahan: 'baja', x: 0, y: 0, dLuar: 406.4, tebal: 12, panjang: 10, zKepala: 2, selimut: {atas: -1, bawah: 1, tebal: 0.1}},
      {jenis: 'timbunan', awal: {x: 0, y: 0}, akhir: {x: 5, y: 0}, lebarAtas: 0, zAtas: 3, talud: 2}]) {
      const s = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: d.jenis === 'tiang' ? 'Z999' : 'U999', data: d}]}}));
      assert.equal(s.ok, false, JSON.stringify(d));
    }
    const rab = json(await c.callTool({name: 'volume_rab', arguments: {}}));
    fs.writeFileSync(path.join(keluar, 'kps-rab.json'), JSON.stringify(rab, null, 1));
    const dm = rab.find(d => d.nama === 'PEKERJAAN DERMAGA');
    const b = k => dm.baris.find(x => x.kode === k);
    const nMiring = Object.values(m.elemen).filter(d => d.miring).length;
    assert.equal(b('DM-091').vol, nMiring);
    assert.ok(b('DM-301').vol > 500 && b('DM-302').vol > 100, JSON.stringify([b('DM-301'), b('DM-302')]));
    assert.equal(b('DM-090').vol, Object.values(m.elemen).filter(d => d.tipe === 'pilecap').length);
    // lembar gabungan, lembar bagian tampak, dan gabungan bebas (v0.41)
    for (const jenis of ['gabung:denah@G3+pondasi@G3', 'gabung:denah@G4+pondasi@G4', 'gabung:depan@G1+kiri@G1', 'depan@G1#1', 'depan@G1#2', 'gabung:potongan:X1+potongan:X3', 'gabung:balok@G3+pelat@G3', 'gabung:balok@G4+pelat@G4', 'det:1', 'det:2', 'det:3']) {
      const g = await c.callTool({name: 'gambar_2d', arguments: {jenis, kertas: 'A3'}});
      assert.equal(g.content[0].type, 'image', jenis + ': ' + JSON.stringify(g.content[0]).slice(0, 200));
      fs.writeFileSync(path.join(keluar, `kps-${jenis.replace(/[:@#+]/g, '-')}.png`), Buffer.from(g.content[0].data, 'base64'));
    }
    const salahJ = await c.callTool({name: 'gambar_2d', arguments: {jenis: 'gabung:denah@G3+tidakada', kertas: 'A3'}});
    assert.notEqual(salahJ.content[0].type, 'image');
    for (const jenis of ['denah', 'pondasi', 'potongan:X1', 'potongan:X2', 'potongan:X4']) {
      const g = await c.callTool({name: 'gambar_2d', arguments: {jenis, kertas: 'A3'}});
      assert.equal(g.content[0].type, 'image', jenis + ': ' + JSON.stringify(g.content[0]).slice(0, 200));
      fs.writeFileSync(path.join(keluar, `kps-${jenis.replace(':', '-')}.png`), Buffer.from(g.content[0].data, 'base64'));
    }
  } finally {
    await c.close();
    app.kill();
  }
});
