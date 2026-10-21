// Uji dermaga kayu (v0.40): elemen jetiKayu (J) — sah/tolak, volume kayu, RAB DM-201…208, dan gambar 2D/3D.
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

const akar = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const serverMcp = path.join(akar, 'build', 'mcp', 'server', 'index.mjs');
const require = createRequire(import.meta.url);
const json = r => JSON.parse(r.content[0].text);

const JETI = {lebar: 2.5, zLantai: 3, jarakPortal: 2.5, kayu: 'Merbau', tiang: {b: 0.2, panjang: 8, n: 2}, balokKepala: {b: 0.08, h: 0.2, ganda: true},
  gelagar: {b: 0.08, h: 0.15, jarak: 0.6}, papan: {tebal: 0.04, lebar: 0.2, celah: 0.01}, skor: {pasang: true, b: 0.06, h: 0.15}};
// jeti L: ruas 1 sepanjang Y 50 m, ruas 2 sepanjang X 25 m mulai dari tepi ruas 1 (tanpa portal awal)
export function modelJeti() {
  return [
    {id: 'J1', data: {jenis: 'jetiKayu', nama: 'Jeti utama', ...JETI, awal: {x: 0, y: 0}, akhir: {x: 0, y: 50}}},
    {id: 'J2', data: {jenis: 'jetiKayu', nama: 'Jeti kaki', ...JETI, awal: {x: 1.25, y: 50}, akhir: {x: 26.25, y: 50}, portalAwal: false}},
    {id: 'M1', data: {jenis: 'level', nama: 'HWL', datum: 'hwl', z: 1.91}},
    {id: 'M2', data: {jenis: 'level', nama: 'LWL', datum: 'lwl', z: 0}},
    {id: 'M3', data: {jenis: 'level', nama: 'Dasar laut', datum: 'dasar', z: -1}},
    {id: 'X1', data: {jenis: 'potong', nama: 'A', awal: {x: -3, y: 25}, akhir: {x: 3, y: 25}, pandang: 1}}
  ];
}

