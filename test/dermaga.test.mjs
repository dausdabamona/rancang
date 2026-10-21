// Uji elemen dermaga (v0.39): tiang pancang, pile cap, perlengkapan, datum pasang surut, dan RAB divisi Pekerjaan Dermaga.
// Bagian data (sah/tolak) diuji lewat mode berkas MCP; gambar dan RAB diuji bila RANCANG_UJI_ELECTRON=1.
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

// Dermaga contoh: trestle 4 baris tiang × 12 as (jarak 3 m) + kepala 4 × 6; ±0,00 = LWS
export function modelDermaga() {
  const ubah = [];
  let nZ = 0, nF = 0, nR = 0, nO = 0;
  const zPelat = 3.16, tPelat = 0.30, hPC = 0.9, zPC = zPelat - hPC, zKepala = zPC + 0.1;
  const titik = [];
  for (let i = 0; i < 12; i++) for (const y of [-4.5, -1.5, 1.5, 4.5]) titik.push([i * 3, y]);
  for (let i = 0; i < 4; i++) for (let j = 0; j < 6; j++) titik.push([36 + i * 3, -7.5 + j * 3]);
  for (const [x, y] of titik) {
    ubah.push({id: 'Z' + ++nZ, data: {jenis: 'tiang', nama: 'Tiang ' + nZ, bahan: 'baja', x, y, dLuar: 508, tebal: 12, panjang: 40, zKepala, panjangSegmen: 12, coating: true,
      isian: {panjang: 4, fc: 24.9, tul: {n: 10, d: 19}}}});
    ubah.push({id: 'F' + ++nF, data: {jenis: 'pondasi', tipe: 'pilecap', nama: 'Pile cap ' + nF, x, y, p: 0.9, l: 0.9, tebal: hPC, z0: zPC, tulPlat: {d: 16, s: 0.15, ulir: true}, fc: 29, selimut: 0.075}});
  }
  const balok = (a, b) => ubah.push({id: 'R' + ++nR, data: {jenis: 'ringbalk', peran: 'balok', awal: {x: a[0], y: a[1]}, akhir: {x: b[0], y: b[1]}, b: 0.25, h: 0.5, z0: zPelat - 0.5,
    tul: {n: 6, d: 16, ulir: true}, sengkang: {d: 10, s: 0.15}, fc: 29, selimut: 0.05}});
  for (const y of [-4.5, -1.5, 1.5, 4.5]) balok([0, y], [33, y]);
  for (let i = 0; i < 12; i++) balok([i * 3, -4.5], [i * 3, 4.5]);
  ubah.push({id: 'W1', data: {jenis: 'plat', nama: 'Lantai trestle', alas: [{x: -0.5, y: -5}, {x: 34.5, y: -5}, {x: 34.5, y: 5}, {x: -0.5, y: 5}], z0: zPelat, tebal: tPelat, fc: 29, tul: {d: 13, s: 0.15}}});
  ubah.push({id: 'W2', data: {jenis: 'plat', nama: 'Lantai kepala', alas: [{x: 34.5, y: -8}, {x: 45.5, y: -8}, {x: 45.5, y: 8}, {x: 34.5, y: 8}], z0: zPelat, tebal: tPelat, fc: 29, tul: {d: 13, s: 0.15}}});
  for (const y of [-6, 0, 6]) {
    ubah.push({id: 'O' + ++nO, data: {jenis: 'perlengkapan', tipe: 'bolder', kapasitas: 15, x: 45, y, z0: zPelat + tPelat, rotasi: 270}});
    ubah.push({id: 'O' + ++nO, data: {jenis: 'perlengkapan', tipe: 'fender', panjang: 1.5, model: 'V 300H', x: 45.5, y, z0: zPelat + tPelat, rotasi: 270}});
  }
  ubah.push({id: 'O' + ++nO, data: {jenis: 'perlengkapan', tipe: 'pju', tinggi: 6, x: 20, y: 4.7, z0: zPelat + tPelat, rotasi: 180}});
  ubah.push({id: 'O' + ++nO, data: {jenis: 'perlengkapan', tipe: 'tanggaMonyet', tinggi: 3.5, x: 45.5, y: 3, z0: zPelat + tPelat, rotasi: 270}});
  ubah.push({id: 'M1', data: {jenis: 'level', nama: 'HWL', datum: 'hwl', z: 1.91}});
  ubah.push({id: 'M2', data: {jenis: 'level', nama: 'MSL', datum: 'msl', z: 1.21}});
  ubah.push({id: 'M3', data: {jenis: 'level', nama: 'LWL', datum: 'lwl', z: 0}});
  ubah.push({id: 'M4', data: {jenis: 'level', nama: 'Dasar laut', datum: 'dasar', z: -2}});
  ubah.push({id: 'X1', data: {jenis: 'potong', nama: 'A', awal: {x: 6, y: -10}, akhir: {x: 6, y: 10}, pandang: 1}});
  ubah.push({id: 'X2', data: {jenis: 'potong', nama: 'B', awal: {x: -3, y: 0}, akhir: {x: 48, y: 0}, pandang: -1}});
  return {ubah, nTiang: titik.length};
}

