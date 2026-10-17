// Penyimpanan proyek desktop: satu berkas .rancang (JSON) per proyek.
// Proses utama memegang data; halaman membaca dan menulis lewat IPC. Modul ini murni Node agar bisa diuji tanpa Electron.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {EventEmitter} = require('node:events');

const FORMAT = 'rancang-proyek';
const KOLEKSI = ['elemen', 'grup', 'komponen', 'kusen'];
const POLA_ID = /^[A-Z]\d+$/;

const hash = teks => crypto.createHash('sha1').update(teks).digest('hex');
const salin = x => (x == null ? x : JSON.parse(JSON.stringify(x)));

function kosong() {
  return {format: FORMAT, versi: 1, aplikasi: 'RANCANG', disimpan: null, setel: {}, elemen: {}, grup: {}, komponen: {}, kusen: {}};
}

// Baca dan rapikan isi berkas; dokumen yang id-nya tidak sah dibuang
function urai(teks) {
  let d;
  try { d = JSON.parse(teks); } catch { throw new Error('Berkas proyek rusak: bukan JSON yang sah.'); }
  if (!d || d.format !== FORMAT || typeof d.elemen !== 'object') throw new Error('Berkas ini bukan proyek RANCANG.');
  const hasil = kosong();
  hasil.setel = d.setel && typeof d.setel === 'object' ? d.setel : {};
  for (const k of KOLEKSI) {
    for (const [id, x] of Object.entries(d[k] || {})) if (POLA_ID.test(id) && x && typeof x === 'object') hasil[k][id] = x;
  }
  hasil.disimpan = d.disimpan || null;
  return hasil;
}

// Tulis aman: berkas sementara lalu ganti nama, agar berkas tidak setengah tertulis bila listrik mati
function tulisAman(jalur, teks) {
  fs.mkdirSync(path.dirname(jalur), {recursive: true});
  const tmp = jalur + '.tmp';
  fs.writeFileSync(tmp, teks);
  fs.renameSync(tmp, jalur);
}

class Proyek extends EventEmitter {
  constructor({tundaSimpan = 400} = {}) {
    super();
    this.jalur = null;
    this.data = kosong();
    this.tundaSimpan = tundaSimpan;
    this.timer = null;
    this.hashTerakhir = null;
    this.pantauAktif = false;
  }

  // Buka berkas; bila belum ada, dibuat kosong. Cadangan .bak dibuat dari isi lama.
  buka(jalur) {
    this.simpanSekarang();
    this.hentikanPantau();
    const abs = path.resolve(jalur);
    if (fs.existsSync(abs)) {
      const teks = fs.readFileSync(abs, 'utf8');
      this.data = urai(teks);
      try { fs.copyFileSync(abs, abs + '.bak'); } catch (err) { console.error('[penyimpanan] gagal membuat cadangan', err); }
      this.hashTerakhir = hash(teks);
    } else {
      this.data = kosong();
      this.jalur = abs;
      this.simpanSekarang(true);
    }
    this.jalur = abs;
    this.pantau();
    this.emit('dibuka', abs);
    return abs;
  }

  awal() {
    const d = this.data;
    return {setel: salin(d.setel), elemen: salin(d.elemen), grup: salin(d.grup), komponen: salin(d.komponen), kusen: salin(d.kusen)};
  }

  set(koleksi, id, isi) {
    if (!KOLEKSI.includes(koleksi)) throw new Error('Koleksi tidak dikenal: ' + koleksi);
    if (!POLA_ID.test(id)) throw new Error('Id tidak sah: ' + id);
    if (isi == null) delete this.data[koleksi][id];
    else this.data[koleksi][id] = salin(isi);
    this.jadwalkanSimpan();
  }

  setel(isi) {
    this.data.setel = salin(isi || {});
    this.jadwalkanSimpan();
  }

  teks() {
    const d = {...this.data, disimpan: new Date().toISOString()};
    return JSON.stringify(d, null, 1);
  }

  jadwalkanSimpan() {
    clearTimeout(this.timer);
    this.timer = setTimeout(() => this.simpanSekarang(), this.tundaSimpan);
  }

  simpanSekarang(paksa = false) {
    if (!this.timer && !paksa) return;
    clearTimeout(this.timer);
    this.timer = null;
    if (!this.jalur) return;
    const teks = this.teks();
    try {
      tulisAman(this.jalur, teks);
      this.hashTerakhir = hash(fs.readFileSync(this.jalur, 'utf8'));
      this.emit('tersimpan', this.jalur);
    } catch (err) {
      console.error('[penyimpanan] gagal menyimpan', err);
      this.emit('galat', new Error('Gagal menyimpan proyek: ' + err.message));
    }
  }

  simpanSebagai(jalur) {
    const abs = path.resolve(jalur);
    this.hentikanPantau();
    this.jalur = abs;
    this.simpanSekarang(true);
    this.pantau();
    this.emit('dibuka', abs);
    return abs;
  }

  // Pantau berkas: bila diubah dari luar (misalnya oleh Claude lewat folder tersambung), muat ulang dan kirim selisihnya
  pantau() {
    if (!this.jalur || this.pantauAktif) return;
    this.pantauAktif = true;
    this._pantauJalur = this.jalur;
    fs.watchFile(this.jalur, {interval: 800}, () => this.periksaLuar());
  }

  hentikanPantau() {
    if (this.pantauAktif && this._pantauJalur) fs.unwatchFile(this._pantauJalur);
    this.pantauAktif = false;
  }

  periksaLuar() {
    if (!this.jalur || this.timer) return null;
    let teks;
    try { teks = fs.readFileSync(this.jalur, 'utf8'); } catch { return null; }
    const h = hash(teks);
    if (h === this.hashTerakhir) return null;
    let baru;
    try { baru = urai(teks); } catch (err) { this.emit('galat', err); return null; }
    this.hashTerakhir = h;
    const selisih = bandingkan(this.data, baru);
    this.data = baru;
    if (selisih.ada) this.emit('ubahLuar', selisih);
    return selisih;
  }
}

// Selisih per koleksi: [{id, data}] dengan data null untuk yang dihapus
function bandingkan(lama, baru) {
  const hasil = {ada: false, setel: null, koleksi: {}};
  for (const k of KOLEKSI) {
    const p = [];
    for (const [id, x] of Object.entries(baru[k])) if (JSON.stringify(lama[k][id]) !== JSON.stringify(x)) p.push({id, data: x});
    for (const id of Object.keys(lama[k])) if (!(id in baru[k])) p.push({id, data: null});
    if (p.length) { hasil.koleksi[k] = p; hasil.ada = true; }
  }
  if (JSON.stringify(lama.setel) !== JSON.stringify(baru.setel)) { hasil.setel = baru.setel; hasil.ada = true; }
  return hasil;
}

module.exports = {Proyek, urai, bandingkan, tulisAman, kosong, KOLEKSI, FORMAT, POLA_ID};
