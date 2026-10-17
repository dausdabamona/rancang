'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {Proyek, urai, bandingkan, kosong} = require('../electron/penyimpanan');

const folderUji = () => fs.mkdtempSync(path.join(os.tmpdir(), 'rancang-test-'));
const dinding = (x = 4) => ({jenis: 'dinding', awal: {x: 0, y: 0}, akhir: {x, y: 0}, tebal: 0.15, tinggi: 3});

test('membuat berkas baru bila belum ada', () => {
  const f = path.join(folderUji(), 'baru.rancang');
  const p = new Proyek();
  p.buka(f);
  p.hentikanPantau();
  assert.ok(fs.existsSync(f));
  assert.equal(JSON.parse(fs.readFileSync(f, 'utf8')).format, 'rancang-proyek');
});

test('menyimpan perubahan ke berkas dan membuat cadangan saat dibuka lagi', () => {
  const f = path.join(folderUji(), 'a.rancang');
  const p = new Proyek({tundaSimpan: 5});
  p.buka(f);
  p.set('elemen', 'D1', dinding());
  p.setel({nama: 'Uji'});
  p.simpanSekarang();
  p.hentikanPantau();
  const isi = JSON.parse(fs.readFileSync(f, 'utf8'));
  assert.deepEqual(isi.elemen.D1, dinding());
  assert.equal(isi.setel.nama, 'Uji');
  const q = new Proyek();
  q.buka(f);
  q.hentikanPantau();
  assert.ok(fs.existsSync(f + '.bak'));
  assert.deepEqual(q.awal().elemen.D1, dinding());
});

test('menolak id dan koleksi yang tidak sah', () => {
  const p = new Proyek();
  assert.throws(() => p.set('elemen', 'd1', {}), /Id tidak sah/);
  assert.throws(() => p.set('lain', 'D1', {}), /Koleksi tidak dikenal/);
});

test('menghapus dokumen dengan data null', () => {
  const f = path.join(folderUji(), 'h.rancang');
  const p = new Proyek({tundaSimpan: 5});
  p.buka(f);
  p.set('elemen', 'D1', dinding());
  p.set('elemen', 'D1', null);
  p.simpanSekarang();
  p.hentikanPantau();
  assert.equal(JSON.parse(fs.readFileSync(f, 'utf8')).elemen.D1, undefined);
});

test('urai menolak berkas bukan proyek RANCANG dan membuang id rusak', () => {
  assert.throws(() => urai('{"a":1}'), /bukan proyek RANCANG/);
  assert.throws(() => urai('bukan json'), /bukan JSON/);
  const d = urai(JSON.stringify({...kosong(), elemen: {D1: dinding(), 'x-1': dinding()}}));
  assert.deepEqual(Object.keys(d.elemen), ['D1']);
});

test('bandingkan mengenali tambah, ubah, hapus, dan setelan', () => {
  const lama = {...kosong(), elemen: {D1: dinding(), D2: dinding(2)}};
  const baru = {...kosong(), elemen: {D1: dinding(5), D3: dinding(3)}, setel: {nama: 'B'}};
  const s = bandingkan(lama, baru);
  assert.ok(s.ada);
  const p = Object.fromEntries(s.koleksi.elemen.map(x => [x.id, x.data]));
  assert.deepEqual(p.D1, dinding(5));
  assert.deepEqual(p.D3, dinding(3));
  assert.equal(p.D2, null);
  assert.deepEqual(s.setel, {nama: 'B'});
});

test('perubahan berkas dari luar dimuat ulang, tulisan sendiri diabaikan', () => {
  const f = path.join(folderUji(), 'l.rancang');
  const p = new Proyek({tundaSimpan: 5});
  p.buka(f);
  p.hentikanPantau();
  p.set('elemen', 'D1', dinding());
  p.simpanSekarang();
  assert.equal(p.periksaLuar(), null, 'tulisan sendiri tidak dianggap perubahan luar');
  const luar = JSON.parse(fs.readFileSync(f, 'utf8'));
  luar.elemen.D1.tinggi = 2.5;
  fs.writeFileSync(f, JSON.stringify(luar));
  const s = p.periksaLuar();
  assert.ok(s && s.ada);
  assert.equal(p.awal().elemen.D1.tinggi, 2.5);
});