test('jeti kayu: model, RAB kayu, dan gambar', {skip: process.env.RANCANG_UJI_ELECTRON !== '1'}, async () => {
  const data = fs.mkdtempSync(path.join(os.tmpdir(), 'rancang-jeti-')), proyek = path.join(data, 'jeti.rancang');
  fs.writeFileSync(proyek, JSON.stringify({format: 'rancang-proyek', versi: 1, aplikasi: 'RANCANG', setel: {nama: 'Uji jeti'}, elemen: {}, grup: {}, komponen: {}, kusen: {}}));
  const electron = require('electron');
  const argv = [akar, proyek, '--use-angle=swiftshader', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'];
  if (process.platform === 'linux') argv.push('--no-sandbox');
  const app = spawn(electron, argv, {env: {...process.env, RANCANG_DATA_DIR: data}, stdio: 'ignore'});
  const c = new Client({name: 'uji-jeti', version: '1.0.0'});
  await c.connect(new StdioClientTransport({command: process.execPath, args: [serverMcp], env: {...process.env, RANCANG_DATA_DIR: data}, stderr: 'inherit'}));
  const keluar = process.env.RANCANG_UJI_KELUAR || os.tmpdir();
  try {
    let info = null;
    for (let i = 0; i < 120 && !(info && info.aplikasiBerjalan); i++) {
      await new Promise(r => setTimeout(r, 500));
      try { info = json(await c.callTool({name: 'info_proyek', arguments: {}})); } catch { info = null; }
    }
    assert.ok(info && info.aplikasiBerjalan, 'aplikasi tidak siap');
    const r = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: modelJeti()}}));
    assert.equal(r.ok, true, JSON.stringify(r));
    const salah = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: 'J9', data: {jenis: 'jetiKayu', ...JETI, lebar: 0, awal: {x: 0, y: 0}, akhir: {x: 5, y: 0}}}]}}));
    assert.equal(salah.ok, false);
    const rab = json(await c.callTool({name: 'volume_rab', arguments: {}}));
    fs.writeFileSync(path.join(keluar, 'jeti-rab.json'), JSON.stringify(rab, null, 1));
    const dm = rab.find(d => d.nama === 'PEKERJAAN DERMAGA');
    assert.ok(dm, 'divisi dermaga');
    const b = k => dm.baris.find(x => x.kode === k);
    // ruas 1: 20 bentang → 21 portal × 2 = 42 tiang; ruas 2: 10 bentang, tanpa portal awal → 10 × 2 = 20
    assert.equal(b('DM-202').vol, (42 + 20) * 8);
    assert.ok(Math.abs(b('DM-201').vol - 62 * 0.2 * 0.2 * 8) < 1e-3, JSON.stringify(b('DM-201')));
    // papan: ruas 1 ceil(50/0,21)=239, ruas 2 ceil(25/0,21)=120
    assert.ok(Math.abs(b('DM-205').vol - (239 + 120) * 0.2 * 0.04 * 2.5) < 1e-3, JSON.stringify(b('DM-205')));
    for (const k of ['DM-203', 'DM-204', 'DM-206', 'DM-207', 'DM-208']) assert.ok(b(k) && b(k).vol > 0, k);
    for (const jenis of ['denah', 'pondasi', 'potongan:X1', 'depan']) {
      const g = await c.callTool({name: 'gambar_2d', arguments: {jenis, kertas: 'A3'}});
      assert.equal(g.content[0].type, 'image', jenis + ': ' + JSON.stringify(g.content[0]).slice(0, 200));
      fs.writeFileSync(path.join(keluar, `jeti-${jenis.replace(':', '-')}.png`), Buffer.from(g.content[0].data, 'base64'));
    }
    const t3 = await c.callTool({name: 'tangkap_layar_3d', arguments: {tampilan: 'iso'}});
    fs.writeFileSync(path.join(keluar, 'jeti-3d.png'), Buffer.from(t3.content[0].data, 'base64'));
    // v0.45: tiang pipa baja — jeti hanya rangka atas; tiang dari elemen Z, baris DM-201/202 hilang
    const baja = {...JETI, kayu: 'Besi', tiang: {b: 0.219, panjang: 8, n: 2, bahan: 'baja'}, balokKepala: {b: 0.1, h: 0.2, ganda: false}};
    const rb = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [
      {id: 'J1', data: null}, {id: 'J2', data: null},
      {id: 'J3', data: {jenis: 'jetiKayu', nama: 'Jeti baja', ...baja, awal: {x: 0, y: 0}, akhir: {x: 0, y: 10}}},
      {id: 'Z1', data: {jenis: 'tiang', bahan: 'baja', dLuar: 219, tebal: 8, x: -1.14, y: 0.11, zKepala: 2.61, panjang: 9, panjangSegmen: 12, coating: true}}]}}));
    assert.equal(rb.ok, true, JSON.stringify(rb));
    const rab2 = json(await c.callTool({name: 'volume_rab', arguments: {}}));
    const dm2 = rab2.find(d => d.nama === 'PEKERJAAN DERMAGA'), b2 = k => dm2.baris.find(x => x.kode === k);
    assert.ok(!b2('DM-201') && !b2('DM-202'), 'tiang kayu tidak boleh muncul');
    // 10 m: 4 bentang → 5 portal × 2 titik = 10 baut kepala tiang; skor 5 × 2 batang × 2 baut = 20
    assert.ok(b2('DM-203') && b2('DM-207').vol === 30, JSON.stringify(b2('DM-207')));
    assert.ok(dm2.baris.some(x => /219/.test(x.uraian)), 'baris tiang pipa Ø219');
    const gp = await c.callTool({name: 'gambar_2d', arguments: {jenis: 'potongan:X1', kertas: 'A3'}});
    assert.equal(gp.content[0].type, 'image');
  } finally {
    await c.close();
    app.kill();
  }
});