function siapkanFolder() {
  const data = fs.mkdtempSync(path.join(os.tmpdir(), 'rancang-dermaga-'));
  const proyek = path.join(data, 'dermaga.rancang');
  fs.writeFileSync(proyek, JSON.stringify({format: 'rancang-proyek', versi: 1, aplikasi: 'RANCANG', setel: {nama: 'Uji dermaga'}, elemen: {}, grup: {}, komponen: {}, kusen: {}}));
  return {data, proyek};
}
async function sambung(dataDir) {
  const client = new Client({name: 'uji-dermaga', version: '1.0.0'});
  await client.connect(new StdioClientTransport({command: process.execPath, args: [serverMcp], env: {...process.env, RANCANG_DATA_DIR: dataDir}, stderr: 'inherit'}));
  return client;
}

test('dermaga: aplikasi menerima model, menggambar, dan menghitung RAB dermaga', {skip: process.env.RANCANG_UJI_ELECTRON !== '1'}, async () => {
  const {data, proyek} = siapkanFolder();
  const electron = require('electron');
  const argv = [akar, proyek, '--use-angle=swiftshader', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'];
  if (process.platform === 'linux') argv.push('--no-sandbox');
  const app = spawn(electron, argv, {env: {...process.env, RANCANG_DATA_DIR: data}, stdio: 'ignore'});
  const c = await sambung(data);
  const keluar = process.env.RANCANG_UJI_KELUAR || os.tmpdir();
  try {
    let info = null;
    for (let i = 0; i < 120 && !(info && info.aplikasiBerjalan); i++) {
      await new Promise(r => setTimeout(r, 500));
      try { info = json(await c.callTool({name: 'info_proyek', arguments: {}})); } catch { info = null; }
    }
    assert.ok(info && info.aplikasiBerjalan, 'aplikasi tidak siap');
    const {ubah, nTiang} = modelDermaga();
    const r = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: ubah}}));
    assert.equal(r.ok, true, JSON.stringify(r));
    // data tidak sah ditolak: tiang pipa tanpa tebal, perlengkapan tipe asing, datum asing
    for (const salah of [{id: 'Z900', data: {jenis: 'tiang', bahan: 'baja', x: 0, y: 0, dLuar: 508, panjang: 40, zKepala: 2}},
      {id: 'O900', data: {jenis: 'perlengkapan', tipe: 'jangkar', x: 0, y: 0, z0: 0}},
      {id: 'M900', data: {jenis: 'level', nama: 'X', datum: 'pasang', z: 1}}]) {
      const t = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [salah]}}));
      assert.equal(t.ok, false, salah.id);
    }
    // v0.46.1: garis bantu tegak (sejajar sumbu Z) sah; tegak dengan label as ditolak
    const tg = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: 'Q950', data: {jenis: 'bantu', nama: 'Bantu tegak', awal: {x: 3, y: 1.5, z: 0}, akhir: {x: 3, y: 1.5, z: 5}}}]}}));
    assert.equal(tg.ok, true, JSON.stringify(tg));
    const tgAs = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: 'Q951', data: {jenis: 'bantu', nama: 'As', awal: {x: 3, y: 1.5, z: 0}, akhir: {x: 3, y: 1.5, z: 5}, as: {label: 'Z'}}}]}}));
    assert.equal(tgAs.ok, false);
    const tgDatar = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: 'Q952', data: {jenis: 'bantu', nama: 'Titik', awal: {x: 3, y: 1.5}, akhir: {x: 3, y: 1.5}}}]}}));
    assert.equal(tgDatar.ok, false);
    await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: 'Q950', data: null}]}});
    const rab = json(await c.callTool({name: 'volume_rab', arguments: {}}));
    const dermaga = rab.find(d => d.nama === 'PEKERJAAN DERMAGA');
    assert.ok(dermaga, 'divisi Pekerjaan Dermaga ada');
    const baris = k => dermaga.baris.find(b => b.kode === k);
    // pipa Ø508 × 12: 0,02466 × 12 × 496 = 146,78 kg/m; 72 tiang × 40 m
    assert.ok(Math.abs(baris('DM-011').vol - 0.02466 * 12 * 496 * 40 * nTiang) < 1, JSON.stringify(baris('DM-011')));
    assert.equal(baris('DM-012').vol, 40 * nTiang);
    assert.equal(baris('DM-013').vol, 3 * nTiang);
    assert.equal(baris('DM-014').vol, nTiang);
    assert.equal(baris('DM-090').vol, nTiang);
    assert.equal(baris('DM-101').vol, 3);
    assert.equal(baris('DM-102').vol, 3);
    fs.writeFileSync(path.join(keluar, 'dermaga-rab.json'), JSON.stringify(rab, null, 1));
    // v0.46: RAB berharga — harga bawaan bersatuan sama, status asumsi/termasuk/kosong, total = jumlah + PPN 11 %
    const hr = json(await c.callTool({name: 'hitung_rab', arguments: {}}));
    const bh = k => hr.divisi.flatMap(d => d.baris).find(b => b.kode === k);
    assert.equal(bh('DM-011').harga, 37620); assert.equal(bh('DM-011').status, 'asumsi');
    assert.equal(bh('DM-090').status, 'termasuk'); assert.equal(bh('DM-090').jumlah, 0);
    assert.equal(bh('ST-011').status, 'perwali');
    assert.ok(hr.jumlah > 0 && hr.total === hr.jumlah + Math.round(hr.jumlah * 0.11), JSON.stringify({j: hr.jumlah, t: hr.total}));
    assert.ok(hr.nilaiStatus.asumsi > 0 && hr.porsiAsumsi > 0 && hr.porsiAsumsi < 1);
    const sumDiv = hr.divisi.reduce((a, d) => a + d.jumlah, 0);
    assert.ok(Math.abs(sumDiv - hr.jumlah) <= hr.divisi.length, `${sumDiv} vs ${hr.jumlah}`);
    for (const jenis of ['denah', 'pondasi', 'potongan:X1', 'potongan:X2', 'depan']) {
      const g = await c.callTool({name: 'gambar_2d', arguments: {jenis, kertas: 'A3'}});
      assert.equal(g.content[0].type, 'image', jenis + ': ' + JSON.stringify(g.content[0]).slice(0, 200));
      fs.writeFileSync(path.join(keluar, `dermaga-${jenis.replace(':', '-')}.png`), Buffer.from(g.content[0].data, 'base64'));
    }
    // v0.43.1: as di bagian yang dihilangkan garis putus tidak digambar (gelembung tidak bertumpuk di celah),
    // ukuran antar as menyambung ke as terlihat berikutnya dengan nilai sebenarnya
    const asUji = [];
    for (let i = 0; i < 12; i++) asUji.push({id: 'Q' + (900 + i), data: {jenis: 'bantu', nama: 'As T' + (i + 1), awal: {x: i * 3, y: -10}, akhir: {x: i * 3, y: 10}, as: {label: 'T' + (i + 1)}}});
    asUji.push({id: 'L900', data: {jenis: 'gambar2d', bentuk: 'putus', lembar: 'denah', tempel: 'gambar', arah: 'datar', titik: [{x: 4.5, y: 0, z: 0}, {x: 28.5, y: 0, z: 0}], gaya: {tebal: 0.3}}});
    const ra = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: asUji}}));
    assert.equal(ra.ok, true, JSON.stringify(ra));
    const sv = await c.callTool({name: 'gambar_2d', arguments: {jenis: 'denah', kertas: 'A3', format: 'svg'}});
    const svg = sv.content.map(k => k.text || '').join('');
    const ada = l => new RegExp(`>${l}</text>`).test(svg);
    for (const l of ['T1', 'T2', 'T11', 'T12']) assert.ok(ada(l), `as ${l} terlihat harus digambar`);
    for (const l of ['T3', 'T5', 'T8', 'T10']) assert.ok(!ada(l), `as ${l} di bagian yang dihilangkan tidak boleh digambar`);
    assert.ok(/>27,00</.test(svg), 'ukuran T2–T11 menyambung dengan nilai sebenarnya 27,00');
    // simbol garis putus datar hanya selebar benda yang dipendekkan (pelat trestle 10 m) ± 2 mm, bukan setinggi seluruh gambar
    const skala = Number((/1 : (\d+)/.exec(svg) || [])[1]);
    const putih = /<g data-g2="L900"><rect [^>]*height="([\d.]+)"/.exec(svg);
    assert.ok(skala > 0 && putih, 'skala dan simbol garis putus ada di SVG');
    assert.ok(Math.abs(Number(putih[1]) - (10 * 1000 / skala + 4)) < 0.6, `tinggi penutup ${putih[1]} mm harus selebar trestle pada 1:${skala}`);
    // v0.44.1: di potongan memanjang bergaris putus, rantai jarak tiang tidak bertumpuk di celah;
    // ukuran menyambung dari tiang terlihat terakhir ke tiang terlihat berikutnya dengan nilai sebenarnya
    const putusPot = {id: 'L901', data: {jenis: 'gambar2d', bentuk: 'putus', lembar: 'potongan:X2', tempel: 'gambar', arah: 'datar', titik: [{x: 4.5, y: 0, z: 0}, {x: 28.5, y: 0, z: 0}], gaya: {tebal: 0.3}}};
    assert.equal(json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [putusPot]}})).ok, true);
    const sp = (await c.callTool({name: 'gambar_2d', arguments: {jenis: 'potongan:X2', kertas: 'A3', format: 'svg'}})).content.map(k => k.text || '').join('');
    const n300 = (sp.match(/>300</g) || []).length;
    assert.ok(n300 >= 1 && n300 <= 6, `jarak 300 cm hanya untuk tiang terlihat (ada ${n300})`);
    assert.ok(/>2700</.test(sp), 'jarak tiang menyambung melewati celah garis putus: 2700 cm');
    // v0.45: tiang dipendekkan 1,0 m di bawah LWL di potongan (skala kerja), dengan label ujung tiang
    const sx = (await c.callTool({name: 'gambar_2d', arguments: {jenis: 'potongan:X1', kertas: 'A3', format: 'svg'}})).content.map(k => k.text || '').join('');
    assert.ok(/Ujung tiang -37,64 · L 40,00 m/.test(sx), 'label ujung tiang di potongan bertiang dipendekkan');
    assert.ok(/LWL ±0,00/.test(sx), 'daftar muka air tetap tampil');
    // v0.45: penanda potongan B (lingkaran r 2,4 mm) di potongan melintang A; di potongan B penanda A jatuh di bagian putus sehingga tidak digambar
    assert.ok(/<circle cx="[\d.]+" cy="[\d.]+" r="2.4" fill="#fff"/.test(sx), 'penanda potongan B di potongan A');
    assert.ok(!/<circle cx="[\d.]+" cy="[\d.]+" r="2.4" fill="#fff"/.test(sp), 'penanda di bagian putus tidak digambar');
    // v0.45: kotak Keterangan lembar detail dari mutu model
    assert.equal(json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: 'E950', data: {jenis: 'detail', template: 'pileCapDermaga', sumber: 'F1', lembar: 'det:9', skala: 25}}]}})).ok, true);
    const sdk = (await c.callTool({name: 'gambar_2d', arguments: {jenis: 'det:9', kertas: 'A3', format: 'svg'}})).content.map(k => k.text || '').join('');
    assert.ok(/KETERANGAN/.test(sdk) && /Mutu beton fc' 29 MPa/.test(sdk) && /BjTS 420, fy 420 MPa/.test(sdk), 'kotak keterangan berisi mutu beton dan besi');
    // v0.44.0: detail perbesaran dengan judul, bingkai persegi, garis penghubung, dan isi rinci (label tulangan, mutu bahan)
    const det = {jenis: 'gambar2d', bentuk: 'perbesar', lembar: 'potongan:X1', tempel: 'gambar', titik: [{x: 6, y: 4.5, z: 2.9}, {x: 6, y: 5.4, z: 2.9}],
      letak: {x: 300, y: 80}, skala: 20, nomor: '7', judul: 'Pertemuan pelat dan balok tepi', bingkai: 'persegi', rasio: 1.5, penghubung: true};
    const rd = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: 'L901', data: det}]}}));
    assert.equal(rd.ok, true, JSON.stringify(rd));
    const sd = (await c.callTool({name: 'gambar_2d', arguments: {jenis: 'potongan:X1', kertas: 'A3', format: 'svg'}})).content.map(k => k.text || '').join('');
    assert.ok(/>DETAIL 7</.test(sd) && />Pertemuan pelat dan balok tepi</.test(sd), 'judul detail tampil');
    assert.ok(/<clipPath id="kp-L901"><rect /.test(sd), 'bingkai persegi');
    fs.writeFileSync(path.join(keluar, 'dermaga-detail.svg'), sd);
    assert.ok(/Ø13-150 atas &amp; bawah/.test(sd), 'label tulangan pelat dari data elemen');
    assert.ok(/6D16 · Ø10-150/.test(sd), 'label tulangan balok dari data elemen');
    assert.ok(/Mutu beton fc&#39; [^<]*29 MPa/.test(sd), 'keterangan mutu bahan');
    assert.ok(!/url\(#arsir-beton/.test(sd), 'arsir digambar langsung, tanpa pola SVG');
    // isi rinci bisa dimatikan per detail
    const rm = json(await c.callTool({name: 'terapkan_perubahan', arguments: {perubahan: [{id: 'L901', data: {...det, rinci: {label: false, bahan: false}}}]}}));
    assert.equal(rm.ok, true, JSON.stringify(rm));
    const sm = (await c.callTool({name: 'gambar_2d', arguments: {jenis: 'potongan:X1', kertas: 'A3', format: 'svg'}})).content.map(k => k.text || '').join('');
    assert.ok(!/atas &amp; bawah/.test(sm) && !/Mutu beton/.test(sm), 'label dan mutu bahan dimatikan');
    const g7 = await c.callTool({name: 'gambar_2d', arguments: {jenis: 'potongan:X1', kertas: 'A3'}});
    fs.writeFileSync(path.join(keluar, 'dermaga-detail-perbesaran.png'), Buffer.from(g7.content[0].data, 'base64'));
    const t3 = await c.callTool({name: 'tangkap_layar_3d', arguments: {tampilan: 'iso'}});
    fs.writeFileSync(path.join(keluar, 'dermaga-3d.png'), Buffer.from(t3.content[0].data, 'base64'));
  } finally {
    await c.close();
    app.kill();
  }
});
