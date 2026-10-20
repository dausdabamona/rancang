// Uji server MCP hasil bundel (build/mcp). Jalankan `npm run build` dulu.
// Mode berkas selalu diuji; mode aplikasi (Electron) diuji bila RANCANG_UJI_ELECTRON=1.
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

const kosong = () => ({format: 'rancang-proyek', versi: 1, aplikasi: 'RANCANG', setel: {nama: 'Uji'}, elemen: {}, grup: {}, komponen: {}, kusen: {}});
const dinding = (x = 4) => ({jenis: 'dinding', nama: 'Dinding uji', awal: {x: 0, y: 0}, akhir: {x, y: 0}, tebal: 0.15, tinggi: 3, z0: 0});

function siapkanFolder() {
  const data = fs.mkdtempSync(path.join(os.tmpdir(), 'rancang-mcp-'));
  const proyek = path.join(data, 'uji.rancang');
  fs.writeFileSync(proyek, JSON.stringify(kosong()));
  return {data, proyek};
}
async function sambung(dataDir) {
  const client = new Client({name: 'uji-rancang', version: '1.0.0'});
  await client.connect(new StdioClientTransport({command: process.execPath, args: [serverMcp], env: {...process.env, RANCANG_DATA_DIR: dataDir}, stderr: 'inherit'}));
  return client;
}
const json = r => JSON.parse(r.content[0].text);

test('mode berkas: membaca, menerapkan, dan menolak perubahan tanpa aplikasi', async () => {
  assert.ok(fs.existsSync(serverMcp), 'jalankan npm run build:mcp dulu');
  const {data, proyek} = siapkanFolder();
  fs.writeFileSync(path.join(data, 'mcp-jembatan.json'), JSON.stringify({proyek}));
  const c = await sambung(data);
  try {
    const {tools} = await c.listTools();
    assert.ok(tools.some(t => t.name === 'terapkan_perubahan'));
    assert.ok(tools.some(t => t.name === 'gambar_2d'));
    assert.ok(tools.some(t => t.name === 'pilihan_pengguna'));
    const info = json(await c.callTool({name: 'info_proyek', arguments: {}}));
    assert.equal(info.aplikasiBerjalan, false);
    // aplikasi tertutup: tidak ada pilihan pengguna, dan Claude diberi tahu jelas
    const pil = json(await c.callTool({name: 'pilihan_pengguna', arguments: {}}));
    assert.equal(pil.aplikasiBerjalan, false);
    assert.match(pil.catatan, /tidak sedang berjalan/);
    const r = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: 'D1', data: dinding()}]}}));
    assert.equal(r.ok, true);
    const isi = JSON.parse(fs.readFileSync(proyek, 'utf8'));
    assert.equal(isi.elemen.D1.diubahOleh, 'claude');
    const tolak = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: 'B1', data: {jenis: 'bukaan', dinding: 'D99', lebar: 1, tinggi: 2, jarak: 0}}]}}));
    assert.equal(tolak.ok, false);
    const ambil = json(await c.callTool({name: 'ambil_elemen', arguments: {ids: ['D1', 'D2']}}));
    assert.equal(ambil.D1.tebal, 0.15);
    assert.equal(ambil.D2, null);
    const daftar = json(await c.callTool({name: 'daftar_elemen', arguments: {jenis: 'dinding'}}));
    assert.equal(daftar.total, 1);
    const panduan = await c.callTool({name: 'panduan_data', arguments: {}});
    assert.match(panduan.content[0].text, /Panduan data model RANCANG/);
    assert.match(panduan.content[0].text, /Label terhubung: tambahkan sumber/);
  } finally { await c.close(); }
});

test('mode aplikasi: MCP mengendalikan RANCANG desktop yang berjalan', {skip: process.env.RANCANG_UJI_ELECTRON !== '1'}, async () => {
  const {data, proyek} = siapkanFolder();
  const electron = require('electron');
  const argv = [akar, proyek, '--use-angle=swiftshader', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'];
  if (process.platform === 'linux') argv.push('--no-sandbox');
  const app = spawn(electron, argv, {env: {...process.env, RANCANG_DATA_DIR: data}, stdio: 'ignore'});
  const c = await sambung(data);
  try {
    let info = null;
    for (let i = 0; i < 120 && !(info && info.aplikasiBerjalan); i++) {
      await new Promise(r => setTimeout(r, 500));
      try { info = json(await c.callTool({name: 'info_proyek', arguments: {}})); } catch { info = null; }
    }
    assert.ok(info && info.aplikasiBerjalan, 'aplikasi tidak siap');
    assert.equal(path.resolve(info.proyek), path.resolve(proyek));
    const r = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [
      {id: 'D1', data: dinding(5)},
      {id: 'B1', data: {jenis: 'bukaan', tipe: 'pintu', kode: 'P1', dinding: 'D1', jarak: 1, lebar: 0.8, tinggi: 2.1, ambang: 0}}
    ]}}));
    assert.equal(r.ok, true, JSON.stringify(r));
    const tolak = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: 'D2', data: {jenis: 'dinding'}}]}}));
    assert.equal(tolak.ok, false);
    const g = await c.callTool({name: 'gambar_2d', arguments: {jenis: 'denah'}});
    assert.equal(g.content[0].type, 'image');
    assert.ok(g.content[0].data.length > 1000);
    const svg = await c.callTool({name: 'gambar_2d', arguments: {jenis: 'denah', format: 'svg'}});
    assert.match(svg.content[0].text, /<svg/);
    const t3 = await c.callTool({name: 'tangkap_layar_3d', arguments: {tampilan: 'iso'}});
    assert.equal(t3.content[0].type, 'image');
    const rab = json(await c.callTool({name: 'volume_rab', arguments: {}}));
    assert.ok(Array.isArray(rab) && rab.length > 0);
    // pilihan pengguna: awalnya kosong, lalu info_proyek dan pilihan_pengguna sama-sama melihat pilihan yang dibuat di halaman
    const kosong = json(await c.callTool({name: 'pilihan_pengguna', arguments: {}}));
    assert.equal(kosong.aplikasiBerjalan, true);
    assert.deepEqual(kosong.terpilih, []);
    assert.equal(kosong.grupDibuka, null);
    assert.match(kosong.catatan, /belum memilih/);
    const info2 = json(await c.callTool({name: 'info_proyek', arguments: {}}));
    assert.equal(info2.pilihan.jumlah, 0);
    const isi = JSON.parse(fs.readFileSync(proyek, 'utf8'));
    assert.equal(isi.elemen.B1.dinding, 'D1');
    fs.writeFileSync(path.join(os.tmpdir(), 'rancang-uji-denah.png'), Buffer.from(g.content[0].data, 'base64'));
    fs.writeFileSync(path.join(os.tmpdir(), 'rancang-uji-3d.png'), Buffer.from(t3.content[0].data, 'base64'));
  } finally {
    await c.close();
    app.kill();
  }
});
